#==============================================================================
# Plot historical CDIAC emissions.
#   Author: Michael Erb
#==============================================================================

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

plt.style.use('ggplot')
save_instead_of_plot = True


#%% LOAD DATA

output_dir = "C:/Users/erbm/Dropbox/Academia/AppState/Manuscripts/Submitted/2026_Erb_Marland_CDIAC/3rd_submission/analysis/figures/"

data_dir1 = 'C:/Users/erbm/Documents/GitHub/CDIAC-Fossil-Fuels/output/Products/Past_Products/CDIAC_2022/'
data_dir2 = 'C:/Users/erbm/Documents/GitHub/CDIAC-Fossil-Fuels/data/Products/'
data_dir3 = 'C:/Users/erbm/Dropbox/Academia/AppState/Project_CDIAC/code_and_data_archive/data_ess_dive/data/CSV-FILES/CSV-FILES/'

# Load the global data
data_global_2022 = pd.read_excel(data_dir1+'global.1750_2022.xlsx')
data_global_2021 = pd.read_excel(data_dir2+'/2021_Global_Data_Product.xlsx')
data_global_2020 = pd.read_excel(data_dir2+'/2020_Global_Data_Product.xlsx')
data_global_2019 = pd.read_excel(data_dir2+'/2019_Global_Data_Product.xlsx')
data_global_2018 = pd.read_excel(data_dir2+'/2018_Global_Data_Product.xlsx')
data_global_2017 = pd.read_excel(data_dir2+'/2017_Global_Data_Product.xlsx')
data_global_2016 = pd.read_excel(data_dir2+'/2016_Global_Data_Product.xlsx')
data_global_2015 = pd.read_excel(data_dir2+'/2015_Global_Data_Product.xlsx')
data_global_2014 = pd.read_csv(data_dir3+'global.1751_2014.csv',skiprows=[1])
data_global_2013 = pd.read_csv(data_dir3+'global.1751_2013.csv',skiprows=[1])
data_global_2011 = pd.read_csv(data_dir3+'global.1751_2011.csv',skiprows=[1])
data_global_2010 = pd.read_csv(data_dir3+'global.1751_2010.csv',skiprows=[1])
data_global_2009 = pd.read_csv(data_dir3+'global.1751_2009.csv',skiprows=[1])
data_global_2008 = pd.read_csv(data_dir3+'global.1751_2008.csv',skiprows=[1])


#%% RENAME COLUMNS

# Rename the total column - global data
data_global_2022 = data_global_2022.rename(columns={"Emissions from fossil fuels and cement production (million metric tons of C)":"Total"})
data_global_2021 = data_global_2021.rename(columns={"Total carbon emissions from fossil fuel consumption and cement production (million metric tons of C)":"Total"})
data_global_2020 = data_global_2020.rename(columns={"Total carbon emissions from fossil fuel consumption and cement production (million metric tons of C)":"Total"})
data_global_2019 = data_global_2019.rename(columns={"Total carbon emissions from fossil fuel consumption and cement production (million metric tons of C)":"Total"})
data_global_2018 = data_global_2018.rename(columns={"Total carbon emissions from fossil fuel consumption and cement production (million metric tons of C)":"Total"})
data_global_2017 = data_global_2017.rename(columns={"Total carbon emissions from fossil fuel consumption and cement production (million metric tons of C)":"Total"})
data_global_2016 = data_global_2016.rename(columns={"Total carbon emissions from fossil fuel consumption and cement production (million metric tons of C)":"Total"})
data_global_2015 = data_global_2015.rename(columns={"Total carbon emissions from fossil fuel consumption and cement production (million metric tons of C)":"Total"})
data_global_2014 = data_global_2014.rename(columns={"Total carbon emissions from fossil fuel consumption and cement production (million metric tons of C)":"Total"})
data_global_2013 = data_global_2013.rename(columns={"Total carbon emissions from fossil fuel consumption and cement production (million metric tons of C)":"Total"})
data_global_2011 = data_global_2011.rename(columns={"Total carbon emissions from fossil fuel consumption and cement production (million metric tons of C)":"Total"})
data_global_2010 = data_global_2010.rename(columns={"Total carbon emissions from fossil fuel consumption and cement production (million metric tons of C)":"Total"})
data_global_2009 = data_global_2009.rename(columns={"Total carbon emissions from fossil-fuels (million metric tons of C)":"Total"})
data_global_2008 = data_global_2008.rename(columns={"Total carbon emissions from fossil-fuels (million metric tons of C)":"Total",
                                                    'Year"':"Year"})

# Remove the first year from the 2022 dataset
data_global_2022 = data_global_2022.iloc[1:].reset_index(drop=True)

#%% TIME SERIES - GLOBAL TOTAL

# Color scale for regions
colormap_selected1 = plt.cm.tab20
colors = colormap_selected1(np.linspace(0,1,20))

plt.figure(figsize=(10,5))
ax1 = plt.subplot2grid((1,1),(0,0))

ax1.plot(data_global_2022['Year'],data_global_2022['Total'],label='2022',c='k')
ax1.plot(data_global_2021['Year'],data_global_2021['Total'],label='2021',c=colors[0,:])
ax1.plot(data_global_2020['Year'],data_global_2020['Total'],label='2020',c=colors[1,:])
ax1.plot(data_global_2019['Year'],data_global_2019['Total'],label='2019',c=colors[2,:])
ax1.plot(data_global_2018['Year'],data_global_2018['Total'],label='2018',c=colors[3,:])
ax1.plot(data_global_2017['Year'],data_global_2017['Total'],label='2017',c=colors[4,:])
ax1.plot(data_global_2016['Year'],data_global_2016['Total'],label='2016',c=colors[5,:])
ax1.plot(data_global_2015['Year'],data_global_2015['Total'],label='2015',c=colors[6,:])
ax1.plot(data_global_2014['Year'],data_global_2014['Total'],label='2014',c=colors[7,:])
ax1.plot(data_global_2013['Year'],data_global_2013['Total'],label='2013',c=colors[8,:])
ax1.plot(data_global_2011['Year'],data_global_2011['Total'],label='2011',c=colors[9,:])
ax1.plot(data_global_2010['Year'],data_global_2010['Total'],label='2010',c=colors[10,:])
ax1.plot(data_global_2009['Year'],data_global_2009['Total'],label='2009',c=colors[11,:])
ax1.plot(data_global_2008['Year'],data_global_2008['Total'],label='2008',c=colors[12,:])
ax1.legend(loc='upper left',ncol=2)
ax1.set_ylabel('Emissions (Mt C)')
ax1.set_xlabel('Year')
ax1.set_title('Global carbon emissions for each release',fontsize=14)
#ax1.set_xlim([1950,2022])
ax1.set_xlim([1950,2022.5])
ax1.set_ylim([0,11000])

if save_instead_of_plot:
    plt.savefig(output_dir+'fig8_historical_comparison_global_totals.png',dpi=300,format='png',bbox_inches='tight')
    plt.close()
else:
    plt.show()


#%% TIME SERIES - GLOBAL DIFF

plt.figure(figsize=(10,5))
ax1 = plt.subplot2grid((1,1),(0,0))

ax1.plot(data_global_2021['Year'],data_global_2022['Total'][:-1] - data_global_2021['Total'],label='2022 - 2021',c='k')
ax1.plot(data_global_2020['Year'],data_global_2021['Total'][:-1] - data_global_2020['Total'],label='2021 - 2020',c=colors[0,:])
ax1.plot(data_global_2019['Year'],data_global_2020['Total'][:-1] - data_global_2019['Total'],label='2020 - 2019',c=colors[1,:])
ax1.plot(data_global_2018['Year'],data_global_2019['Total'][:-1] - data_global_2018['Total'],label='2019 - 2018',c=colors[2,:])
ax1.plot(data_global_2017['Year'],data_global_2018['Total'][:-1] - data_global_2017['Total'],label='2018 - 2017',c=colors[3,:])
ax1.plot(data_global_2016['Year'],data_global_2017['Total'][:-1] - data_global_2016['Total'],label='2017 - 2016',c=colors[4,:])
ax1.plot(data_global_2015['Year'],data_global_2016['Total'][:-1] - data_global_2015['Total'],label='2016 - 2015',c=colors[5,:])
ax1.plot(data_global_2014['Year'],data_global_2015['Total'][:-1] - data_global_2014['Total'],label='2015 - 2014',c=colors[6,:])
ax1.plot(data_global_2013['Year'],data_global_2014['Total'][:-1] - data_global_2013['Total'],label='2014 - 2013',c=colors[7,:])
ax1.plot(data_global_2011['Year'],data_global_2013['Total'][:-2] - data_global_2011['Total'],label='2013 - 2011',c=colors[8,:])
ax1.plot(data_global_2010['Year'],data_global_2011['Total'][:-1] - data_global_2010['Total'],label='2011 - 2010',c=colors[9,:])
ax1.plot(data_global_2009['Year'],data_global_2010['Total'][:-1] - data_global_2009['Total'],label='2010 - 2009',c=colors[10,:])
ax1.plot(data_global_2008['Year'],data_global_2009['Total'][:-1] - data_global_2008['Total'],label='2009 - 2008',c=colors[11,:])

ax1.legend(loc='lower left',ncol=2)
ax1.set_ylabel('Emissions (Mt C)')
ax1.set_xlabel('Year')
ax1.set_title('Global carbon emissions - differences between each release',fontsize=14)
ax1.set_xlim([1950,2022])
#ax1.set_xlim([1950,2022.5])

if save_instead_of_plot:
    plt.savefig(output_dir+'fig8b_historical_comparison_global_totals_diff.png',dpi=300,format='png',bbox_inches='tight')
    plt.close()
else:
    plt.show()
