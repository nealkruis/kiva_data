import sys
import csv
import os

with open('founds.csv','rU') as f:
    reader = csv.reader(f)
    reader.next()
    for row in reader:
        dir_name = 'S'+row[0]+'AP'+row[1]+'HV'+row[2]+'A'+row[3]
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
            os.symlink('../../bin/run.sh',dir_name+'/run.sh')
            os.symlink('../../bin/jrun.sh',dir_name+'/jrun.sh')
            with open(dir_name+'/found.txt','w') as soln:
                soln.write('# Set values below\n\n')
                if row[0] == 'S':
                  soln.write(":foundation_shape=>'-',\n")
                  soln.write(":foundation_area=>"+row[3]+"|'ft2',\n")
                  soln.write(":foundation_aspect_ratio=>1")
                elif row[0] == 'H':
                  soln.write(":foundation_shape=>'H',\n")
                  soln.write(":foundation_area=>"+row[3]+"|'ft2',\n")
                  soln.write(":length=>"+row[4]+"|'ft',\n")
                  soln.write(":width=>"+row[5]+"|'ft',\n")
                  soln.write(":a_dim=>"+row[6]+"|'ft',\n")
                  soln.write(":b_dim=>"+row[7]+"|'ft'")

if __name__ == '__main__':
    pass