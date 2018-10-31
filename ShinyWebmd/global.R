library(dplyr)
library(plotly)
library(shiny)

webmd_alldrugs <- read.csv("webmd_drugs.csv")

webmd_alldrugs['comment'] = NULL
#webmd_alldrugs['drug'] = tolower(webmd_alldrugs['drug'])
#webmd_alldrugs['condition'] = tolower(webmd_alldrugs['condition'])

drugs_easeOfUse = webmd_alldrugs %>%
  group_by(., drug, easeOfUse) %>%
  summarise(., count = n())
drugs_effectiveness = webmd_alldrugs %>%
  group_by(., drug, effectiveness) %>%
  summarise(., count = n())
drugs_satisfaction = webmd_alldrugs %>%
  group_by(., drug, satisfaction) %>%
  summarise(., count = n())
