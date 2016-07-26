#!/usr/bin/env python


#
#
#    __ \          |                                 |      |                _ \  _)       
#    |   |   _` |  __|   _` |   __|   _` |   __|  _` |      __|   _ \       |   |  |   _ \ 
#    |   |  (   |  |    (   |  (     (   |  |    (   |      |    (   |      ___/   |   __/ 
#   ____/  \__,_| \__| \__,_| \___| \__,_| _|   \__,_|     \__| \___/      _|     _| \___| 
#                                                                                          
#                                                                                          


print '''
    --------------------------------------------------------------------------------------------------
    
       __ \          |                                 |      |                _ \  _)       
       |   |   _` |  __|   _` |   __|   _` |   __|  _` |      __|   _ \       |   |  |   _ \ 
       |   |  (   |  |    (   |  (     (   |  |    (   |      |    (   |      ___/   |   __/ 
      ____/  \__,_| \__| \__,_| \___| \__,_| _|   \__,_|     \__| \___/      _|     _| \___| 
      
    --------------------------------------------------------------------------------------------------
'''    



import re
from sys import argv
import os.path
from optparse import OptionParser
from math import sqrt,fabs

from collections import OrderedDict

parser = OptionParser()
parser.add_option("-s", "--stat",   dest="stat",          default=False, action="store_true")  # ignore systematic uncertainties to consider statistical uncertainties only
#parser.add_option("-S", "--force-shape", dest="shape",    default=False, action="store_true")  # ignore systematic uncertainties to consider statistical uncertainties only
#parser.add_option("-a", "--asimov", dest="asimov",  default=False, action="store_true")
#parser.add_option("-m", "--mass", dest="mass",  default=125, type="float")
#from DatacardParser import *

parser.add_option("--plotFile",   dest="plotFile",          default="" )

(options, args) = parser.parse_args()
options.bin = True # fake that is a binary output, so that we parse shape lines
options.noJMax = False
options.nuisancesToExclude = ''


plot = {}
legend = {}
if os.path.exists(options.plotFile) :
   handle = open(options.plotFile,'r')
   exec(handle)
   handle.close()




import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")

from HiggsAnalysis.CombinedLimit.DatacardParser import *




DC = parseCard(file(args[0]), options)


signals     = DC.list_of_signals()
backgrounds = DC.list_of_backgrounds()



for channel in DC.exp:
  print " channel = ", channel
  target = open('pie_'+channel+'.C', 'w')

  target.write('void pie_' + channel + '(){  \n')

  target.write('  TCanvas *cpie = new TCanvas("cpie","TPie test",700,700);')
  
  signalRate = {}
  backgroundRate = {}
  allRate = OrderedDict()
  allSignal = 0.
  
  for s in signals :
    if s in DC.exp[channel].keys(): # possible that some backgrounds/signals appear only in some channels
      #print ''
      #print '', s
      #print '', DC.exp[channel][s]
      signalRate[s] = DC.exp[channel][s]
      allRate[s]    = DC.exp[channel][s]
      allSignal    += DC.exp[channel][s]
      

  for b in backgrounds :
    if b in DC.exp[channel].keys(): # possible that some backgrounds/signals appear only in some channels
      #print ''
      #print '', b
      #print '', DC.exp[channel][b]
      backgroundRate[b] = DC.exp[channel][b]
      allRate[b]        = DC.exp[channel][b]



  target.write('  Float_t vals[] = {' + ', '.join(format(valueRate, "10.3f") for valueRate in allRate.values()) + '};   \n')
  target.write('  Int_t colors[] = {' + ', '.join(format(plot[valueName]['color'], "d") for valueName in allRate.keys()) + '};   \n')
  target.write('  Int_t nvals = ' + str(int(len(allRate))) + '; \n')
    
  target.write('  TPie *pie4 = new TPie("pie4","",nvals,vals,colors);   \n')
  for isample in range(len(allRate)):
    target.write('  pie4->SetEntryLabel(' + str(isample) + ', "' + allRate.keys()[isample]  + '");  \n')


  target.write('  pie4->SetRadius(.2);  \n')
  target.write('  pie4->SetLabelsOffset(.01);  \n')
  target.write('  pie4->SetLabelFormat("%txt   %perc");  \n')
  
  target.write('  pie4->Draw("nol <");  \n')
  
  target.write('  TCanvas *cpie2 = new TCanvas("cpie2","TPie test",700,700);  \n')
  target.write('  pie4->SetLabelFormat("%txt");  \n')
  target.write('  pie4->Draw("nol <");  \n')
  target.write('  cpie2 -> SaveAs("pie_'+channel+'.png");  \n')
  target.write('\n')

 
 
 
  target.write('  Float_t vals_reduced[] = {' + format(allSignal, "10.3f") + ',' + ', '.join(format(valueRate, "10.3f") for valueRate in backgroundRate.values()) + '};   \n')
  target.write('  Int_t colors_reduced[] = {' + format(632, "d") + ',' + ', '.join(format(plot[valueName]['color'], "d") for valueName in backgroundRate.keys()) + '};   \n')
  #                                                   kRed
  target.write('  Int_t nvals_reduced = ' + str(int(1+len(backgroundRate))) + '; \n')
    
  target.write('  TPie *pie4_reduced = new TPie("pie4_reduced","",nvals_reduced,vals_reduced,colors_reduced);   \n')
  target.write('  pie4_reduced->SetEntryLabel(0, "Signal");  \n')
  for isample in range(len(backgroundRate)):
    target.write('  pie4_reduced->SetEntryLabel(' + str(isample+1) + ', "' + backgroundRate.keys()[isample]  + '");  \n')


  target.write('  pie4_reduced->SetRadius(.2);  \n')
  target.write('  pie4_reduced->SetLabelsOffset(.01);  \n')
  target.write('  pie4_reduced->SetLabelFormat("%txt   %perc");  \n')
  
  target.write('  pie4_reduced->Draw("nol <");  \n')
  
  target.write('  TCanvas *cpie2_reduced = new TCanvas("cpie2_reduced","TPie test",700,700);  \n')
  target.write('  pie4_reduced->SetLabelFormat("%txt");  \n')
  target.write('  pie4_reduced->Draw("nol <");  \n')
  target.write('  cpie2_reduced -> SaveAs("pie_reduced_'+channel+'.png");  \n')
 


  target.write('  Float_t vals_reduced_signal[] = {' + ', '.join(format(valueRate, "10.3f") for valueRate in signalRate.values()) + '};   \n')
  target.write('  Int_t colors_reduced_signal[] = {' + ', '.join(format(plot[valueName]['color'], "d") for valueName in signalRate.keys()) + '};   \n')
  target.write('  Int_t nvals_reduced_signal = ' + str(int(len(signalRate))) + '; \n')
    
  target.write('  TPie *pie4_reduced_signal = new TPie("pie4_reduced_signal","",nvals_reduced_signal,vals_reduced_signal,colors_reduced_signal);   \n')
  for isample in range(len(signalRate)):
    target.write('  pie4_reduced_signal->SetEntryLabel(' + str(isample) + ', "' + signalRate.keys()[isample]  + '");  \n')


  target.write('  pie4_reduced_signal->SetRadius(.2);  \n')
  target.write('  pie4_reduced_signal->SetLabelsOffset(.01);  \n')
  target.write('  pie4_reduced_signal->SetLabelFormat("%txt   %perc");  \n')
  
  target.write('  pie4_reduced_signal->Draw("nol <");  \n')
  
  target.write('  TCanvas *cpie2_reduced_signal = new TCanvas("cpie2_reduced_signal","TPie test",700,700);  \n')
  target.write('  pie4_reduced_signal->SetLabelFormat("%txt");  \n')
  target.write('  pie4_reduced_signal->Draw("nol <");  \n')
  target.write('  cpie2_reduced_signal -> SaveAs("pie_reduced_signal_'+channel+'.png");  \n')

  target.write('} \n')
  target.write('\n')
  

  target.close()
  
  
  os.system('root -l -q pie_'+channel+'.C')  




