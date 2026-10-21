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

category_to_plot = 'total'
#category_to_plot = 'solid fuels'
#category_to_plot = 'liquid fuels'
#category_to_plot = 'gas fuels'
#category_to_plot = 'cement production'
#category_to_plot = 'gas flaring'
#category_to_plot = 'bunker'

if category_to_plot == 'total': extra_txt = ''
else: extra_txt = ' - '+category_to_plot


#%% LOAD DATA

data_dir   = "C:/Users/erbm/Documents/GitHub/CDIAC-Fossil-Fuels/output/Products/Past_Products/CDIAC_2022/"
output_dir = "C:/Users/erbm/Dropbox/Academia/AppState/Manuscripts/Submitted/2026_Erb_Marland_CDIAC/proofs/analysis/figures/"

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

# Open the country lookup file
dir_lookup = 'C:/Users/erbm/Documents/GitHub/CDIAC-Fossil-Fuels/data/Lookups/'
country_lookup = pd.read_excel(dir_lookup+'Country_Lookup.xlsx')

# Replace some country names
data_national.loc[data_national['Nation'] == 'Union of Soviet Socialist Republics [former]', 'Nation']   = 'USSR'
data_national.loc[data_national['Nation'] == 'Republic of Moldova', 'Nation']                            = 'Moldova'
data_national.loc[data_national['Nation'] == 'Russian Federation', 'Nation']                             = 'Russia'
data_national.loc[data_national['Nation'] == 'German Democratic Republic [former]', 'Nation']            = 'German Democratic Republic (East)'
data_national.loc[data_national['Nation'] == 'Germany, Federal Republic of', 'Nation']                   = 'Federal Republic of Germany (West)'
data_national.loc[data_national['Nation'] == 'Yugoslavia [former Socialist Federal Republic]', 'Nation'] = 'Yugoslavia'
data_national.loc[data_national['Nation'] == 'The former Yugoslav Republic of Macedonia', 'Nation']      = 'North Macedonia'
country_lookup.loc[country_lookup['Country_Name'] == 'Union of Soviet Socialist Republics [former]', 'Country_Name']   = 'USSR'
country_lookup.loc[country_lookup['Country_Name'] == 'Republic of Moldova', 'Country_Name']                            = 'Moldova'
country_lookup.loc[country_lookup['Country_Name'] == 'Russian Federation', 'Country_Name']                             = 'Russia'
country_lookup.loc[country_lookup['Country_Name'] == 'German Democratic Republic [former]', 'Country_Name']            = 'German Democratic Republic (East)'
country_lookup.loc[country_lookup['Country_Name'] == 'Germany, Federal Republic of', 'Country_Name']                   = 'Federal Republic of Germany (West)'
country_lookup.loc[country_lookup['Country_Name'] == 'Yugoslavia [former Socialist Federal Republic]', 'Country_Name'] = 'Yugoslavia'
country_lookup.loc[country_lookup['Country_Name'] == 'The former Yugoslav Republic of Macedonia', 'Country_Name']      = 'North Macedonia'


#%% SETUP

keys_national = ['total','solid fuels','liquid fuels','gas fuels','cement production','gas flaring','bunker']

# Set things up
years_all   = np.arange(min(data_national['Year']),max(data_national['Year'])+1)
nations_all = np.unique(data_national['Nation'])
n_years   = len(years_all)
n_nations = len(nations_all)
national_total_all = np.zeros((n_nations,n_years)); national_total_all[:] = np.nan


#%% REFORMAT NATIONAL TOTALS INTO A SINGLE ARRAY

# Rearrange data
i=0; nation_txt = nations_all[i]
for i,nation_txt in enumerate(nations_all):
    nation_year  = np.array(data_national['Year'].loc[data_national['Nation'] == nation_txt])
    nation_total = np.array(data_national[category_to_plot].loc[data_national['Nation'] == nation_txt])
    ind_years = np.where(np.isin(years_all,nation_year))[0]
    national_total_all[i,ind_years] = nation_total
    #
    country_lookup.loc[country_lookup['Country_Name'] == nation_txt, 'Earliest'] = min(nation_year)
    country_lookup.loc[country_lookup['Country_Name'] == nation_txt, 'Latest']   = max(nation_year)

# Sort the countries by their earliest year
country_lookup = country_lookup.sort_values(['Earliest','Latest','Country_Name'], ascending=[True, False, True])  #TODO: Work on this sort
country_lookup = country_lookup.reset_index()

# Collections
collections_all = pd.unique(country_lookup['Collection'])
collections = [text for text in collections_all if str(text) != 'nan']


#%% SPECIFY ORDER OF COUNTRIES

# Specify the order to plot countries, to improve the plots.
order_countries = {}
order_countries["Soviet Union"] = ['USSR',
                                   'Armenia',
                                   'Azerbaijan',
                                   'Belarus',
                                   'Estonia',
                                   'Georgia',
                                   'Kazakhstan',
                                   'Kyrgyzstan',
                                   'Latvia',
                                   'Lithuania',
                                   'Moldova',
                                   'Russia',
                                   'Tajikistan',
                                   'Turkmenistan',
                                   'Ukraine',
                                   'Uzbekistan']
order_countries["Germany"] = ['Germany',
                              'German Democratic Republic (East)',
                              'Federal Republic of Germany (West)']
order_countries["Yugoslavia"] = ['Yugoslavia',
                                 'Croatia',
                                 'North Macedonia',
                                 'Slovenia',
                                 'Bosnia and Herzegovina',
                                 'Kosovo',
                                 'Serbia and Montenegro',
                                 'Montenegro',
                                 'Serbia']


#%% FIGURE - COMBINED

colormap_selected = plt.cm.tab20
colors = colormap_selected(np.linspace(0,1,18))
letters = ['a','b','c']

# Make figure
f,ax = plt.subplots(3,1,sharex=True,figsize=(10,9))
ax = ax.ravel()

num,collection_selected = 1,'Soviet Union'
for num,collection_selected in enumerate(['Germany','Soviet Union','Yugoslavia']):
    #
    # Get countries in collection
    if collection_selected in list(order_countries.keys()):
        countries_in_region = order_countries[collection_selected]
    else:
        ind_in_region = np.where(country_lookup['Collection_for_website'] == collection_selected)[0]
        countries_in_region = country_lookup.loc[ind_in_region]["Country_Name"]
    n_nations_selected = len(countries_in_region)
    data_in_collection = np.zeros((n_nations_selected,n_years)); data_in_collection[:] = np.nan
    #
    # Get data for nation
    for i,country_txt in enumerate(countries_in_region):
        ind_data = np.where(nations_all == country_txt)[0]
        data_in_collection[i,:] = national_total_all[ind_data,:]
    #
    bool_isnan = np.isnan(data_in_collection)
    if sum(bool_isnan.flatten()) > 0:
        data_in_collection[bool_isnan] = 0
    #
    for i in range(n_nations_selected):
        if i == 0:
            ax[num].bar(years_all,data_in_collection[i,:]/1000,bottom=0,width=1,color=colors[i],label=list(countries_in_region)[i])
        else:
            sum_of_previous = np.nansum(data_in_collection[:i,:],axis=0)
            ax[num].bar(years_all,data_in_collection[i,:]/1000,bottom=sum_of_previous/1000,width=1,color=colors[i],label=list(countries_in_region)[i])
    #
    #ax[num].legend(loc='center left',ncol=1,fontsize=8,bbox_to_anchor=[1,.5])
    if collection_selected == 'Soviet Union': ax[num].legend(loc='upper left',fontsize=9,ncol=2)
    else: ax[num].legend(loc='upper left',fontsize=9)
    if collection_selected == 'Yugoslavia': ax[num].set_ylim(0,37)
    ax[num].set_xlim(1899.5,2022.5)
    ax[num].set_ylabel('Emissions (Mt C)')
    ax[num].set_title('('+letters[num]+') '+collection_selected+extra_txt,fontsize=14,loc='left')

ax[2].set_xlabel('Year')
if save_instead_of_plot:
    plt.savefig(output_dir+'fig7_collections_'+category_to_plot.replace(' ','_')+'.png',dpi=300,format='png',bbox_inches='tight')
    plt.close()
else:
    plt.show()


#%% VALUES FOR THE USSR

countries_in_region = order_countries['Soviet Union']
n_nations_selected = len(countries_in_region)
data_in_collection = np.zeros((n_nations_selected,n_years)); data_in_collection[:] = np.nan

# Get data for nation
for i,country_txt in enumerate(countries_in_region):
    ind_data = np.where(nations_all == country_txt)[0]
    data_in_collection[i,:] = national_total_all[ind_data,:]

total_for_countries = np.nansum(data_in_collection,axis=0)
ind_before_breakup = np.where((years_all <= 1991))[0]
ind_after_breakup  = np.where((years_all >  1991))[0]

max_before = np.nanmax(total_for_countries[ind_before_breakup])
min_after  = np.nanmin(total_for_countries[ind_after_breakup])
print('USSR:')
print('Max before breakup',max_before)
print('Min after breakup', min_after)
print('Fraction min over max:',min_after/max_before)


#%% MAKE STACKPLOT OF TOTALS - NATIONAL

"""
# Make a time series
collection_selected = 'Soviet Union'
#collection_selected = 'Yugoslavia'
def make_stackplot(collection_selected):
    #
    #%%
    # Get countries in collection
    if collection_selected in list(order_countries.keys()):
        countries_in_region = order_countries[collection_selected]
    else:
        ind_in_region = np.where(country_lookup['Collection_for_website'] == collection_selected)[0]
        countries_in_region = country_lookup.loc[ind_in_region]["Country_Name"]
    n_nations_selected = len(countries_in_region)
    data_in_collection = np.zeros((n_nations_selected,n_years)); data_in_collection[:] = np.nan
    #
    # Get data for nation
    for i,country_txt in enumerate(countries_in_region):
        ind_data = np.where(nations_all == country_txt)[0]
        data_in_collection[i,:] = national_total_all[ind_data,:]
    #
    bool_isnan = np.isnan(data_in_collection)
    if sum(bool_isnan.flatten()) > 0:
        data_in_collection[bool_isnan] = 0
    #
    # Make figure
    plt.figure(figsize=(10,3))
    ax1 = plt.subplot2grid((1,1),(0,0))
    #
    for i in range(n_nations_selected):
        if i == 0:
            ax1.bar(years_all,data_in_collection[i,:]/1000,bottom=0,width=1,color=colors[i],label=list(countries_in_region)[i])
        else:
            sum_of_previous = np.nansum(data_in_collection[:i,:],axis=0)
            ax1.bar(years_all,data_in_collection[i,:]/1000,bottom=sum_of_previous/1000,width=1,color=colors[i],label=list(countries_in_region)[i])
    #
    #ax1.legend(loc='center left',ncol=1,fontsize=8,bbox_to_anchor=[1,.5])
    if collection_selected == 'Soviet Union': ax1.legend(loc='upper left',fontsize=10,ncol=2)
    else: ax1.legend(loc='upper left',fontsize=10)
    if collection_selected == 'Yugoslavia': ax1.set_ylim(0,37)
    ax1.set_xlim(1899.5,2022.5)
    ax1.set_ylabel('Emissions (Mt C)')
    ax1.set_xlabel('Year')
    ax1.set_title(collection_selected+extra_txt,fontsize=14,loc='left')
    #
    if save_instead_of_plot:
        plt.savefig(output_dir+'figZ_7_collection_'+category_to_plot.replace(' ','_')+'_'+collection_selected.replace(' ','_')+'.png',dpi=300,format='png',bbox_inches='tight')
        plt.close()
    else:
        plt.show()


#%% MAKE A FIGURE FOR EACH COLLECTION

collections_to_plot = ['Germany',
                       'Soviet Union',
                       'Yugoslavia']  # 'Czechoslovakia','Pakistan','Rhodesia-Nyasaland','Sudan',

for collection_selected in collections:
#for collection_selected in collections_to_plot:
    make_stackplot(collection_selected)
"""