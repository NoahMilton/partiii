#!/bin/bash
#Let's get some color
RED='\033[0;31m'
UBlue='\033[4;34m'
NC='\033[0m' # No Color
#
folderprefix=modulus_           #prefix for location of vel_ directories that ontain force files
filetomove=force_jkrpw.csv      #file to move and gather from each vel_ dir.

folderofcsvs=force_jkrpw_
velocityfiles=vel_
N=99				#number of velocity files in each case

for i in ./$folderprefix*
do
        cd $i
        bash /home/nm623/tools/moveFile_rename.sh $filetomove   #moveFile
        #cd $folderofcsvs$i
	#python3 /home/nm623/tools/python/coeffs_of_restitution10.py $velocityfiles $N
	#cd ..
	cd ..
done

for i in $folderprefix*
do
	cd $i
	cd $folderofcsvs$i
	python3 /home/nm623/tools/python/coeffs_of_restitution11.py $velocityfiles $N ../../CORs$i
	cd ..
	cd ..
done
