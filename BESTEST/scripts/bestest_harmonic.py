print "Import libraries..."

from gen_bestest import *

def getValues(case, solution):
    if (solution.ref):
        return readXLSTimeseries(case, solution.ID)
    else:
        return readTimeseries(case, solution.ID)

def readXLSTimeseries(case, ID):
    worksheet = workbook.sheet_by_name(ID)
    if (case == 'GC40a'):
        if (ID == 'FLUENT'):
            col = 5
        else:
            col = 4
    elif (case == 'GC40b'):
        if (ID == 'FLUENT'):
            col = 7
        else:
            col = 5
    else:
        if (ID == 'FLUENT'):
            col = 9
        else:
            col = 6
            
    return worksheet.col_values(col,130,8890)

def readTimeseries(case, ID):
    df = pd.read_csv('../'+case+'/'+ID+'/Timeseries.csv',
                    header=0,
                    names=['time','W'],
                    parse_dates=True,
                    index_col=0)
    
    return list(df.ix['2100'].W)

def getXLSsum(case, ID):
    worksheet = workbook.sheet_by_name(ID)
    if (case == 'GC40a'):
        row = 69
    elif (case == 'GC40b'):
        row = 70
    elif (case == 'GC45b'):
        row = 71
    elif (case == 'GC50b'):
        row = 72
    elif (case == 'GC55b'):
        row = 73
    elif (case == 'GC70b'):
        row = 74
    elif (case == 'GC80b'):
        row = 75
    elif (case == 'GC40c'):
        row = 76
    elif (case == 'GC45c'):
        row = 77
    elif (case == 'GC55c'):
        row = 78
    elif (case == 'GC80c'):
        row = 79
    
    
    return worksheet.cell_value(row,4)
    

def getSum(case, solution):
    if (solution.ref):
        total = getXLSsum(case, solution.ID)
    else:
        total = sum(readTimeseries(case,solution.ID))/1000.0
    
    return total    

def fmt(x):
    return '{:,.0f}'.format(x)
        
print "Read results..."    

solutions = []
solutions.append(trnsys_solution)
solutions.append(fluent_solution)
solutions.append(matlab_solution)
solutions.append(ade_solution)
solutions.append(explicit_solution)
solutions.append(adi_solution)
solutions.append(implicit_solution)
solutions.append(cn_solution)

# Line Chart
print "Create figure for GC40a..."

file_name = 'bestest_gc40a'

# Figure style
sns.set_style("white", {'axes.grid': False,
                        'xtick.direction':'in', 
                        'ytick.direction':'in',
                        'xtick.major.size':4,
                        'ytick.major.size':4})

sns.set_context("paper", rc={'axes.labelsize': 16, 'xtick.labelsize': 12, 'ytick.labelsize': 12})
sns.set_palette('Dark2',8)
fig = plt.figure()
ax = fig.add_subplot(111)

for soln in solutions:
    print "...Plotting: " + soln.name
    soln.values = getValues('GC40a',soln)
    ax.plot(soln.values, label=soln.name,linewidth=0.5)

ax.set_ylim([2000,3400])
ax.set_xlim([0,8760])
ax.set_ylabel('Slab Heat Loss [W]')
ax.set_xlabel('Hour of Year')

box = ax.get_position()
ax.set_position([box.x0, box.y0 + box.height*0.2, box.width, box.height*0.8])

ax.legend(loc='upper center', ncol=4, bbox_to_anchor=(0.5,-0.15), fancybox=True)

fig.savefig(output_dir + 'images/' + file_name + '.pdf')

# Line Chart
print "Create figure for GC40b..."

file_name = 'bestest_gc40b'

# Figure style
sns.set_context("paper", rc={'axes.labelsize': 16, 'xtick.labelsize': 12, 'ytick.labelsize': 12})
sns.set_palette('Dark2',8)
figb = plt.figure()
axb = figb.add_subplot(111)

for soln in solutions:
    print "...Plotting: " + soln.name
    soln.values = getValues('GC40b',soln)
    axb.plot(soln.values, label=soln.name,linewidth=0.5)

axb.set_ylim([2000,3400])
axb.set_xlim([0,8760])
axb.set_ylabel('Slab Heat Loss [W]')
axb.set_xlabel('Hour of Year')

box = axb.get_position()
axb.set_position([box.x0, box.y0 + box.height*0.2, box.width, box.height*0.8])

axb.legend(loc='upper center', ncol=4, bbox_to_anchor=(0.5,-0.15), fancybox=True)

figb.savefig(output_dir + 'images/' + file_name + '.pdf')

# Line Chart
print "Create figure for GC40c..."

file_name = 'bestest_gc40c'

# Figure style
sns.set_context("paper", rc={'axes.labelsize': 16, 'xtick.labelsize': 12, 'ytick.labelsize': 12})
sns.set_palette('Dark2',8)
figc = plt.figure()
axc = figc.add_subplot(111)

for soln in solutions:
    print "...Plotting: " + soln.name
    soln.values = getValues('GC40c',soln)
    axc.plot(soln.values, label=soln.name,linewidth=0.5)

axc.set_ylim([1600,3000])
axc.set_xlim([0,8760])
axc.set_ylabel('Slab Heat Loss [W]')
axc.set_xlabel('Hour of Year')

box = axc.get_position()
axc.set_position([box.x0, box.y0 + box.height*0.2, box.width, box.height*0.8])

axc.legend(loc='upper center', ncol=4, bbox_to_anchor=(0.5,-0.15), fancybox=True)

figc.savefig(output_dir + 'images/' + file_name + '.pdf')

# Case 40 table

print "Create Case 40 table..."

file_name = 'bestest_gc40'

wb = xlrd.open_workbook('Fourier.xlsx')

cases = ['GC40a','GC40b','GC40c']

table_text = "\\begin{tabular}{@{}llccccc@{}}\n"
table_text += "\\toprule\n"
table_text += "\\multicolumn{2}{l}{\\textbf{Case/Solution}} & "
table_text += "\\begin{tabular}[c]{@{}c@{}}$\\bar{\\dot{Q}}$\\\\ {[W]}\\end{tabular} & "
table_text += "\\begin{tabular}[c]{@{}c@{}}$\\dot{Q}_{year}$\\\\ {[W]}\\end{tabular} & "
table_text += "\\begin{tabular}[c]{@{}c@{}}$\\Phi_{year}$\\\\ {[days]}\\end{tabular} & "
table_text += "\\begin{tabular}[c]{@{}c@{}}$\\dot{Q}_{day}$\\\\ {[W]}\\end{tabular} & "
table_text += "\\begin{tabular}[c]{@{}c@{}}$\\Phi_{day}$\\\\ {[hours]}\\end{tabular} \\\\ \\midrule \n"

case_values = {}
cm = plt.get_cmap('RdBu')


for case in cases:
    q_a = []
    q_y = []
    p_y = []
    q_d = []
    p_d = []
    for soln in solutions:
        ws = wb.sheet_by_name(case + '|' + soln.ID)
        q_a.append(ws.cell_value(1,0))
        q_y.append(ws.cell_value(1,1))
        p_y.append(ws.cell_value(1,2)-15.0)
        q_d.append(ws.cell_value(1,3))
        p_d.append(ws.cell_value(1,4)-4.0)
    case_values[case] = []
    case_values[case].append(q_a)
    case_values[case].append(q_y)
    case_values[case].append(p_y)
    case_values[case].append(q_d)
    case_values[case].append(p_d)
             
scale = 10.0
for case in cases:
    table_text += "\\multicolumn{2}{l}{\\textbf{"+ case +":}} & & & & & \\\\ \n"
    for soln in solutions:
        ws = wb.sheet_by_name(case + '|' + soln.ID)
        table_text += " & " + soln.name
        
        value = ws.cell_value(1,0)
        fp = np.percentile(np.array(case_values[case][0]),25)
        tp = np.percentile(np.array(case_values[case][0]),75)
        med = np.percentile(np.array(case_values[case][0]),50)
        irq = (tp - fp)
        min = med - irq*scale
        max = med + irq*scale
        deg = 1 - (value - min)/(max - min)
        color = cm(deg)
        
        q_ave = '\\cellcolor[rgb]{'+ str(color[0]) + ',' + str(color[1]) +',' + str(color[2]) + '}' +'{:,.0f}'.format(value)
        
        value = ws.cell_value(1,1)
        fp = np.percentile(np.array(case_values[case][1]),25)
        tp = np.percentile(np.array(case_values[case][1]),75)
        med = np.percentile(np.array(case_values[case][1]),50)
        irq = (tp - fp)
        min = med - irq*scale
        max = med + irq*scale
        deg = 1 - (value - min)/(max - min)
        color = cm(deg)

        q_year = '\\cellcolor[rgb]{'+ str(color[0]) + ',' + str(color[1]) +',' + str(color[2]) + '}' +'{:,.0f}'.format(value)

        value = ws.cell_value(1,2) - 15.0
        fp = np.percentile(np.array(case_values[case][2]),25)
        tp = np.percentile(np.array(case_values[case][2]),75)
        med = np.percentile(np.array(case_values[case][2]),50)
        irq = (tp - fp)
        min = med - irq*scale
        max = med + irq*scale
        deg = 1 - (value - min)/(max - min)
        color = cm(deg)

        phi_year = '\\cellcolor[rgb]{'+ str(color[0]) + ',' + str(color[1]) +',' + str(color[2]) + '}' +'{:,.1f}'.format(value)

        value = ws.cell_value(1,3)
        fp = np.percentile(np.array(case_values[case][3]),25)
        tp = np.percentile(np.array(case_values[case][3]),75)
        med = np.percentile(np.array(case_values[case][3]),50)
        irq = (tp - fp)
        min = med - irq*scale
        max = med + irq*scale
        deg = 1 - (value - min)/(max - min)
        color = cm(deg)
        
        q_day = '\\cellcolor[rgb]{'+ str(color[0]) + ',' + str(color[1]) +',' + str(color[2]) + '}' +'{:,.1f}'.format(value)
        
        value = ws.cell_value(1,4) - 4.0
        fp = np.percentile(np.array(case_values[case][4]),25)
        tp = np.percentile(np.array(case_values[case][4]),75)
        med = np.percentile(np.array(case_values[case][4]),50)
        irq = (tp - fp)
        min = med - irq*scale
        max = med + irq*scale
        deg = 1 - (value - min)/(max - min)
        color = cm(deg)

        phi_day = '\\cellcolor[rgb]{'+ str(color[0]) + ',' + str(color[1]) +',' + str(color[2]) + '}' +'{:,.1f}'.format(value)
        
        table_text += " & " + q_ave + " & " + q_year + " & " + phi_year + " & " + q_day + " & " + phi_day
        if soln.ID == 'CrankNicolson':
            if case == 'GC40c':
                table_text += " \\\\  \\bottomrule \n"
            else:
                table_text += " \\\\  \\midrule \n"
        else:
            table_text += " \\\\ \n"


table_text += "\\end{tabular}"

with open(output_dir + 'tables/' + file_name + '.tex','w') as f:
    f.write(table_text)

# Bar chart
print "Creating Bar Charts..."
sns.set_style("white", {'axes.grid': False,
                        'xtick.direction':'in', 
                        'ytick.direction':'in',
                        'xtick.major.size':0,
                        'ytick.major.size':0})
sns.set_context("paper", rc={'axes.labelsize': 16, 'xtick.labelsize': 8, 'ytick.labelsize': 12})

file_name = "bestest_harmonic"

fig1 = plt.figure()
ax1 = fig1.add_subplot(111)

fig2 = plt.figure()
ax2 = fig2.add_subplot(111)

cases = ['GC40a',
         'GC40b',
         'GC40c',
         'GC45b',
         'GC45c',
         'GC50b',
         'GC55b',
         'GC55c',
         'GC70b',
         'GC80b',
         'GC80c']

names = []
colors = []
hatches = []

for soln in solutions:
    names.append(soln.name)
    colors.append(soln.color)
    hatches.append(soln.hatch)
    soln.values = []
    soln.times = []



width = 1
ticks1 = []
ticks2 = []
i1 = 1
i2 = 1

data = []
time_data = []


for case in cases:
    ticks1.append(i1+4)
    ticks2.append(i2+2.5)
    for soln in solutions:
        print "...Calculating: " + case + ": " + soln.name
        value = getSum(case, soln)
        soln.values.append(value)
        if case == 'GC50b':
            value = value/10.0
        data.append(ax1.bar(i1, value, width, color=soln.color, hatch=soln.hatch))
        time = getTime(case,soln)
        soln.times.append(time)
        if (not soln.ref):
            time_data.append(ax2.bar(i2, time, width, color=soln.color,hatch=soln.hatch))
            i2+=1
        i1+=1
    i1+=1
    i2+=1

box = ax1.get_position()
ax1.set_position([box.x0, box.y0 + box.height*0.1, box.width, box.height*0.9])
ax1.set_autoscalex_on(False)
ax1.set_xlim([0,i1])
ax1.set_xticks(ticks1)
ax1.set_xticklabels(cases)
ax1.yaxis.grid()
ax1.set_ylabel('Annual Slab Heat Loss [kWh]')

legend = ax1.legend(data[:8], names[:8], loc='upper center', ncol=4, bbox_to_anchor=(0.5,-0.05),
                   fancybox=True)

fig1.savefig('../figures/' + file_name + '.png')
fig1.savefig(output_dir + 'images/' + file_name + '.pdf')

box = ax2.get_position()
ax2.set_position([box.x0, box.y0 + box.height*0.1, box.width, box.height*0.9])

ax2.set_xlim([0,i2])
#ax2.set_ylim([1,100000])
ax2.set_xticks(ticks2)
ax2.set_xticklabels(cases)
ax2.yaxis.grid()
ax2.set_ylabel('Simulation Wall Time [s]')

legend2 = ax2.legend(time_data[:5], names[3:], loc='upper center', ncol=5, bbox_to_anchor=(0.5,-0.05),
                   fancybox=True)


fig2.savefig(output_dir + 'images/' + file_name + '_times.pdf')

# Create Table
print "Create table..."

d = {}
for soln in solutions:
    d[soln.name] = soln.values
    
df = pd.DataFrame(d, index=cases)
df = df[names].T

df.to_latex(output_dir + 'tables/' + file_name + '.tex',float_format=fmt)

d = {}
for soln in solutions:
    if (not soln.ref):
        d[soln.name] = soln.times
    
df = pd.DataFrame(d, index=cases)
df = df[names[3:]].T

df.to_latex(output_dir + 'tables/' + file_name + '_times.tex',float_format=fmt)


print "Done."



if __name__ == '__main__':
    pass