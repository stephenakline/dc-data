# ----------------------------------------------------------------------------------------------------- #
# Purpose: Load in DC block centroid data, and filter to only keep centroids with a population
#          greater than zero, and then output.
# ----------------------------------------------------------------------------------------------------- #

rm(list = ls())
DIR = paste0(getwd(), "/grocery-store")
DATA_DIR = paste0(getwd(), "/data")

# libaries
library(dplyr)
library(ggplot2)
library(maptools)
library(rgdal)
library(geosphere)
library(stringr)

# load in block centroid data
all_centroid = read.table(paste0(DATA_DIR, "/tigerline/dc-block-population-centroid.txt"), header = TRUE, sep = "\t")

# reshape data, filter to only keep blocks with people in it
centroid = all_centroid %>%
  mutate(COUNTYFP10 = str_pad(as.character(COUNTYFP10), width=3, pad="0"),
         TRACTCE10 = str_pad(as.character(TRACTCE10), width=6, pad="0"),
         GEOID10 = paste0(STATEFP10, COUNTYFP10, TRACTCE10, BLOCKCE10)) %>%
  filter(P0010001 > 0) %>% # census block must have a population
  select(GEOID10, X, Y) %>%
  rename(longitude = X, latitude = Y)

# save results in groups of 1500 (due to GoogleMaps API limits)
centroid_1 = centroid[1:1455, ]
centroid_2 = centroid[1456:2911, ]
centroid_3 = centroid[2911:4364, ]

write.csv(centroid_1, file = paste0(DIR, "/inter/block-centroid-with-pops-1.csv"), row.names = FALSE)
write.csv(centroid_2, file = paste0(DIR, "/inter/block-centroid-with-pops-2.csv"), row.names = FALSE)
write.csv(centroid_3, file = paste0(DIR, "/inter/block-centroid-with-pops-3.csv"), row.names = FALSE)
