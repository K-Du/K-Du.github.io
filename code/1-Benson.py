import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('')
df.columns = df.columns.str.strip()

#De-cumulative-ize the entries data
df['ENTRIES_hourly'] = df['ENTRIES'].diff().fillna(0)
#Filter outliers
df = df[(0<df.ENTRIES_hourly) & (df.ENTRIES_hourly<3900)]

#Filter out non-regular lines
df = df[df.DESC == "REGULAR"]

#Datetime parser
df.TIME = pd.to_datetime(df.TIME)
df.TIME = df.TIME.dt.hour

#Binning the data into every 4 hours

for i in xrange(0, 25, 4):
    df.TIME.loc[(df.TIME >= i) & (df.TIME < i+4)] = i

#Creates new dataframe with total weekly entries by time
df_time = df.groupby(['TIME']).sum().reset_index()

#Shows lines with the greateest difference between peak-high and low entries
print df.groupby(['LINENAME'])\
.aggregate(lambda x: x.max() - x.min())\
.reset_index()\
.sort_values('ENTRIES_hourly', ascending = False)\
.head(5)

#Generating estmated data
df_time.loc[df_time.TIME == 0, 'ENTRIES_hourly_projected'] = 1.5 * df_time.loc[df_time.TIME == 0, 'ENTRIES_hourly'] 
df_time.loc[df_time.TIME == 4, 'ENTRIES_hourly_projected'] = 4 * df_time.loc[df_time.TIME == 4, 'ENTRIES_hourly']
df_time.loc[df_time.TIME == 8, 'ENTRIES_hourly_projected'] = 1.1 * df_time.loc[df_time.TIME == 8, 'ENTRIES_hourly']
df_time.loc[df_time.TIME == 12, 'ENTRIES_hourly_projected'] = .9 * df_time.loc[df_time.TIME == 12, 'ENTRIES_hourly']
df_time.loc[df_time.TIME == 16, 'ENTRIES_hourly_projected'] = .9 * df_time.loc[df_time.TIME == 16, 'ENTRIES_hourly']
df_time.loc[df_time.TIME == 20, 'ENTRIES_hourly_projected'] = .9 * df_time.loc[df_time.TIME == 20, 'ENTRIES_hourly']

plt.plot(df_time.TIME, df_time.ENTRIES_hourly)
plt.plot(df_time.TIME, df_time.ENTRIES_hourly_projected)
plt.xlabel('Time')
plt.ylabel('Weekly Entries')
plt.xscale('linear')
plt.show()


