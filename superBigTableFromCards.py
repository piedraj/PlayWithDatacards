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
parser.add_option("-f", "--file", dest="inputFile",  help="input file to join samples",   default="", type="string")
parser.add_option("-D", "--doSignal", dest="doSignal",  help="create signal column",   default=True,   action="store_false")



(options, args) = parser.parse_args()
options.bin = True # fake that is a binary output, so that we parse shape lines
options.noJMax = False
options.nuisancesToExclude = ''
errors




joinSamples = {}
if os.path.exists(options.inputFile):
  handle = open(options.inputFile,'r')
  exec(handle)
  handle.close()


print " reduced "
print "joinSamples = " , joinSamples




from DatacardParser import *

DC = parseCard(file(args[0]), options)
nuisToConsider = [ y for y in DC.systs ]


# prepare a useful table : [channel][nuisance][process] = value of uncertainty (e.g. 0.02 for 2%)
allerrors = {}
for nuis in nuisToConsider:
    if nuis[2] == 'gmN': gmN = nuis[3][0]
    else               : gmN = 0
    for channel in nuis[4]:
        #print channel  
        #   e.g. of_0j
        if channel not in allerrors.keys(): allerrors[channel] = {}
        if nuis[0] not in allerrors[channel].keys(): allerrors[channel][nuis[0]] = {}
        #print nuis[0]
        #  e.g. QCDscale_WW, lumi_8TeV, ...
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

            #  e.g.    of_0j    lumi      WW         2% (0.02)
            allerrors[channel][nuis[0]][process] = newError





size = "footnotesize"

print "========================="
print "========================="

# each channel (e.g. of_0j) is trated separately
for channel in DC.exp:

    ##################
    # inverted table #
    ##################


    print " CHANNEL = ", channel
    print "\n"
    print "========================="
    print "\n latex style \n"

    signals     = DC.list_of_signals()
    backgrounds = DC.list_of_backgrounds()
    allprocesses = DC.list_of_procs()

    totsig    = {}
    errtotsig = {}
    totbkg    = {}
    errtotbkg = {}

    toJoin = {}
    toRemove = []  # because joint!
    for newname,lista in joinSamples.iteritems() :
        for rem in lista :
            toRemove.append (rem)
        #toJoin.update ({newname: (rate, error)})
        toJoin.update ({newname: (0., 0.)})

    # now add the "not merged" in the joint list, as singletons
    for rem in toRemove.iteritems() :
      toJoin.update ({rem: (0., 0.)})
      joinSamples.update ({rem : [rem]})


    # for a given nuisance the effects on all processes sum up linearly
    
    # prepare a useful table : [nuisance][joined process] = value of uncertainty in absolute values (e.g. +/- 23.54)
    all_absolute_errors_joined = {}

    for nuis, proc_error in allerrors[channel].iteritems() :
      all_absolute_errors_joined[nuis] = {}
      for proc, error in proc_error.iteritems() :
        for newname,lista in joinSamples.iteritems() :
          if proc in lista :
           if newname not in all_absolute_errors_joined[nuis].keys():
             all_absolute_errors_joined[nuis][newname] = DC.exp[channel][proc] * allerrors[channel][nuis][proc]
           else :
             all_absolute_errors_joined[nuis][newname] = all_absolute_errors_joined[nuis][newname] +  DC.exp[channel][proc] * allerrors[channel][nuis][proc]


    # prepare a useful table : [nuisance][signal or background] = value of uncertainty in absolute values (e.g. +/- 23.54)
    all_absolute_errors_signal     = {}
    all_absolute_errors_background = {}

    for nuis, proc_error in allerrors[channel].iteritems() :
      all_absolute_errors_signal[nuis] = 0.
      all_absolute_errors_background[nuis] = 0.
      for proc, error in proc_error.iteritems() :
        if proc in signals :
        all_absolute_errors_signal[nuis] = all_absolute_errors_signal[nuis]  +  DC.exp[channel][proc] * allerrors[channel][nuis][proc]
        if proc in backgrounds :
        all_absolute_errors_background[nuis] = all_absolute_errors_background[nuis]  +  DC.exp[channel][proc] * allerrors[channel][nuis][proc]
        
    # calculate global
    # signal
    for s in signals :
        if channel not in    totsig.keys():    totsig[channel] = 0.0
        if channel not in errtotsig.keys(): errtotsig[channel] = 0.0
        totsig[channel]    = totsig[channel]    + DC.exp[channel][s]
    
    # background
    for b in backgrounds :
        if channel not in    totbkg.keys():    totbkg[channel] = 0.0
        if channel not in errtotbkg.keys(): errtotbkg[channel] = 0.0
        totbkg[channel]    = totbkg[channel]    + DC.exp[channel][b]

    # all the samples, in joint mode
    # first upload the total rate ...
    for newname,lista in joinSamples.iteritems() :
        for p in allprocesses :
            if p in lista :
                (rate, error) = toJoin[newname]
                rate  = rate  + DC.exp[channel][p]
                toJoin.update ({newname: (rate, error)})
    # ... then upload the uncertainty on the total rate -> absolute uncertainty is summed in quadrature among different nuisances
    for nuis, proc_error in all_absolute_errors_joined.iteritems() :
      for proc, error in all_absolute_errors_joined[nuis].iteritems() :
        if proc in joinSamples.keys() :
          (rate, error) = toJoin[newname]
          error = sqrt((error*error) + (all_absolute_errors_joined[nuis][proc]*all_absolute_errors_joined[nuis][proc]))
          toJoin.update ({newname: (rate, error)})
          
          
          
    #############a      
    # now print #

    print "\\begin{table}[h!]\\begin{center}"
    print ("\\%s{" % size),

    print "\n\n\n"
    print "\\begin{tabular}{"
    print ("c|"), # nuisance
    for newname,lista in joinSamples.iteritems() :
        isAsignal = False
        for s in signals :
            if s in lista :
                isAsignal = True
        if isAsignal :
            print ("c |"),

    if options.doSignal :
        print ("|c||"), # total sig
    else :
        print ("|"), # total sig
    for newname,lista in joinSamples.iteritems() :
        isAbackground = False
        for b in backgrounds :
            if b in lista :
                isAbackground = True
        if isAbackground :
            print ("c |"),
    print ("|c|"), # total bkg
    print "} "




    # now print
    for newname,lista in joinSamples.iteritems() :
        isAsignal = False
        for s in signals :
            if s in lista :
                isAsignal = True
        if isAsignal :
            (rate, error) = toJoin[newname]
            print (" & %5.1f $\\pm$ %5.1f (%5.1f \\%%) " % ( rate ,error, error/rate*100)),

    if options.doSignal : 
        print (" & %5.1f $\\pm$ %5.1f (%5.1f \\%%) " % (totsig[channel],errtotsig[channel],errtotsig[channel]/totsig[channel]*100)),


    for newname,lista in joinSamples.iteritems() :
        isAbackground = False
        for b in backgrounds :
            if b in lista :
                isAbackground = True
        if isAbackground :
            (rate, error) = toJoin[newname]
            #print "name = ",newname," :: ",rate," +/- ", error
            print (" & %5.1f $\\pm$ %5.1f (%5.1f \\%%) " % ( rate ,error, error/rate * 100)),

    print (" & %5.1f $\\pm$ %5.1f (%5.1f \\%%) " % (totbkg[channel],errtotbkg[channel],errtotbkg[channel]/totbkg[channel]*100)),
    print ("\\\\  \\hline \\hline  ")


    ## start list of nuisances
    for nuis in nuisToConsider:
        if channel in nuis[4]:
            #print (" %13s " % nuis[0].translate(None, '_')),
            print (" %13s " % nuis[0].replace('_', '-')),

            # update the error, not the rate!
            for newname,lista in joinSamples.iteritems() :
                #toJoin.update ({newname: (rate, error)})
                (rate,error) = toJoin[newname]
                if nuis[0] in all_absolute_errors_joined.keys() :
                  if newname in all_absolute_errors_joined[nuis[0]].keys() :
                    toJoin.update ({newname: (rate, all_absolute_errors_joined[nuis[0]][newname])})

            # first the signals
            for newname,lista in joinSamples.iteritems() :
              isAsignal = False
              for s in signals :
                if s in lista :
                  isAsignal = True
              if isAsignal :
                if nuis[0] in all_absolute_errors_joined.keys() :
                  if newname in all_absolute_errors_joined[nuis[0]].keys() :
                    toJoin.update ({newname: (rate, all_absolute_errors_joined[nuis[0]][newname])})
                            if (newError != 0) :
                                print (" & $\\pm$ %3.2f (%1.1f \\%%) " % (DC.exp[channel][s],all_absolute_errors_joined[nuis[0]][newname], all_absolute_errors_joined[nuis[0]][newname] / DC.exp[channel][s] *100)),
                            else : 
                                print (" & -"),

                if nuis[0] in all_absolute_errors_joined.keys() :



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

                        if s not in toRemove :
                            if (newError != 0) :
                                print (" & $\\pm$ %3.2f (%1.1f \\%%) " % (DC.exp[channel][s]*newError,newError*100)),
                            else : 
                                print (" & -"),
                        else:
                            for newname,lista in joinSamples.iteritems() :
                                if s in lista: # it should, at least in one of these lists, since it is in "toRemove"
                                    (rate,error) = toJoin[newname]
                                    error = sqrt(error*error + DC.exp[channel][s]*newError*DC.exp[channel][s]*newError)
                                    toJoin.update ({newname: (rate, error)})

                        #temperror = temperror + DC.exp[channel][s]*newError*DC.exp[channel][s]*newError
                        # for a given nuisance the errors are added linearly among different samples, and NOT in quadrature
                        temperror = temperror + DC.exp[channel][s]*newError
                    else :
                        if s not in toRemove :
                            print (" & -"),

            for newname,lista in joinSamples.iteritems() :
                isAsignal = False
                for s in signals :
                    if s in lista :
                        isAsignal = True
                if isAsignal :
                    (rate, error) = toJoin[newname]
                    if error != 0 :
                        print (" & $\\pm$ %3.2f (%1.1f \\%%) " % ( error, error/rate*100)),
                    else :
                        print (" & - "),


            # for a given nuisance the errors are added linearly among different samples, and NOT in quadrature
            #temperror = sqrt(temperror)
            if options.doSignal : 
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

                        if b not in toRemove :
                            if (newError != 0) :
                                print (" & $\\pm$ %3.2f (%1.1f \\%%) " % (DC.exp[channel][b]*newError,newError*100)),
                            else : 
                                print (" & -"),
                        else :
                            for newname,lista in joinSamples.iteritems() :
                                if b in lista: # it should, at least in one of these lists, since it is in "toRemove"
                                    (rate,error) = toJoin[newname]
                                    error = sqrt(error*error + DC.exp[channel][b]*newError*DC.exp[channel][b]*newError)
                                    toJoin.update ({newname: (rate, error)})
                                    #print "p[ + ",b,"::",newname,"] :: rate = ",rate, " +/- ",error

                        # for a given nuisance the errors are added linearly among different samples, and NOT in quadrature
                        #temperror = temperror + DC.exp[channel][b]*newError*DC.exp[channel][b]*newError
                        temperror = temperror + DC.exp[channel][b]*newError
                    else :
                        if b not in toRemove :
                            print (" & -"),

            # for a given nuisance the errors are added linearly among different samples, and NOT in quadrature
            #temperror = sqrt(temperror)

            for newname,lista in joinSamples.iteritems() :
                isAbackground = False
                for b in backgrounds :
                    if b in lista :
                        isAbackground = True
                if isAbackground :
                    (rate, error) = toJoin[newname]
                    if error != 0 :
                        print (" & $\\pm$ %3.2f (%1.1f \\%%) " % ( error, error/rate*100)),
                    else :
                        print (" & - "),

            if (temperror != 0) : print (" &  $\\pm$ %5.1f (%5.1f \\%%) " % (temperror,temperror/totbkg[channel]*100)),
            else : print (" &  - "),
            print ("\\\\  \\hline ")


    print ("\\hline ")

    print "\\end{tabular}"
    print "\n\n\n"

    print "}"
    print "\\end{center}"
    print "\\end{table}"


    print "========================="
    print "\n\n\n"










print " this is the end ..."
print "\n\n\n"


