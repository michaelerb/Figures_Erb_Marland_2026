#==============================================================================
# Make plots of sectoral emissions
#   Author: Michael Erb
#==============================================================================

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

plt.style.use('ggplot')
save_instead_of_plot = True


#%% LOAD DATA

data_dir = "C:/Users/erbm/Documents/GitHub/CDIAC-Fossil-Fuels/output/Products/Past_Products/CDIAC_2022/"
output_dir = "C:/Users/erbm/Dropbox/Academia/AppState/Manuscripts/Submitted/2026_Erb_Marland_CDIAC/proofs/analysis/figures/"

# Load the sectoral data
data_sectoral = pd.read_excel(data_dir+'sectoral.1995_2022.xlsx')
keys_sectoral = ["Total (Sectoral)",
                 "Electric, CHP, Heat Plants",
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
                 "Manufacture of Cement",
                 "Bunkered (Marine)",
                 "Bunkered (Aviation)"]

# Open the country lookup file
dir_lookup = 'C:/Users/erbm/Documents/GitHub/CDIAC-Fossil-Fuels/data/Lookups/'
country_lookup = pd.read_excel(dir_lookup+'Country_Lookup.xlsx')


#%% REFORMAT DATA - GLOBAL

data_sectoral_global = data_sectoral[data_sectoral["Nation"] == 'Global']
data_sectoral_global_2022 = data_sectoral_global[data_sectoral_global["Year"] == 2022]
sectoral_total_all = np.array(data_sectoral_global[keys_sectoral]).transpose()
years_sectoral     = data_sectoral_global['Year']


#%% SETUP

# Set things up
years_all   = np.arange(min(data_sectoral['Year']),max(data_sectoral['Year'])+1)
nations_all = np.unique(data_sectoral['Nation'])
regions_all = np.unique(country_lookup['UN_Region'])

n_years   = len(years_all)
n_nations = len(nations_all)
n_regions = len(regions_all)
#n_sectors = len(keys_sectoral)

national_total_all = {}
regional_total_all = {}
for sector_txt in keys_sectoral:
    national_total_all[sector_txt] = np.zeros((n_nations,n_years)); national_total_all[sector_txt][:] = np.nan
    regional_total_all[sector_txt] = np.zeros((n_regions,n_years)); regional_total_all[sector_txt][:] = np.nan

#national_total_all = np.zeros((n_sectors,n_nations,n_years)); national_total_all[:] = np.nan
#regional_total_all = np.zeros((n_sectors,n_regions,n_years)); regional_total_all[:] = np.nan


#%% REFORMAT DATA - BY NATION

# Select the variable to plot
#variable_to_plot = 'Total'
#variable_to_plot = 'Bunker'

# Rearrange data
i=0; nation_txt = nations_all[i]; sector_txt = keys_sectoral[0]
for i,nation_txt in enumerate(nations_all):
    nation_year = np.array(data_sectoral['Year'].loc[data_sectoral['Nation'] == nation_txt])
    ind_years = np.where(np.isin(years_all,nation_year))[0]
    for sector_txt in keys_sectoral:
        nation_data = np.array(data_sectoral[sector_txt].loc[data_sectoral['Nation'] == nation_txt])
        national_total_all[sector_txt][i,ind_years] = nation_data


#%% REFORMAT DATA - BY REGION

# Sum the countries into their regions
i = 0; region_txt = regions_all[i]
labels_regions = regions_all
for i,region_txt in enumerate(regions_all):
    ind_in_region = np.where(country_lookup['UN_Region'] == region_txt)[0]
    countries_in_region = country_lookup.loc[ind_in_region]["Country_Name"]
    bool_for_data = np.isin(nations_all,list(countries_in_region))
    for sector_txt in keys_sectoral:
        regional_total_all[sector_txt][i,:] = np.nansum(national_total_all[sector_txt][bool_for_data,:], axis=0)
        # NaNs mess up the stackplot. Replace them with 0
        regional_total_all[sector_txt][np.isnan(regional_total_all[sector_txt])] = 0


#%% FIGURES

letters = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

# Generate a list of colors, like those used in the regional time series plot
colormap_selected1 = plt.cm.tab20
colors1 = colormap_selected1(np.linspace(0,1,20))
colormap_selected2 = plt.cm.Set2
colors2 = colormap_selected2(np.linspace(0,1,8))
colors_regions = np.concatenate((colors2[:3,:],colors1),axis=0)

# Make a time series
f,ax = plt.subplots(4,5,sharex=True,figsize=(22,11))
ax = ax.ravel()

# Sector plot
for i,sector_txt in enumerate(keys_sectoral):
    ax[i].stackplot(years_all,regional_total_all[sector_txt][::-1]/1000,labels=labels_regions[::-1],colors=colors_regions[::-1])
    if sector_txt == 'Manufact, Constr, Non-Fuel Industry': sector_txt = 'Manufact, Constr, Non-Fuel'
    ax[i].set_title('('+letters[i]+') '+sector_txt,fontsize=11,loc="left")
    ax[i].set_ylim(ymin=0)
    ax[i].set_xlim(1995,2022)
    #ax[i].set_xlim(1995,2022.5)
    if i in [0,5,10,15]: ax[i].set_ylabel('Emissions (Mt C)')
    if i >= 15:       ax[i].set_xlabel('Year')
    if i == 17:       ax[i].legend(loc='lower center',bbox_to_anchor=(.5,-.97),reverse=True,fontsize=13,ncol=6)

#ax[19].set_axis_off()
plt.suptitle('Carbon emissions from different sectors',fontsize=20,y=0.94)
plt.subplots_adjust(top=0.87)

if save_instead_of_plot:
    plt.savefig(output_dir+'figS2_sectoral_emissions.png',dpi=300,format='png',bbox_inches='tight')
    plt.close()
else:
    plt.show()


#%% FIGURES - PLOT TOTALS

# Make a time series
f,ax = plt.subplots(4,5,sharex=True,figsize=(22,11))
ax = ax.ravel()

# Sector plot
for i,sector_txt in enumerate(keys_sectoral):
    ax[i].fill_between(years_sectoral,sectoral_total_all[i,:]*0,sectoral_total_all[i,:]/1000)
    if sector_txt == 'Manufact, Constr, Non-Fuel Industry': sector_txt = 'Manufact, Constr, Non-Fuel'
    ax[i].set_title('('+letters[i]+') '+sector_txt,fontsize=11,loc="left")
    ax[i].set_ylim(ymin=0)
    ax[i].set_xlim(1995,2022)
    #ax[i].set_xlim(1995,2022.5)
    if i in [0,5,10,15]: ax[i].set_ylabel('Emissions (Mt C)')
    if i >= 15:       ax[i].set_xlabel('Year')

#ax[19].set_axis_off()
plt.suptitle('Carbon emissions from different sectors',fontsize=20,y=0.94)
plt.subplots_adjust(top=0.87)

if save_instead_of_plot:
    plt.savefig(output_dir+'figS2b_sectoral_emissions.png',dpi=300,format='png',bbox_inches='tight')
    plt.close()
else:
    plt.show()

