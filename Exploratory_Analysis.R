# LOADING PACKAGES
library(tidyverse)

# SET WORKING DIRECTORY TO FILE DIRECTORY (RSTUDIO ONLY)
# You may need to install the lastest version of the rstudioapi.
setwd(dirname(rstudioapi::getActiveDocumentContext()$path))

### Is media cost the base that everyone bids over?
### Average outcomes over time

data <- read.csv("DataChallenge2019_GreenhouseGroup_Bidding_Algorithms_Tests.csv", sep=";")
### Weird empty lines in the middle of the data frame.
data <- data[!is.na(data$advertiser_id),]


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
