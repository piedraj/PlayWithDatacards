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
        if channel not in errors.keys(): errors[channel] = {}
        for process in nuis[4][channel]:
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
    if '0j' not in x and '1j' not in x and '2j' not in x: continue
    for y in DC.exp[x]:
        print "%10s %10s %10.2f +/- %10.2f (rel = %10.2f)" % (x,y,DC.exp[x][y],DC.exp[x][y]*errors[x][y],errors[x][y])

#def findVals(samp,thisExp,thisErr):
    #val = 0
    #err = 0
    #for s in samp:
        #for k in thisExp:
            #if s == k:
                #val += thisExp[k]
                #if k in thisErr:
                    #err += thisExp[k]*thisExp[k]*thisErr[k]*thisErr[k]
                #else:
                    #print "Warning: %s has no error associated with it for %s with value %.2f" % (s,k,thisExp[k])
    #return (val,sqrt(err))

#jets = ['0j','1j','2j']
#channels = ['sf','of']
#chanlabels = ['$ee/\\mu\\mu$','$e\\mu$']
#order = [ 'DY', 'Top', 'WJet','VV', 'WW', 'sum', 'signal', 'data'  ]
#samplesTemp = [ ['DYLL','DYee','DYmm','DYTT','EMBTT'], ['Top'], ['WJet'], ['VV','Vg'], ['ggWW','WW'], [], ['ggH','vbfH','wzttH'], [] ]
#labelsTemp  = [ 'Z$/\\gamma^*$', '\\ttbar+tW', 'W+jets', 'VV+V$\\gamma^{(*)}$', 'WW', "all bkg.", ("\\mh{%d}~\\GeV"%options.mass), 'data' ]
#samples = dict(zip(order,samplesTemp))
#labels = dict(zip(order,labelsTemp))

#headerS  =  "& %-15s"
#floatS   =  "& $%5.1f\pm%5.1f$"
#intS     =  "& $%12d$" 
#firstCol =  "%-10s"

#for jet in jets:
    #label = "ddYields%sM%d" % (jet,options.mass)
    #size = "footnotesize"
    #file = open(label+".tex",'w')
    ## Print the header
    #sums = {}
    #errs = {}
    #for samp in order:
        #sums[samp] = 0
        #errs[samp] = 0

    #caption = """
#Background contributions and data yields for \\usedLumi of integrated 
#luminosity after the full cut-based selection in the %s bin for a Higgs 
#mass of %d \\GeV. The data-driven correction are applied. 
#""" % ( "one-jet" if jet == '1j' else 'zero-jet', options.mass )

    ## Print leading tex stuff
##     print >> file, "\\begin{table}[h!]\\begin{center}"
##     print >> file, "\\caption{{ {0} \\label{{ {1} }} }}".format(caption,label)
##     print >> file, "\\%s{\\begin{tabular}{c|c|c|c|c|c|c|c|c||c||c} \\hline" % size

    ## Print the header
    #if jet == '3j' and options.mass == 110: 
        #print >> file, firstCol % '$m_{\mathrm{H}}$~[\GeV]',
        #labels['signal'] = 'signal'
    #print >> file, firstCol%"",
    #for samp in order:
            #if jet != '3j' or options.mass == 110: print >> file, headerS % (labels[samp]),
    #if jet != '3j' or options.mass == 110: print >> file, "\\\\ \\hline"

    ## print each row
    #ic=0
    #for chan in channels if jet != '3j' else ['bin']:
        #totVal = totErr = 0
        ## print the label
        #if chan != 'bin': print >> file, firstCol%chanlabels[ic],

        ## grab the right yields from DC
        #thisExp = None
        #for x in DC.exp.keys(): 
            #if jet in x and (chan in x or jet =='3j'): 
                #thisExp = DC.exp[x]
                #thisErr = errors[x]
                #thisDat = DC.obs[x]
        #if not thisExp: 
            #print "WTF: %s %s " % (jet,chan)
        #ic+=1

        ## print each contribution
        #for i,samp in enumerate(order):
            #if samp in ['signal','sum','data']: continue;
            #(val,err) = findVals(samples[samp],thisExp,thisErr)
            #totVal += val; totErr += err*err;
            #if chan != 'bin': print >> file, floatS % (val,err),
            #sums[samp] += val; errs[samp] += err*err
            #sums['sum'] += val; errs['sum'] += err*err
        #if chan != 'bin': print >> file, floatS % (totVal,sqrt(totErr)),
        #(val,err) = findVals(samples['signal'],thisExp,thisErr)
        #sums['signal'] += val; errs['signal'] += err*err
        #if chan != 'bin': print >> file, floatS %  (val,err),
        ## blind
        ##if chan != 'bin': print >> file, "&- \\\\"#(intS % thisDat) + "\\\\"
        #if chan != 'bin': print >> file, (intS % thisDat) + "\\\\" 
        #sums['data'] += thisDat
    ## Print the sums
    #if chan != 'bin': print >> file, firstCol % ("total"),
    #else            : print >> file, firstCol % ("$%d$"%options.mass),
    #for samp in order:
        #print >> file, floatS%(sums[samp],sqrt(errs[samp])) if samp!='data' else intS%(sums[samp]) ,
        ## blind
        ##print >> file, floatS%(sums[samp],sqrt(errs[samp])) if samp!='data' else "&-", #intS%(sums[samp]) ,
                       

    ## print the trailing tex stuff
    #print >> file, " \\\\ "
    #print >> file

