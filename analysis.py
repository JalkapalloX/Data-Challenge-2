# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as st

data = pd.read_csv('Data/DataChallenge2019_GreenhouseGroup_Bidding_Algorithms_Tests.csv',
                   sep=';').dropna(how='all')

data['small_pi'] = data['creative_size_small'] / data['impressions']
data['medium_pi'] = data['creative_size_medium'] / data['impressions']
data['large_pi'] = data['creative_size_large'] / data['impressions']
data['inview_pi'] = data['impressions_inview'] / data['impressions']
data['abovefold_pi'] = data['impressions_above_fold'] / data['impressions']
data['clicks_pi'] = data['clicks'] / data['impressions']

data['Post-view conv pi'] = data['post_view_conv'] / data['impressions']
data['Post-click conv pi'] = data['post_click_conv'] / data['impressions']

data['Post-view conv pe'] = data['Post-view conv pi'] / (data['buyer_bid'] / 1000)
data['Post-click conv pe'] = data['Post-click conv pi'] / (data['buyer_bid'] / 1000)
data['Conv pi'] = (data['Post-view conv pi'] + data['Post-click conv pi']) / data['impressions']

data['UU view pi'] = data['unique_user_inview'] / data['impressions']
data['UU click pi'] = data['unique_user_is_click'] / data['impressions']

data['UU view pe'] = data['unique_user_inview'] / data['impressions'] / (data['buyer_bid'] / 1000)
data['UU click pe'] = data['unique_user_is_click'] / data['impressions'] / (data['buyer_bid'] / 1000)
data['Conv pe'] = (data['post_view_conv'] + data['post_click_conv']) / (data['buyer_bid'] / 1000)

data['start_date'] = pd.to_datetime(data['start_date'])
data['end_date'] = pd.to_datetime(data['end_date'])
data['campaign_duration'] = (data['end_date'] - data['start_date']).dt.days

def agency_AB_performance(values, data=data):

    a_mean = []
    b_mean = []
    delta = []
    indicator = []
    rel_increase = []
    p_value_delta = []
    test_count = []
    
    for i in values:
        if ' pe' in i:
            data = data[data['buyer_bid'] > 0]
        global df
        df = data.groupby(['campaign_group_id', 'operating_system', 'device_type', 'test_group'])[i].sum().unstack().dropna()
        df2 = data.groupby(['campaign_group_id', 'operating_system', 'device_type', 'test_group'])['impressions'].sum().unstack().dropna()
        
        df = pd.concat([df, df2], axis=1)
        df.columns = ['A', 'B', 'A_count', 'B_count']
        
        indicator.append(i)
        a_mean.append(np.mean(df['A']))
        b_mean.append(np.mean(df['B']))
        delta.append(np.mean(df['B']) - np.mean(df['A']))
        rel_increase.append((np.mean(df['B']) - np.mean(df['A']))/abs(np.mean(df['A'])))

        # Z-test B > A
        x_bar = df['B']
        q = df['A']

        z = (x_bar-q) * np.sqrt((df['A_count'] + df['B_count'])/(q*(1-q)))
        pval = 2*(1-st.norm.cdf(abs(z)))
        count = 0
        y=0
        for i in pval:
            if i < 0.05:
                count += 1
            y += 1
        
        p_value_delta.append(count)
        test_count.append(y)


    performance_df = pd.DataFrame()
    performance_df['indicator'] = indicator
    performance_df['A_mean'] = a_mean
    performance_df['B_mean'] = b_mean
    performance_df['delta'] = delta
    performance_df['%increase'] = rel_increase
    performance_df['sig_count'] = p_value_delta
    performance_df['test_count'] = test_count
    
    return performance_df
        
brand_rec_performance = agency_AB_performance(values=['UU click pi',
                                                      'UU view pi',
                                                      'UU click pe',
                                                      'UU view pe'])

sales_performance = agency_AB_performance(values=['Conv pi',
                                                  'Conv pe',
                                                  'Post-view conv pi',
                                                  'Post-click conv pi',
                                                  'Post-view conv pe',
                                                  'Post-click conv pe'])

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
#plt.scatter(x=data['campaign_duration'], y=data['UU click pi'])

#ax.set_title("Unique user click per impression per euro", fontsize=21)
#plt.xlabel("Campaign duration (days)", fontsize=15)
