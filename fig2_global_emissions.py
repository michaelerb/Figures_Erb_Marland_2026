#==============================================================================
# Plot global CDIAC emissions by fuel type.
#   Author: Michael Erb
#==============================================================================

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

plt.style.use('ggplot')
save_instead_of_plot = True


#%% LOAD DATA

data_dir   = "C:/Users/erbm/Documents/GitHub/CDIAC-Fossil-Fuels/output/Products/Past_Products/CDIAC_2022/"
output_dir = "C:/Users/erbm/Dropbox/Academia/AppState/Manuscripts/Submitted/2026_Erb_Marland_CDIAC/3rd_submission/analysis/figures/"

# Load the data
data_global = pd.read_excel(data_dir+'global.1750_2022.xlsx')
data_global = data_global.rename(columns={"Emissions from fossil fuels and cement production (million metric tons of C)":"Total",
                                          "Emissions from solid fuel consumption": "Solid fuels",
                                          "Emissions from liquid fuel consumption":"Liquid fuels",
                                          "Emissions from gas fuel consumption":   "Gas fuels",
                                          "Emissions from cement production":      "Cement production",
                                          "Emissions from gas flaring and venting":"Gas flaring/venting",
                                          "Emissions per capita (metric tons of carbon)":"Per capita",
                                          "Emissions from bunker fuels (also included in other categories)":"Bunker",
                                          "Emissions from aviation bunker fuels (subset of bunker emissions)":"Bunker aviation"})


#%% TIME SERIES

# Compute upper and lower bounds
total_lower = data_global["Total"] * (1 - 0.084)
total_upper = data_global["Total"] * (1 + 0.084)

keys_to_plot = ['Solid fuels','Liquid fuels','Gas fuels','Cement production','Gas flaring/venting']

# Make maps
plt.figure(figsize=(10,5))
ax1 = plt.subplot2grid((1,1),(0,0))

plot1 = ax1.stackplot(data_global['Year'],np.array(data_global[keys_to_plot]).transpose(),labels=keys_to_plot)
ax1.plot(data_global['Year'],total_lower,color='gray',linestyle='--',linewidth=.75,zorder=3)
ax1.plot(data_global['Year'],total_upper,color='gray',linestyle='--',linewidth=.75,zorder=3)
#ax1.plot(data_global['Year'],data_global['Total'],c='blue',label='Total')
ax1.plot(data_global['Year'],data_global['Bunker'],c='gray',label='Bunker')
ax1.legend(loc='upper left')
ax1.set_ylim(0,14000)
ax1.set_ylabel('Emissions (Mt C)')
ax1.set_xlabel('Year')
ax1.set_title('Global carbon emissions by source',fontsize=14)
#ax1.set_xlim(1750,2022)
ax1.set_xlim(1749.5,2022.5)
#ax1.axhline(y=data_global['Total'].iloc[-1])
ax1.set_xticks([1750,1800,1850,1900,1950,2000,2022])

ax1_right = ax1.twinx()
ax1_right.plot(data_global['Year'],data_global['Per capita'],c='tab:orange',label='Total per capita',zorder=0)
#ax1_right.legend(loc='upper left', bbox_to_anchor=[0,.72])
ax1_right.legend(loc='upper left', bbox_to_anchor=[0,.673])
ax1_right.set_ylim(0,1.4)
ax1_right.set_ylabel('Emissions per capita (t C)',color='tab:orange')
ax1_right.grid(False)
ax1_right.tick_params(colors='tab:orange')

#ax1.set_zorder(ax1_right.get_zorder()+1)
#ax1.patch.set_visible(False)
if save_instead_of_plot:
    plt.savefig(output_dir+'fig2_global_emissions.png',dpi=300,format='png',bbox_inches='tight')
    plt.close()
else:
    plt.show()


#%% FIGURE WITH SEPERATE CURVES

# Make maps
plt.figure(figsize=(10,5))
ax1 = plt.subplot2grid((1,1),(0,0))

for key_txt in keys_to_plot:
    plot1 = ax1.plot(data_global['Year'],data_global[key_txt],label=key_txt)

ax1.legend(loc='upper left')
ax1.set_ylim(0,4500)
ax1.set_ylabel('Emissions (Mt C)')
ax1.set_xlabel('Year')
ax1.set_title('Global carbon emissions by source',fontsize=14)
#ax1.set_xlim(1750,2022)
ax1.set_xlim(1749.5,2022.5)
ax1.set_xticks([1750,1800,1850,1900,1950,2000,2022])

if save_instead_of_plot:
    plt.savefig(output_dir+'figZ_2a_global_emissions.png',dpi=300,format='png',bbox_inches='tight')
    plt.close()
else:
    plt.show()

