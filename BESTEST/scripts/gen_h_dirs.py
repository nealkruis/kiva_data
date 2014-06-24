import sys
import csv
import os

with open('../H-Sens/solns.csv','rU') as f:
    reader = csv.reader(f)
    reader.next()
    for row in reader:
        dir_name = 'M'+row[0]+'T'+row[1]+'P'+row[2]+'N'+row[3]+'W'+row[4]
        if not os.path.exists('../H-Sens/'+dir_name):
            os.makedirs('../H-Sens/'+dir_name)
            os.symlink('../../bin/run.sh','../H-Sens/'+dir_name+'/run.sh')
            os.symlink('../../bin/jrun.sh','../H-Sens/'+dir_name+'/jrun.sh')
            with open('../H-Sens/'+dir_name+'/soln.txt','w') as soln:
                soln.write('# Set values below\n\n')
                if (row[0] == "K"):
                  soln.write(':init_method=>"KUSUDA",\n')
                elif (row[0] == "C"):
                  soln.write(':init_method=>"CONSTANT",\n')
                else: # elif (row[0] == "S"):
                  soln.write(':init_method=>"STEADY-STATE",\n')
                soln.write(':init_temp=>'+row[1]+',\n')
                soln.write(':imp_timestep=>'+row[2]+',\n')
                soln.write(':imp_periods=>'+row[3]+',\n')
                soln.write(':warmup_days=>'+str(int(row[4])/24))


if __name__ == '__main__':
    pass