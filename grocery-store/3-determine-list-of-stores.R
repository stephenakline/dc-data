# ----------------------------------------------------------------------------------------------------- #
# Purpose: [------]
# ----------------------------------------------------------------------------------------------------- #

rm(list = ls())
DIR = getwd()

# libaries
library(dplyr)
library(tidyr)
library(stringr)

# options to clean up printing
options(digits=11)

# load in store data
files = list.files(paste0(DIR, "/inter/")) 
files_to_load = subset(files, grepl("^stores", files)) # only keep files that start with 'stores'

store_data = data.frame()
for(i in files_to_load) {
  temp = read.csv(paste0(DIR, "/inter/", i), stringsAsFactors = FALSE)
  store_data = rbind(store_data, temp)
}
rm(temp)

# clean up data
store_data = store_data %>% select(-X)

# reshape data --> http://stackoverflow.com/questions/25925556/gather-multiple-sets-of-columns-with-tidyr
store_wide = store_data[, 1:8] %>% gather(key, value, storename.0:storevicinity.0) %>%
# store_wide = store_data %>% gather(key, value, storename.0:storevicinity.2) %>%
  separate(key, c("feature", "id")) %>%
  arrange(GEOID10) 
  # spread(id, value)

# get list of unique stores
unique_store_ids = store_wide %>% filter(feature == "storeid") %>% select(value) %>% distinct()
list_store_names = store_wide %>% filter(feature == "storename") %>% select(GEOID10, id, value) %>% distinct()

list_stores_by_id = left_join(unique_store_ids, store_wide, by = "value") %>% rename(store_id = value) %>% select(-feature)
list_stores = left_join(list_stores_by_id, list_store_names, by = c("GEOID10", "id")) %>% rename(store_name = value)

# get count of appearnce by store
counts_of_stores = list_stores %>% group_by(store_name) %>% summarise(count = n())
print(paste0('the unique number of stores is: ', nrow(counts_of_stores)))
