#==============================================================================
# Calculate values for 2022 and change in the global and national data. Make a
# table.
#   Author: Michael Erb
#   Date: 2/24/2026
#==============================================================================

import numpy as np
import pandas as pd
import scipy
#import matplotlib.pyplot as plt


#%% LOAD DATA

data_dir   = "C:/Users/erbm/Documents/GitHub/CDIAC-Fossil-Fuels/output/Products/Past_Products/CDIAC_2022/"
output_dir = "C:/Users/erbm/Dropbox/Academia/AppState/Manuscripts/Submitted/2026_Erb_Marland_CDIAC/3rd_submission/analysis/figures/"

# Load the total data
data_total = pd.read_excel(data_dir+'total.2022.xlsx')
data_total = data_total.rename(columns={"Emissions from fossil fuels and cement production (thousand metric tons of C)":"Emissions"})
data_total_sorted = data_total.sort_values('Emissions', ascending=False)
nations_top_10   = data_total_sorted['Nation'][0:10].values

# Load the data
data_global = pd.read_excel(data_dir+'global.1750_2022.xlsx')
data_global = data_global.rename(columns={"Emissions from fossil fuels and cement production (million metric tons of C)":"Total",
                                          "Emissions from solid fuel consumption": "Solid fuels",
                                          "Emissions from liquid fuel consumption":"Liquid fuels",
                                          "Emissions from gas fuel consumption":   "Gas fuels",
                                          "Emissions from cement production":      "Cement production",
                                          "Emissions from gas flaring and venting":"Gas flaring",
                                          "Emissions per capita (metric tons of carbon)":"Per capita",
                                          "Emissions from bunker fuels (also included in other categories)":"Bunker",
                                          "Emissions from aviation bunker fuels (subset of bunker emissions)":"Bunker aviation"})

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

# Sort the national data by total emissions
data_national = data_national.sort_values("Total", ascending=False)

# Load population data
dir_population = 'C:/Users/erbm/Documents/GitHub/CDIAC-Fossil-Fuels/data/Inputs/Demographic/'
data_population = pd.read_excel(dir_population+'WPP2024_GEN_F01_DEMOGRAPHIC_INDICATORS_COMPACT.xlsx',skiprows=16)
data_population = data_population.rename(columns={"Region, subregion, country or area *":"Location",
                                                  "Location code": "Location_code",
                                                  "Total Population, as of 1 January (thousands)":"Population"})
data_population = data_population[['Location','Location_code','Year','Population']]


#%% FUNCTION TO CALCULATE TRENDS

year_start = 2013

# Function to calculate a trend
#data_selected, var_txt = data_global, 'Total'
#data_selected, var_txt = pop_global,'Population'
#data_selected, var_txt = data_nation,'Total'
def calc_trend(data_selected, var_txt):
    # Select the data
    data_selected_years = data_selected[(data_selected["Year"] >= year_start) & (data_selected["Year"] <= 2022)]
    var_selected   = data_selected_years[var_txt].values
    years_selected = data_selected_years['Year'].values
    # Compute values as a percentage of the first year
    var_year_start = data_selected_years[data_selected_years["Year"] == year_start][var_txt].values
    var_selected = (var_selected / var_year_start) * 100
    var_selected = var_selected.astype(float)
    # Compute linear regression
    slope, intercept, rvalue, pvalue, stderr = scipy.stats.linregress(years_selected,var_selected)
    return slope

#plt.plot(years_selected,var_selected)


#%% ADD GLOBAL AND NATIONAL VALUES

# For each nation, calculate the 10 year trend for each category
values_all_df = pd.DataFrame(columns=["Rank","Nation","Total_CO2","Population","PerCapita","Emissions_change","Population_change","PerCapita_change","Emissions_change_per","Population_change_per","PerCapita_change_per"])

# Get data for year_start and 2022
data_global_2022       = data_global[data_global["Year"] == 2022]
data_global_year_start = data_global[data_global["Year"] == year_start]
pop_global             = data_population[data_population["Location_code"] == 900]
pop_global_2022        = pop_global[pop_global["Year"] == 2022]
pop_global_year_start  = pop_global[pop_global["Year"] == year_start]

# Calculate trends over the selected interval
global_total_trend     = calc_trend(data_global,'Total')
global_pop_trend       = calc_trend(pop_global,'Population')
global_percapita_trend = calc_trend(data_global,'Per capita')

# Add the global data
values_all_df.loc[0,"Rank"]              = ""
values_all_df.loc[0,"Nation"]            = "Global"
values_all_df.loc[0,"Total_CO2"]         = round(data_global_2022["Total"].values[0])
values_all_df.loc[0,"Population"]        = round(pop_global_2022["Population"].values[0] / 1000)
values_all_df.loc[0,"PerCapita"]         = round(data_global_2022["Per capita"].values[0], 1)
values_all_df.loc[0,"Emissions_change"]  = round(((data_global_2022["Total"].values[0]      - data_global_year_start["Total"].values[0])      / data_global_year_start["Total"].values[0]) * 100, 1)
values_all_df.loc[0,"Population_change"] = round(((pop_global_2022["Population"].values[0]  - pop_global_year_start["Population"].values[0])  / pop_global_year_start["Population"].values[0]) * 100, 1)
values_all_df.loc[0,"PerCapita_change"]  = round(((data_global_2022["Per capita"].values[0] - data_global_year_start["Per capita"].values[0]) / data_global_year_start["Per capita"].values[0]) * 100, 1)
values_all_df.loc[0,"Emissions_change_per"]  = round(global_total_trend, 1)
values_all_df.loc[0,"Population_change_per"] = round(global_pop_trend, 1)
values_all_df.loc[0,"PerCapita_change_per"]  = round(global_percapita_trend, 1)

# Add the national data
i = 0; nation_txt = nations_top_10[i]
for i,nation_txt in enumerate(nations_top_10):
    #
    # Get data for nation
    nation_id = data_total_sorted['Nation ID'][i]
    #
    # Get data for year_start and 2022
    data_nation            = data_national[data_national["Nation ID"] == nation_id]
    data_nation_2022       = data_nation[data_nation["Year"] == 2022]
    data_nation_year_start = data_nation[data_nation["Year"] == year_start]
    pop_nation             = data_population[data_population["Location_code"] == nation_id]
    pop_nation_2022        = pop_nation[pop_nation["Year"] == 2022]
    pop_nation_year_start  = pop_nation[pop_nation["Year"] == year_start]
    #
    # Calculate trends over the selected interval
    nation_total_trend     = calc_trend(data_nation,'Total')
    nation_pop_trend       = calc_trend(pop_nation,'Population')
    nation_percapita_trend = calc_trend(data_nation,'Per capita')
    #
    # For each key, calculate the trend of the last 10 years
    values_all_df.loc[i+1,"Rank"]              = i+1
    values_all_df.loc[i+1,"Nation"]            = nation_txt
    values_all_df.loc[i+1,"Total_CO2"]         = round(data_nation_2022["Total"].values[0] / 1000)
    values_all_df.loc[i+1,"Population"]        = round(pop_nation_2022["Population"].values[0] / 1000)
    values_all_df.loc[i+1,"PerCapita"]         = round(data_nation_2022["Per capita"].values[0], 1)
    values_all_df.loc[i+1,"Emissions_change"]  = round(((data_nation_2022["Total"].values[0]      - data_nation_year_start["Total"].values[0])      / data_nation_year_start["Total"].values[0]) * 100, 1)
    values_all_df.loc[i+1,"Population_change"] = round(((pop_nation_2022["Population"].values[0]  - pop_nation_year_start["Population"].values[0])  / pop_nation_year_start["Population"].values[0]) * 100, 1)
    values_all_df.loc[i+1,"PerCapita_change"]  = round(((data_nation_2022["Per capita"].values[0] - data_nation_year_start["Per capita"].values[0]) / data_nation_year_start["Per capita"].values[0]) * 100, 1)
    values_all_df.loc[i+1,"Emissions_change_per"]  = round(nation_total_trend, 1)
    values_all_df.loc[i+1,"Population_change_per"] = round(nation_pop_trend, 1)
    values_all_df.loc[i+1,"PerCapita_change_per"]  = round(nation_percapita_trend, 1)


#%% SAVE DATA

values_all_df.to_excel(output_dir+'table1_values.xlsx', index=False)
