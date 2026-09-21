#==============================================================================
# Make a map showing the different UN regions.
#   Author: Michael Erb
#==============================================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import cartopy.crs as ccrs
import geopandas as gpd

save_instead_of_plot = True

# Choose the regions to plot
regions_to_plot = 'UN_Region'
#regions_to_plot = 'Continent'


#%% LOAD DATA - NATIONAL DATA

data_dir = "C:/Users/erbm/Documents/GitHub/CDIAC-Fossil-Fuels/output/Products/Past_Products/CDIAC_2022/"
output_dir = "C:/Users/erbm/Dropbox/Academia/AppState/Manuscripts/Submitted/2026_Erb_Marland_CDIAC/3rd_submission/analysis/figures/"

# Load the country lookup data
country_lookup = pd.read_excel(data_dir+'Country_Lookup.xlsx')
country_lookup = country_lookup.rename(columns={"Alpha3_code":"Code"})
country_lookup.loc[country_lookup["Country_Name"] == "Antarctic Fisheries","Code"] = "ATA"  # Add a code for Antarctica

# Load the Natural Earth data
borders_naturalearth = gpd.read_file("P:/data_weather/data_NaturalEarth/ne_50m_admin_0_countries.zip")
borders_naturalearth.loc[borders_naturalearth["NAME"] == "Kosovo", "ISO_A3_EH"] = "XKX"  # Account for Kosovo
# Note: The nation "Bonaire, Sint Eustatius, and Saba" has no data in Natural Earth


#%% PREPARATION

# Remove rows with nan in the selected column
data_selected = country_lookup.dropna(subset=[regions_to_plot,'Code'])
groups = np.sort(np.unique(data_selected[regions_to_plot]))

# Check to see that the codes match
codes_cdiac = np.sort(np.unique(data_selected['Code']))
codes_ne    = np.sort(np.unique(borders_naturalearth['ISO_A3_EH']))
codes_not_found = list(set(codes_cdiac) - set(codes_ne))
print('Country codes not found:',codes_not_found)
data_without_codes = data_selected[data_selected['Code'].isin(codes_not_found)]

# Join with the Natural Earth data
data_selected = pd.merge(data_selected, borders_naturalearth, left_on='Code', right_on='ISO_A3_EH', how='left')
data_selected = data_selected[~data_selected["Code"].isin(codes_not_found)]

# Sort the data by region
#country_lookup = country_lookup.sort_values(by=[regions_to_plot])


#%% ASSIGN COLORS

# Generate a list of colors, like those used in the regional time series plot
colormap_selected1 = plt.cm.tab20
colors1 = colormap_selected1(np.linspace(0,1,20))
colormap_selected2 = plt.cm.Set2
colors2 = colormap_selected2(np.linspace(0,1,8))
colors_regions = np.concatenate((colors2[:3,:],colors1),axis=0)

# A function to turn RBG values into hexcodes
def rgb_to_hex(rgb_values):
    if len(rgb_values) == 4: rgb_values = rgb_values[:3]
    if max(rgb_values) <= 1: rgb_values = rgb_values*255
    rgb_values = rgb_values.astype(int)
    hex_values = "#%02x%02x%02x" % (rgb_values[0],rgb_values[1],rgb_values[2])
    return hex_values

# Set colors to use
legend_values = []
for i,value_txt in enumerate(groups):
    data_selected.loc[data_selected[regions_to_plot] == value_txt, "Color"] = rgb_to_hex(colors_regions[i,:])
    legend_values.append(Patch(facecolor=rgb_to_hex(colors_regions[i,:]), label=value_txt))


#%% FIGURES - MAP

# Make map
plt.figure(figsize=(10,12))
ax1 = plt.subplot2grid((1,1),(0,0),projection=ccrs.PlateCarree()); ax1.set_extent([0,359.99,-60,86],ccrs.PlateCarree())
ax1.add_geometries(data_selected['geometry'], crs=ccrs.PlateCarree(),
                   #edgecolor = 'k', linewidth = .25,
                   facecolor = data_selected['Color'])
ax1.legend(handles=legend_values, loc="upper center", fontsize = 6.5, ncol=6, bbox_to_anchor=(.5,0))
ax1.coastlines()
ax1.spines['geo'].set_edgecolor('black')

if save_instead_of_plot:
    plt.savefig(output_dir+'figS1_map_regions_'+regions_to_plot+'.png',dpi=300,format='png',bbox_inches='tight')
    plt.close()
else:
    plt.show()
