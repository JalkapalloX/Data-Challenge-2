# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np

data = pd.read_csv('Data/DataChallenge2019_GreenhouseGroup_Bidding_Algorithms_Tests.csv',
                   sep=';').dropna(how='all')


data['small_per_impression'] = data['creative_size_small'] / data['impressions']
data['medium_per_impression'] = data['creative_size_medium'] / data['impressions']
data['large_per_impression'] = data['creative_size_large'] / data['impressions']
data['inview_per_impression'] = data['impressions_inview'] / data['impressions']
data['abovefold_per_impression'] = data['impressions_above_fold'] / data['impressions']
data['clicks_per_impression'] = data['clicks'] / data['impressions']

data['conv_per_inview'] = data['post_view_conv'] / data['impressions_inview']
data['conv_per_click'] = data['post_click_conv'] / data['clicks']

data['UU_inview_per_UU_impression'] = data['unique_user_inview'] / data['unique_user_impressions']
data['UU_click_per_UU_impression'] = data['unique_user_is_click'] / data['unique_user_impressions']

data['UU_conv_per_UU_inview'] = data['unique_user_post_view_conv'] / data['unique_user_inview']
data['UU_conv_per_UU_click'] = data['unique_user_post_click_conv'] / data['unique_user_is_click']

data['inview/impression/euro'] = data['inview_per_impression'] / data['buyer_bid']
data['clicks/impression/euro'] = data['clicks_per_impression'] / data['buyer_bid']
data['UU_clicks/impression/euro'] = data['UU_click_per_UU_impression'] / data['buyer_bid']

def AB_performance(values, data=data):
    A_mean = []
    B_mean = []
    delta = []
    indicator = []
    rel_increase = []

    for i in values:
        if 'euro' in i:
            data = data[data['buyer_bid'] > 0]
    
        df = data.groupby(['campaign_group_id', 'operating_system', 'device_type', 'test_group'])[i].sum().unstack().dropna()
        indicator.append(i)
        A_mean.append(np.mean(df['A']))
        B_mean.append(np.mean(df['B']))
        delta.append(np.mean(df['B']) - np.mean(df['A']))
        rel_increase.append((np.mean(df['B']) - np.mean(df['A']))/abs(np.mean(df['A'])))

    performance_df = pd.DataFrame()
    performance_df['A_mean'] = A_mean
    performance_df['B_mean'] = B_mean
    performance_df['delta'] = delta
    performance_df['indicator'] = indicator
    performance_df['%increase'] = rel_increase
    
    return performance_df
        
reach_performance = AB_performance(values=['inview_per_impression', 
                                           'clicks_per_impression', 
                                           'UU_inview_per_UU_impression', 
                                           'UU_click_per_UU_impression'])

targeting_performance = AB_performance(values=['conv_per_inview',
                                               'conv_per_click',
                                               'UU_conv_per_UU_inview',
                                               'UU_conv_per_UU_click'])

efficiency_performance = AB_performance(values=['inview/impression/euro',
                                                'clicks/impression/euro',
                                                'UU_clicks/impression/euro'])
    
