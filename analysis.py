# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

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
data['Conv pi'] = data['Post-view conv pi'] + data['Post-click conv pi']

data['Post-view conv pe'] = data['Post-view conv pi'] / (data['media_cost'] / 1000)
data['Post-click conv pe'] = data['Post-click conv pi'] / (data['media_cost'] / 1000)
data['Conv pe'] = (data['Post-view conv pe'] + data['Post-click conv pe'])

data['UU view pi'] = data['unique_user_inview'] / data['impressions']
data['UU click pi'] = data['unique_user_is_click'] / data['impressions']

data['UU view pe'] = data['UU view pi'] / (data['media_cost'] / 1000)
data['UU click pe'] = data['UU click pi'] / (data['media_cost'] / 1000)

data['start_date'] = pd.to_datetime(data['start_date'])
data['end_date'] = pd.to_datetime(data['end_date'])
data['campaign_duration'] = (data['end_date'] - data['start_date']).dt.days


def agency_AB_performance(values, data=data):

    a_mean = []
    b_mean = []
    delta = []
    indicator = []
    rel_increase = []
    p_value_higher = []
    p_value_lower = []
    test_count = []
    
    for i in values:

        data = data[data['buyer_bid'] > 0]
        data.drop_duplicates(['campaign_group_id', 'operating_system', 'device_type', 'test_group'], inplace=True)

        global df
    
        df = data.groupby(['campaign_group_id', 'operating_system', 'device_type', 'test_group'])[i].mean().unstack().dropna()
        df2 = data.groupby(['campaign_group_id', 'operating_system', 'device_type', 'test_group'])['impressions'].sum().unstack().dropna()
        
        df = pd.concat([df, df2], axis=1)
        df.columns = ['A', 'B', 'A_count', 'B_count']
        
        df = df[(df['A'] != 0) & (df['B'] != 0)]
        
        df['diff'] = df['B'] - df['A']
        
        indicator.append(i)
        a_mean.append(np.mean(df['A']))
        b_mean.append(np.mean(df['B']))
        delta.append(np.mean(df['B']) - np.mean(df['A']))
        rel_increase.append((np.mean(df['B']) - np.mean(df['A']))/abs(np.mean(df['A'])) * 100)
        
        # Z-test B > A
        p1 = df['A']
        p2 = df['B']
        var1 = p1*(1-p1)
        var2 = p2*(1-p2)

        z = (p2-p1)/(var1/df['A_count'] + var2/df['B_count'])**0.5
        pval = norm.cdf(z)
        count = 0

        for i in pval:
            if i < 0.05:
                count += 1

        p_value_higher.append(count)
        test_count.append(df['A'].count())
        
        # Z-test A > B
        p1 = df['B']
        p2 = df['A']

        var1 = p1*(1-p1)
        var2 = p2*(1-p2)

        z = (p2-p1)/(var1/df['A_count'] + var2/df['B_count'])**0.5
        pval = norm.cdf(z)
        count = 0

        for i in pval:
            if i < 0.05:
                count += 1

        p_value_lower.append(count)

    performance_df = pd.DataFrame()
    performance_df['indicator'] = indicator
    performance_df['A_mean'] = a_mean
    performance_df['B_mean'] = b_mean
    performance_df['delta'] = delta
    performance_df['%increase'] = rel_increase
    performance_df['sig_count_higher'] = p_value_higher
    performance_df['sig_count_lower'] = p_value_lower
    performance_df['test_count'] = test_count
    
    return performance_df



agency_AB_performance(values=['UU click pi', 'UU view pi']).to_csv("Agency_branding_performance.csv")

agency_AB_performance(values=['Conv pi',
                                                  'Post-view conv pi',
                                                  'Post-click conv pi']).to_csv("Agency_sales_performance.csv")
    

def agency_AB_performance(values, 
                          data=data,
                          cost_efficiency=False):

    a_mean = []
    b_mean = []
    delta = []
    indicator = []
    rel_increase = []
    p_value_higher = []
    p_value_lower = []
    test_count = []
    
    for i in values:

        data = data[data['buyer_bid'] > 0]
        data.drop_duplicates(['campaign_group_id', 'operating_system', 
                              'device_type', 'test_group'], 
                              inplace=True)

        global df
        df = data.groupby(['campaign_group_id', 'operating_system', 'device_type', 'test_group'])[i].mean().unstack().dropna()
        df2 = data.groupby(['campaign_group_id', 'operating_system', 'device_type', 'test_group'])['impressions'].sum().unstack().dropna()
        
        df = pd.concat([df, df2], axis=1)
        df.columns = ['A', 'B', 'A_count', 'B_count']
        
        df = df[(df['A'] != 0) & (df['B'] != 0)]
        
        a_mean_series = df['A'] / df['A_count']
        b_mean_series = df['B'] / df['B_count']
        
        df['diff'] = b_mean_series - a_mean_series
        
        indicator.append(i)
        a_mean.append(np.mean(a_mean_series))
        b_mean.append(np.mean(b_mean_series))
        delta.append(np.mean(df['B']) - np.mean(df['A']))
        rel_increase.append((np.mean(df['B']) - np.mean(df['A']))/abs(np.mean(df['A'])) * 100)
        
        # Z-test B > A
        p1 = a_mean_series
        p2 = b_mean_series
        var1 = p1*(1-p1)
        var2 = p2*(1-p2)

        z = (p2-p1)/(var1/df['A_count'] + var2/df['B_count'])**0.5
        pval = norm.cdf(z)
        count = 0

        for i in pval:
            if i < 0.05:
                count += 1

        p_value_higher.append(count)
        test_count.append(df['A'].count())
        
        # Z-test A > B
        p1 = df['B']
        p2 = df['A']

        var1 = p1*(1-p1)
        var2 = p2*(1-p2)

        z = (p2-p1)/(var1/df['A_count'] + var2/df['B_count'])**0.5
        pval = norm.cdf(z)
        count = 0

        for i in pval:
            if i < 0.05:
                count += 1

        p_value_lower.append(count)

    performance_df = pd.DataFrame()
    performance_df['indicator'] = indicator
    performance_df['A_mean'] = a_mean
    performance_df['B_mean'] = b_mean
    performance_df['delta'] = delta
    performance_df['%increase'] = rel_increase
    performance_df['sig_count_higher'] = p_value_higher
    performance_df['sig_count_lower'] = p_value_lower
    performance_df['test_count'] = test_count
    
    return performance_df

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
