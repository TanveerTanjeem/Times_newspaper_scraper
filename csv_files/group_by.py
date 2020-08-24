import pandas as pd

from sklearn import preprocessing
df = pd.read_csv('ninetytwodays.csv')

grouped = df.groupby(['dates']).dates.agg('count').to_frame('count').reset_index()
grouped['dates'] = pd.to_datetime(grouped.dates, infer_datetime_format = True)
grouped.sort_values(by = "dates", ascending= True, inplace = True, ignore_index=True)
grouped['standardized'] = preprocessing.scale(grouped['dates'])
grouped.to_csv('temp.csv')
#print(df)