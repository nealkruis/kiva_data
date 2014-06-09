#!/bin/bash
params compose ../../../templates/template.params -f "../../test.txt;../case.txt;soln.txt" -o instance.yaml
kiva instance.yaml ../*.epw Timeseries.csv
