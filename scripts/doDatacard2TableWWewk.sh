
mkdir scripts/WWewk/
cp -r /afs/cern.ch/user/a/amassiro/scratch0/VBF/Limit/CMSSW_6_1_0/src/qqHWWlnln-WW2jewk-2012-01Jan-Cut2012-SF-21/   scripts/WWewk/
cp -r /afs/cern.ch/user/a/amassiro/scratch0/VBF/Limit/CMSSW_6_1_0/src/qqHWWlnln-WW2jewk-2012-01Jan-Cut2012-SF-05/   scripts/WWewk/
cp -r /afs/cern.ch/user/a/amassiro/scratch0/VBF/Limit/CMSSW_6_1_0/src/qqHWWlnln-WW2jewk-2012-01Jan-Cut2012-DF-21/   scripts/WWewk/
cp -r /afs/cern.ch/user/a/amassiro/scratch0/VBF/Limit/CMSSW_6_1_0/src/qqHWWlnln-WW2jewk-2012-01Jan-Cut2012-DF-05/   scripts/WWewk/


cd scripts/WWewk/qqHWWlnln-WW2jewk-2012-01Jan-Cut2012-SF-21/
python     ../../../../ModificationDatacards/TransformShapeToCutBased.py     -d    hww-19.36fb.mH125.sf_2j_shape.txt
cd -

cd scripts/WWewk/qqHWWlnln-WW2jewk-2012-01Jan-Cut2012-SF-05/
python     ../../../../ModificationDatacards/TransformShapeToCutBased.py     -d    hww-19.36fb.mH125.sf_2jtche05_shape.txt
cd -

cd scripts/WWewk/qqHWWlnln-WW2jewk-2012-01Jan-Cut2012-DF-21/
python     ../../../../ModificationDatacards/TransformShapeToCutBased.py     -d    hww-19.36fb.mH125.of_2j_shape.txt
cd -

cd scripts/WWewk/qqHWWlnln-WW2jewk-2012-01Jan-Cut2012-DF-05/
python     ../../../../ModificationDatacards/TransformShapeToCutBased.py     -d    hww-19.36fb.mH125.of_2jtche05_shape.txt
cd -




echo "SF loose tche"
python bigTableFromCards.py  scripts/WWewk/qqHWWlnln-WW2jewk-2012-01Jan-Cut2012-SF-21/hww-19.36fb.mH125.sf_2j_shape.txt    -f scripts/joinSamples.py


# tableFromCards.py

echo "SF tight tche"
python bigTableFromCards.py  scripts/WWewk/qqHWWlnln-WW2jewk-2012-01Jan-Cut2012-SF-05/hww-19.36fb.mH125.sf_2jtche05_shape.txt
# tableFromCards.py

echo "DF loose tche"
python bigTableFromCards.py  scripts/WWewk/qqHWWlnln-WW2jewk-2012-01Jan-Cut2012-DF-21/hww-19.36fb.mH125.of_2j_shape.txt
# tableFromCards.py

echo "DF tight tche"
python bigTableFromCards.py  scripts/WWewk/qqHWWlnln-WW2jewk-2012-01Jan-Cut2012-DF-05/hww-19.36fb.mH125.of_2jtche05_shape.txt
# tableFromCards.py
