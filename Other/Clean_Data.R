# SET WORKING DIRECTORY TO FILE DIRECTORY (RSTUDIO ONLY)
# You may need to install the lastest version of the rstudioapi.
setwd(dirname(rstudioapi::getActiveDocumentContext()$path))

data <- read.csv("DataChallenge2019_GreenhouseGroup_Bidding_Algorithms_Tests.csv", sep=";")

clean_by <- function(data, column.names) {
  # Delete empty lines
  data <- data[!is.na(data$advertiser_id),]
  
  ### Buyer bid is per 1000, but linearly relates to impressions
  # Some buyer bids are 0's
  if("buyer_bid" %in% column.names) {
    data <- data[data$buyer_bid != 0,]
  }
  
  # Sometimes there are conversions after clicks but no clicks
  if("clicks" %in% column.names) {
    data <- data[!(data$clicks == 0 & data$post_click_conv != 0),]
  }
  
  ### These numbers are questionable regardless.
  if("unique_user_is_click" %in% column.names) {
    data <- data[data$unique_user_is_click >= data$unique_user_post_click_conv,]
  }
  
  if("unique_user_post_click_conv" %in% column.names) {
    data <- data[data$unique_user_is_click >= data$unique_user_post_click_conv,]
  }
  
  return(data)
}

omit_zeros <- function(data, column.names) {
  for(i in column.names) {
    data <- data[ data[[ i ]] != 0,]
  }
}

get_AB <- function(data) {
  A_data <- data[data$test_group == "A",]
  A_data$test_id <- paste0(A_data$device_type, "_", A_data$operating_system, "_", A_data$campaign_group_id)
  
  B_data <- data[data$test_group == "B",]
  B_data$test_id <- paste0(B_data$device_type, "_", B_data$operating_system, "_", B_data$campaign_group_id)
  
  test_data <- rbind(A_data[sapply(A_data$test_id, function(x) {(x %in% B_data$test_id)}),],
                     B_data[sapply(B_data$test_id, function(x) {(x %in% A_data$test_id)}),])

  return(test_data)
}