# LOADING PACKAGES
if (!require("tidyverse")) install.packages("tidyverse")
library(tidyverse)

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

# CORRELATING BUYER BID WITH OUTCOMES
cor(data$buyer_bid, data[,colnames(data)[18:ncol(data)]], use = "pairwise")

### Clicks and unique_user_is_click correlate best and about as much

buyer_bid_est <- lm(buyer_bid ~ clicks + post_click_conv + post_view_conv + unique_user_impressions +
                  unique_user_inview + unique_user_is_click, data = data)

### However, those two variables are not considered to have a significant effect here. (Be aware of collinearity, though.)

data$exp_bid <- buyer_bid_est$fitted.values
data$bid_difference <- data$exp_bid - data$buyer_bid

boxplot(bid_difference ~ operating_system, data = data)
### Excuse me, what the f***?

plot(data$exp_bid, data$buyer_bid)
### Outliers spotted, use logarithmic values

### Heinz, Amro and Achmea have buyer_bids = 0?!

### Interest of agency (by Jaymon): two-sample t-test
cor(data$buyer_bid, data$test_group)

