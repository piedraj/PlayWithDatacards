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
    for process in allprocesses :
      if process not in toRemove :
        toJoin.update ({rem: (0., 0.)})
        joinSamples.update ({rem : [rem]})

    print "joinSamples = ",joinSamples

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

    #print "all_absolute_errors_joined"
    #print all_absolute_errors_joined

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
        #print "is ", proc, " in ", joinSamples.keys()
        if proc in joinSamples.keys() :
          (rate, error) = toJoin[newname]
          error = sqrt((error*error) + (all_absolute_errors_joined[nuis][proc]*all_absolute_errors_joined[nuis][proc]))
          toJoin.update ({newname: (rate, error)})

    # and upload the tot signal and tot background errors
    for nuis, proc_error in allerrors[channel].iteritems() :
      errtotbkg[channel]  = sqrt(errtotbkg[channel]*errtotbkg[channel]  + all_absolute_errors_background[nuis]*all_absolute_errors_background[nuis])
    for nuis, proc_error in allerrors[channel].iteritems() :
      errtotsig[channel]  = sqrt(errtotsig[channel]*errtotsig[channel]  + all_absolute_errors_signal[nuis]*all_absolute_errors_signal[nuis])
      
     
          
    #############a      
    # now print #

    print "\\begin{table}[h!]\\begin{center}"
    print ("\\%s{" % size),

    # print the table structure
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


    # print the samples name
    
    for s in signals :
        if ( channel in nuis[4] ) and ( s not in toRemove ):
            print ("& %13s " % s),
    for newname,lista in joinSamples.iteritems() :
        isAsignal = False
        for s in signals :
            if s in lista :
                isAsignal = True
        if isAsignal :
            print ("& %13s " % newname),

    if options.doSignal : 
        print ("& %13s " % "signal"),

    for b in backgrounds :
        if ( channel in nuis[4] ) and ( b not in toRemove ) :
            print ("& %13s " % b),
    for newname,lista in joinSamples.iteritems() :
        isAbackground = False
        for b in backgrounds :
            if b in lista :
                isAbackground = True
        if isAbackground :
            print ("& %13s " % newname),
    print ("& %13s " % "background"),

    print ("\\\\  \\hline ")




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
                  #print "all_absolute_errors_joined[",nuis[0],"] = ", all_absolute_errors_joined[nuis[0]]
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
                    #toJoin.update ({newname: (rate, all_absolute_errors_joined[nuis[0]][newname])})
                    denumerator = DC.exp[channel][s]
                    if (denumerator != 0.) :
                      print (" & $\\pm$ %3.2f (%1.1f \\%%) " % (all_absolute_errors_joined[nuis[0]][newname], all_absolute_errors_joined[nuis[0]][newname] / DC.exp[channel][s] *100)),
                    else : 
                      print (" & -"),
                  else : 
                    print (" & -"),
                else : 
                  print (" & -"),

            # then the signal summary
            if nuis[0] in all_absolute_errors_signal.keys() :
              print (" & $\\pm$ %5.1f (%5.1f \\%%) " % (all_absolute_errors_signal[nuis[0]],all_absolute_errors_signal[nuis[0]]/totsig[channel]*100)),
            else : print (" &  - "),
            

            # second the backgrounds
            for newname,lista in joinSamples.iteritems() :
              isAsignal = False
              for s in signals :
                if s in lista :
                  isAsignal = True
              if not isAsignal :
                if nuis[0] in all_absolute_errors_joined.keys() :
                  if newname in all_absolute_errors_joined[nuis[0]].keys() :
                    #toJoin.update ({newname: (rate, all_absolute_errors_joined[nuis[0]][newname])})
                    denumerator = DC.exp[channel][s]
                    if (denumerator != 0.) :
                      print (" & $\\pm$ %3.2f (%1.1f \\%%) " % (all_absolute_errors_joined[nuis[0]][newname], all_absolute_errors_joined[nuis[0]][newname] / DC.exp[channel][s] *100)),
                    else : 
                      print (" & -"),
                  else : 
                    print (" & -"),
                else : 
                  print (" & -"),

            # then the background summary
            if nuis[0] in all_absolute_errors_background.keys() :
              print (" & $\\pm$ %5.1f (%5.1f \\%%) " % (all_absolute_errors_background[nuis[0]],all_absolute_errors_background[nuis[0]]/totbkg[channel]*100)),
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


