unset module
#!/bin/bash
#set -xv
## The Script
## Change into the current working directory
#$ -cwd
##
## Pass all environment variables to the job_maybe not required
#$ -V 
##
## To use bash _maybe not required
#$ -S /bin/bash
##
## The name for the job. It will be displayed this way on qstat
# 
##
## Number of cores to request
#
##
## Queue Name
# 
##
##
# 
# 

##Run the job
## ${COMMAND}
##
##Get the fold name
PPREFIX="${PWD##*/}"
echo $PWD
echo $PPREFIX
date1=$(date +"%s")

CORES=$NSLOTS

#cat /proc/cpuinfo
hostname
echo "We submit id ($SGE_TASK_ID) using $NSLOTS cpu on $(date) " > time.log

# We only need our anancoda libraries
# module purge
#source /home/xizhong/anaconda3/bin/activate mfix-19.1

##Run the job
caseName=$(ls in.liggghts) #only one mfx should be exist in the fold
echo $caseName
mpirun -np ${CORES} $HOME/LIGGGHTS/LIGGGHTS-PUBLIC/lmp_auto -in $caseName | tee lmp.log

echo "The job ${JOBID} finished on $(date)" >>time.log
date2=$(date +"%s")
DIFF=$(($date2-$date1))
echo "Duration: $(($DIFF / 3600 )) hours $((($DIFF % 3600) / 60)) minutes $(($DIFF % 60)) seconds" >> time.log
#! And use date to convert the seconds back to something more meaningful
echo Took `date +%H:%M:%S -ud @${DIFF}`
echo "Total time in second: $DIFF">>time.log

##Run the job
####${COMMAND}
