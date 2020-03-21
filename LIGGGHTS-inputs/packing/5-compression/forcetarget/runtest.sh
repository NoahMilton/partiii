unset module
# Test script to run a simulation and output files in a more tidy way
# want easy access to:
#			rdfoutput.txt	coordination.csv	post/* 
#/bin/bash
#Let's get some color
RED='\033[0;31m'
UBlue='\033[4;34m'
NC='\033[0m' # No Color
#

variable=forcetarget_		# change variable
rep1=(0.01 0.1 1 10 100)	# change values to use for 'variable'
inFile=in.liggghts			# ensure correct
k=2	# Number of cores to use

len=${#rep1[*]}
echo "$variable" > variables.txt        # output the rep1 values to .txt
echo "$len" >>variables.txt
for (( i=0; i<len; i++)); do echo "${rep1[$i]}" >> variables.txt ; done

seed1=aaaa
j=0	#initialise the 'value' index
batchPrefix=$variable            #change here

mkdir -p "$batchPrefix"{01..05}		# ensure match w. number of values for rep1
for i in ./$batchPrefix*
do
  if [ -d "$i" ]	# check if a directory exists
  then
     cp -rf $inFile $i  #in.liggghts	# past as in.liggghts as required by qsub
     cp ~/tools/LIGGGHTS/*.sh $i			# copy bash files for qsub_node.sh and runOnejob.sh
     cp -rf top_plate.stl $i
     cd $i 					# enter that directory
     mv $inFile in.liggghts
     sed -i 's/'"$seed1"'/'"${rep1[$j]}"'/g' in.liggghts 	# Change rep2[$j] to rep2 if using python
     bash runOneJob.sh $k		# run liggghts in que system using number of cores specified
     j=$(( j+1 ))		# increase j to go to the next 
     cd ..			# go to parent directory for next run
  fi
done
