#==============================================================================
# Make a plot of changes in 2020 vs 2019/2021.
#   Author: Michael Erb
#==============================================================================

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

plt.style.use('ggplot')
save_instead_of_plot = True


#%% LOAD DATA

data_dir   = "C:/Users/erbm/Documents/GitHub/CDIAC-Fossil-Fuels/output/Products/Past_Products/CDIAC_2022/"
output_dir = "C:/Users/erbm/Dropbox/Academia/AppState/Manuscripts/Submitted/2026_Erb_Marland_CDIAC/proofs/analysis/figures/"

# Load the global data
data_global = pd.read_excel(data_dir+'global.1750_2022.xlsx')
data_global = data_global.rename(columns={"Emissions from fossil fuels and cement production (million metric tons of C)":"Total"})
data_global = data_global[['Year','Total']]
data_global['Nation'] = 'Global'

# Load the national data
data_national = pd.read_excel(data_dir+'nation.1750_2022.xlsx')
data_national = data_national.rename(columns={"Emissions from fossil fuels and cement production (thousand metric tons of C)":"Total"})
data_national = data_national[['Nation','Year','Total']]

# Load the sectoral data
data_sectoral = pd.read_excel(data_dir+'sectoral.1995_2022.xlsx')
keys_sectoral = ["Electric, CHP, Heat Plants",
                 "Energy Industries Own Use",
                 "Non-energy Use",
                 "Manufact, Constr, Non-Fuel Industry",
                 "Road Transport",
                 "Rail Transport",
                 "Domestic Aviation",
                 "Domestic Navigation",
                 "Other Transport",
                 "Pipeline Transport",
                 "Household",
                 "Agriculture, Forestry, Fishing",
                 "Commerce and Public Services",
                 "Other Consumption",
                 "Losses",
                 "Flaring and Venting of Natural Gas",
                 "Manufacture of Cement"]
keys_sectoral_all = ['Nation','Year']+keys_sectoral
data_sectoral = data_sectoral[keys_sectoral_all]


#%% PROCESS DATA

# Remove non-nations
not_nations = ['Global','Africa','Asia','Europe','North America','Oceania','South America','Annex I','Non-Annex I'] # NOTE: For older years, remove Antarctica too.
data_sectoral_global = data_sectoral[data_sectoral['Nation'] == 'Global']
data_sectoral = data_sectoral[~data_sectoral['Nation'].isin(not_nations)]

# Combine the dataframes
data_all   = pd.merge(data_national,data_sectoral,       how='outer',on=['Nation','Year'])
global_all = pd.merge(data_global,  data_sectoral_global,how='outer',on=['Nation','Year'])


#%% CALCULATIONS

# Get an array of all the nations
nation_array = np.unique(data_all['Nation'])
n_nations = len(nation_array)

# Set up variables
global_values_fraction = {}
values_2019_all        = {}
values_2020_all        = {}
values_2021_all        = {}
values_diff            = {}
values_fraction        = {}
values_fraction_valid  = {}
keys_all = ['Total']+keys_sectoral

# Find differences for global values
for key_txt in keys_all:
    global_years = np.array(global_all['Year'])
    global_total = np.array(global_all[key_txt])
    ind_2019 = np.where(global_years == 2019)[0][0]
    ind_2020 = np.where(global_years == 2020)[0][0]
    ind_2021 = np.where(global_years == 2021)[0][0]
    global_2020        = global_total[ind_2020]
    global_surrounding = (global_total[ind_2019]+global_total[ind_2021])/2
    global_values_fraction[key_txt] = (global_2020 / global_surrounding) * 100

# Loop through the keys, finding differences
for key_txt in keys_all:
    #
    # Get the values for 2020 and the mean of 2019 and 2021 for each country
    values_2019        = np.zeros((n_nations)); values_2019[:]        = np.nan
    values_2020        = np.zeros((n_nations)); values_2020[:]        = np.nan
    values_2021        = np.zeros((n_nations)); values_2021[:]        = np.nan
    values_surrounding = np.zeros((n_nations)); values_surrounding[:] = np.nan
    #
    i=0; nation_txt = nation_array[i]
    for i,nation_txt in enumerate(nation_array):
        data_nation = data_all[data_all['Nation'] == nation_txt]
        nation_years = np.array(data_nation['Year'])
        nation_total = np.array(data_nation[key_txt])
        if ((2019 in nation_years) & (2020 in nation_years) & (2021 in nation_years)):
            ind_2019 = np.where(nation_years == 2019)[0][0]
            ind_2020 = np.where(nation_years == 2020)[0][0]
            ind_2021 = np.where(nation_years == 2021)[0][0]
            values_2019[i] = nation_total[ind_2019]
            values_2020[i] = nation_total[ind_2020]
            values_2021[i] = nation_total[ind_2021]
            values_surrounding[i] = (nation_total[ind_2019]+nation_total[ind_2021])/2
    #
    # Save values
    values_2019_all[key_txt] = values_2019
    values_2020_all[key_txt] = values_2020
    values_2021_all[key_txt] = values_2021
    #
    # Compute the difference
    values_diff[key_txt]     =  values_2020 - values_surrounding
    values_fraction[key_txt] = (values_2020 / values_surrounding) * 100
    values_fraction_valid[key_txt] = values_fraction[key_txt][np.isfinite(values_fraction[key_txt])]
    #
    """
    print('Range of emissions:',np.nanmin(values_2020),np.nanmax(values_2020))
    print('Range of emissions:',np.nanmin(values_surrounding),np.nanmax(values_surrounding))
    print('Range of diffs:',np.nanmin(values_diff),np.nanmax(values_diff))
    print('Range of diffs, fraction:',np.nanmin(values_fraction),np.nanmax(values_fraction))
    """


#%% 2021 vs 2019

# Compute the fractional difference
values_2021_vs_2019 = (values_2021_all['Total'] / values_2019_all['Total']) * 100
values_2021_vs_2019_valid = values_2021_vs_2019[np.isfinite(values_2021_vs_2019)]

# Make a histogram
plt.figure(figsize=(4,5))
ax1 = plt.subplot2grid((1,1),(0,0))

ax1.boxplot(values_2021_vs_2019_valid, showfliers=True, patch_artist=True,
            boxprops=dict(facecolor="lightblue", color="k"), zorder=5)
ax1.axhline(y=100,c='gray',linestyle='--',linewidth=1)
ax1.set_ylabel('Relative emissions (%)')
#ax1.set_ylim([0,160])
plt.xticks(fontsize=9, rotation=90)
ax1.set_title('2021 emissions compared to 2019',fontsize=14)

if save_instead_of_plot:
    plt.savefig(output_dir+'figZ_4a_change_2021_vs_2019_hist.png',dpi=300,format='png',bbox_inches='tight')
    plt.close()
else:
    plt.show()



#%% FIGURES - HISTOGRAM

keys_short = ["Total",
              "Electric, CHP,\nHeat Plants",
              "Energy Industries\nOwn Use",
              "Non-energy Use",
              "Manufact, Constr,\nNon-Fuel Industry",
              "Road Transport",
              "Rail Transport",
              "Domestic\nAviation",
              "Domestic\nNavigation",
              "Other\nTransport",
              "Pipeline\nTransport",
              "Household",
              "Agriculture,\nForestry, Fishing",
              "Commerce and\nPublic Services",
              "Other\nConsumption",
              "Losses",
              "Flaring/Venting\nof Natural Gas",
              "Manufacture\nof Cement"]

# Make a histogram
plt.figure(figsize=(10,5))
ax1 = plt.subplot2grid((1,1),(0,0))

ax1.boxplot(values_fraction_valid.values(), tick_labels=keys_short, showfliers=False, patch_artist=True,
            boxprops=dict(facecolor="lightblue", color="k"), zorder=5)
zeros_ones = np.zeros(len(values_fraction['Total']))+1
for i,key_txt in enumerate(keys_all):
    ax1.scatter(i+1,global_values_fraction[key_txt],c='tab:red',zorder=10)
    """
    #ax1.scatter(zeros_ones*(i+1),values_fraction[key_txt], values_2020_all[key_txt]/250, color="tab:blue", alpha=0.5, zorder=5)
    for j,nation_txt in enumerate(nation_array):
        if   nation_txt == 'China':         dot_color = 'tab:blue'
        elif nation_txt == 'United States': dot_color = 'tab:green'
        elif nation_txt == 'India':         dot_color = 'tab:orange'
        else: continue
        ax1.scatter(i+1,values_fraction[key_txt][j],c=dot_color,zorder=10)
    """
    
ax1.axhline(y=100,c='gray',linestyle='--',linewidth=1)
ax1.set_ylabel('Relative emissions (%)')
ax1.set_ylim([0,160])
plt.xticks(fontsize=9, rotation=90)
#plt.xticks(fontsize=9, rotation=0)
ax1.set_title('2020 emissions compared to 2019/2021',fontsize=14)

if save_instead_of_plot:
    plt.savefig(output_dir+'fig4_change_2020_vs_surrounding_hist.png',dpi=300,format='png',bbox_inches='tight')
    plt.close()
else:
    plt.show()


#%% FIGURES - LARGEST AND SMALLEST CHANGES

# For each category, sort the data and make a figure
i = 0; key_txt = 'Total'
for i,key_txt in enumerate(keys_all):
    #
    # Get valid values for selected category
    values_fraction_selected = values_fraction[key_txt]
    ind_valid = np.isfinite(values_fraction_selected)
    values_fraction_valid2 = values_fraction_selected[ind_valid]
    nation_valid = nation_array[ind_valid]
    #
    # Get the top and bottom 10 nations
    ind_sorted = np.argsort(values_fraction_valid2)
    values_fraction_sorted = values_fraction_valid2[ind_sorted][::-1]
    nation_sorted = nation_valid[ind_sorted][::-1]
    rows_top    = np.arange(10)
    rows_bottom = np.arange(10)+len(values_fraction_sorted)-10
    rows_to_select = np.concatenate((rows_top,rows_bottom),axis=0)
    data_to_plot = values_fraction_sorted[rows_to_select]
    nations_to_plot = nation_sorted[rows_to_select]
    rank_to_plot = rows_to_select+1
    y_int = np.arange(len(rank_to_plot))
    #
    # Set up plotting details
    if key_txt == 'Total': unit_txt = 'Mt C'
    else:                  unit_txt = 'kt C'
    nation_labels = []
    for j in range(len(rank_to_plot)):
        nation_labels.append(str(rank_to_plot[j])+'. '+nations_to_plot[j][:20])
    #
    # Make a scatterplot
    plt.figure(figsize=(6,8))
    ax1 = plt.subplot2grid((1,1),(0,0))
    #
    ax1.scatter(data_to_plot,y_int)
    ax1.axvline(x=100,c='gray',linestyle='--',linewidth=1,alpha=0.5)
    ax1.axhline(y=9.5,c='gray',linestyle='--',linewidth=1,alpha=0.5)
    ax1.set_ylim(y_int[-1]+0.5,y_int[0]-0.5)
    ax1.set_yticks(y_int)
    ax1.set_yticklabels(nation_labels)
    ax1.set_xlabel('Relative emissions (%)')
    ax1.set_title('2020 emissions compared to 2019/2021 for largest changes\n'+key_txt,fontsize=14)
    #
    if save_instead_of_plot:
        plt.savefig(output_dir+'figZ_4a_'+str(i).zfill(2)+'_largest_changes_'+key_txt+'.png',dpi=300,format='png',bbox_inches='tight')
        plt.close()
    else:
        plt.show()
