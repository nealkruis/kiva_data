print "Import libraries..."

from gen_bestest import *

def readTimeseries(case, ID):
    df = pd.read_csv('../'+case+'/'+ID+'/Timeseries.csv',
                    header=0,
                    names=['time','W'],
                    parse_dates=True,
                    index_col=0)
    
    return list(df.ix['2100'].W)
        
print "Read results..."    

ids = ['30', '20', '15', '10', '5']

# Line Chart
print "Create figure..."
file_name = 'ade_timesteps'

# Figure style
sns.set_style("whitegrid", {'axes.grid': False})
sns.set_context("paper", {'axes.labelsize': 16, 'xtick.labelsize': 12, 'ytick.labelsize': 12})
sns.set_palette('Dark2',8)
fig = plt.figure()
ax = fig.add_subplot(111)

for id in ids:
    print "...Plotting: " + id + ' min'
    values = getValues('ADE-Timestep',id)
    ax.plot(values, label=id + ' min')

print "...Plotting: Implicit"
values = getValues('GC40a','Implicit')
ax.plot(values, label='Implicit')


ax.set_ylim([0,4000])
ax.set_xlim([0,8760])

ax.legend(loc='upper center', ncol=5, bbox_to_anchor=(0.5,-0.05), fancybox=True)
ax.yaxis.grid()

plt.show()
#fig.savefig(output_dir + 'images/' + file_name + '.pdf')

print "Done."



if __name__ == '__main__':
    pass