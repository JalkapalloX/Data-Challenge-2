# LOADING PACKAGES
if (!require("tidyverse")) install.packages("tidyverse")
library(tidyverse)
if (!require("data.table")) install.packages("data.table")
library(data.table)

# SET WORKING DIRECTORY TO FILE DIRECTORY (RSTUDIO ONLY)
# You may need to install the lastest version of the rstudioapi.
setwd(dirname(rstudioapi::getActiveDocumentContext()$path))

# PREPROCESSING

data <- read.csv("original dataset/DataChallenge2019_GreenhouseGroup_Bidding_Algorithms_Tests.csv", sep=";")

data$advertiser_id <- factor(data$advertiser_id)
data$campaign_group_id <- factor(data$campaign_group_id)
data$campaign_id <- factor(data$campaign_id)
data$start_date <- as.Date(data$start_date)
data$end_date <- as.Date(data$end_date)

### Weird empty lines in the middle of the data frame.
data <- data[!is.na(data$advertiser_id),]

data2 <- data
data2$small_per_impression <- data$creative_size_small / data$impressions
data2$medium_per_impression <- data$creative_size_medium / data$impressions
data2$large_per_impression <- data$creative_size_large / data$impressions
data2$inview_per_impression <- data$impressions_inview / data$impressions
data2$abovefold_per_impression <- data$impressions_above_fold / data$impressions
data2$clicks_per_impression <- data$clicks / data$impressions

data2$conv_per_inview <- data$post_view_conv / data$impressions_inview

data2$conv_per_click <- data$post_click_conv / data$clicks

data2$UU_inview_per_UU_impression <- data$unique_user_inview / data$unique_user_impressions
data2$UU_click_per_UU_impression <- data$unique_user_is_click / data$unique_user_impressions

data2$UU_conv_per_UU_inview <- data$unique_user_post_view_conv / data$unique_user_inview

data2$UU_conv_per_UU_click <- data$unique_user_post_click_conv / data$unique_user_is_click

# EXPLORING DATA

# two-sample t-test:
data_ttest <- na.omit(dcast(data2, campaign_group_id+device_type+operating_system~test_group, fun=mean, value.var=c("UU_conv_per_UU_click")))
data_ttest$increase <- data_ttest$B - data_ttest$A
