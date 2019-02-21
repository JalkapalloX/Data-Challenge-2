# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
from statsmodels.stats.proportion import proportions_ztest

data = pd.read_csv('Data/DataChallenge2019_GreenhouseGroup_Bidding_Algorithms_Tests.csv',
                   sep=';').dropna(how='all')


data['small_per_impression'] = data['creative_size_small'] / data['impressions']
data['medium_per_impression'] = data['creative_size_medium'] / data['impressions']
data['large_per_impression'] = data['creative_size_large'] / data['impressions']
data['inview_per_impression'] = data['impressions_inview'] / data['impressions']
data['abovefold_per_impression'] = data['impressions_above_fold'] / data['impressions']
data['clicks_per_impression'] = data['clicks'] / data['impressions']

data['Post-view conversions per impression'] = data['post_view_conv'] / data['impressions']
data['Post-click conversions per impression'] = data['post_click_conv'] / data['impressions']

data['Post-view conversions per impression '] = data['Post-view conversions per impression'] / (data['buyer_bid'] / 1000)
data['Post-click conversions per impression '] = data['Post-click conversions per impression'] / (data['buyer_bid'] / 1000)

data['Unique user view per impression'] = data['unique_user_inview'] / data['impressions']
data['Unique user click per impression'] = data['unique_user_is_click'] / data['impressions']

data['Unique user view per impression '] = data['unique_user_inview'] / data['impressions'] / (data['buyer_bid'] / 1000)
data['Unique user click per impression '] = data['unique_user_is_click'] / data['impressions'] / (data['buyer_bid'] / 1000)
data['2'] = (data['post_view_conv'] + data['post_click_conv']) / (data['buyer_bid'] / 1000)

data['start_date'] = pd.to_datetime(data['start_date'])
data['end_date'] = pd.to_datetime(data['end_date'])
data['campaign_duration'] = (data['end_date'] - data['start_date']).dt.days

def agency_AB_performance(values, data=data):
    A_mean = []
    B_mean = []
    delta = []
    indicator = []
    rel_increase = []
    p_value_delta = 

    
    for i in values:
        if 'impression ' in i:
            data = data[data['buyer_bid'] > 0]
    
        df = data.groupby(['campaign_group_id', 'operating_system', 'device_type', 'test_group'])[i].sum().unstack().dropna()
        indicator.append(i)
        A_mean.append(np.mean(df['A']))
        B_mean.append(np.mean(df['B']))
        delta.append(np.mean(df['B']) - np.mean(df['A']))
        rel_increase.append((np.mean(df['B']) - np.mean(df['A']))/abs(np.mean(df['A'])))
        stat, pval = proportions_ztest(count, nobs)


        
    performance_df = pd.DataFrame()
    performance_df['A_mean'] = A_mean
    performance_df['B_mean'] = B_mean
    performance_df['delta'] = delta
    performance_df['indicator'] = indicator
    performance_df['%increase'] = rel_increase
    
    
    return performance_df
        
eff_reach_performance = agency_AB_performance(values=['Unique user click per impression'])

sales_performance = agency_AB_performance(values=['Post-view conversions per impression',
                                                  'Post-click conversions per impression'])

cost_efficiency_performance = agency_AB_performance(values=[
                                                'Unique user view per impression '])


    
def plot_group_barchart(dataframe, title):
    fig, ax = plt.subplots(figsize=(6, 12))
    ind = np.arange(len(dataframe))                                   # the x locations for the groups
    width = 0.35                                                      # the width of the bars
    p1 = ax.bar(ind, dataframe['A_mean'], width, color='lightblue', bottom=0)
    p2 = ax.bar(ind + width, dataframe['B_mean'], width, color='darkblue', bottom=0)
    #ax.set_title(title, fontsize=21)
    ax.set_xticks(ind + width / 2)
    ax.set_xticklabels(tuple(dataframe['indicator']), fontsize=14)
    #ax.legend((p1[0], p2[0]), ('Control algorithm', 'Bidwiser algorith'), fontsize=15)
    fig.savefig(fname=title)
    

#plot_group_barchart(dataframe=eff_reach_performance , title=' ')
    
#fig, ax = plt.subplots(figsize=(14, 8))
plt.scatter(x=data['campaign_duration'], y=data['Unique user click per impression'])

ax.set_title("Unique user click per impression per euro", fontsize=21)
plt.xlabel("Campaign duration (days)", fontsize=15)
