#==============================================================================
# Make national and sectoral plots of the largest emitters.
#   Author: Michael Erb
#==============================================================================

import numpy as np
import matplotlib.pyplot as plt
#import scipy.cluster.hierarchy as hierarchy
import pandas as pd

plt.style.use('ggplot')
save_instead_of_plot = True


#%% LOAD DATA

data_dir   = "C:/Users/erbm/Documents/GitHub/CDIAC-Fossil-Fuels/output/Products/Past_Products/CDIAC_2022/"
output_dir = "C:/Users/erbm/Dropbox/Academia/AppState/Manuscripts/Submitted/2026_Erb_Marland_CDIAC/proofs/analysis/figures/"

# Load the total data
data_total = pd.read_excel(data_dir+'total.2022.xlsx')
data_total = data_total.rename(columns={"Emissions from fossil fuels and cement production (thousand metric tons of C)":"Emissions"})
#data_total_sorted = data_total.sort_values('Emissions', ascending=False)
#top_50 = data_total_sorted['Nation'][0:50].values
data_total = data_total[["Nation ID","Emissions"]]

# Load the national data
data_national = pd.read_excel(data_dir+'nation.1750_2022.xlsx')
data_national = data_national.rename(columns={"Emissions from fossil fuels and cement production (thousand metric tons of C)":"Total",
                                              "Emissions from solid fuel consumption": "Solid fuels",
                                              "Emissions from liquid fuel consumption":"Liquid fuels",
                                              "Emissions from gas fuel consumption":   "Gas fuels",
                                              "Emissions from cement production":      "Cement production",
                                              "Emissions from gas flaring and venting":"Gas flaring/venting",
                                              "Emissions per capita (metric tons of carbon)":"Per capita",
                                              "Emissions from bunker fuels (not included in the totals)":"Bunker",
                                              "Emissions from aviation bunker fuels (subset of bunker emissions)":"Bunker aviation"})
nation_array = np.unique(data_national['Nation'])

# Load the sectoral data
data_sectoral = pd.read_excel(data_dir+'sectoral.1995_2022.xlsx')

# Open the country lookup file
dir_lookup = 'C:/Users/erbm/Documents/GitHub/CDIAC-Fossil-Fuels/data/Lookups/'
country_lookup = pd.read_excel(dir_lookup+'Country_Lookup.xlsx')
country_lookup = country_lookup[["Country_ID","Country_Name_Short"]]
country_lookup = country_lookup.rename(columns={"Country_ID":"Nation ID","Country_Name_Short":"Nation_short"})
country_lookup.loc[country_lookup["Nation_short"] == "South Korea","Nation_short"] = "Rep. of Korea"

#%% FORMAT THE DATA - NATIONAL

# Get data from 2022
data_national_2022 = data_national[data_national['Year'] == 2022].copy()

# Get shorter names for the nations
data_national_2022 = pd.merge(data_national_2022,country_lookup, on="Nation ID", how="left")

# Calculate the percentage for each category
keys_national = ['Solid fuels','Liquid fuels','Gas fuels','Cement production','Gas flaring/venting']
for key_txt in keys_national:
    data_national_2022[key_txt] = (data_national_2022[key_txt] / data_national_2022['Total']) * 100

# Get a subset of the data to plot
data_national_2022_sorted = data_national_2022.sort_values('Total', ascending=False)
data_national_selected = data_national_2022_sorted.iloc[:50,:]
data_national_selected = data_national_selected[['Nation_short']+keys_national]
data_national_selected = data_national_selected.fillna(0)
#data_national_selected[data_national_selected['Nation'].isin(top_50)]


#%% FORMAT THE DATA - SECTORAL

# Get data from 2022
data_sectoral_2022 = data_sectoral[data_sectoral['Year'] == 2022].copy()
data_sectoral_2022 = pd.merge(data_sectoral_2022, data_total, on="Nation ID", how="outer")

# Get shorter names for the nations
data_sectoral_2022 = pd.merge(data_sectoral_2022,country_lookup, on="Nation ID", how="left")


#%% SECTORAL - PERCENTAGE BY SECTOR

# Compute total of selected categories
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
data_sectoral_selected = data_sectoral_2022.copy()
#data_sectoral_selected["total_sectoral"] = data_sectoral_selected[keys_sectoral].sum(axis=1)

# Calculate the percentage for each category
for key_txt in keys_sectoral:
    data_sectoral_selected[key_txt] = (data_sectoral_selected[key_txt] / data_sectoral_selected['Total (Sectoral)']) * 100

# Get a subset of the data to plot
data_sectoral_selected = data_sectoral_selected.sort_values('Emissions', ascending=False)
data_sectoral_selected = data_sectoral_selected.iloc[:50,:]
data_sectoral_selected = data_sectoral_selected[['Nation_short']+keys_sectoral]
data_sectoral_selected = data_sectoral_selected.fillna(0)


#%% SECTORAL - PERCENTAGE BY CATEGORY

# Compute total of selected categories
keys_categories = ['Electric, CHP, heat plants','Industry','Transport','Household','Other']
data_categories_selected = data_sectoral_2022.copy()

# Calculate the percentage for each category
for key_txt in keys_categories:
    if   key_txt == 'Electric, CHP, heat plants': sectors_to_select = ["Electric, CHP, Heat Plants"]
    elif key_txt == 'Industry':  sectors_to_select = ["Energy Industries Own Use",
                                                      "Manufact, Constr, Non-Fuel Industry",
                                                      "Commerce and Public Services"]
    elif key_txt == 'Transport': sectors_to_select = ["Transport"]
    elif key_txt == 'Household': sectors_to_select = ["Household"]
    elif key_txt == 'Other':     sectors_to_select = ["Agriculture, Forestry, Fishing",
                                                      "Non-energy Use",
                                                      "Other Consumption",
                                                      "Losses",
                                                      "Flaring and Venting of Natural Gas",
                                                      "Manufacture of Cement"]
    data_categories_selected[key_txt] = (data_categories_selected[sectors_to_select].sum(axis=1) / data_categories_selected['Total (Sectoral)']) * 100

# Get a subset of the data to plot
data_categories_selected = data_categories_selected.sort_values('Emissions', ascending=False)
data_categories_selected = data_categories_selected.iloc[:50,:]
data_categories_selected = data_categories_selected[['Nation_short']+keys_categories]
data_categories_selected = data_categories_selected.fillna(0)


#%% FIGURE - COMBINED

# Set colors
#colormap_selected = plt.cm.tab20
#colors = colormap_selected(np.linspace(0,1,20))
colormap_selected = plt.cm.tab20c
colors = colormap_selected(np.linspace(0,1,15))

# Make a plot
f,(ax1,ax2) = plt.subplots(1,2,sharex=True,figsize=(10,8))

data_national_selected.plot(
    x = 'Nation_short',
    kind = 'barh',
    stacked = True,
    title = '(a) Distribution by fuel type',
    mark_right = True,
    xlim = (0,100),
    legend = False,
    width = .9,
    xlabel = 'Share of national emissions (%)',
    ylabel = '',
    ax = ax1
    ).legend(ncol=1, fontsize=8, loc='lower center', bbox_to_anchor = (.12,-.26), title="(a) Fuel types")
ax1.invert_yaxis()
ax1.tick_params(labelsize=8)

# Make a plot
data_sectoral_selected.plot(
    x = 'Nation_short',
    kind = 'barh',
    stacked = True,
    title = '(b) Distribution by sector',
    mark_right = True,
    xlim = (0,100),
    legend = False,
    width = .9,
    xlabel = 'Share of national emissions (%)',
    ylabel = '',
    color = colors,
    ax = ax2
    ).legend(ncol=3, fontsize=8, loc='lower center', bbox_to_anchor = (.12,-.26), title="(b) Sectors")
ax2.invert_yaxis()
ax2.yaxis.tick_right()
ax2.tick_params(labelsize=8)
if save_instead_of_plot: plt.savefig(output_dir+'fig6b_distributions.png',dpi=300,format='png',bbox_inches='tight') 


#%% FIGURE - COMBINED

# Set colors
colormap_selected = plt.cm.Paired
colors = colormap_selected(np.linspace(0,1,5))

# Make a plot
f,(ax1,ax2) = plt.subplots(1,2,sharex=True,figsize=(10,8))

data_national_selected.plot(
    x = 'Nation_short',
    kind = 'barh',
    stacked = True,
    title = '(a) Distribution by fuel type',
    mark_right = True,
    xlim = (0,100),
    legend = False,
    width = .9,
    xlabel = 'Share of national emissions (%)',
    ylabel = '',
    ax = ax1
    ).legend(ncol=3, fontsize=8, loc='lower center', bbox_to_anchor = (.5,-.15))
ax1.invert_yaxis()
ax1.tick_params(labelsize=8)

# Make a plot
data_categories_selected.plot(
    x = 'Nation_short',
    kind = 'barh',
    stacked = True,
    title = '(b) Distribution by sector',
    mark_right = True,
    xlim = (0,100),
    legend = False,
    width = .9,
    xlabel = 'Share of national emissions (%)',
    ylabel = '',
    color = colors,
    ax = ax2
    ).legend(ncol=3, fontsize=8, loc='lower center', bbox_to_anchor = (.5,-.15))
ax2.invert_yaxis()
ax2.yaxis.tick_right()
ax2.tick_params(labelsize=8)
if save_instead_of_plot: plt.savefig(output_dir+'fig6_distributions_simple.png',dpi=300,format='png',bbox_inches='tight') 


