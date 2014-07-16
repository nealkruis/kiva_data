import sys
import csv
import os

with open('../SS-Sens/solns.csv','rU') as f:
    reader = csv.reader(f)
    reader.next()
    for row in reader:
        dir_name = 'D'+row[0]+'F'+row[1]+'C'+row[2]+'G'+row[3]+'T'+row[4]
        if not os.path.exists('../SS-Sens/'+dir_name):
            os.makedirs('../SS-Sens/'+dir_name)
            os.symlink('../../bin/run.sh','../SS-Sens/'+dir_name+'/run.sh')
            os.symlink('../../bin/jrun.sh','../SS-Sens/'+dir_name+'/jrun.sh')
            with open('../SS-Sens/'+dir_name+'/soln.txt','w') as soln:
                soln.write('# Set values below\n\n')
                soln.write(':deep_ground_depth=>'+row[0]+',\n')
                soln.write(':far_field_width=>'+row[1]+',\n')
                soln.write(':min_cell_dim=>0.0'+row[2]+',\n')
                soln.write(':max_cell_growth=>'+row[3][0]+'.'+row[3][1:]+',\n')
                exp = float(row[4][0]+'.'+row[4][1:]);
                tol = 10**(-exp)
                tol_str = str(tol)
                soln.write(':linear_solver_tolerance=>'+tol_str)


if __name__ == '__main__':
    pass