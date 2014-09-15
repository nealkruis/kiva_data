#!/bin/bash

if [ $# -ne 1 ]
then
  echo "Invalid arguments: enter only the walltime length in hours"
  exit 1
fi

queue='serial'

cpus=24

temp=$(dirname $(dirname $PWD))
test=${temp##*/}
temp=$(dirname $PWD)
case=${temp##*/}
soln=${PWD##*/}

sbatch --qos $queue --workdir=$PWD --nodes=1 --ntasks-per-node=$cpus --time=$1:00:00 \
--export=GOMP_CPU_AFFINITY="0-$(( cpus - 1 ))" \
--output=log.out --error=error.out \
--mail-type=ALL --mail-user=neal.kruis@bigladdersoftware.com \
--job-name=$test-$case-$soln run.sh
