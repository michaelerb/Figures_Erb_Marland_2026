#==============================================================================
# Makes some overview figures of the CDIAC data, showing emissions by nation,
# region, fuel type, and sector.
#   Author: Michael Erb
#==============================================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import cartopy.crs as ccrs
import geopandas as gpd

plt.style.use('ggplot')
save_instead_of_plot = True


#%% LOAD DATA

data_dir   = "C:/Users/erbm/Documents/GitHub/CDIAC-Fossil-Fuels/output/Products/Past_Products/CDIAC_2022/"
output_dir = "C:/Users/erbm/Dropbox/Academia/AppState/Manuscripts/Submitted/2026_Erb_Marland_CDIAC/proofs/analysis/figures/"

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

# Open the country lookup file
country_lookup = pd.read_excel(data_dir+'Country_Lookup.xlsx')
country_lookup = country_lookup.rename(columns={"Alpha3_code":"Code"})
country_lookup.loc[country_lookup["Country_Name"] == "Antarctic Fisheries","Code"] = "ATA"  # Add a code for Antarctica

borders_naturalearth = gpd.read_file("P:/data_weather/data_NaturalEarth/ne_50m_admin_0_countries.zip")
borders_naturalearth.loc[borders_naturalearth["NAME"] == "Kosovo", "ISO_A3_EH"] = "XKX"  # Account for Kosovo
# Note: The nation "Bonaire, Sint Eustatius, and Saba" has no data in Natural Earth


#%% PREPARATION

# Remove rows with nan in the selected column
data_selected = country_lookup.dropna(subset=["Continent",'Code'])
groups = np.sort(np.unique(data_selected["Continent"]))

# Check to see that the codes match
codes_cdiac = np.sort(np.unique(data_selected['Code']))
codes_ne    = np.sort(np.unique(borders_naturalearth['ISO_A3_EH']))
codes_not_found = list(set(codes_cdiac) - set(codes_ne))
print('Country codes not found:',codes_not_found)
data_without_codes = data_selected[data_selected['Code'].isin(codes_not_found)]

# Join with the Natural Earth data
data_selected = pd.merge(data_selected, borders_naturalearth, left_on='Code', right_on='ISO_A3_EH', how='left')
data_selected = data_selected[~data_selected["Code"].isin(codes_not_found)]

# Join with the CDIAC data
data_national = pd.merge(data_national, country_lookup[["Country_ID","Continent"]], left_on='Nation ID', right_on='Country_ID', how='left')


#%% COMPUTE SUMS OVER CONTINENTS

regional_total_all = data_national.groupby(["Continent","Year"]).sum().reset_index()
regional_total_all = regional_total_all[["Continent","Year","Total"]]
regional_total_all = regional_total_all.pivot(index="Year",columns="Continent",values="Total").reset_index()

regional_total_all = regional_total_all.fillna(0)
labels_regions = list(regional_total_all.keys())[1:]


#%% ASSIGN COLORS

# Color scale
colors_default = plt.rcParams['axes.prop_cycle'].by_key()['color']
colors_default[2], colors_default[3] = colors_default[3], colors_default[2]

# Set colors to use
legend_values = []
for i,value_txt in enumerate(groups):
    data_selected.loc[data_selected["Continent"] == value_txt, "Color"] = colors_default[6-i]
    legend_values.append(Patch(facecolor=colors_default[6-i], label=value_txt))


#%% MAKE STACKPLOT OF TOTALS - REGIONAL

# Make a time series
plt.figure(figsize=(14,4))
ax1 = plt.subplot2grid((1,1),(0,0))
ax1_inset = ax1.inset_axes([.01,.21,.4,.65],projection=ccrs.PlateCarree()); ax1_inset.set_extent([0,359.99,-60,86],ccrs.PlateCarree())

ax1.stackplot(regional_total_all["Year"],np.transpose(regional_total_all[labels_regions])[::-1]/1000,labels=labels_regions[::-1],colors=colors_default)
#ax1.stackplot(years_all,regional_total_all[::-1]/1000,labels=labels_regions[::-1],colors=colors_default)
handles, labels = ax1.get_legend_handles_labels()
ax1.legend(handles[::-1],labels[::-1],loc='upper left',ncol=7,fontsize=10)
ax1.set_ylabel('Emissions (Mt C)')
ax1.set_xlabel('Year')
ax1.set_title('Carbon emissions by continent',fontsize=14)
ax1.set_ylim(0,10000)
ax1.set_xlim(1850,2022.5)
ax1.set_xticks([1850,1900,1950,2000,2022])

# Add a map
ax1_inset.add_geometries(data_selected['geometry'], crs=ccrs.PlateCarree(),
                         facecolor = data_selected['Color'])
ax1_inset.coastlines()
ax1_inset.spines['geo'].set_edgecolor('black')
ax1_inset.spines['geo'].set_linewidth(.5)
ax1_inset.set_title("Modern regions shown",fontsize=10)

if save_instead_of_plot:
    plt.savefig(output_dir+'fig0_abstract_a_stackplot.png',dpi=300,format='png',bbox_inches='tight')
    plt.close()
else:
    plt.show()
