#!/bin/bash
params compose ../../../templates/template.params -f "../../test.txt;../loc.txt;found.txt" -o instance.yaml
kiva instance.yaml ../*.epw Timeseries.csv
