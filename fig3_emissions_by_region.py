#==============================================================================
# Makes some overview figures of the CDIAC data, showing emissions by nation,
# region, fuel type, and sector.
#   Author: Michael Erb
#==============================================================================

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

plt.style.use('ggplot')
save_instead_of_plot = True


#%% LOAD DATA

data_dir   = 'C:/Users/erbm/Documents/GitHub/CDIAC-Fossil-Fuels/output/Products/Past_Products/CDIAC_2022/'
output_dir = 'C:/Users/erbm/Dropbox/Academia/AppState/Manuscripts/Submitted/2026_Erb_Marland_CDIAC/3rd_submission/analysis/figures/'

# Load the national data
data_national = pd.read_excel(data_dir+'nation.1750_2022.xlsx')
data_national = data_national.rename(columns={"Emissions from fossil fuels and cement production (thousand metric tons of C)":"Total",
                                              "Emissions from solid fuel consumption": "Solid fuels",
                                              "Emissions from liquid fuel consumption":"Liquid fuels",
                                              "Emissions from gas fuel consumption":   "Gas fuels",
                                              "Emissions from cement production":      "Cement production",
                                              "Emissions from gas flaring and venting":"Gas flaring",
                                              "Emissions per capita (metric tons of carbon)":"Per capita",
                                              "Emissions from bunker fuels (not included in the totals)":"Bunker",
                                              "Emissions from aviation bunker fuels (subset of bunker emissions)":"Bunker aviation"})

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

# Open the country lookup file
dir_lookup = 'C:/Users/erbm/Documents/GitHub/CDIAC-Fossil-Fuels/data/Lookups/'
country_lookup = pd.read_excel(dir_lookup+'Country_Lookup.xlsx')


#%% SETUP

keys_national = ['Total','Solid fuels','Liquid fuels','Gas fuels','Cement production','Gas flaring','Bunker']

# Set things up
years_all   = np.arange(min(data_national['Year']),max(data_national['Year'])+1)
nations_all = np.unique(data_national['Nation'])
regions_all = np.unique(country_lookup['UN_Region'])

n_years   = len(years_all)
n_nations = len(nations_all)
n_regions = len(regions_all)
#n_sectors = len(keys_sectoral)

national_total_all = np.zeros((n_nations,n_years)); national_total_all[:] = np.nan
regional_total_all = np.zeros((n_regions,n_years)); regional_total_all[:] = np.nan
#sectoral_total_all = np.zeros((n_sectors,n_years)); sectoral_total_all[:] = np.nan


#%% REFORMAT DATA - BY NATION

# Select the variable to plot
variable_to_plot = 'Total'
#variable_to_plot = 'Bunker'

# Rearrange data
i=0; nation_txt = nations_all[i]
for i,nation_txt in enumerate(nations_all):
    nation_year  = np.array(data_national['Year'].loc[data_national['Nation'] == nation_txt])
    nation_total = np.array(data_national[variable_to_plot].loc[data_national['Nation'] == nation_txt])
    ind_years = np.where(np.isin(years_all,nation_year))[0]
    national_total_all[i,ind_years] = nation_total

# Sort the nations by their largest contribution
emissions_max = np.nanmax(national_total_all,axis=1)
ind_sorted = np.argsort(-emissions_max)
nations_all_sorted = nations_all[ind_sorted]
national_total_sorted = national_total_all[ind_sorted,:]


#%% REFORMAT DATA - BY REGION

letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

# Sum the countries into their regions
i = 0; region_txt = regions_all[i]
labels_regions = []
for i,region_txt in enumerate(regions_all):
    ind_in_region = np.where(country_lookup['UN_Region'] == region_txt)[0]
    countries_in_region = country_lookup.loc[ind_in_region]["Country_Name"]
    bool_for_data = np.isin(nations_all_sorted,list(countries_in_region))
    regional_total = np.nansum(national_total_sorted[bool_for_data,:], axis=0)
    regional_total_all[i,:] = regional_total
    labels_regions.append(region_txt+' ('+str(int(regional_total[-1]/1000))+')')
    #labels_regions.append(letters[i]+'. '+region_txt+' ('+str(int(regional_total[-1]/1000))+')')

# Sort the regions by their largest contribution
emissions_max_regions = np.nanmax(regional_total_all,axis=1)
ind_sorted = np.argsort(-emissions_max_regions)
regions_all_sorted = regions_all[ind_sorted]
regional_total_sorted = regional_total_all[ind_sorted,:]


#%% REFORMAT DATA - BY SECTOR

data_sectoral_global = data_sectoral[data_sectoral["Nation"] == 'Global']
data_sectoral_global_2022 = data_sectoral_global[data_sectoral_global["Year"] == 2022]
years_sectoral     = data_sectoral_global['Year']
sectoral_total_all = np.array(data_sectoral_global[keys_sectoral]).transpose()

# Create labels
labels_sectors = []
for i,sector_txt in enumerate(keys_sectoral):
    value_sector = data_sectoral_global_2022[sector_txt].values[0]
    labels_sectors.append(sector_txt+' ('+str(int(value_sector/1000))+')')
    #labels_sectors.append(letters[i]+'. '+sector_txt+' ('+str(int(value_sector/1000))+')')

# Sort the sectors by their largest contribution
emissions_max_sectors = np.nanmax(sectoral_total_all,axis=1)
ind_sorted = np.argsort(-emissions_max_sectors)
labels_sectors_sorted = np.array(labels_sectors)[ind_sorted]
sectoral_total_sorted = sectoral_total_all[ind_sorted,:]


#%% FORMAT DATA

# NaNs mess up the stackplot. Replace them with 0
national_total_all[np.isnan(national_total_all)] = 0
regional_total_all[np.isnan(regional_total_all)] = 0
sectoral_total_all[np.isnan(sectoral_total_all)] = 0
national_total_sorted[np.isnan(national_total_sorted)] = 0
regional_total_sorted[np.isnan(regional_total_sorted)] = 0
sectoral_total_sorted[np.isnan(sectoral_total_sorted)] = 0


#%% MAKE STACKPLOT OF TOTALS - NATIONAL

# Make a time series
plt.figure(figsize=(10,5))
ax1 = plt.subplot2grid((1,1),(0,0))

ax1.stackplot(years_all,national_total_sorted/1000,labels=nations_all_sorted)
ax1.legend(loc='upper left',ncol=5,fontsize=2.95)
ax1.set_xlim(1750,2022)
#ax1.set_xlim(1750.5,2022.5)
ax1.set_ylabel('Emissions (Mt C)')
ax1.set_xlabel('Year')
ax1.set_title('Carbon emissions from all nations - '+variable_to_plot,fontsize=14)
ax1.set_xticks([1750,1800,1850,1900,1950,2000,2022])

if save_instead_of_plot:
    plt.savefig(output_dir+'figZ_2a_stackplot_nations_'+variable_to_plot+'.png',dpi=300,format='png',bbox_inches='tight')
    plt.close()
else:
    plt.show()

#%% CREATE COLOR SCALES

# Color scale for regions
colormap_selected1 = plt.cm.tab20
colors1 = colormap_selected1(np.linspace(0,1,20))
colormap_selected2 = plt.cm.Set2
colors2 = colormap_selected2(np.linspace(0,1,8))
colors_regions = np.concatenate((colors2[:3,:],colors1),axis=0)

# Color scale for sectors
colormap_selected3 = plt.cm.tab20c
colors3 = colormap_selected3(np.linspace(0,1,15))
colors_sectors = np.concatenate((colors3,colors2[1:2,:],colors2[3:4,:]),axis=0)
"""
colormap_selected4 = plt.cm.tab20
colors4 = colormap_selected4(np.linspace(0,1,20))
colors_sectors = colors4[:-4]
"""


#%% MAKE STACKPLOT OF TOTALS - REGIONAL
"""
# Make a time series
plt.figure(figsize=(10,5))
ax1 = plt.subplot2grid((1,1),(0,0))

ax1.stackplot(years_all,regional_total_all[::-1]/1000,labels=labels_regions[::-1],colors=colors_regions[::-1])
letters_to_plot = ['WE','EE','WA','SA','SEA','EA','NA']
values_to_plot = [168,1040,1820,2640,3350,5300,8200]
for i in range(len(letters_to_plot)):
    ax1.text(2019.5,values_to_plot[i],letters_to_plot[i],va='center',ha='center',fontsize=7)

handles, labels = ax1.get_legend_handles_labels()
ax1.legend(handles[::-1],labels[::-1],loc='upper left',ncol=1,fontsize=7)
ax1.set_ylabel('Emissions (Mt C)')
ax1.set_xlabel('Year')
ax1.set_title('Carbon emissions from each region',fontsize=14)
ax1.set_ylim(0,10000)
ax1.set_xlim(1850,2022)
#ax1.set_xlim(1850,2022.5)
ax1.set_xticks([1850,1900,1950,2000,2022])

if save_instead_of_plot:
    plt.savefig(output_dir+'figZ_2b_stackplot_regions_'+variable_to_plot+'.png',dpi=300,format='png',bbox_inches='tight')
    plt.close()
else:
    plt.show()


#%% MAKE STACKPLOT OF TOTALS - SECTORAL

# Make a time series
plt.figure(figsize=(2,5))
ax1 = plt.subplot2grid((1,1),(0,0))

ax1.stackplot(years_sectoral,sectoral_total_all[::-1]/1000,labels=labels_sectors[::-1],colors=colors_sectors[::-1])
handles, labels = ax1.get_legend_handles_labels()
ax1.legend(handles[::-1],labels[::-1],loc='upper left',ncol=1,fontsize=8,bbox_to_anchor=[1.02,.8])
#ax1.set_ylabel('Emissions (Mt C)')
ax1.set_xlabel('Year')
ax1.set_title('Sectors',fontsize=14)
ax1.set_ylim(0,10000)
ax1.set_xlim(1995,2022)
#ax1.set_xlim(1994.5,2022.5)

if save_instead_of_plot:
    plt.savefig(output_dir+'figZ_2c_stackplot_sectors_'+variable_to_plot+'.png',dpi=300,format='png',bbox_inches='tight')
    plt.close()
else:
    plt.show()
"""

#%% COMBINED

# Flip the arrays for easier use
regional_total_flipped = regional_total_all[::-1]
sectoral_total_flipped = sectoral_total_all[::-1]

# Make a time series
plt.figure(figsize=(13,5))
ax1 = plt.subplot2grid((1,21),(0,0),colspan=18)
ax2 = plt.subplot2grid((1,21),(0,18),colspan=3)
#f, (ax1,ax2) = plt.subplots(1,2,width_ratios=[15,1],figsize=(13,5))

regional_sum = np.sum(regional_total_flipped,axis=0)
regional_sum_lower = regional_sum * (1 - 0.084)
regional_sum_upper = regional_sum * (1 + 0.084)

# Region plot
ax1.stackplot(years_all,regional_total_flipped/1000,labels=labels_regions[::-1],colors=colors_regions[::-1])
#ax1.plot(years_all,regional_sum_lower/1000,color='gray',linestyle='--',linewidth=.75)
#ax1.plot(years_all,regional_sum_upper/1000,color='gray',linestyle='--',linewidth=.75)
"""
for i in range(len(labels_regions)):
    if regional_total_flipped[i,-1] > 300000:
        sum_plus_half_value = np.nansum(regional_total_flipped[:i,-1],axis=0) + (regional_total_flipped[i,-1]/2)
        letter_txt = labels_regions[::-1][i][:1]
        ax1.text(2018,sum_plus_half_value/1000,letter_txt,va='center')
        print(letter_txt,sum_plus_half_value/1000)
"""
#letters_to_plot = ['t','q','n','m','l','k','g']
letters_to_plot = ['WE','EE','WA','SA','SEA','EA','NA']
values_to_plot = [168,1040,1820,2640,3350,5300,8200]
for i in range(len(letters_to_plot)):
    ax1.text(2019.5,values_to_plot[i],letters_to_plot[i],va='center',ha='center',fontsize=7)

handles1, labels1 = ax1.get_legend_handles_labels()
ax1.legend(handles1[::-1],labels1[::-1],loc='upper left',ncol=1,fontsize=7,title="(a) Regions")
ax1.set_ylabel('Emissions (Mt C)')
ax1.set_xlabel('Year')
ax1.set_title('(a) Carbon emissions by region',fontsize=14,loc="center")
ax1.set_ylim(0,10000)
#ax1.set_xlim(1850,2022)
ax1.set_xlim(1850,2022.5)
ax1.set_xticks([1850,1900,1950,2000,2022])

# Sector plot
ax2.stackplot(years_sectoral,sectoral_total_flipped/1000,labels=labels_sectors[::-1],colors=colors_sectors[::-1])
"""
for i in range(len(labels_sectors)):
    #if sectoral_total_flipped[i,-1] > 300000:
        sum_plus_half_value = np.nansum(sectoral_total_flipped[:i,-1],axis=0) + (sectoral_total_flipped[i,-1]/2)
        letter_txt = labels_sectors[::-1][i][:1]
        ax2.text(2018,sum_plus_half_value/1000,letter_txt,va='center')
        print(letter_txt,sum_plus_half_value/1000)
"""
handles2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(handles2[::-1],labels2[::-1],loc='upper left',ncol=1,fontsize=7,bbox_to_anchor=[-4.9,1],title="(b) Sectors")  # [-5.5,1]
#ax2.set_ylabel('Emissions (Mt C)')
ax2.set_xlabel('Year')
ax2.set_title('(b) Sectors',fontsize=14,loc="center")
ax2.set_ylim(0,10000)
#ax2.set_xlim(1995,2022)
ax2.set_xlim(1994.5,2022.5)
ax2.set_yticklabels([])
ax2.set_xticks([2000,2022])

if save_instead_of_plot:
    plt.savefig(output_dir+'fig3_stackplot_combined_'+variable_to_plot+'.png',dpi=300,format='png',bbox_inches='tight')
    plt.close()
else:
    plt.show()


