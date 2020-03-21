unset module
#!/bin/bash
#This is to batch run a series of cases
#usage chmod 755 run.sh or bash run.sh

#Here is the input
JOB_NAME=${PWD##*/}
QUEUE='new.q'
NODE='20'
CORES='5'


#Let's get some color first
RED='\033[0;31m'
UBlue='\033[4;34m'
NC='\033[0m' # No Color

#check if there is input
if [ $# -gt 0 ]; then
    echo -e "${UBlue}qsub contains $# arguments${NC}"
    if [ $# -eq 3 ]; then
        QUEUE=$1
        NODE=$(printf "%d" $2)
        CORES=$(printf "%d" $3) 
    elif [ $# -eq 2 ]; then
        NODE=$(printf "%d" $1)
        CORES=$(printf "%d" $2) 
    elif [ $# -eq 1 ]; then
        CORES=$(printf "%d" $1)
    else
        echo -e "${RED}Something wrong with the number of input ${NC}"
        exit 0
    fi
else
    echo -e "${RED}Command line contains no arguments, we use default settings${NC}"
fi

if [ $# -gt 1 ]; then
	FULLQ=${QUEUE}'@compute-0-'${NODE}
else
	FULLQ=${QUEUE}
fi

echo -e "${RED}Directory: $PWD${NC}?" #current folder name with full path
echo -e "Folder Name: ${RED} ${PWD##*/}${NC}" #current folder name without prefix
echo -e "We are going to submit ${RED}${CORES} CPU ${NC} job to  ${RED}${FULLQ}${NC}\n"
echo -e "Please remember to change ${RED} liggghts exe ${NC} and  ${RED} input file in qsub ${NC}\n"

#seed=$(grep -i 'np' qsub_node.sh | awk {'print $3'})
#echo $seed
# -i is to rewrite the in file
#sed -i 's/'"$seed"'/'"$CORES"'/g' qsub_node.sh
rm -rf output.* error.*
qsub -q ${FULLQ}  -pe mpi ${CORES} -N ${JOB_NAME} -o output.${JOB_NAME} -e error.${JOB_NAME} qsub_node.sh | tee qsub.log

