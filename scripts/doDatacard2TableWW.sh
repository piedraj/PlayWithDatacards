

echo "DF 0J"
python tableFromCards.py  /afs/cern.ch/user/a/amassiro/public/xLatinos/ww/WWDFcut0jet/hww-19.36fb.mH125.of_0j_shape.txt

echo "DF 1J"
python tableFromCards.py  /afs/cern.ch/user/a/amassiro/public/xLatinos/ww/WWDFcut1jet/hww-19.36fb.mH125.of_1j_shape.txt

echo "SF 0J"
python tableFromCards.py  /afs/cern.ch/user/a/amassiro/public/xLatinos/ww/WWSFcut0jet/hww-19.36fb.mH125.sf_0j_shape.txt

echo "SF 1J"
python tableFromCards.py  /afs/cern.ch/user/a/amassiro/public/xLatinos/ww/WWSFcut1jet/hww-19.36fb.mH125.sf_1j_shape.txt

echo "All"
python tableFromCards.py  /afs/cern.ch/user/a/amassiro/public/xLatinos/ww/hww-19.36fb.mH125.txt