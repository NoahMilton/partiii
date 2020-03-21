#/bin/bash
#Let's get some color
RED='\033[0;31m'
UBlue='\033[4;34m'
NC='\033[0m' # No Color
#

#Input here
casePrefix=vel_ 		#change here!! xizhong
inFile=in.hertz 		#change here !! name of the liggghts input file
k=1 		#number of cpu to be use; here 1 cpu
j=0 		# To record number of cases, we start with 0
seed1=aaaa 	#string to be replace
#rep1=(2.5) not needed for python version 	#change here !!, the values of velocity to be run
mkdir -p "$casePrefix"{01..99} 	#change here !!, the last 11 is the number of cases to run
init=3.1                        #only use for python line can ignore if that line is comment
step=0.1   
for i in ./$casePrefix*	 	#loop all cases
do 
  if [ -d "$i" ] 	#check if it is a directory
  then 
      \cp -rf $inFile $i 	#copy the input file (change here!!)
      cp ~/tools/LIGGGHTS/*.sh $i 	#copy a bash file here
      cd $i 			#enter the directory 
      rep1=$(python3 -c "print($step*($j)+$init)")    
      echo -e " ${RED}case $j:${NC} seed: $seed1 rep: ${rep1}" 	#To print the case num and rep val
      sed -i 's/'"$seed1"'/'"${rep1}"'/g' in.hertz 			#To print the case num and rep val
      mv $inFile in.liggghts 	# change the name of liggght input which is required in runOneJob.sh
      bash runOneJob.sh $k	#run liggghts in the queue system
      j=$(( j+1 )) 		#increase j
      cd ..   			#go to the parent directory for next file   
  fi
done

#find the keyword line and output $6 str
#grep -i 'pack seed' in.* | awk {'print $6'}
 
