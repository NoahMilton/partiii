#/bin/bash
#Let's get some color
RED='\033[0;31m'
UBlue='\033[4;34m'
NC='\033[0m' # No Color
#

#Input here
casePrefix=vel_			#change here 
batchPrefix=optimum_ 		#change here
inFile=in.jkrpw 		#change here !! name of the liggghts input file
j=0 		# Number of modulus cases record
k=1		# Number of cpu to use, here use 1
seed1=aaaa      # string to replace for velocity 
seed2=bbbb 	# string to replace for modulus
rep2=(1)	# modulus values to use
init=2.0	# Values for velocity calculations in python
step=0.1
mkdir -p "$batchPrefix"{01} 	#change here number of modulus cases to run  
for i in ./$batchPrefix*
do 
  if [ -d "$i" ] 	#check if it is a directory
  then 
      \cp -rf $inFile $i 	#copy input file
      cp ~/tools/LIGGGHTS/*.sh $i 	#copy a bash file here
      cp -rf DoE_ligght_queue_python.sh $i
      cd $i  
      echo -e " ${RED}case $j:${NC} seed: $seed2 rep: ${rep2[$j]}" 	#print the case num and rep val
      sed -i 's/'"$seed2"'/'"${rep2[$j]}"'/g' in.jkrpw 	# Change rep2[$j] to rep2 if using python
	#rep1=(2.5) not needed for python version. If (1 2 3) change echo and sed to rep1[$j]
      n=0	# Number of velocity cases, record

	mkdir -p "$casePrefix"{001..190}  #change here, number of velocity cases to run
	for i in ./$casePrefix*
	do
	  if [ -d "$i" ]        #check if a velocity directory
	  then
	      \cp -rf $inFile $i        #copy the input file
	      cp ~/tools/LIGGGHTS/*.sh $i       #copy a bash file here
	      cd $i                     #enter the velocity directory 
	      rep1=$(python3 -c "print($step*($n)+$init)")	# calculate this velocity
	      echo -e " ${RED}case $j:${NC} seed: $seed1 rep: ${rep1}"  #To print the case num and rep val
	      sed -i 's/'"$seed1"'/'"${rep1}"'/g' in.jkrpw              #To print the case num and rep val
	      mv $inFile in.liggghts    #change the name of liggght input which is required in runOneJob.sh
	      bash runOneJob.sh $k      #run liggghts in the queue system
	      n=$(( n+1 ))              #increase n
	      cd ..                     #go to the modulus directory for next file   
	  fi
	done

      j=$(( j+1 )) 		#increase j for next modulus directory
      cd ..   			#go to the parent directory for next modulus batch   
  fi
done
