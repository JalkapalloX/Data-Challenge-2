# ADVERTISER STAKEHOLDER ANALYSIS

# Q: Which ad characteristics have the highest pay-off regarding extra costs and extra sales?

# LOADING PACKAGES
library(tidyverse)
library(Hmisc)
library(dummies)

# SET WORKING DIRECTORY TO FILE DIRECTORY (RSTUDIO ONLY)
# You may need to install the lastest version of the rstudioapi.
setwd(dirname(rstudioapi::getActiveDocumentContext()$path))

data <- read.csv("DataChallenge2019_GreenhouseGroup_Bidding_Algorithms_Tests.csv", sep=";")
data <- data[!is.na(data$advertiser_id),]   # Delete empty lines

# ~~~ Part 1 ~~~ #
# CREATIVE SIZE
data$creative <- ifelse(data$creative_size_small != 0 & data$creative_size_medium == 0 & data$creative_size_large == 0, "small",
                        ifelse(data$creative_size_small == 0 & data$creative_size_medium != 0 & data$creative_size_large == 0, "medium",
                               ifelse(data$creative_size_small == 0 & data$creative_size_medium == 0 & data$creative_size_large != 0, "large", "mix")))
data$creative <- as.factor(data$creative)

# VIOLINPLOT SHOWING THE LOG DISTRIBUTION OF BUYER BIDS BY CREATIVE SIZE
ggplot(data = data, mapping=aes(x=creative, y=log(buyer_bid), fill=creative)) + geom_violin() +
  geom_jitter(shape=16, position=position_jitter(0.1)) +
  scale_fill_brewer(palette="Blues")


# ~~~ Part 2 ~~~ #
# User properties: device type, operating system

advertiser_dummies <- dummy(data$advertiser_name, sep=":")
colnames(advertiser_dummies) <- levels(data$advertiser_name)[2:13]
impressions_by_advertiser <- advertiser_dummies * data$impressions

# Bid model assuming linear relation of buyer_bid and impressions by advertiser
bid_model1 <- lm(data$buyer_bid ~ impressions_by_advertiser)
summary(bid_model1)

data$exp_bid <- bid_model1$fitted.values

# PLOT 2 SHOWING THAT THIS ESTIMATION IS TERRIBLY ACCURATE
ggplot(data=data, mapping=aes(x=exp_bid, y=buyer_bid)) +
  geom_point() +
  geom_smooth(method=lm)

device_dummies <- dummy(data$device_type, sep=":")
colnames(device_dummies) <- levels(data$device_type)[2:3]

os_dummies <- dummy(data$operating_system, sep=":")
colnames(os_dummies) <- levels(data$operating_system)[2:6]

cs_dummies <- dummy(data$creative, sep=":")
colnames(cs_dummies) <- levels(data$creative)

# Neither device, nor operating system, nor creative size seem to have any impact on the buyer_bid,
# though they may still be related to impressions themselves.
# Takeaway is, impressions by e.g. MacOS user don't seem to be valued more than non-MacOS users.
summary(lm(data$buyer_bid ~ impressions_by_advertiser + device_dummies + os_dummies + cs_dummies))

data$buy_click_prop <- data$post_click_conv / data$clicks          # Proportions are faulty
data$buys_view_prop <- data$post_view_conv / data$impressions      # Proportions are faulty

# Large and small images have way lower click props but this seems to be related to other factors
ggplot(data = data, mapping=aes(x=creative, y=buy_click_prop, fill=creative)) + geom_violin() +
  geom_jitter(shape=16, position=position_jitter(0.1)) +
  scale_fill_brewer(palette="Blues")

# Mobile phone users seem less willing to pay
ggplot(data = data, mapping=aes(x=operating_system, y=buy_click_prop, fill=operating_system)) + geom_violin() +
  geom_jitter(shape=16, position=position_jitter(0.1)) +
  scale_fill_brewer(palette="Blues")
