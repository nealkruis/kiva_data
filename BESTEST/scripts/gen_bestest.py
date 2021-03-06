print "...sys"
import sys

print "...os"
import os

print "...matplotlib"
import matplotlib.pyplot as plt

print "...seaborn"
import seaborn as sns

print "...xlrd"
import xlrd

print "...csv"
import csv

print "...pandas"
import pandas as pd

print "...numpy"
import numpy as np

print "...math"
import math

print "...re"
import re

print "...datetime"
from datetime import datetime, timedelta

print "Read Excel results..."


workbook = xlrd.open_workbook('../doc/GC-InDepth-Results.XLS')
output_dir = '/Users/nkruis/Documents/workspace/Thesis/'

class Solution:
    def __init__(self):
        self.name = ""
        self.color = []
        self.hatch = ""
        self.ID = ""
        self.ref = False
        self.values = []
        self.times = []
        self.line_color = []
        

def getTime(case, soln):
    if soln.ref:
        return 0.0
    else:
        with open('../'+case+'/'+soln.ID+'/log.out') as f:
            lines = f.readlines()
        for line in lines:
            if 'Elapsed Time:' in line:
                time_string = re.search('Elapsed Time: (.*)\n',line).group(1)
                continue
        time = datetime.strptime(time_string,"%H:%M:%S.%f")
        delta = timedelta(hours=time.hour, minutes=time.minute, seconds=time.second, microseconds=time.microsecond)
        return delta.total_seconds()       
        

#Original

gray = sns.color_palette("Greys",4)
orrd = sns.color_palette("OrRd",5)

palette = sns.color_palette("Blues",4)
#palette[2] = gray[0]
#palette[0] = orrd[0]
#palette[1] = orrd[3]

colors = [palette[3],
          palette[1],
          palette[1],
          palette[1],
          palette[2],
          palette[2],
          palette[2],
          palette[2],
          palette[2],
          palette[2]]
          
          
hatches = ['',
           '',
           '////',
           '\\\\\\\\',
           '',
           '////',
           '\\\\\\\\',
           'xxxx',
           '---',
           '------']


'''
#Canned scheme
palette = sns.color_palette('Paired',10)

colors = [palette[1],
          palette[2],
          palette[5],
          palette[6],
          palette[9],
          palette[0],
          palette[3],
          palette[4],
          palette[7],
          palette[8]]

hatches = ['xxxx',
           '////',
           '////',
           '////',
           '',
           '',
           '',
           '',
           '',
           '']
'''
'''
#BESTEST Original Scheme!
colors = ['m',
          '#1BC3F9',
          '#1BC3F9',
          '#1BC3F9',
          'w',
          'w',
          'w',
          'w',
          'w',
          'w']

hatches = ['',
           'ooo',
           'xxxx',
           '.....',
           '////',
           '\\\\\\\\',
           'xxxx',
           '---',
           '------',
           '+++']
'''

solutions = []

j = 0

analytical_solution = Solution()
analytical_solution.color = colors[j]
analytical_solution.hatch = hatches[j]
analytical_solution.ref = True
analytical_solution.name = "Analytical"
analytical_solution.ID = "Analytical"
solutions.append(analytical_solution)
j += 1

trnsys_solution = Solution()
trnsys_solution.color = colors[j]
trnsys_solution.hatch = hatches[j]
trnsys_solution.ref = True
trnsys_solution.name = "TRNSYS"
trnsys_solution.ID = "TRNSYS"
solutions.append(trnsys_solution)
j += 1

fluent_solution = Solution()
fluent_solution.color = colors[j]
fluent_solution.hatch = hatches[j]
fluent_solution.ref = True
fluent_solution.name = "FLUENT"
fluent_solution.ID = "FLUENT"
solutions.append(fluent_solution)
j += 1

matlab_solution = Solution()
matlab_solution.color = colors[j]
matlab_solution.hatch = hatches[j]
matlab_solution.ref = True
matlab_solution.name = "MATLAB"
matlab_solution.ID = "MATLAB"
solutions.append(matlab_solution)
j += 1

ss_solution = Solution()
ss_solution.color = colors[j]
ss_solution.hatch = hatches[j]
ss_solution.ref = False
ss_solution.name = "Kiva: Steady-State"
ss_solution.ID = "SteadyState"
solutions.append(ss_solution)
j += 1

ade_solution = Solution()
ade_solution.color = colors[j]
ade_solution.hatch = hatches[j]
ade_solution.ref = False
ade_solution.name = "Kiva: ADE"
ade_solution.ID = "ADE"
solutions.append(ade_solution)
j += 1

explicit_solution = Solution()
explicit_solution.color = colors[j]
explicit_solution.hatch = hatches[j]
explicit_solution.ref = False
explicit_solution.name = "Kiva: Explicit"
explicit_solution.ID = "Explicit"
solutions.append(explicit_solution)
j += 1

adi_solution = Solution()
adi_solution.color = colors[j]
adi_solution.hatch = hatches[j]
adi_solution.ref = False
adi_solution.name = "Kiva: ADI"
adi_solution.ID = "ADI"
solutions.append(adi_solution)
j += 1

implicit_solution = Solution()
implicit_solution.color = colors[j]
implicit_solution.hatch = hatches[j]
implicit_solution.ref = False
implicit_solution.name = "Kiva: Implicit"
implicit_solution.ID = "Implicit"
solutions.append(implicit_solution)
j += 1

cn_solution = Solution()
cn_solution.color = colors[j]
cn_solution.hatch = hatches[j]
cn_solution.ref = False
cn_solution.name = "Kiva: Crank-Nicolson"
cn_solution.ID = "CrankNicolson"
solutions.append(cn_solution)
j += 1

if __name__ == '__main__':
    pass