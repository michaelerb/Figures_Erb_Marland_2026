#==============================================================================
# Make some figures comparing this product and the previous one.
#   Author: Michael Erb
#==============================================================================

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

plt.style.use('ggplot')
save_instead_of_plot = True


#%% LOAD DATA

output_dir = "C:/Users/erbm/Dropbox/Academia/AppState/Manuscripts/Submitted/2026_Erb_Marland_CDIAC/proofs/analysis/figures/"

# Load the national data
data_national_2022 = pd.read_excel('C:/Users/erbm/Documents/GitHub/CDIAC-Fossil-Fuels/output/Products/Past_Products/CDIAC_2022/nation.1750_2022.xlsx')
data_national_2021 = pd.read_excel('C:/Users/erbm/Documents/GitHub/CDIAC-Fossil-Fuels/output/Products/Past_Products/CDIAC_2021/nation.1751_2021.xlsx')

# Rename columns
data_national_2022 = data_national_2022.rename(columns={"Emissions from fossil fuels and cement production (thousand metric tons of C)":"Total"})
data_national_2021 = data_national_2021.rename(columns={"Total CO2 emissions from fossil-fuels and cement production (thousand metric tons of C)":"Total"})

# Open the country lookup file
dir_lookup = 'C:/Users/erbm/Documents/GitHub/CDIAC-Fossil-Fuels/data/Lookups/'
country_lookup = pd.read_excel(dir_lookup+'Country_Lookup.xlsx')
country_lookup = country_lookup[['Country_Name_Legacy','Country_ID','Alpha3_code']]


#%% CALCULATIONS

# Get totals for the year 2021
data_national_2022 = data_national_2022[data_national_2022['Year'] == 2021]
data_national_2022 = data_national_2022[['Nation','Nation ID','Total']]
data_national_2021 = data_national_2021[data_national_2021['Year'] == 2021]
data_national_2021 = data_national_2021[['Nation','Total']]

# Convert units from kt C to Mt C
data_national_2021['Total'] = data_national_2021['Total'] / 1000
data_national_2022['Total'] = data_national_2022['Total'] / 1000

# For the 2021 data, get the Nation IDs
data_national_2021 = pd.merge(data_national_2021, country_lookup, left_on="Nation", right_on="Country_Name_Legacy", how="left")
data_national_2021 = data_national_2021.rename(columns={"Total":"Total_2021",
                                                        "Country_ID":"Nation ID",
                                                        "Nation":"Nation_2021",
                                                        "Alpha3_code":"Code"})
data_national_2021 = data_national_2021[['Nation_2021','Nation ID','Code','Total_2021']]

# Put the data together
data_national_2022 = data_national_2022.rename(columns={"Total":"Total_2022"})
data_national_all = pd.merge(data_national_2021, data_national_2022, on="Nation ID", how="outer")
data_national_all = data_national_all[['Nation','Nation_2021','Nation ID','Code','Total_2021','Total_2022']]
data_national_all = data_national_all[data_national_all['Nation ID'] != 590]

# Print some output
print("Nations with data in 2021 only:")
print(data_national_all[data_national_all['Nation'].isnull()])
print("Nations with data in 2022 only:")
print(data_national_all[data_national_all['Nation_2021'].isnull()])

# Compute the difference
data_national_all = data_national_all.dropna()
data_national_all['Total_change'] = data_national_all['Total_2022'] - data_national_all['Total_2021']
data_national_all['Total_change_percent'] = (data_national_all['Total_change'] / data_national_all['Total_2021']) * 100

n_nations = len(data_national_all['Total_2021'])
value_max = max([max(data_national_all['Total_2021']),max(data_national_all['Total_2022'])])
value_max = 3200


#%% FIGURE 1

countries_to_label = ["TON","SHN","GNQ","MNG","MLI","KWT","QAT","SOM","CAF","SYR","TUN","PER","TKM","VEN","SGP","COL", \
                      "BGD","ARE","SAU","IRN","JPN","NGA","IRQ","TWN","KOR", \
                      "RUS","IND","USA","CHN"]

# Get info about the selected countries
nations_labeled = data_national_all[data_national_all["Code"].isin(countries_to_label)]

# Make a scatterplot
f,ax = plt.subplots(1,3,sharey=True,figsize=(18,6))

ax[0].scatter(data_national_all['Total_2021'],data_national_all['Total_change_percent'],25,zorder=2)
ax[0].set_xlim(-.1,30)
ax[0].tick_params(axis="both",labelsize=12)
ax[0].set_ylabel('Percent change, current product (%)',fontsize=13)

ax[1].scatter(data_national_all['Total_2021'],data_national_all['Total_change_percent'],25,zorder=2)
ax[1].tick_params(axis="both",labelsize=12)
ax[1].set_xlim(30,300)

ax[2].scatter(data_national_all['Total_2021'],data_national_all['Total_change_percent'],25,zorder=2)
ax[2].tick_params(axis="both",labelsize=12)
ax[2].set_xlim(300,3350)

for i in range(n_nations):
    nation_txt   = data_national_all['Code'].iloc[i]
    value_total  = data_national_all['Total_2021'].iloc[i]
    value_change = data_national_all['Total_change_percent'].iloc[i]
    if nation_txt in ["RUS","CAN","SAU","IDN","SHN","BGD","ARE"]:
        va = "top"
        vertical_adjust = -1.75
    else:
        va = "bottom"
        vertical_adjust = .75
    if nation_txt in countries_to_label:
        if data_national_all['Total_2021'].iloc[i] < 30:
            ax[0].text(value_total,value_change+vertical_adjust,nation_txt,va=va)
        elif data_national_all['Total_2021'].iloc[i] < 300:
            ax[1].text(value_total,value_change+vertical_adjust,nation_txt,va=va)
        else:
            ax[2].text(value_total,value_change+vertical_adjust,nation_txt,va=va)

for i in range(3):
    ax[i].axhline(y=0,linestyle='dashed',linewidth=1,color='gray',alpha=0.5)
    ax[i].set_ylim(-100,100)
    ax[i].set_xlabel('Emissions in 2021, previous product (Mt C)',fontsize=13)

plt.suptitle('2021 emissions in current and previous products',fontsize=18,y=0.96)
plt.subplots_adjust(top=0.9,wspace=.05)

if save_instead_of_plot:
    plt.savefig(output_dir+'fig1_scatter_values_2021_change_percent.png',dpi=300,format='png',bbox_inches='tight')
    plt.close()
else:
    plt.show()


#%% FIGURE 1

countries_to_label2 = ["MLI","GNQ","SHN","TON","ARE","CAN","KOR","SAU","IRN","JPN","TWN","NGA","IRQ","VEN","TKM","CAF","SOM"]  # "DEU","IDN"

# Make a scatterplot
f,ax = plt.subplots(1,2,sharey=True,figsize=(12,6))

ax[0].scatter(data_national_all['Total_2021'],data_national_all['Total_change_percent'],25,zorder=2)
ax[0].set_xlim(-1,325)
ax[0].set_ylabel('Percent change, current product (%)',fontsize=10)

ax[1].scatter(data_national_all['Total_2021'],data_national_all['Total_change_percent'],25,zorder=2)
ax[1].set_xlim(325,3350)

for i in range(n_nations):
    nation_txt   = data_national_all['Code'].iloc[i]
    value_total  = data_national_all['Total_2021'].iloc[i]
    value_change = data_national_all['Total_change_percent'].iloc[i]
    if nation_txt in ["RUS","CAN","SAU","IDN"]: va = "top"
    else: va = "bottom"
    if nation_txt in countries_to_label2:
        ax[0].text(value_total,value_change,nation_txt,va=va)
    if data_national_all['Total_2021'].iloc[i] > 325:
        ax[1].text(value_total,value_change,nation_txt,va=va)

for i in range(2):
    ax[i].axhline(y=0,linestyle='dashed',linewidth=1,color='gray',alpha=0.5)
    ax[i].set_ylim(-100,100)
    ax[i].set_xlabel('Emissions in 2021, previous product (Mt C)',fontsize=10)

plt.suptitle('2021 emissions in current and previous products',fontsize=14,y=0.96)
plt.subplots_adjust(top=0.9,wspace=.05)

if save_instead_of_plot:
    plt.savefig(output_dir+'fig1b_scatter_values_2021_change_percent.png',dpi=300,format='png',bbox_inches='tight')
    plt.close()
else:
    plt.show()



#%% FIGURE 1

# Make a scatterplot
f,ax = plt.subplots(1,2,figsize=(14,7))

ax[0].scatter(data_national_all['Total_2021'],data_national_all['Total_2022'],50,zorder=2)
ax[0].set_xlim(0,value_max); ax[0].set_ylim(0,value_max)
ax[0].add_patch(plt.Rectangle((0,0), 300, 300, edgecolor='gray', fill=False, linestyle="--"))  # (xy), width, height

ax[1].scatter(data_national_all['Total_2021'],data_national_all['Total_2022'],50,zorder=2)
ax[1].set_xlim(0,300); ax[1].set_ylim(0,300)

for i in range(2):
    ax[i].plot([0,value_max],[0,value_max], color='gray', linestyle="dashed",linewidth=1,alpha=0.5,zorder=1)
    ax[i].set_xlabel('Emissions in 2021, previous product (Mt C)')
    ax[i].set_ylabel('Emissions in 2021, current product (Mt C)')
    ax[i].set_box_aspect(1)

plt.suptitle('2021 emissions in current and previous products',fontsize=14,y=0.96)
plt.subplots_adjust(top=1)

if save_instead_of_plot:
    plt.savefig(output_dir+'fig1c_scatter_values_2021.png',dpi=300,format='png',bbox_inches='tight')
    plt.close()
else:
    plt.show()