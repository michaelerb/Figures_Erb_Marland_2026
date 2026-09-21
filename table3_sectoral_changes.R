#===============================================================================
# This script loads each of the primary datasets and prints some calculated
# values. This script supports calculations discussed throughout the paper.
#   Author: Michael Erb
#===============================================================================

library(tidyverse)
library(readxl)
library(writexl)

# LOAD DATA --------------------------------------------------------------------

data_dir   <- "C:/Users/erbm/Documents/GitHub/CDIAC-Fossil-Fuels/output/Products/Past_Products/CDIAC_2022/"
output_dir <- "C:/Users/erbm/Dropbox/Academia/AppState/Manuscripts/Submitted/2026_Erb_Marland_CDIAC/3rd_submission/analysis/figures/"

# Load datasets
data_sectoral <- read_excel(paste0(data_dir,"sectoral.1995_2022.xlsx"))
names(data_sectoral)[1] <- "Nation"

# CALCULATIONS -----------------------------------------------------------------

# Calculate changes between 1995 and 2022 for all sectors
data_sectoral_global_change <- data_sectoral %>% 
  filter(Year %in% c(1995,2022), Nation == 'Global') %>% 
  select(-c("Nation","Nation ID","Nation ISO")) %>% 
  pivot_longer(cols = !c('Year'), names_to='Sector', values_to='value') %>% 
  pivot_wider(names_from='Year') %>% 
  mutate(Change = `2022` - `1995`,
         Percent_change = ((`2022` - `1995`) / `1995`) * 100) %>% 
  mutate(Int_1995 = as.integer(round(`1995`/1000)),
         Int_2022 = as.integer(round(`2022`/1000)),
         Int_change = as.integer(round(Change/1000)),
         #Int_change2 = Int_2022 - Int_1995,
         Int_percent = as.integer(round(Percent_change))) %>% 
  select(-c(`1995`,`2022`,Change,Percent_change)) %>% 
  filter(!Sector %in% c('Total (Reference)','Transport','Difference (Reference - Sectoral)','Bunkered','Per Capita Total Emissions'))

# Write the data to a file
write_xlsx(data_sectoral_global_change, paste0(output_dir,'table3_sectoral_changes.xlsx'))
