print "...sys"
import sys

print "...matplotlib"
import matplotlib.pyplot as plt

print "...seaborn"
import seaborn as sns

print "...xlrd"
import xlrd

print "...csv"
import csv

print "...numpy"
import numpy as np

print "...pandas"
import pandas as pd

print "...re"
import re

print "...datetime"
from datetime import datetime, timedelta

output_dir = '/Users/nkruis/Documents/workspace/Thesis/'

def getTime(solution):
    with open('../SS-Sens/'+solution+'/log.out') as f:
        time_table = f.readlines()
    for line in time_table:
        if 'Elapsed Time:' in line:
            time_string = re.search('Elapsed Time: (.*)\n',line).group(1)
            continue
    time = datetime.strptime(time_string,"%H:%M:%S.%f")
    delta = timedelta(hours=time.hour, minutes=time.minute, seconds=time.second, microseconds=time.microsecond)
    return delta.total_seconds()       

def getLastValue(solution):
    with open('../SS-Sens/'+solution+'/Timeseries.csv') as f:
        time_table = f.readlines()
        reader = csv.reader([time_table[-1]])
        for row in reader:
            val = row[1]

    return float(val)

def getPercentDiff(solution):
    ref = getLastValue('D40F40C03T6')
    val = getLastValue(solution)
    diff = (val-ref)/ref*100.0
    return diff

def cellSolution(x,y):
    return 'D40F40C' + x + 'G' + y + 'T60'
        
def generate2Dtable(output_file,X,Y,function,format):        
    lines = []
    header = "\\begin{tabular}{c|"
    
    for x in X:
        header += "c"
        
    header += "}"
    
    lines.append(header)
    
    first_row = "\\diaghead(1,-1){\hskip1cm}{F [m]}{D [m]} "
    
    for x in X:
        first_row += " & " + x
        
    first_row += " \\\\ \\hline"
    
    lines.append(first_row)
    
    for y in Y:
        row = y
        for x in X:
            row += " & " + format.format(function(cellSolution(x,y)))
        row += " \\\\[5pt]"
        lines.append(row)
    
    footer = "\\end{tabular}"
    lines.append(footer)
    
    with open(output_file,'w') as f:
        for line in lines:
            f.write(line + "\n")

def to_percent(x, pos=0): 
     return '{:.0%}'.format(x)
from matplotlib.ticker import FuncFormatter 


ideal = 2432.59
y1 = 2380
y2 = 2500
         
# Mesh Detail
C = ["03","06","09","12"]
G = ["110","115","120","130","140","160","200"]


sns.set_style("white", {'xtick.direction':'in', 
                        'ytick.direction':'in',
                        'xtick.major.size':4,
                        'ytick.major.size':4})


sns.set_context("paper", rc = {'axes.labelsize': 16, 
                               'xtick.labelsize': 12, 
                               'ytick.labelsize': 12,
                               'legend.fontsize': 12})


cp = sns.color_palette("GnBu",5)
sns.set_palette(cp[1:])
fig1 = plt.figure()
ax1 = fig1.add_subplot(111)
file_name = "ss_sens_mesh"

x = [1.1,1.15,1.2,1.3,1.4,1.6,2]

markers = ['o','^','s','D','x','+']
linestyles = ['-','--','-.',':']

col = '0.5'
lst = linestyles[0]

i = 0

for c in C:
    y = []
    lab = int(c)
    lab_str = str(lab) + " mm"
    for g in G:
        y.append(getLastValue('D40F40C'+c+'G'+g+'T60'))
    ax1.plot(x,y,linestyle=lst,linewidth=1, marker=markers[i], label=lab_str)
    i+=1

y = []
for g in G:
    y.append(ideal)
ax1.plot(x,y,label="Analytical",color='k')

y = []
for g in G:
    y.append(ideal + 0.001*ideal)
ax1.plot(x,y,'k--',label="+/- 0.1%",linewidth=0.5)

y = []
for g in G:
    y.append(ideal - 0.001*ideal)
ax1.plot(x,y,'k--',linewidth=0.5)

box = ax1.get_position()
ax1.set_position([box.x0, box.y0 + box.height*0.1, box.width, box.height*0.9])

ax1.legend(loc='upper center',title='Min. Cell Dim., $\Delta r_{min}$',ncol=3)
ax1.get_legend().get_title().set_fontsize(14)
ax1.set_ylim([y1,y2])
ax1.set_ylabel('Slab Heat Loss [W]')
ax1.set_xlabel('Geometric Growth Factor, $R$')

ax1p = ax1.twinx()
ax1p.set_ylim([(y1 - ideal)/ideal,(y2 - ideal)/ideal])
ax1p.set_position([box.x0, box.y0 + box.height*0.1, box.width, box.height*0.9])
ax1p.yaxis.set_major_formatter(FuncFormatter(to_percent)) 

fig1.gca().invert_xaxis()
    
fig1.savefig(output_dir + 'images/' + file_name + '.pdf')

'''
fig2 = plt.figure()
ax2 = fig2.add_subplot(111, frameon=False, xticks=[], yticks=[])
file_name = "ss_sens_mesh_times"

y = []
for c in C:
    v = []
    for g in G:
        v.append(getTime('D40F40C'+c+'G'+g+'T60'))
    y.append(v)

y = np.array(y)
    
normal = plt.Normalize(0, 600)

ax2.table(cellText=y,rowLabels=C,colLabels=G,loc='center',cellColours=plt.cm.hot_r(normal(y)))
    
fig2.savefig(output_dir + 'images/' + file_name + '.pdf')
'''
fig2 = plt.figure()
ax2 = fig2.add_subplot(111)
file_name = "ss_sens_mesh_times"

i = 0
for c in C:
    y = []
    lab = int(c)
    lab_str = str(lab) + " mm"
    for g in G:
        y.append(getTime('D40F40C'+c+'G'+g+'T60'))
    ax2.plot(x,y,linestyle=lst,linewidth=1, marker=markers[i], label=lab_str)
    i+=1

box = ax2.get_position()
ax2.set_position([box.x0, box.y0 + box.height*0.1, box.width, box.height*0.9])

ax2.legend(loc='upper left',title='Min. Cell Dim., $\Delta r_{min}$')
ax2.get_legend().get_title().set_fontsize(14)
ax2.set_ylim([0,35])
ax2.set_ylabel('Simulation Wall Time [S]')
ax2.set_xlabel('Geometric Growth Factor, $R$')


    
fig2.gca().invert_xaxis()
    
fig2.savefig(output_dir + 'images/' + file_name + '.pdf')

# Boundary Distances
F = ["10","20","30","40"]
D = F

cp = sns.color_palette("OrRd",5)
sns.set_palette(cp[1:])

fig3 = plt.figure()
ax3 = fig3.add_subplot(111)
file_name = "ss_sens_bound"

x = [10,20,30,40]

i = 0
for f in F:
    y = []
    lab_str = f + " m"
    for d in D:
        y.append(getLastValue('D'+d+'F'+f+'C06G120T60'))
    ax3.plot(x,y,marker=markers[i],linewidth=1, label=lab_str)
    i+=1

y = []
for f in F:
    y.append(ideal)
ax3.plot(x,y,label="Analytical",color='k')

y = []
for f in F:
    y.append(ideal + 0.001*ideal)
ax3.plot(x,y,'k--',label="+/- 0.1%",linewidth=0.5)

y = []
for f in F:
    y.append(ideal - 0.001*ideal)
ax3.plot(x,y,'k--',linewidth=0.5)

box = ax3.get_position()
ax3.set_position([box.x0, box.y0 + box.height*0.1, box.width, box.height*0.9])

ax3.legend(loc='lower center',title='Far-Field Width',ncol=3)
ax3.get_legend().get_title().set_fontsize(14)
ax3.set_ylim([y1,y2])
ax3.set_ylabel('Slab Heat Loss [W]')
ax3.set_xlabel('Deep-Ground Depth [m]')

ax3p = ax3.twinx()
ax3p.set_ylim([(y1 - ideal)/ideal,(y2 - ideal)/ideal])
ax3p.set_position([box.x0, box.y0 + box.height*0.1, box.width, box.height*0.9])
ax3p.yaxis.set_major_formatter(FuncFormatter(to_percent)) 

        
fig3.savefig(output_dir + 'images/' + file_name + '.pdf')


fig4 = plt.figure()
ax4 = fig4.add_subplot(111)
file_name = "ss_sens_bound_times"

i = 0
for f in F:
    y = []
    lab_str = f + " m"
    for d in D:
        y.append(getTime('D'+d+'F'+f+'C06G120T60'))
    ax4.plot(x,y, marker=markers[i],linewidth=1, label=lab_str)
    i+=1

box = ax4.get_position()
ax4.set_position([box.x0, box.y0 + box.height*0.1, box.width, box.height*0.9])

ax4.legend(loc='upper left',title='Far-Field Width')
ax4.get_legend().get_title().set_fontsize(14)
ax4.set_ylim([0,35])
ax4.set_ylabel('Simulation Wall Time [S]')
ax4.set_xlabel('Deep-Ground Depth [m]')
        
fig4.savefig(output_dir + 'images/' + file_name + '.pdf')

# Tolerance
#T = ["35","3625","375","3875","40","4125","425","4375","45","475","50","55","60"]
T = ["40","4125","425","4375","45","475","50","55","60"]

x = []
for t in T:
    x.append(10**(-float(t[0]+'.'+t[1:])))

cp = sns.color_palette("Greys",4)
sns.set_palette([cp[1],cp[3]])


fig5 = plt.figure()
ax5 = fig5.add_subplot(111)
file_name = "ss_sens_tol"

y = []
for t in T:
    y.append(getLastValue('D40F40C06G120T'+t))

l1 = ax5.plot(x[1:],y[1:],'-o',color=sns.color_palette()[3],linewidth=1,label='Heat Flow')

y = []
for t in T:
    y.append(ideal)
l2 = ax5.plot(x,y,label="Analytical",color='k')

y = []
for t in T:
    y.append(ideal + 0.001*ideal)
l3 = ax5.plot(x,y,'k--',label="+/- 0.1%",linewidth=0.5)

y = []
for t in T:
    y.append(ideal - 0.001*ideal)
ax5.plot(x,y,'k--',linewidth=0.5)

box = ax5.get_position()
ax5.set_position([box.x0, box.y0 + box.height*0.1, box.width, box.height*0.9])

ax5.set_ylim([y1,y2])
ax5.set_ylabel('Slab Heat Loss [W]')
ax5.set_xlabel('Tolerance')
ax5.set_xscale('log')

ax6 = ax5.twinx()

y = []
for t in T:
    y.append(getTime('D40F40C06G120T'+t))
l4 = ax6.plot(x[1:],y[1:],marker='^',linewidth=1,label='Time')

box = ax6.get_position()
ax6.set_position([box.x0, box.y0 + box.height*0.1, box.width, box.height*0.9])

ax6.set_ylim([0,35])
ax6.set_ylabel('Simulation Wall Time [s]')
ax6.set_xscale('log')

lns = l1 + l2 + l3 + l4
labs = [l.get_label() for l in lns]

ax5.legend(lns, labs, loc='upper right')


fig5.gca().invert_xaxis()        
fig5.savefig(output_dir + 'images/' + file_name + '.pdf')


if __name__ == '__main__':
    pass