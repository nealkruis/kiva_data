print "Import libraries..."

from gen_bestest import *

from matplotlib.ticker import FuncFormatter 

years = ['2097','2098','2099','2100','2101','2102','2103']

def getTime(dir):
    with open('../H-Sens/' + dir + '/log.out') as f:
        lines = f.readlines()
    for line in lines:
        if 'Elapsed Time:' in line:
            time_string = re.search('Elapsed Time: (.*)\n',line).group(1)
            continue
    time = datetime.strptime(time_string,"%H:%M:%S.%f")
    delta = timedelta(hours=time.hour, minutes=time.minute, seconds=time.second, microseconds=time.microsecond)
    return delta.total_seconds()       
        
class Result:
    def __init__(self, dir):
        self.method = dir
        
        self.df = pd.read_csv('../H-Sens/' + dir + '/Timeseries.csv',
                              header=0,
                              names=['time','W'],
                              parse_dates=True,
                              index_col=0,
                              na_filter=False)

        sums = []
        diffs = []
        for year in years:
            sum = self.df.ix[year].W.sum()
            sums.append(sum)
            
        n_years = 7
        for i in range(0,7):
            if i == 0:
                diffs.append(None)
            else:
                diff = abs(sums[i] - sums[i-1])/sums[i-1]
                if (diff < 0.001 and i+1 < n_years):
                    n_years = i+1
                diffs.append(diff)
        
        self.net_diff = abs(sums[0] - sums[6])/sums[6]
        self.first_diff = abs(sums[0] - sums[1])
        self.n_years = n_years
        self.sums = sums
        self.diffs = diffs
        self.time = getTime(dir)

def to_percent(x, pos=0): 
     return '{:.0%}'.format(x)

def to_percent2(x, pos=0):
    if abs(x) >= 0.1:
        return '{:.1f}\%'.format(100*x)
    #elif x >= 0.01:
    #    return '{:.1f}\%'.format(100*x)
    else:
        return '{:.2f}\%'.format(100*x)

print "Read results..."    

results = {}

for path in os.walk('../H-Sens'):
    for dir in path[1]:
        #if ('W0' in dir and ('P0' in dir or 'P168N12' in dir)):
        if ('W0' in dir):
            print "Reading: " + dir
            results[dir] = Result(dir)


'''
plots = ["MKT10P0N0W0","MST10P168N12W0"]
for plot in plots:
    results[plot] = Result(plot)
'''
        
# Line Chart
print "Create figure..."


# Figure style
sns.set_palette('YlGnBu',5)
sns.set_style("white", {'axes.grid': False, 
                        'legend.frameon': True,
                        'xtick.direction':'in', 
                        'ytick.direction':'in',
                        'xtick.major.size':4,
                        'ytick.major.size':4})

sns.set_context("paper", rc={'axes.labelsize': 16, 
                          'xtick.labelsize': 12, 
                          'ytick.labelsize': 12,
                          'legend.fontsize': 10})

year_1_fig = plt.figure()
year_1_ax = year_1_fig.add_subplot(111)
file_name = "init_methods_first_year"

plots = ["MKT10P0N0W0","MCT10P0N0W0","MST10P0N0W0","MST10P168N12W0"]
labels = ["Kusuda",
          "Constant Temperature (10$^\circ$C)",
          "Steady-State",
          "Accelerated"]

for i, plot in enumerate(plots):
    year_1_ax.plot(list(results[plot].df.ix['2097'].W), label=labels[i])
    #year_1_ax.plot(list(results[plot].df.W), label=labels[i])

line, = year_1_ax.plot(list(results["MST10P168N12W0"].df.ix['2103'].W),'k--', label='Ideal')
year_1_ax.plot(list(results["MCT30P0N0W0"].df.ix['2097'].W), label='Constant Temperature (30$^\circ$C)')

labels.append("Constant Temperature (30$^\circ$C)")
plots.append("MCT30P0N0W0")

box = year_1_ax.get_position()
year_1_ax.set_position([box.x0, box.y0 + box.height*0.1, box.width, box.height*0.9])
year_1_ax.legend(loc='upper right', fancybox=True)


line.set_dashes([16, 16])


#year_1_ax.yaxis.grid()
year_1_ax.set_ylim([1000,5000])
year_1_ax.set_xlim([0,8760])
year_1_ax.set_ylabel('Slab Heat Loss [W]')
year_1_ax.set_xlabel('Hour of Year')

year_1_fig.savefig(output_dir + 'images/' + file_name + '.pdf')

# Multi-year
sns.set_context("paper", rc={'axes.labelsize': 16, 
                          'xtick.labelsize': 12, 
                          'ytick.labelsize': 12,
                          'legend.fontsize': 9})

my_fig = plt.figure()
my_ax = my_fig.add_subplot(111)
file_name = "init_methods_multi_year"

for i, plot in enumerate(plots[:-1]):
    ys = [y/1000000. for y in results[plot].sums]
    my_ax.plot([1,2,3,4,5,6,7],ys,marker='o', label=labels[i])

ideal = results["MST10P168N12W0"].sums[6]/1000000.
ys = [ideal] * 7
my_ax.plot([1,2,3,4,5,6,7],ys,'k--', label='Ideal')

ys = [y/1000000. for y in results["MCT30P0N0W0"].sums]
my_ax.plot([1,2,3,4,5,6,7],ys,marker='o', label=labels[4])

box = my_ax.get_position()
my_ax.set_position([box.x0, box.y0 + box.height*0.1, box.width, box.height*0.9])
my_ax.legend(loc='lower right', fancybox=True)

y1 = 14.
y2 = 30.

#my_ax.yaxis.grid()
my_ax.set_ylabel('Annual Slab Heat Loss [MWh]')
my_ax.set_xlabel('Year')
my_ax.set_xlim([0.5,7.5])
my_ax.set_ylim([y1,y2])

my_axp = my_ax.twinx()
my_axp.set_ylim([(y1 - ideal)/ideal,(y2 - ideal)/ideal])
my_axp.set_position([box.x0, box.y0 + box.height*0.1, box.width, box.height*0.9])
my_axp.yaxis.set_major_formatter(FuncFormatter(to_percent)) 


my_fig.savefig(output_dir + 'images/' + file_name + '.pdf')

table = {}
target = results["MST10P168N12W0"].sums[6]

labels[1] = "\\begin{tabular}[c]{@{}c@{}}Constant\\\\ Temperature (10$^\circ$C)\\end{tabular}"
labels[4] = "\\begin{tabular}[c]{@{}c@{}}Constant\\\\ Temperature (30$^\circ$C)\\end{tabular}"

for r in results:
    if r in plots:
        if "MKT10P0" in r:
            label = labels[0]
        elif "MCT10P0" in r:
            label = labels[1]
        elif "MCT30P0" in r:
            label = labels[4]
        elif "MST10P0" in r:
            label = labels[2]
        elif "MST10P168" in r:
            label = labels[3]
            
        diffs = []
        for n in results[r].sums:
            diffs.append((n - target)/target)
        table[label] = diffs
        
df = pd.DataFrame(table, index=[1,2,3,4,5,6,7])
df.index.name = "Year"
#df = df[labels].T

table_text = df.to_latex(float_format=to_percent2, 
                         escape=False,
                         columns=labels).replace('rrrrr','ccccc')
                         
with open(output_dir + 'tables/' + file_name + '.tex','w') as f:
    f.write(table_text)

########################################
sns.set_style("white", {'axes.grid': False, 
                        'legend.frameon': True,
                        'xtick.direction':'in', 
                        'ytick.direction':'in',
                        'xtick.major.size':4,
                        'ytick.major.size':0})
sns.set_context("paper", rc={'axes.labelsize': 16, 
                          'xtick.labelsize': 12, 
                          'ytick.labelsize': 12,
                          'legend.fontsize': 10})

sns.set_palette('YlOrRd',3)

target = results["MST10P168N12W0"].sums[6]
ideal = np.array(results["MST10P168N12W0"].df.ix['2103'].W)

min_t = min(results[d].time for d in results)

fig2 = plt.figure()
ax2 = fig2.add_subplot(111)
file_name = "init_methods_time_diffs"
sns.set_context("paper", rc={'axes.labelsize': 16, 
                          'xtick.labelsize': 12, 
                          'ytick.labelsize': 12,
                          'legend.fontsize': 8})

for key in results:
    if 'P0N0W0' in key:
        color = 'w'
        size = 20
        linewidth = 1
        method = re.search('M(.*)T',key).group(1)
        if (method == "K"):
            marker = 's'
        elif (method == "C"):
            temp = re.search('T(.*)P',key).group(1)
            if temp == "10":
                marker = 'v'
            else:
                marker = '^'
        else:
            marker = 'o'
    else:
        linewidth = None
        period = re.search('P(.*)N',key).group(1)
        n = re.search('N(.*)W',key).group(1)
        warmup = re.search('W(.*)',key).group(1)
    
        #duration = int(n)*int(period) + int(warmup)
        #norm_duration = int(float(duration)/672.0*5.0)
        #size = norm_duration + 5
        duration = int(n)*int(period) + int(warmup)
        norm_duration = int(float(duration)/672.0)
        size = 20
        
        #if (warmup == "0"):
        #    marker = 'o'
        #elif (warmup == "168"):
        #    marker = 's'
        #else:
        #    marker = '^'
         
        if (norm_duration == 3):
            marker = '^'
        elif (norm_duration == 6):
            marker = 'D'
        elif (norm_duration == 12):
            marker = 's'
        else:
            marker = 'o'
         
            
        if (period == "24"):
            color = sns.color_palette()[0]
        elif (period == "168"):
            color = sns.color_palette()[1]
        else:
            color = sns.color_palette()[2]
    
    time = results[key].time - min_t
    diff = (results[key].sums[0]-target)/target
    values = np.array(results[key].df.ix['2097'].W)
    #rmsd = math.sqrt(np.mean((ideal - values)**2))
    x= time
    y = diff
    ax2.scatter(x,y,c=color,s=size,marker=marker,linewidths=linewidth)

dx = -100
dy = 0

'''
handles = [plt.scatter(dx,dy,c='w',s=20,marker='s',linewidths=1),
           plt.scatter(dx,dy,c='w',s=20,marker='v',linewidths=1),
           plt.scatter(dx,dy,c='w',s=20,marker='^',linewidths=1),
           plt.scatter(dx,dy,c='w',s=20,marker='o',linewidths=1),
           plt.scatter(dx,dy,c=sns.color_palette()[0],s=65,marker='o'),
           plt.scatter(dx,dy,c=sns.color_palette()[1],s=65,marker='o'),
           plt.scatter(dx,dy,c=sns.color_palette()[2],s=65,marker='o'),
           plt.scatter(dx,dy,c='0.5',s=65,marker='o'),
           plt.scatter(dx,dy,c='0.5',s=65,marker='s'),
           plt.scatter(dx,dy,c='0.5',s=65,marker='^'),
           plt.scatter(dx,dy,c='0.5',s=20,marker='o'),
           plt.scatter(dx,dy,c='0.5',s=35,marker='o'),
           plt.scatter(dx,dy,c='0.5',s=65,marker='o'),
           plt.scatter(dx,dy,c='0.5',s=125,marker='o')]

labels = ['Kusuda',
          'Constant Temp. (10$^\circ$C)',
          'Constant Temp. (30$^\circ$C)',
          'Steady-State',
          'Daily Timesteps',
          'Weekly Timesteps',
          'Monthly Timesteps',
          'No Warm-up',
          '1 Week Warm-up',
          '1 Month Warm-up',
          '3 Months Init.',
          '6 Months Init.',
          '12 Months Init.',
          '24 Months Init.']
'''

handles = [plt.scatter(dx,dy,c='w',s=20,marker='s',linewidths=1),
           plt.scatter(dx,dy,c='w',s=20,marker='v',linewidths=1),
           plt.scatter(dx,dy,c='w',s=20,marker='^',linewidths=1),
           plt.scatter(dx,dy,c='w',s=20,marker='o',linewidths=1),
           plt.scatter(dx,dy,c='0.5',s=20,marker='^'),
           plt.scatter(dx,dy,c='0.5',s=20,marker='D'),
           plt.scatter(dx,dy,c='0.5',s=20,marker='s'),
           plt.scatter(dx,dy,c='0.5',s=20,marker='o'),
           plt.scatter(dx,dy,c=sns.color_palette()[0],s=20,marker='p'),
           plt.scatter(dx,dy,c=sns.color_palette()[1],s=20,marker='p'),
           plt.scatter(dx,dy,c=sns.color_palette()[2],s=20,marker='p')]

labels = ['Kusuda',
          'Constant Temp. (10$^\circ$C)',
          'Constant Temp. (30$^\circ$C)',
          'Steady-State',
          '3 Months Init.',
          '6 Months Init.',
          '12 Months Init.',
          '24 Months Init.',
          'Daily Timesteps',
          'Weekly Timesteps',
          'Monthly Timesteps']

box = ax2.get_position()
ax2.set_position([box.x0 +  box.width*0.05, box.y0 + box.height*0.05, box.width*0.95, box.height*0.8])
ax2.legend(handles, labels, loc='upper center', ncol=3, bbox_to_anchor=(0.5,1.3), fancybox=True)
ax2.yaxis.grid()
ax2.set_xlim([-20,1250])
ax2.set_ylim([-0.35,0.35])
ax2.set_ylabel('Relative Difference in \n Annual Slab Heat Loss')
ax2.set_xlabel('Additional Simulation Wall Time [s]')


ax2.yaxis.set_major_formatter(FuncFormatter(to_percent)) 

fig2.savefig(output_dir + 'images/' + file_name + '.pdf')


print "Done."



if __name__ == '__main__':
    pass