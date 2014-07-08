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

cases = ['GC40a']

# Line Chart
print "Create figure..."
file_name = 'bestest_gc40a'

# Figure style
sns.set_style("whitegrid", {'axes.grid': False})
sns.set_context("paper", {'axes.labelsize': 16, 'xtick.labelsize': 12, 'ytick.labelsize': 12})
sns.set_palette('Dark2',8)
fig = plt.figure()
ax = fig.add_subplot(111)

for soln in solutions:
    print "...Plotting: " + soln.name
    soln.values = getValues('GC40a',soln)
    ax.plot(soln.values, label=soln.name)

ax.set_ylim([0,4000])
ax.set_xlim([0,8760])

ax.legend(loc='upper center', ncol=5, bbox_to_anchor=(0.5,-0.05), fancybox=True)
ax.yaxis.grid()

plt.show()
#fig.savefig(output_dir + 'images/' + file_name + '.pdf')

print "Done."



if __name__ == '__main__':
    pass