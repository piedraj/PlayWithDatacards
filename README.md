PlayWithDatacards
=================

Tools for datacards

Where:

    /afs/cern.ch/user/a/amassiro/Limit/PlayWithDatacards


# Modification tools

look here:

    https://github.com/amassiro/ModificationDatacards



# Transform datacard into a table:


    python tableFromCards.py  /afs/cern.ch/user/a/amassiro/public/xLatinos/ww/WWDFcut0jet/hww-19.36fb.mH125.of_0j_shape.txt

    python tableFromCards.py   /afs/cern.ch/user/a/amassiro/Limit/ModificationDatacards/hwidth/0jetDF8TeV/hww-19.36fb.mH125.of_0j_shape.txt
    python tableFromCards.py   /afs/cern.ch/user/a/amassiro/Limit/ModificationDatacards/hwidth/1jetDF8TeV/hww-19.36fb.mH125.of_1j_shape.txt
    python tableFromCards.py   /afs/cern.ch/user/a/amassiro/Limit/ModificationDatacards/hwidth/2jetDF8TeV/hww-19.36fb.mH125.of_2j_shape.txt

    python tableFromCards.py   /afs/cern.ch/user/a/amassiro/Framework/CMSSW_7_6_3/src/PlotsConfigurations/Configurations/ggHTest/datacards/hww2l2v_13TeV_em_0j/mllVSmth/datacard.txt
    


# expand all nuisances:

    python bigTableFromCards.py  /afs/cern.ch/user/a/amassiro/public/xLatinos/ww/WWDFcut0jet/hww-19.36fb.mH125.of_0j_shape.txt
    python bigTableFromCards.py --file scripts/joinSamples.py  /afs/cern.ch/user/a/amassiro/public/xLatinos/ww/WWDFcut0jet/hww-19.36fb.mH125.of_0j_shape.txt
    
    python bigTableFromCards.py --file scripts/joinSamples.py  /afs/cern.ch/user/a/amassiro/public/xLatinos/ww_26Sep2014_MG/WWDFcut0jet/hww-19.36fb.mH125.of_0j_shape.txt
    python bigTableFromCards.py --file scripts/joinSamples.py  /afs/cern.ch/user/a/amassiro/public/xLatinos/ww_26Sep2014_MG/WWSFcut0jet/hww-19.36fb.mH125.sf_0j_shape.txt

    python bigTableFromCards.py --file scripts/joinSamples.py  /afs/cern.ch/user/a/amassiro/public/xLatinos/ww_26Sep2014_POW/WWDFcut0jet/hww-19.36fb.mH125.of_0j_shape.txt
    python bigTableFromCards.py --file scripts/joinSamples.py  /afs/cern.ch/user/a/amassiro/public/xLatinos/ww_26Sep2014_POW/WWSFcut0jet/hww-19.36fb.mH125.sf_0j_shape.txt

    python bigTableFromCards.py --file scripts/joinSamples.py  /afs/cern.ch/user/a/amassiro/public/xLatinos/ww_26Sep2014_MCatNLO/WWDFcut0jet/hww-19.36fb.mH125.of_0j_shape.txt
    python bigTableFromCards.py --file scripts/joinSamples.py  /afs/cern.ch/user/a/amassiro/public/xLatinos/ww_26Sep2014_MCatNLO/WWSFcut0jet/hww-19.36fb.mH125.sf_0j_shape.txt

    python bigTableFromCards.py --file scripts/joinSamples.py  /afs/cern.ch/user/a/amassiro/public/xLatinos/ww_17Oct2014_POW/WWDFcut0jet/hww-19.36fb.mH125.of_0j_shape.txt
    python bigTableFromCards.py --file scripts/joinSamples.py  /afs/cern.ch/user/a/amassiro/public/xLatinos/ww_17Oct2014_POW/WWSFcut0jet/hww-19.36fb.mH125.sf_0j_shape.txt

    python bigTableFromCards.py --file scripts/joinSamples_hwidth.py  /afs/cern.ch/user/a/amassiro/Limit/ModificationDatacards/hwidth/0jetDF8TeV/hww-19.36fb.mH125.of_0j_shape.txt
    python bigTableFromCards.py --file scripts/joinSamples_hwidth.py  /afs/cern.ch/user/a/amassiro/Limit/ModificationDatacards/hwidth/1jetDF8TeV/hww-19.36fb.mH125.of_1j_shape.txt
    python bigTableFromCards.py --file scripts/joinSamples_hwidth.py  /afs/cern.ch/user/a/amassiro/Limit/ModificationDatacards/hwidth/2jetDF8TeV/hww-19.36fb.mH125.of_2j_shape.txt

    python superBigTableFromCards.py --file scripts/joinSamples_hwidth.py  /afs/cern.ch/user/a/amassiro/Limit/ModificationDatacards/hwidth/0jetDF8TeV/hww-19.36fb.mH125.of_0j_shape.txt
    python superBigTableFromCards.py --file scripts/joinSamples_hwidth.py  /afs/cern.ch/user/a/amassiro/Limit/ModificationDatacards/hwidth/1jetDF8TeV/hww-19.36fb.mH125.of_1j_shape.txt
    python superBigTableFromCards.py --file scripts/joinSamples_hwidth.py  /afs/cern.ch/user/a/amassiro/Limit/ModificationDatacards/hwidth/2jetDF8TeV/hww-19.36fb.mH125.of_2j_shape.txt

    python bigTableFromCards.py   --file scripts/joinSamples_ggH.py    /afs/cern.ch/user/a/amassiro/Framework/CMSSW_7_6_3/src/PlotsConfigurations/Configurations/ggHTest/datacards/hww2l2v_13TeV_em_0j/mllVSmth/datacard.txt
    



e.g.

    for ww
    bash scripts/doDatacard2TableWW.sh

    for wwewk
    bash scripts/doDatacard2TableWWewk.sh


# Combine cards

    cd /afs/cern.ch/user/a/amassiro/scratch0/VBF/Limit/CMSSW_6_1_0/src
    export SCRAM_ARCH=slc5_amd64_gcc462
    cmsenv
    combineCards.py ww_sf_0j=/afs/cern.ch/user/a/amassiro/public/xLatinos/ww/WWSFcut0jet/hww-19.36fb.mH125.sf_0j_shape.txt   \
                    ww_of_0j=/afs/cern.ch/user/a/amassiro/public/xLatinos/ww/WWDFcut0jet/hww-19.36fb.mH125.of_0j_shape.txt   \
                    ww_sf_1j=/afs/cern.ch/user/a/amassiro/public/xLatinos/ww/WWSFcut1jet/hww-19.36fb.mH125.sf_1j_shape.txt   \
                    ww_of_1j=/afs/cern.ch/user/a/amassiro/public/xLatinos/ww/WWDFcut1jet/hww-19.36fb.mH125.of_1j_shape.txt > \
                    /afs/cern.ch/user/a/amassiro/public/xLatinos/ww/hww-19.36fb.mH125.txt


# Official tools

    python      test/systematicsAnalyzer.py    \
        /afs/cern.ch/user/a/amassiro/Framework/CMSSW_7_6_3/src/PlotsConfigurations/Configurations/ggHTest/datacards/hww2l2v_13TeV_em_0j/mllVSmth/datacard.txt   \
       --all    -m      125     -f      html    >       ~/www/tmp/ggh_systematics.html
    
    python      test/systematicsAnalyzer.py    \
        /afs/cern.ch/user/a/amassiro/Framework/CMSSW_7_6_3/src/PlotsConfigurations/Configurations/ggHTest/datacards/hww2l2v_13TeV_em_0j/mllVSmth/datacard.txt   \
       --all    -m      125     -f      tex    >     hww2l2v_13TeV_em_0j.tex
    

    
    # do all these steps
    
    cd /afs/cern.ch/user/a/amassiro/Limit/PlayWithDatacards
    cd /afs/cern.ch/user/a/amassiro/Framework/Combine/CMSSW_7_1_15/src/HiggsAnalysis/CombinedLimit
    cmsenv
    scramv1 b -j 20
    cd -
    
    python      systematicsAnalyzer.py    \
        /afs/cern.ch/user/a/amassiro/Framework/CMSSW_7_6_3/src/PlotsConfigurations/Configurations/ggHTest/datacards/hww2l2v_13TeV_em_0j/mllVSmth/datacard.txt   \
       --all    -m      125     -f      tex    >     hww2l2v_13TeV_em_0j.tex
    
    python      systematicsAnalyzer.py    \
        /afs/cern.ch/user/a/amassiro/Framework/CMSSW_7_6_3/src/PlotsConfigurations/Configurations/ggHTest/datacards/hww2l2v_13TeV_me_0j/mllVSmth/datacard.txt   \
       --all    -m      125     -f      tex    >     hww2l2v_13TeV_me_0j.tex
    
    python      systematicsAnalyzer.py    \
        /afs/cern.ch/user/a/amassiro/Framework/CMSSW_7_6_3/src/PlotsConfigurations/Configurations/ggHTest/datacards/hww2l2v_13TeV_em_1j/mllVSmth/datacard.txt   \
       --all    -m      125     -f      tex    >     hww2l2v_13TeV_em_1j.tex
    
    python      systematicsAnalyzer.py    \
        /afs/cern.ch/user/a/amassiro/Framework/CMSSW_7_6_3/src/PlotsConfigurations/Configurations/ggHTest/datacards/hww2l2v_13TeV_me_1j/mllVSmth/datacard.txt   \
       --all    -m      125     -f      tex    >     hww2l2v_13TeV_me_1j.tex
    
    
    
    
    
    
    
    
    