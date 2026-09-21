#===============================================================================
# This script loads each of the primary datasets and prints some calculated
# values. This script supports calculations discussed throughout the paper.
#   Author: Michael Erb
#===============================================================================

library(tidyverse)
library(readxl)

# LOAD DATA --------------------------------------------------------------------

# Load datasets
data_dir <- "C:/Users/erbm/Documents/GitHub/CDIAC-Fossil-Fuels/output/Products/Past_Products/CDIAC_2022/"
data_total     <- read_excel(paste0(data_dir,"total.2022.xlsx"))
data_global    <- read_excel(paste0(data_dir,"global.1750_2022.xlsx"))
data_national  <- read_excel(paste0(data_dir,"nation.1750_2022.xlsx"))
data_sectoral  <- read_excel(paste0(data_dir,"sectoral.1995_2022.xlsx"))
country_lookup <- read_excel(paste0(data_dir,"Country_Lookup.xlsx"))

# PREPARE DATA -----------------------------------------------------------------

# Make column names easier to use
names(data_total) <- c("Nation","Nation_ID","Nation_ISO","Year","Total")
names(data_global) <- c("Year","Total","Solid","Liquid","Gas","Cement","Flaring","PerCapita","Bunker","AviationBunker")
names(data_national) <- c("Nation","Nation_ID","Nation_ISO","Year","Total","Solid","Liquid","Gas","Cement","Flaring","PerCapita","Bunker","AviationBunker")
names(data_sectoral) <- c("Nation","Nation_ID","Nation_ISO","Year","TotalRef","TotalSec",
                          "Diff","Electric","OwnUse","NonEnergy",
                          "Manufacturing","Transport","RoadTransport","RailTransport",
                          "Aviation","Navigation","OtherTrans","PipelineTrans","Household",
                          "Agriculture","Commerce","OtherConsump","Losses","Bunker",
                          "MarineBunker","AviationBunker","Flaring","Cement",
                          "PerCapita")

# SECTION 3: GLOBAL AND NATIONAL TOTALS AND TRENDS -----------------------------

# Print percent changes in total emissions between years
data_global_2022 <- data_global %>% 
  filter(Year == 2022)
data_global_2021 <- data_global %>% 
  filter(Year == 2021)
data_global_2020 <- data_global %>% 
  filter(Year == 2020)
data_global_2019 <- data_global %>% 
  filter(Year == 2019)
message('Global CO2 emissions in 2022: ',data_global_2022$Total)
message('Percent change, 2022 compared to 2021: ',round(((data_global_2022$Total - data_global_2021$Total) / data_global_2021$Total) * 100, digits=2),' %')
message('Percent change, 2022 compared to 2019: ',round(((data_global_2022$Total - data_global_2019$Total) / data_global_2019$Total) * 100, digits=2),' %')

# Totals and the sum of nations
data_sectoral_global_2022 <- data_sectoral %>% 
  filter(Year == 2022, Nation == 'Global')
data_national_2022 <- data_national %>% 
  filter(Year == 2022)
data_sectoral_2022 <- data_sectoral %>% 
  filter(Year == 2022,
         !Nation %in% c('Global','Africa','Asia','Europe','North America','Oceania','South America','Annex I','Non-Annex I')) # NOTE: For older years, remove Antarctica too.
message('Carbon emissions in 2022 (reference, global): ',data_sectoral_global_2022$TotalRef)
message('Carbon emissions in 2022 (sectoral, global):  ',data_sectoral_global_2022$TotalSec)
message('Carbon emissions in 2022 (reference, sum of nations): ',sum(data_national_2022$Total))
message('Carbon emissions in 2022 (sectoral, sum of nations):  ',sum(data_sectoral_2022$TotalSec))
message('Carbon emissions in 2022 (reference, global - nations): ',data_sectoral_global_2022$TotalRef - sum(data_national_2022$Total))
message('Carbon emissions in 2022 (sectoral, global - nations):  ',data_sectoral_global_2022$TotalSec - sum(data_sectoral_2022$TotalSec))

# Total drop during COVID
message('Percent change, 2020 compared to 2019: ',round(((data_global_2020$Total - data_global_2019$Total) / data_global_2019$Total) * 100, digits=2),' %')

# SECTION 4: SECTORAL DATA -----------------------------------------------------

# Print changes in sectoral vs reference total for every nation
data_sectoral_change <- data_sectoral %>% 
  filter(Year == 2022) %>% 
  select(Nation,TotalRef,TotalSec) %>% 
  mutate(Sec_over_ref = (TotalSec / TotalRef) * 100) %>% 
  mutate(Percent_reduction = 100 - Sec_over_ref)

data_sectoral_change_selected <- data_sectoral_change %>% 
  filter(Nation %in% c('China','Argentina','Sweden','Russian Federation','United States','Switzerland-Liechtenstein','Austria'))
print(data_sectoral_change_selected)

data_sectoral_change_allyears <- data_sectoral %>% 
  select(Nation,TotalRef,TotalSec) %>% 
  mutate(Sec_over_ref = (TotalSec / TotalRef) * 100) %>% 
  mutate(Percent_reduction = 100 - Sec_over_ref) %>% 
  filter(Nation %in% c('Greece','Australia','Brazil','United States','Albania','Somolia'))

# Percent of global emissions resulting from different sectors
message('Percent of global emissions resulting from specific sectors:')
message('Electricity and heat: ',             round((data_sectoral_global_2022$Electric / data_sectoral_global_2022$TotalSec) * 100, digits=1),' %')
message('Road transport: ',                   round((data_sectoral_global_2022$RoadTransport / data_sectoral_global_2022$TotalSec) * 100, digits=1),' %')
message('Manufacturing, construction, etc.: ',round((data_sectoral_global_2022$Manufacturing / data_sectoral_global_2022$TotalSec) * 100, digits=1),' %')

# Calculate changes between 1995 and 2022 for all sectors
data_sectoral_global_change <- data_sectoral %>% 
  filter(Year %in% c(1995,2022), Nation == 'Global') %>% 
  select(-c("Nation","Nation_ID","Nation_ISO")) %>% 
  pivot_longer(cols = !c('Year'), names_to='Sector', values_to='value') %>% 
  pivot_wider(names_from='Year') %>% 
  mutate(Change = (`2022` - `1995`) / 1000,
         Percent_change = ((`2022` - `1995`) / `1995`) * 100) %>% 
  filter(!Sector %in% c('TotalRef','TotalSec','Diff','PerCapita')) %>% 
  arrange(desc(Change))

View(data_sectoral_global_change)

# Calculate road transport in different nations
sectoral_total_road <- data_sectoral %>% 
  filter(Nation %in% c('United States','India'), Year == 2022) %>% 
  select(Nation,TotalSec,RoadTransport) %>% 
  mutate(percent = (RoadTransport / TotalSec) * 100)
message('Percent of road transport:')
print(sectoral_total_road)

sectoral_total_manufacturing <- data_sectoral %>% 
  filter(Nation %in% c('United States','India'), Year == 2022) %>% 
  select(Nation,TotalSec,Manufacturing) %>% 
  mutate(percent = (Manufacturing / TotalSec) * 100)
message('Percent of manufacturing:')
print(sectoral_total_manufacturing)

# Percent of emissions resulting from different sectors for specific countries
data_sectoral_2022_qatar <- data_sectoral %>% 
  filter(Year == 2022, Nation == 'Qatar')
data_sectoral_2022_drcongo <- data_sectoral %>% 
  filter(Year == 2022, Nation == 'Democratic Republic of the Congo')
data_sectoral_2022_uk <- data_sectoral %>% 
  filter(Year == 2022, Nation == 'United Kingdom')
message('Per capita, Qatar: ',   round(data_sectoral_2022_qatar$PerCapita, digits=3))
message('Per capita, DR Congo: ',round(data_sectoral_2022_drcongo$PerCapita, digits=3))
message('Percentage household, Qatar: ',   round((data_sectoral_2022_qatar$Household / data_sectoral_2022_qatar$TotalSec) * 100, digits=2),' %')
message('Percentage household, DR Congo: ',round((data_sectoral_2022_drcongo$Household / data_sectoral_2022_drcongo$TotalSec) * 100, digits=2),' %')
message('Percentage household, UK: ',      round((data_sectoral_2022_uk$Household / data_sectoral_2022_uk$TotalSec) * 100, digits=2),' %')

# For post-Soviet national emissions, see "values_trends_in_former_soviet_nations.py"

# SUPPLEMENT -------------------------------------------------------------------

# Calculate the percentage of U.S. emissions that are from non-energy usage
data_sectoral_2022_US <- data_sectoral_2022 %>% 
  filter(Nation == 'United States')
message('Percentage household, U.S.: ',round((data_sectoral_2022_US$NonEnergy / data_sectoral_2022_US$TotalSec) * 100, digits=2),' %')

# MORE -------------------------------------------------------------------------

# Comparison of methods
message('Difference ((sec - ref)/ref):',      (data_sectoral_global_2022$TotalSec - data_sectoral_global_2022$TotalSec) / data_sectoral_global_2022$TotalRef)
message('Carbon emissions in 2022 (bunkers):',data_sectoral_global_2022$Bunker)


