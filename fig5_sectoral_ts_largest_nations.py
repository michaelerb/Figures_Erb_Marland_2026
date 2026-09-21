#==============================================================================
# Make national and sectoral plots of the largest emitters.
#   Author: Michael Erb
#==============================================================================

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

plt.style.use('ggplot')
save_instead_of_plot = True

# Set how many nations to plot
nations_to_plot_txt = 'top10'
#nations_to_plot_txt = 'top25'
#nations_to_plot_txt = 'formerSoviet'


#%% LOAD DATA

data_dir   = "C:/Users/erbm/Documents/GitHub/CDIAC-Fossil-Fuels/output/Products/Past_Products/CDIAC_2022/"
output_dir = "C:/Users/erbm/Dropbox/Academia/AppState/Manuscripts/Submitted/2026_Erb_Marland_CDIAC/3rd_submission/analysis/figures/"

# Load the total data
data_total = pd.read_excel(data_dir+'total.2022.xlsx')
data_total = data_total.rename(columns={"Emissions from fossil fuels and cement production (thousand metric tons of C)":"Emissions"})

# Load the national data
data_national = pd.read_excel(data_dir+'nation.1750_2022.xlsx')
data_national = data_national.rename(columns={"Emissions from fossil fuels and cement production (thousand metric tons of C)":"total",
                                              "Emissions from solid fuel consumption": "solid fuels",
                                              "Emissions from liquid fuel consumption":"liquid fuels",
                                              "Emissions from gas fuel consumption":   "gas fuels",
                                              "Emissions from cement production":      "cement production",
                                              "Emissions from gas flaring and venting":"gas flaring",
                                              "Emissions per capita (metric tons of carbon)":"per capita",
                                              "Emissions from bunker fuels (not included in the totals)":"bunker"})
nation_array = np.unique(data_national['Nation'])

# Load the sectoral data
data_sectoral = pd.read_excel(data_dir+'sectoral.1995_2022.xlsx')


#%% FIND THE LARGEST EMITTERS

# Sort the 2022 totals
data_total_sorted = data_total.sort_values('Emissions', ascending=False)

print(" === 10 largest emitters in 2022 ===")
print(data_total_sorted.iloc[0:10,:])

# Get an array of all the nations
nations_all     = data_total_sorted['Nation'].values
top_emitters    = data_total_sorted['Nation'][0:10].values
top_emitters_25 = data_total_sorted['Nation'][0:25].values

# Get data for selected countries
former_soviet = ['Union of Soviet Socialist Republics [former]',
                 'Russian Federation',
                 'Kazakhstan',
                 'Ukraine',
                 'Uzbekistan',
                 'Turkmenistan',
                 'Belarus',
                 'Azerbaijan',
                 'Georgia',
                 'Lithuania',
                 'Estonia',
                 'Kyrgyzstan',
                 'Tajikistan',
                 'Armenia',
                 'Latvia',
                 'Republic of Moldova']
#data_total_selected = data_total_sorted[data_total_sorted['Nation'].isin(former_soviet)]


#%% SET KEYS

keys_national_all = ['Year','solid fuels','liquid fuels','gas fuels','cement production','gas flaring','per capita']
keys_national = keys_national_all[1:6]

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
# Color scale for sectors
colormap_selected2 = plt.cm.Set2
colors2 = colormap_selected2(np.linspace(0,1,8))
colormap_selected3 = plt.cm.tab20c
colors3 = colormap_selected3(np.linspace(0,1,15))
colors_sectors = np.concatenate((colors3,colors2[1:2,:],colors2[3:4,:]),axis=0)
"""
colormap_selected4 = plt.cm.tab20
colors4 = colormap_selected4(np.linspace(0,1,20))
colors_sectors = colors4[:-4]
"""

#%% LOOP THROUGH THE NATIONS, MAKING TIME SERIES
"""
i=8; nation_txt = nations_all[i]
#for i,nation_txt in enumerate(top_emitters):
for i,nation_txt in enumerate(nations_all):
    #
    print('Making figures: '+str(i+1)+'/'+str(len(nations_all)))
    #
    # Find data for the selected nation
    data_stackplot_all = data_national[keys_national_all].loc[data_national['Nation'] == nation_txt]
    #
    # Fill in missing years
    years_all = np.arange(1750,2023)
    index_new = pd.Index(years_all, name='Year')
    data_stackplot_all = data_stackplot_all.set_index('Year').reindex(index_new).reset_index()
    total_nation     = data_total['Emissions'].loc[data_total['Nation'] == nation_txt].values[0]
    #
    # Get data to plot
    data_stackplot   = data_stackplot_all[keys_national]
    years_nation     = data_stackplot_all['Year']
    percapita_nation = data_stackplot_all['per capita']
    data_stackplot = data_stackplot.fillna(0)
    data_stackplot = data_stackplot/1000 # Change units from kt C to Mt C
    #
    # Make a time series
    plt.figure(figsize=(10,5))
    ax1 = plt.subplot2grid((1,1),(0,0))
    #
    ax1.stackplot(years_nation,np.transpose(data_stackplot),labels=['solid fuel','liquid fuel','gas fuel','cement production','gas flaring'])
    ax1.legend(loc='upper left')
    ax1.set_xlim(1995,2022)
    #ax1.set_xlim(1750,2022)
    ax1.set_ylim(ymin=0)
    ax1.set_ylabel('Emissions (Mt C)')
    ax1.set_xlabel('Year')
    ax1.set_title(nation_txt+' - carbon emissions by source',fontsize=14)
    #
    ax1_right = ax1.twinx()
    ax1_right.plot(years_nation,percapita_nation,c='tab:orange',label='Total per capita')
    ax1_right.legend(loc='upper left', bbox_to_anchor=[0,.73])
    ax1_right.set_ylim(ymin=0)
    ax1_right.set_ylabel('Emissions per capita (t C)',color='tab:orange')
    ax1_right.grid(False)
    ax1_right.tick_params(colors='tab:orange')
    #
    if save_instead_of_plot:
        plt.savefig(output_dir+'ts_national'+str(total_nation).zfill(7)+'_'+nation_txt.replace(' ','')+'.png',dpi=150,format='png')  # ,bbox_inches='tight'
        plt.close()
    else:
        plt.show()


#%% LOOP THROUGH THE NATIONS, MAKING SECTORAL TIME SERIES

i=0; nation_txt = nations_all[i]
#for i,nation_txt in enumerate(top_emitters):
for i,nation_txt in enumerate(nations_all):
    #
    print('Making figures: '+str(i+1)+'/'+str(len(nations_all)))
    #
    # Find data for the selected nation
    data_stackplot   = data_sectoral[keys_sectoral].loc[data_sectoral['Nation'] == nation_txt]
    years_nation     = data_sectoral['Year'].loc[data_sectoral['Nation'] == nation_txt]
    percapita_nation = data_sectoral['Per Capita Total Emissions'].loc[data_sectoral['Nation'] == nation_txt]
    total_nation     = data_total['Emissions'].loc[data_total['Nation'] == nation_txt].values[0]
    data_stackplot[np.isnan(data_stackplot)] = 0
    data_stackplot = data_stackplot/1000 # Change units from kt C to Mt C
    #
    # Make a time series
    plt.figure(figsize=(10,5))
    ax1 = plt.subplot2grid((1,1),(0,0))
    ax1.set_prop_cycle('color',colors_sectors)
    #
    #ax1.stackplot(years_nation,np.transpose(data_stackplot),labels=keys_sectoral)
    ax1.stackplot(years_nation,np.transpose(data_stackplot)[::-1],labels=keys_sectoral[::-1],colors=colors_sectors[::-1])
    ax1.legend(loc='center left',fontsize=7,reverse=True,bbox_to_anchor=[1,.5])
    ax1.set_xlim(1995,2022)
    ax1.set_ylabel('Emissions (Mt C)')
    ax1.set_xlabel('Year')
    ax1.set_title(nation_txt+' - sectoral carbon emissions',fontsize=14)
    #
    if save_instead_of_plot:
        plt.savefig(output_dir+'ts_sectoral_'+str(total_nation).zfill(7)+'_'+nation_txt.replace(' ','')+'.png',dpi=150,format='png')  # ,bbox_inches='tight'
        plt.close()
    else:
        plt.show()
"""

#%% MAKE A COMBINED NATIONAL FIGURE

letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

# Set parameters
if nations_to_plot_txt == 'top10':
    f,ax = plt.subplots(2,5,sharex=True,figsize=(22,6))
    nations_to_plot = top_emitters
    title_txt = 'ten largest emitters'
elif nations_to_plot_txt == 'top25':
    f,ax = plt.subplots(5,5,sharex=True,figsize=(22,15))
    nations_to_plot = top_emitters_25
    title_txt = '25 largest emitters'
elif nations_to_plot_txt == 'formerSoviet':
    f,ax = plt.subplots(4,4,sharex=True,figsize=(22,15))
    nations_to_plot = former_soviet
    title_txt = 'former soviet countries'

ax = ax.ravel()
ax_right = {}

# Loop through the nations, making a plot for each
i = 0; nation_txt = nations_to_plot[i]
for i,nation_txt in enumerate(nations_to_plot):
    #
    # Find data for the selected nation
    data_stackplot_all = data_national[keys_national_all].loc[data_national['Nation'] == nation_txt]
    #
    # Fill in missing years
    years_all = np.arange(1750,2023)
    index_new = pd.Index(years_all, name='Year')
    data_stackplot_all = data_stackplot_all.set_index('Year').reindex(index_new).reset_index()
    #
    # Get data to plot
    data_stackplot   = data_stackplot_all[keys_national].copy()
    years_nation     = data_stackplot_all['Year']
    percapita_nation = data_stackplot_all['per capita']
    data_stackplot = data_stackplot.fillna(0)
    data_stackplot = data_stackplot/1000 # Change units from Mt C to Gt C
    #
    ax[i].stackplot(years_nation,np.transpose(data_stackplot),labels=['solid fuel','liquid fuel','gas fuel','cement production','gas flaring'])
    if i == (len(nations_to_plot)-3): ax[i].legend(loc='lower center',bbox_to_anchor=(.5,-.45),reverse=True,fontsize=12,ncol=5)
    if i in [0,5,10,15,20]:           ax[i].set_ylabel('Emissions (Mt C)')
    if i >= (len(nations_to_plot)-5): ax[i].set_xlabel('Year')
    ax[i].set_ylim(ymin=0)
    ax[i].set_xlim(1995,2022)
    #ax[i].set_xlim(1994.5,2022.5)
    #ax[i].set_xlim(1750,2022)
    if nations_to_plot_txt == 'formerSoviet':
        ax[i].set_xlim(1985,2022)
    if nations_to_plot_txt in ['top10','top25']:
        if   i < 2: ax[i].set_ylim(0,3200)
        elif i < 5: ax[i].set_ylim(0,800)
        else:       ax[i].set_ylim(0,250)
    #ax[i].set_title(nation_txt,fontsize=12)
    ax[i].set_title(letters[i]+'. '+nation_txt,fontsize=12,loc='left')
    #
    ax_right[i] = ax[i].twinx()
    ax_right[i].plot(years_nation,percapita_nation,c='tab:orange',label='Total per capita')
    #ax_right[i].set_ylim(ymin=0)
    ax_right[i].set_ylim(0,7)
    if i in [4,9]: ax_right[i].set_ylabel('Per capita (t C)',color='tab:orange')
    ax_right[i].grid(False)
    ax_right[i].tick_params(colors='tab:orange')

plt.suptitle('National carbon emissions from the '+title_txt,fontsize=20,y=0.94)
plt.subplots_adjust(top=0.85)

if save_instead_of_plot:
    plt.savefig(output_dir+'figZ_5_top_emitters_national_'+nations_to_plot_txt+'.png',dpi=150,format='png',bbox_inches='tight')
    plt.close()
else:
    plt.show()


#%% MAKE A COMBINED SECTORAL FIGURE

if   nations_to_plot_txt == 'top10': f,ax = plt.subplots(2,5,sharex=True,figsize=(22,6))
elif nations_to_plot_txt == 'top25': f,ax = plt.subplots(5,5,sharex=True,figsize=(22,15))
elif nations_to_plot_txt == 'formerSoviet': f,ax = plt.subplots(4,4,sharex=True,figsize=(22,15))
ax = ax.ravel()

# Loop through the nations, making a plot for each
for i,nation_txt in enumerate(nations_to_plot):
    #
    ax[i].set_prop_cycle('color',colors_sectors)
    data_stackplot   = data_sectoral[keys_sectoral].loc[data_sectoral['Nation'] == nation_txt].copy()
    years_nation     = data_sectoral['Year'].loc[data_sectoral['Nation'] == nation_txt]
    percapita_nation = data_sectoral['Per Capita Total Emissions'].loc[data_sectoral['Nation'] == nation_txt]
    data_stackplot = data_stackplot.fillna(0)
    data_stackplot = data_stackplot/1000  # Change units from kt C to Mt C
    data_totals = data_national[['Nation','Year','total']].loc[data_national['Nation'] == nation_txt]
    #
    ax[i].stackplot(years_nation,np.transpose(data_stackplot)[::-1],labels=keys_sectoral[::-1],colors=colors_sectors[::-1])
    ax[i].plot(data_totals['Year'],data_totals['total']/1000,'k-')
    if i == (len(nations_to_plot)-3): ax[i].legend(loc='lower center',bbox_to_anchor=(.45,-.7),reverse=True,fontsize=11,ncol=6)
    if i in [0,5,10,15,20]:           ax[i].set_ylabel('Emissions (Mt C)',fontsize=14)
    if i >= (len(nations_to_plot)-5): ax[i].set_xlabel('Year',fontsize=14)
    #ax[i].set_ylim(ymin=0)
    if nations_to_plot_txt in ['top10','top25']:
        if   i < 2: ax[i].set_ylim(0,3200)
        elif i < 5: ax[i].set_ylim(0,800)
        else:       ax[i].set_ylim(0,250)
    ax[i].set_xlim(1995,2022)
    #ax[i].set_xlim(1994.5,2022.5)
    #ax[i].set_title(nation_txt,fontsize=12)
    ax[i].set_title(letters[i]+'. '+nation_txt,fontsize=15,loc='left')
    print(data_totals['total'].iloc[-1]/1000)

plt.suptitle('Sectoral carbon emissions from the '+title_txt,fontsize=24,y=0.96)
plt.subplots_adjust(top=0.85)

if save_instead_of_plot:
    plt.savefig(output_dir+'fig5_top_emitters_sectoral_'+nations_to_plot_txt+'.png',dpi=150,format='png',bbox_inches='tight')
    plt.close()
else:
    plt.show()
