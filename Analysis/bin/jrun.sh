#!/bin/bash

if [ $# -lt 1 ]
then
  echo "Invalid arguments: enter at least the walltime length in hours."
  echo "Other arguments are [queue name] and [number of cpus]."
  exit 1
fi

if [ $# -gt 1 ]
then
  queue=$2
  cpus=$3
else
  queue='serial'
  cpus=24
fi

temp=$(dirname $(dirname $PWD))
test=${temp##*/}
temp=$(dirname $PWD)
case=${temp##*/}
soln=${PWD##*/}

sleep 1

sbatch --qos $queue --workdir=$PWD --nodes=1 --ntasks-per-node=$cpus --time=$1:00:00 \
--export=GOMP_CPU_AFFINITY="0-$(( cpus - 1 ))" \
--output=log.out --error=error.out \
--mail-type=ALL --mail-user=neal.kruis@bigladdersoftware.com \
--job-name=$test-$case-$soln run.sh
