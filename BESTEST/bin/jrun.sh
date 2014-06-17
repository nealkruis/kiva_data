#!/bin/bash

if [ $# -ne 1 ]
then
  echo "Invalid arguments: enter only the walltime length in hours"
  exit 1
fi

rm -f log.out
rm -f error.out

#if [ $1 -gt 4 ]
#then
#  queue='janus-long'
#else
#  queue='janus-short'
#fi

queue='serial'

cpus=24

temp=$(dirname $(dirname $PWD))
test=${temp##*/}
temp=$(dirname $PWD)
case=${temp##*/}
soln=${PWD##*/}

#qsub -q $queue -d $PWD -l nodes=1:ppn=$cpus,walltime=$1:00:00 -v GOMP_CPU_AFFINITY="0-$(( cpus - 1 ))" -j oe -o log.out -m abe -M neal.kruis@bigladdersoftware.com -N $test-$case-$soln run.sh
sbatch --qos $queue --workdir=$PWD --nodes=1 --ntasks-per-node=$cpus --time=$1:00:00 \
--export=GOMP_CPU_AFFINITY="0-$(( cpus - 1 ))" \
--output=log.out --error=error.out \
--mail-type=ALL --mail-user=neal.kruis@bigladdersoftware.com \
--job-name=$test-$case-$soln run.sh
