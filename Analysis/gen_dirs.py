import sys
import csv
import os

locations = ['Hot','Cold','Mixed']

with open('founds.csv','rU') as f:
    reader = csv.reader(f)
    reader.next()
    for row in reader:
      for loc in locations:
          if row[9] == '':
            dir_name = os.path.join(loc,'S'+row[0]+'AP'+row[1]+'F'+row[2]+'I'+row[3])
          else:
            dir_name = os.path.join(loc,'S'+row[0]+'AP'+row[1]+'F'+row[2]+'I'+row[3]+'R'+row[9])
          if not os.path.exists(dir_name):
              print "Generating: " + dir_name
              os.makedirs(dir_name)
              os.symlink('../../bin/run.sh',dir_name+'/run.sh')
              os.symlink('../../bin/jrun.sh',dir_name+'/jrun.sh')
              with open(dir_name+'/found.txt','w') as fnd:
                  fnd.write('# Set values below\n\n')
                  square_area = (4*float(row[1]))**2
                  if row[0] == 'C':
                    fnd.write(":foundation_shape=>'-',\n")
                    fnd.write(":foundation_area=>"+str(square_area)+"|'ft2',\n")
                    fnd.write(":foundation_aspect_ratio=>1,\n")
                    fnd.write(":coord_system=>'CYLINDRICAL',\n")
                    fnd.write(":number_of_dimensions=>2,\n")
                    fnd.write(":reduction_strategy=>'AP',\n\n")
                  elif row[0] == 'L':
                    fnd.write(":foundation_shape=>'-',\n")
                    fnd.write(":foundation_area=>"+str(square_area)+"|'ft2',\n")
                    fnd.write(":foundation_aspect_ratio=>1,\n")
                    fnd.write(":coord_system=>'CARTESIAN',\n")
                    fnd.write(":number_of_dimensions=>2,\n")
                    fnd.write(":reduction_strategy=>'AP',\n\n")
                  else:

                    if row[0] == 'S':
                      fnd.write(":foundation_shape=>'-',\n")
                      fnd.write(":foundation_area=>"+str(square_area)+"|'ft2',\n")
                      fnd.write(":foundation_aspect_ratio=>1,\n")
                    elif row[0] == '#':
                      fnd.write(":foundation_shape=>'H',\n")
                      fnd.write(":foundation_area=>"+row[4]+"|'ft2',\n")
                      fnd.write(":length=>"+row[5]+"|'ft',\n")
                      fnd.write(":width=>"+row[6]+"|'ft',\n")
                      fnd.write(":a_dim=>"+row[7]+"|'ft',\n")
                      fnd.write(":b_dim=>"+row[8]+"|'ft',\n")
                    elif row[0] == 'H':
                      fnd.write(":foundation_shape=>'H',\n")
                      fnd.write(":foundation_area=>"+row[4]+"|'ft2',\n")
                      fnd.write(":length=>"+row[5]+"|'ft',\n")
                      fnd.write(":width=>"+row[6]+"|'ft',\n")
                      fnd.write(":a_dim=>"+row[7]+"|'ft',\n")
                      fnd.write(":b_dim=>"+row[8]+"|'ft',\n")

                    if row[9] == 'NC':
                      fnd.write(":coord_system=>'CYLINDRICAL',\n")
                      fnd.write(":number_of_dimensions=>2,\n")
                      fnd.write(":reduction_strategy=>'NEG',\n\n")
                    elif row[9] == 'NL':
                      fnd.write(":coord_system=>'CARTESIAN',\n")
                      fnd.write(":number_of_dimensions=>2,\n")
                      fnd.write(":reduction_strategy=>'NEG',\n\n")
                    elif row[9] == 'PC':
                      fnd.write(":coord_system=>'CYLINDRICAL',\n")
                      fnd.write(":number_of_dimensions=>2,\n")
                      fnd.write(":reduction_strategy=>'PNEG',\n\n")
                    elif row[9] == 'BC':
                      fnd.write(":coord_system=>'CYLINDRICAL',\n")
                      fnd.write(":number_of_dimensions=>2,\n")
                      fnd.write(":reduction_strategy=>'A-P',\n\n")
                    elif row[9] == 'RC':
                      fnd.write(":coord_system=>'CYLINDRICAL',\n")
                      fnd.write(":number_of_dimensions=>2,\n")
                      fnd.write(":reduction_strategy=>'RR',\n\n")
                    elif row[9] == 'RL':
                      fnd.write(":coord_system=>'CARTESIAN',\n")
                      fnd.write(":number_of_dimensions=>2,\n")
                      fnd.write(":reduction_strategy=>'RR',\n\n")
                    else:
                      fnd.write(":coord_system=>'CARTESIAN',\n")
                      fnd.write(":number_of_dimensions=>3,\n")
                      fnd.write(":use_symmetry=>true,\n\n")


                  if row[2][0] == 'B':
                    fnd.write(":foundation_type=>'BASEMENT',\n")
                    if row[2][1:] == 'EH':
                      fnd.write(":exterior_vertical_depth=>4|'ft',\n")
                    elif row[2][1:] == 'EF':
                      fnd.write(":exterior_vertical_depth=>8|'ft',\n")
                    elif row[2][1:] == 'IF':
                      fnd.write(":interior_vertical_depth=>8|'ft',\n")
                  elif row[2][0] == 'C':
                    fnd.write(":foundation_type=>'CRAWLSPACE',\n")
                    if row[2][1:] == 'EV':
                      fnd.write(":exterior_vertical_depth=>4|'ft',\n")
                    elif row[2][1:] == 'IV':
                      fnd.write(":interior_vertical_depth=>4|'ft',\n")
                    elif row[2][1:] == 'IB':
                      fnd.write(":interior_vertical_depth=>(4|'ft') + (8|'in'),\n")
                      fnd.write(":interior_horizontal_width=>4|'ft',\n")
                  elif row[2][0] == 'S':
                    fnd.write(":foundation_type=>'SLAB',\n")
                    if row[2][1:] == 'EV':
                      fnd.write(":exterior_vertical_depth=>4|'ft',\n")
                    elif row[2][1:] == 'IV':
                      fnd.write(":interior_vertical_depth=>4|'ft',\n")
                    elif row[2][1:] == 'IH':
                      fnd.write(":interior_vertical_depth=>8|'in',\n")
                      fnd.write(":interior_horizontal_width=>4|'ft',\n")
                    elif row[2][1:] == 'EH':
                      fnd.write(":exterior_vertical_depth=>8|'in',\n")
                      fnd.write(":exterior_horizontal_width=>4|'ft',\n")
                    elif row[2][1:] == 'IW':
                      fnd.write(":interior_vertical_depth=>8|'in',\n")
                      fnd.write(":whole_slab=>true,\n")

                  fnd.write("\n:insulation_level=>" + str(float(row[3])) + "|'R-IP'")



if __name__ == '__main__':
    pass
