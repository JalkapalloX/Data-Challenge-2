# -*- coding: utf-8 -*-
import pandas as pd

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

