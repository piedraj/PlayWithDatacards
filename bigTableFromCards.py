#!/usr/bin/env python

import re
from sys import argv
import os.path
from optparse import OptionParser
from math import sqrt,fabs
parser = OptionParser()
parser.add_option("-s", "--stat",   dest="stat",          default=False, action="store_true")  # ignore systematic uncertainties to consider statistical uncertainties only
parser.add_option("-S", "--force-shape", dest="shape",    default=False, action="store_true")  # ignore systematic uncertainties to consider statistical uncertainties only
parser.add_option("-a", "--asimov", dest="asimov",  default=False, action="store_true")
parser.add_option("-m", "--mass", dest="mass",  default=125, type="float")


(options, args) = parser.parse_args()
options.bin = True # fake that is a binary output, so that we parse shape lines
options.noJMax = False
options.nuisancesToExclude = ''

from DatacardParser import *

DC = parseCard(file(args[0]), options)
nuisToConsider = [ y for y in DC.systs ]

errors = {}
for nuis in nuisToConsider:
    if nuis[2] == 'gmN': gmN = nuis[3][0]
    else               : gmN = 0
    for channel in nuis[4]:
        #print channel
        if channel not in errors.keys(): errors[channel] = {}
        for process in nuis[4][channel]:
            newError = 0.
            if nuis[2] == 'gmN': gmN = nuis[3][0]
            if nuis[4][channel][process] == 0: continue
            #print nuis[2],gmN
            if gmN != 0:
                newError = nuis[4][channel][process] * sqrt(gmN) / DC.exp[channel][process]
            else:
                #print nuis[4][channel][process]
                if not isinstance ( nuis[4][channel][process], float ) :
                    # [0.95, 1.23]
                #if len(nuis[4][channel][process]) == 2 :
                    newError = fabs((nuis[4][channel][process][1]-nuis[4][channel][process][0])/2.)   # symmetrized
                else : 
                    newError = fabs(1-nuis[4][channel][process])
            if process in errors[channel].keys():
                errors[channel][process] += newError*newError
            else:
                errors[channel][process] = newError*newError

for channel in errors:
    for process in errors[channel]:
        errors[channel][process] = sqrt(errors[channel][process])

for x in DC.exp:
    for y in DC.exp[x]:
        print "%10s %10s %5.1f $\\pm$ %5.1f (rel = %5.1f)" % (x,y,DC.exp[x][y],DC.exp[x][y]*errors[x][y],errors[x][y])




size = "footnotesize"


# one table fro each channel

for channel in DC.exp:

    print " CHANNEL = ", channel
    print "\n"
    print "========================="
    print "\n latex style \n"

    print "\\begin{table}[h!]\\begin{center}"
    print ("\\%s{\\begin{tabular}{" % size),
    print ("c|"), # name of the sample
    print ("c|"), # yield and total error
    for nuis in nuisToConsider:
        if channel in nuis[4] :
            print ("c |"),
    print "} \\\\  \\hline "


    print (" & "), 
    for nuis in nuisToConsider:
        if channel in nuis[4]:
            print ("& %13s " % channel),
    print ("\\\\  \\hline ")

    print (" & "), # name of the sample
    for nuis in nuisToConsider:
        if channel in nuis[4]:
            print ("& %13s " % nuis[0]),
    print ("\\\\  \\hline ")

    signals     = DC.list_of_signals()
    backgrounds = DC.list_of_backgrounds()

    totsig    = {}
    errtotsig = {}
    totbkg    = {}
    errtotbkg = {}

    for s in signals :
        print (" %13s " % s),
        if s in DC.exp[channel].keys(): # possible that some backgrounds appear only in some channels
            if channel not in    totsig.keys():    totsig[channel] = 0.0
            if channel not in errtotsig.keys(): errtotsig[channel] = 0.0
            totsig[channel]    = totsig[channel]    + DC.exp[channel][s]
            errtotsig[channel] = errtotsig[channel] + (DC.exp[channel][s]*errors[channel][s] * DC.exp[channel][s]*errors[channel][s])
            print (" & %5.1f $\\pm$ %5.1f (%1.1f \\%%) " % (DC.exp[channel][s],DC.exp[channel][s]*errors[channel][s],errors[channel][s]*100)),
            for nuis in nuisToConsider:
                if channel in nuis[4]:
                    temperror = 0.
                    if nuis[2] == 'gmN': gmN = nuis[3][0]
                    else               : gmN = 0
                    if nuis[4][channel][s] != 0:
                        #print nuis[2],gmN
                        if gmN != 0:
                            #print "gmN = ", gmN, " ; DC.exp[",channel,"][",s,"] = ", DC.exp[channel][s], "nuis[4][",channel,"][",s,"] = ", nuis[4][channel][s]
                            temperror = nuis[4][channel][s] * sqrt(gmN) / DC.exp[channel][s]
                        else:
                            #print nuis[4][channel][s]
                            if not isinstance ( nuis[4][channel][s], float ) :
                                # [0.95, 1.23]
                               temperror = fabs((nuis[4][channel][s][1]-nuis[4][channel][s][0])/2.)   # symmetrized
                            else : 
                                temperror = fabs(1-nuis[4][channel][s])
                        if (temperror != 0) : print (" & $\\pm$ %3.2f (%1.1f \\%%) " % (DC.exp[channel][s]*temperror,temperror*100)),
                        else : print (" & -"),
                    else : print (" & -"),
        else :
            print (" & - "),

        print ("\\\\")
    print ("\\hline ")
    print (" %13s " % "signal"),
    errtotsig[channel] = sqrt(errtotsig[channel])
    print (" & %5.1f $\\pm$ %5.1f (%5.1f \\%%) " % (totsig[channel],errtotsig[channel],errtotsig[channel]/totsig[channel]*100)),

    for nuis in nuisToConsider:
        temperror = 0.
        for s in DC.exp[channel].keys(): # possible that some backgrounds appear only in some channels
            if channel in nuis[4]:
                newError = 0.
                if nuis[2] == 'gmN': gmN = nuis[3][0]
                else               : gmN = 0
                if nuis[4][channel][s] == 0: continue
                #print nuis[2],gmN
                if gmN != 0:
                    newError = nuis[4][channel][s] * sqrt(gmN) / DC.exp[channel][s]
                else:
                    #print nuis[4][channel][s]
                    if not isinstance ( nuis[4][channel][s], float ) :
                        # [0.95, 1.23]
                        newError = fabs((nuis[4][channel][s][1]-nuis[4][channel][s][0])/2.)   # symmetrized
                    else :
                        newError = fabs(1-nuis[4][channel][s])
                temperror = temperror + newError*newError

        temperror = sqrt(temperror)
        print (" & $\\pm$ %3.2f (%3.1f \\%%) " % (totsig[channel]*temperror,temperror)),


    print ("\\\\")
    print ("\\hline ")



    for b in backgrounds :
        print (" %13s " % b),
        if b in DC.exp[channel].keys(): # possible that some backgrounds appear only in some channels
            if channel not in    totbkg.keys():    totbkg[channel] = 0.0
            if channel not in errtotbkg.keys(): errtotbkg[channel] = 0.0
            totbkg[channel]    = totbkg[channel]    + DC.exp[channel][b]
            errtotbkg[channel] = errtotbkg[channel] + (DC.exp[channel][b]*errors[channel][b] * DC.exp[channel][b]*errors[channel][b])
            print (" & %5.1f $\\pm$ %5.1f (%1.1f \\%%) " % (DC.exp[channel][b],DC.exp[channel][b]*errors[channel][b],errors[channel][b]*100)),
            for nuis in nuisToConsider:
                if channel in nuis[4]:
                    temperror = 0.
                    if nuis[2] == 'gmN': gmN = nuis[3][0]
                    else               : gmN = 0
                    if nuis[4][channel][b] != 0:
                        #print nuis[2],gmN
                        if gmN != 0:
                            temperror = nuis[4][channel][b] * sqrt(gmN) / DC.exp[channel][b]
                        else:
                            #print nuis[4][channel][b]
                            if not isinstance ( nuis[4][channel][b], float ) :
                                # [0.95, 1.23]
                                temperror = fabs((nuis[4][channel][b][1]-nuis[4][channel][b][0])/2.)   # symmetrized
                            else :
                                temperror = fabs(1-nuis[4][channel][b])
                        if (temperror != 0) : print (" & $\\pm$ %3.2f (%1.1f \\%%) " % (DC.exp[channel][b]*temperror,temperror*100)),
                        else : print (" & -"),
                    else : print (" & -"),
        else :
            print (" & - "),

        print ("\\\\")


    print ("  \\hline ")
    print (" %13s " % "background"),
    errtotbkg[channel] = sqrt(errtotbkg[channel])
    print (" & %5.1f $\\pm$ %5.1f (%5.1f \\%%) " % (totbkg[channel],errtotbkg[channel],errtotbkg[channel]/totbkg[channel]*100)),

    for nuis in nuisToConsider:
        temperror = 0.
        for b in DC.exp[channel].keys(): # possible that some backgrounds appear only in some channels
            if channel in nuis[4]:
                newError = 0.
                if nuis[2] == 'gmN': gmN = nuis[3][0]
                else               : gmN = 0
                if nuis[4][channel][b] == 0: continue
                #print nuis[2],gmN
                if gmN != 0:
                    newError = nuis[4][channel][b] * sqrt(gmN) / DC.exp[channel][b]
                else:
                    #print nuis[4][channel][b]
                    if not isinstance ( nuis[4][channel][b], float ) :
                        # [0.95, 1.23]
                        newError = fabs((nuis[4][channel][b][1]-nuis[4][channel][b][0])/2.)   # symmetrized
                    else :
                        newError = fabs(1-nuis[4][channel][b])
                temperror = temperror + newError*newError

        temperror = sqrt(temperror)
        print (" & $\\pm$ %3.2f (%3.1f \\%%) " % (totbkg[channel]*temperror,temperror)),


    print ("\\\\  \\hline ")



    print "\\end{tabular}"
    print "}"
    print "\\end{center}"
    print "\\end{table}"


    print "========================="
    print "\n\n\n"


    print "\n\n\n"
    print "\n\n\n"
    print "\n\n\n"
    print "\n\n\n"


    ##################
    # inverted table #
    ##################


    print " CHANNEL = ", channel
    print "\n"
    print "========================="
    print "\n latex style \n"

    #signals     = DC.list_of_signals()
    #backgrounds = DC.list_of_backgrounds()

    #totsig    = {}
    #errtotsig = {}
    #totbkg    = {}
    #errtotbkg = {}

    print "\\begin{table}[h!]\\begin{center}"
    print ("\\%s{\\begin{tabular}{" % size),
    print ("c|"), # nuisance
    for s in signals :
        if channel in nuis[4] :
            print ("c |"),
    print ("|c||"), # total sig
    for b in backgrounds :
        if channel in nuis[4] :
            print ("c |"),
    print ("|c|"), # total bkg
    print "} \\\\  \\hline "


    for s in signals :
        if channel in nuis[4]:
            print ("& %13s " % s),
    print ("& %13s " % "signal"),

    for b in backgrounds :
        if channel in nuis[4]:
            print ("& %13s " % b),
    print ("& %13s " % "background"),

    print ("\\\\  \\hline ")

    #for s in signals :
        #if channel not in    totsig.keys():    totsig[channel] = 0.0
        #if channel not in errtotsig.keys(): errtotsig[channel] = 0.0
        #totsig[channel]    = totsig[channel]    + DC.exp[channel][s]
        #errtotsig[channel] = errtotsig[channel] + (DC.exp[channel][s]*errors[channel][s] * DC.exp[channel][s]*errors[channel][s])

    #errtotsig[channel] = sqrt(errtotsig[channel])

    #for b in backgrounds :
        #if channel not in    totbkg.keys():    totbkg[channel] = 0.0
        #if channel not in errtotbkg.keys(): errtotbkg[channel] = 0.0
        #totbkg[channel]    = totbkg[channel]    + DC.exp[channel][b]
        #errtotbkg[channel] = errtotbkg[channel] + (DC.exp[channel][b]*errors[channel][b] * DC.exp[channel][b]*errors[channel][b])

    #errtotbkg[channel] = sqrt(errtotbkg[channel])

    for s in signals :
        print (" & %5.1f $\\pm$ %5.1f (%5.1f \\%%) " % ( DC.exp[channel][s],errors[channel][s]*DC.exp[channel][s],errors[channel][s]*100)),
    print (" & %5.1f $\\pm$ %5.1f (%5.1f \\%%) " % (totsig[channel],errtotsig[channel],errtotsig[channel]/totsig[channel]*100)),

    for b in backgrounds :
        print (" & %5.1f $\\pm$ %5.1f (%5.1f \\%%) " % ( DC.exp[channel][b],errors[channel][b]*DC.exp[channel][s],errors[channel][b]*100)),
    print (" & %5.1f $\\pm$ %5.1f (%5.1f \\%%) " % (totbkg[channel],errtotbkg[channel],errtotbkg[channel]/totbkg[channel]*100)),
    print ("\\\\  \\hline \\hline  ")


    ## start list of nuisances
    for nuis in nuisToConsider:
        if channel in nuis[4]:
            print (" %13s " % nuis[0]),
            temperror = 0.
            for s in signals :
                if s in DC.exp[channel].keys(): # possible that some backgrounds appear only in some channels
                    newError = 0.
                    if nuis[2] == 'gmN': gmN = nuis[3][0]
                    else               : gmN = 0
                    if nuis[4][channel][s] != 0:
                        #print nuis[2],gmN
                        if gmN != 0:
                            #print "gmN = ", gmN, " ; DC.exp[",channel,"][",s,"] = ", DC.exp[channel][s], "nuis[4][",channel,"][",s,"] = ", nuis[4][channel][s]
                            newError = nuis[4][channel][s] * sqrt(gmN) / DC.exp[channel][s]
                        else:
                            #print nuis[4][channel][s]
                            if not isinstance ( nuis[4][channel][s], float ) :
                                # [0.95, 1.23]
                               newError = fabs((nuis[4][channel][s][1]-nuis[4][channel][s][0])/2.)   # symmetrized
                            else : 
                                newError = fabs(1-nuis[4][channel][s])
                        if (newError != 0) : print (" & $\\pm$ %3.2f (%1.1f \\%%) " % (DC.exp[channel][s]*newError,newError*100)),
                        else : print (" & -"),
                        temperror = temperror + DC.exp[channel][s]*newError*DC.exp[channel][s]*newError
                    else : print (" & -"),
            temperror = sqrt(temperror)
            if (temperror != 0) : print (" & $\\pm$ %5.1f (%5.1f \\%%) " % (temperror,temperror/totsig[channel]*100)),
            else : print (" &  - "),

            temperror = 0.
            for b in backgrounds :
                if b in DC.exp[channel].keys(): # possible that some backgrounds appear only in some channels
                    newError = 0.
                    if nuis[2] == 'gmN': gmN = nuis[3][0]
                    else               : gmN = 0
                    if nuis[4][channel][b] != 0:
                        #print nuis[2],gmN
                        if gmN != 0:
                            #print "gmN = ", gmN, " ; DC.exp[",channel,"][",s,"] = ", DC.exp[channel][b], "nuis[4][",channel,"][",s,"] = ", nuis[4][channel][b]
                            newError = nuis[4][channel][b] * sqrt(gmN) / DC.exp[channel][b]
                        else:
                            #print nuis[4][channel][b]
                            if not isinstance ( nuis[4][channel][b], float ) :
                                # [0.95, 1.23]
                               newError = fabs((nuis[4][channel][b][1]-nuis[4][channel][b][0])/2.)   # symmetrized
                            else : 
                                newError = fabs(1-nuis[4][channel][b])
                        if (newError != 0) : print (" & $\\pm$ %3.2f (%1.1f \\%%) " % (DC.exp[channel][b]*newError,newError*100)),
                        else : print (" & -"),
                        temperror = temperror + DC.exp[channel][b]*newError*DC.exp[channel][b]*newError
                    else : print (" & -"),
            temperror = sqrt(temperror)
            if (temperror != 0) : print (" &  $\\pm$ %5.1f (%5.1f \\%%) " % (temperror,temperror/totbkg[channel]*100)),
            else : print (" &  - "),
            print ("\\\\  \\hline ")


    print ("\\hline ")



    print "\\end{tabular}"
    print "}"
    print "\\end{center}"
    print "\\end{table}"


    print "========================="
    print "\n\n\n"

























print " this is the end ..."
print "\n\n\n"


