import os, re
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

DATAFOLD = os.path.join(os.getcwd(), 'data')
IMGFOLD = os.path.join(os.getcwd(), 'imgs')
RECOILS = 'RANGE.txt'
VACANCY = 'VACANCY.txt'

class config:
    isforw: bool = True

    def set_sizes(self, sizes):
        if not self.isforw:
            self.sizes = list(sizes[::-1]) 
        else:
            self.sizes


def plot_recoils(datapath, ax):
    with open(datapath) as f:
        lines = f.readlines()
        line_info = 41
        line_uplim = 44
        x_col = 0
        y_col = 4
        x_field = lines[line_info].split()[x_col]
        y_field = lines[line_info].split()[y_col] + ' recoil atoms' #+ ' ' + lines[line_info+1].split()[y_col] + ' ' + lines[line_info+1].split()[y_col+1]
        units = re.compile(">>>(.*)<<<").search(lines[39]).group(1).strip()
        x = [int(float(line.split()[x_col])) for line in lines[line_uplim:]]
        y = [float(line.split()[y_col]) for line in lines[line_uplim:]]
        ax.bar(x,y, width=10, color='orchid', log=True, label=y_field)

        idx_fst_nonz = next((i for i, x in enumerate(y) if x), None)
    return x_field, y_field, units, x[idx_fst_nonz]

def plot_vacancies(datapath, ax, y_col = 2, color='aqua'):
    with open(datapath) as f:    
        lines = f.readlines()
        line_info = 41
        line_uplim = 44
        line_downlim = 143
        x_col = 0
        x_field = lines[line_info-1].split()[0] + ' ' + lines[line_info].split()[x_col]
        y_field = lines[line_info].split()[y_col] + ' ' + lines[line_info+1].split()[y_col]
        units = re.compile(">>>>(.*)<<<<").search(lines[38]).group(1).strip()
        x = [int(float(line.split()[x_col])) for line in lines[line_uplim:line_downlim]]
        y = [float(line.split()[y_col]) for line in lines[line_uplim:line_downlim]]
        ax.bar(x,y, width=10, color=color, label=y_field)
    return x_field, y_field, units

def plot_recoil_vacancies(datapath, size):
    x_s = size[0]
    y_s = size[1]

    fig, ax = plt.subplots()  #figsize = (10, 7.5)) 

    x_field, y_field, units = plot_vacancies(os.path.join(datapath, VACANCY), ax, 2, 'aqua')
    x_field, y_field, units = plot_vacancies(os.path.join(datapath, VACANCY), ax, 3,'coral')

    ax.set_ylabel(units)

    # twin object for two different y-axis on the sample plot
    ax2=ax.twinx()
    x_field, y_field, units, x_fst_nonz = plot_recoils(os.path.join(datapath, RECOILS), ax2)
    ax2.set_ylabel(y_field + ' [' + units + ']')

    ax.set_xlabel(x_field + ' (Å)')
    # where some data has already been plotted to ax
    handles, labels = ax.get_legend_handles_labels()
    handles2, labels = ax2.get_legend_handles_labels()
    handles.append(*handles2) 
    # plot the legend
    loc = "upper left" if x_s > 50 else "upper right"
    plt.legend(handles=handles, loc=loc)

    ax2.axvline(x=10*x_s, color='black', ls='--')

    
    rect = patches.Rectangle((x_fst_nonz-5, 0), 10*x_s-x_fst_nonz, 0.0089, linewidth=1, edgecolor='r', facecolor='none')
    ax.add_patch(rect)
    plt.text(50, 1550, "hBN", fontsize = 12)
    plt.text(820, 1550, "Graphite", fontsize = 12)
    plt.title('C atoms Recoil distributions vs B/N vacancies distributions\n' + subdir)
    plt.savefig(os.path.join(IMGFOLD, subdir+'.png'), format='png', dpi=300, bbox_inches='tight')

isforw = False

sizes = [
    [80, 20], 
    [50, 50],
    [20, 80]
]

sizes = list(sizes[::-1]) 

subdirs = [
    "He (30 keV) into Graphite (20)+hBN(80)+SiO2 (100)+Si (500)",
    "He (30 keV) into Graphite (50)+hBN(50)+SiO2 (100)+Si (500)",
    "He (30 keV) into Graphite (80)+hBN(20)+SiO2 (100)+Si (500)"
]

for i, subdir in enumerate(subdirs):
    datapath = os.path.join(DATAFOLD, subdir)
    plot_recoil_vacancies(datapath, sizes[i])
    plt.show()
