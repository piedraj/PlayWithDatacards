#
# Create a lot of tables
#

import sys



folder = '/afs/cern.ch/user/a/amassiro/Framework/CMSSW_8_0_5/src/PlotsConfigurations/Configurations/'

list_datacards = {}


list_datacards [ 'em1j13               '  ]  =       [    'ggH/Moriond/datacards/hww2l2v_13TeV_em_1j/mllVSmth/datacard.txt.pruned.txt'                  ,    'True'    ]
list_datacards [ 'me1j13               '  ]  =       [    'ggH/Moriond/datacards/hww2l2v_13TeV_me_1j/mllVSmth/datacard.txt.pruned.txt'                  ,    'True'    ]
list_datacards [ 'em0j13               '  ]  =       [    'ggH/Moriond/datacards/hww2l2v_13TeV_em_0j/mllVSmth/datacard.txt.pruned.txt'                  ,    'True'    ]
list_datacards [ 'me0j13               '  ]  =       [    'ggH/Moriond/datacards/hww2l2v_13TeV_me_0j/mllVSmth/datacard.txt.pruned.txt'                  ,    'True'    ]
list_datacards [ 'of0j13Top            '  ]  =       [    'ggH/Moriond/datacards/hww2l2v_13TeV_top_of0j/events/datacard.txt.pruned.txt'                 ,    'False'    ]
list_datacards [ 'of1j13Top            '  ]  =       [    'ggH/Moriond/datacards/hww2l2v_13TeV_top_of1j/events/datacard.txt.pruned.txt'                 ,    'False'    ]
list_datacards [ 'of0j13DYtt           '  ]  =       [    'ggH/Moriond/datacards/hww2l2v_13TeV_dytt_of0j/events/datacard.txt.pruned.txt'                ,    'False'    ]
list_datacards [ 'of1j13DYtt           '  ]  =       [    'ggH/Moriond/datacards/hww2l2v_13TeV_dytt_of1j/events/datacard.txt.pruned.txt'                ,    'False'    ]
list_datacards [ 'of2j2j13             '  ]  =       [    'ggH2j/Moriond/datacards/hww2l2v_13TeV_of2j/mllVSmth/datacard.txt.pruned.txt'                 ,    'True'    ]
list_datacards [ 'of2j2j13Top          '  ]  =       [    'ggH2j/Moriond/datacards/hww2l2v_13TeV_top_of2j/events/datacard.txt.pruned.txt'               ,    'False'    ]
list_datacards [ 'of2j2j13DYtt         '  ]  =       [    'ggH2j/Moriond/datacards/hww2l2v_13TeV_dytt_of2j/events/datacard.txt.pruned.txt'              ,    'False'    ]
list_datacards [ 'of2jvbf13            '  ]  =       [    'VBF/Moriond/datacards/hww2l2v_13TeV_of2j_vbf_lowmjj/mll/datacard.txt.pruned.txt'             ,    'True'    ]
list_datacards [ 'of2jvbf13Top         '  ]  =       [    'VBF/Moriond/datacards/hww2l2v_13TeV_top_of2j_vbf/events/datacard.txt.pruned.txt'             ,    'False'    ]
list_datacards [ 'of2jvbf13DYtt        '  ]  =       [    'VBF/Moriond/datacards/hww2l2v_13TeV_dytt_of2j_vbf/events/datacard.txt.pruned.txt'            ,    'False'    ]
list_datacards [ 'of2jvh2j13           '  ]  =       [    'VH2j/Moriond/datacards/hww2l2v_13TeV_of2j_vh2j/mll/datacard.txt.pruned.txt'                  ,    'True'    ]
list_datacards [ 'of2jvh2j13Top        '  ]  =       [    'VH2j/Moriond/datacards/hww2l2v_13TeV_top_of2j_vh2j/events/datacard.txt.pruned.txt'           ,    'False'    ]
list_datacards [ 'of2jvh2j13DYtt       '  ]  =       [    'VH2j/Moriond/datacards/hww2l2v_13TeV_dytt_of2j_vh2j/events/datacard.txt.pruned.txt'          ,    'False'    ]
list_datacards [ 'wh3lossf             '  ]  =       [    'WH3l/Moriond/datacards/wh3l_13TeV_ossf/drllmin3l/datacard.txt.pruned.txt'                    ,    'True'    ]
list_datacards [ 'wh3lsssf             '  ]  =       [    'WH3l/Moriond/datacards/wh3l_13TeV_sssf/drllmin3l/datacard.txt.pruned.txt'                    ,    'True'    ]
list_datacards [ 'wh3lwz               '  ]  =       [    'WH3l/Moriond/datacards/wh3l_wz_13TeV/events/datacard.txt.pruned.txt'                         ,    'False'    ]
list_datacards [ 'wh3lzg               '  ]  =       [    'WH3l/Moriond/datacards/wh3l_zg_13TeV/events/datacard.txt.pruned.txt'                         ,    'False'    ]
list_datacards [ 'ICHEP_em_mp_1j_13    '  ]  =       [    'ggH/datacards/hww2l2v_13TeV_em_mp_1j/mllVSmth/datacard.txt.pruned.txt'                       ,    'True'    ]
list_datacards [ 'ICHEP_me_mp_1j_13    '  ]  =       [    'ggH/datacards/hww2l2v_13TeV_me_mp_1j/mllVSmth/datacard.txt.pruned.txt'                       ,    'True'    ]
list_datacards [ 'ICHEP_em_mp_0j_13    '  ]  =       [    'ggH/datacards/hww2l2v_13TeV_em_mp_0j/mllVSmth/datacard.txt.pruned.txt'                       ,    'True'    ]
list_datacards [ 'ICHEP_me_mp_0j_13    '  ]  =       [    'ggH/datacards/hww2l2v_13TeV_me_mp_0j/mllVSmth/datacard.txt.pruned.txt'                       ,    'True'    ]
list_datacards [ 'ICHEP_em_pm_1j_13    '  ]  =       [    'ggH/datacards/hww2l2v_13TeV_em_pm_1j/mllVSmth/datacard.txt.pruned.txt'                       ,    'True'    ]
list_datacards [ 'ICHEP_me_pm_1j_13    '  ]  =       [    'ggH/datacards/hww2l2v_13TeV_me_pm_1j/mllVSmth/datacard.txt.pruned.txt'                       ,    'True'    ]
list_datacards [ 'ICHEP_em_pm_0j_13    '  ]  =       [    'ggH/datacards/hww2l2v_13TeV_em_pm_0j/mllVSmth/datacard.txt.pruned.txt'                       ,    'True'    ]
list_datacards [ 'ICHEP_me_pm_0j_13    '  ]  =       [    'ggH/datacards/hww2l2v_13TeV_me_pm_0j/mllVSmth/datacard.txt.pruned.txt'                       ,    'True'    ]
list_datacards [ 'ICHEP_of0j13Top      '  ]  =       [    'ggH/datacards/hww2l2v_13TeV_top_of0j/events/datacard.txt.pruned.txt'                         ,    'False'    ]
list_datacards [ 'ICHEP_of1j13Top      '  ]  =       [    'ggH/datacards/hww2l2v_13TeV_top_of1j/events/datacard.txt.pruned.txt'                         ,    'False'    ]
list_datacards [ 'ICHEP_of0j13DYtt     '  ]  =       [    'ggH/datacards/hww2l2v_13TeV_dytt_of0j/events/datacard.txt.pruned.txt'                        ,    'False'    ]
list_datacards [ 'ICHEP_of1j13DYtt     '  ]  =       [    'ggH/datacards/hww2l2v_13TeV_dytt_of1j/events/datacard.txt.pruned.txt'                        ,    'False'    ]
list_datacards [ 'ICHEP_of2j2j13       '  ]  =       [    'ggH2j/datacards/hww2l2v_13TeV_of2j/mllVSmth/datacard.txt.pruned.txt'                         ,    'True'    ]
list_datacards [ 'ICHEP_of2j2j13Top    '  ]  =       [    'ggH2j/datacards/hww2l2v_13TeV_top_of2j/events/datacard.txt.pruned.txt'                       ,    'False'    ]
list_datacards [ 'ICHEP_of2j2j13DYtt   '  ]  =       [    'ggH2j/datacards/hww2l2v_13TeV_dytt_of2j/events/datacard.txt.pruned.txt'                      ,    'False'    ]
list_datacards [ 'ICHEP_of2jvbf13      '  ]  =       [    'VBF/datacards/hww2l2v_13TeV_of2j_vbf_lowmjj/mllfine/datacard.txt.pruned.txt'                 ,    'True'    ]
list_datacards [ 'ICHEP_of2jvbf13Top   '  ]  =       [    'VBF/datacards/hww2l2v_13TeV_top_of2j_vbf/events/datacard.txt.pruned.txt.filtered.txt'        ,    'False'    ]
list_datacards [ 'ICHEP_of2jvbf13DYtt  '  ]  =       [    'VBF/datacards/hww2l2v_13TeV_dytt_of2j_vbf/events/datacard.txt.pruned.txt.filtered.txt'       ,    'False'    ]
list_datacards [ 'ICHEP_of2jvh2j13     '  ]  =       [    'VH2j/datacards/hww2l2v_13TeV_of2j_vh2j/mll/datacard.txt.pruned.txt'                          ,    'True'    ]
list_datacards [ 'ICHEP_of2jvh2j13Top  '  ]  =       [    'VH2j/datacards/hww2l2v_13TeV_top_of2j_vh2j/events/datacard.txt.pruned.txt'                   ,    'False'    ]
list_datacards [ 'ICHEP_of2jvh2j13DYtt '  ]  =       [    'VH2j/datacards/hww2l2v_13TeV_dytt_of2j_vh2j/events/datacard.txt.pruned.txt'                  ,    'False'    ]
list_datacards [ 'ICHEP_wh3lossf       '  ]  =       [    'WH3l/datacards/wh3l_13TeV_ossf/drllmin3l/datacard.txt.pruned.txt'                            ,    'True'    ]
list_datacards [ 'ICHEP_wh3lsssf       '  ]  =       [    'WH3l/datacards/wh3l_13TeV_sssf/drllmin3l_sssf/datacard.txt.pruned.txt'                       ,    'True'    ]
list_datacards [ 'ICHEP_wh3lwz         '  ]  =       [    'WH3l/datacards/wh3l_wz_13TeV/events/datacard.txt.pruned.txt'                                 ,    'False'    ]
list_datacards [ 'ICHEP_wh3lzg         '  ]  =       [    'WH3l/datacards/wh3l_zg_13TeV/events/datacard.txt.pruned.txt'                                 ,    'False'    ]
                    

for datacardName, datacard in list_datacards.iteritems():
  #print " datacardName = " , datacardName,
  #print " --> datacard = " , datacard[0]
  
  datacardName = datacardName.replace(' ', '')
  
  if datacard[1] == "False" :
    sys.stdout.write(' python      systematicsAnalyzer.py ' + folder + '/' + datacard[0]                  + ' --all  --legend  ' + datacardName + '   -m      125     -f    tex    -o miniTable_' +  datacardName +  '.tex     >    ' +   datacardName +  '.tex   \n')
  else :
    sys.stdout.write(' python      systematicsAnalyzer.py ' + folder + '/' + datacard[0] +  '   --blind ' + ' --all  --legend  ' + datacardName + '   -m      125     -f    tex    -o miniTable_' +  datacardName +  '.tex     >    ' +   datacardName +  '.tex   \n')
  




#for datacardName, datacard in list_datacards.iteritems():
  #datacardName = datacardName.replace(' ', '')
  #sys.stdout.write(' mkdir ~/public/xLatinos/ICHEP2016/' + datacardName + '\n')
  #sys.stdout.write(' cp    ' + folder +  datacard[0]  + '  ~/public/xLatinos/ICHEP2016/' +  datacardName +  '/    \n')
  
 
 
 
 







