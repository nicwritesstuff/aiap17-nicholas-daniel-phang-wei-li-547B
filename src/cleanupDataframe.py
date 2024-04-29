import pandas as pd

def commenceCleanup(dataframe):

  df = dataframe

  midnight_seconds = pd.to_timedelta('00:00:00').total_seconds()  

  call_duration_bins = [0, 300, 600, 900]
  call_frequency_bins = [0, 10, 20, 30]
  time_labels = ['Overnight', 'Morning', 'Afternoon', 'Evening', 'Night']
  time_bins = [pd.to_timedelta('00:00:00').total_seconds(), pd.to_timedelta('06:00:00').total_seconds(),
               pd.to_timedelta('12:00:00').total_seconds(), pd.to_timedelta('17:00:00').total_seconds(),
               pd.to_timedelta('20:00:00').total_seconds(), pd.to_timedelta('24:00:00').total_seconds()]

  
  flagged_by_carrier_map = {'unlikely': 0, 'suspicious': 1, 'very suspicious': 2}
  

  print('')
  print("Cleaning up label: 'Scam Call'...")
  df['Scam Call'] = df['Scam Call'].str.lower()
  df['Scam Call'] = df['Scam Call'].replace('not scam', 0)
  df['Scam Call'] = df['Scam Call'].replace('scam', 1)
  df['Scam Call'] = df['Scam Call'].astype(int)
  print("Cleaned up label: 'Scam Call'!")


  print('')
  print("Cleaning up attribute: 'Call Duration'...")
  df['Call Duration'] = df['Call Duration'].abs()
  print("Resolved possible negatives: 'Call Duration'")
  
  df['Call Duration'] = pd.cut(df['Call Duration'], bins = call_duration_bins)
  df['Call Duration'] = pd.factorize(df['Call Duration'])[0]
  print("Categorised numerically: 'Call Duration'!")

  
  print('')
  print("Cleaning up attribute: 'Call Frequency'...")
  df['Call Frequency'] = df['Call Frequency'].abs()
  print("Resolved possible negatives: 'Call Frequency'")
  
  df['Call Frequency'] = pd.cut(df['Call Frequency'], bins = call_frequency_bins)
  df['Call Frequency'] = pd.factorize(df['Call Frequency'])[0]
  print("Categorised numerically: 'Call Frequency'!")


  print('')
  print("Cleaning up attribute: 'Flagged by Carrier'...")
  df['Flagged by Carrier'] = df['Flagged by Carrier'].str.lower()
  df['Flagged by Carrier'] = df['Flagged by Carrier'].map(flagged_by_carrier_map)
  print("Mapped: 'Flagged by Carrier'!")

  
  print('')
  print("Cleaning up attribute: 'Is International'...")
  df['Is International'] = df['Is International'].str.lower()
  df['Is International'] = df['Is International'].replace('no', 0)
  df['Is International'] = df['Is International'].replace('yes', 1)
  df['Is International'] = df['Is International'].astype(int)
  print("Cleaned up attribute: 'Is Interational'!")


  print('')
  print("Cleaning up attribute: 'Previous Contact Count'...")
  df['Previous Contact Count'] = df['Previous Contact Count'].abs()
  min_value = df['Previous Contact Count'].min()
  max_value = df['Previous Contact Count'].max()
  df['Previous Contact Count'] = (df['Previous Contact Count'] - min_value) / (max_value - min_value)
  print("Normalised attribute: 'Previous Contact Count'!")



  print('')
  print("Cleaning up attribute: 'Country Prefix'...")
  df['Country Prefix'] = df['Country Prefix'].replace('1', 'US')
  df['Country Prefix'] = df['Country Prefix'].replace('44', 'UK')
  df['Country Prefix'] = df['Country Prefix'].replace('65', 'SG')
  df['Country Prefix'] = df['Country Prefix'].replace('7', 'RU')
  df['Country Prefix'] = df['Country Prefix'].replace('91', 'IN')
  df['Country Prefix'] = df['Country Prefix'].replace('95', 'MM')
  df_cp_onehot = pd.get_dummies(df['Country Prefix'])
  df_cp_onehot = df_cp_onehot.astype(int)
  df = pd.concat([df, df_cp_onehot], axis=1)
  df.drop(columns='Country Prefix', inplace=True)
  print("One-hot Encoded attribute: 'Country Prefix'!")


  print('')
  print("Cleaning up attribute: 'Call Type'...")
  df['Call Type'] = df['Call Type'].str.lower()
  df['Call Type'] = df['Call Type'].replace('whats App', 'whatsApp')
  df_ct_onehot = pd.get_dummies(df['Call Type'])
  df_ct_onehot = df_ct_onehot.astype(int)
  df = pd.concat([df, df_ct_onehot], axis=1)
  df.drop(columns='Call Type', inplace=True)
  print("One-hot Encoded attribute: 'Call Type'!")


  print('')
  print("Cleaning up attribute: 'Timestamp'...")
  df['Timestamp'] = pd.to_datetime(df['Timestamp'])
  df['Month in Year'] = (df['Timestamp'].dt.strftime('%b') + ' ' + df['Timestamp'].dt.year.astype(str))
  df_miy_onehot = pd.get_dummies(df['Month in Year'])
  df_miy_onehot = df_miy_onehot.astype(int)

  
  df['Time'] = df['Timestamp'].dt.time
  df['Time Diff'] = df['Timestamp'].apply(lambda x: (x.hour * 3600 + x.minute * 60 + x.second) - midnight_seconds)
  df['Time Binned'] = pd.cut(df['Time Diff'], bins=time_bins, labels=time_labels, right=False)
  df_tb_onehot = pd.get_dummies(df['Time Binned'])
  df_tb_onehot = df_tb_onehot.astype(int)

  
  df = pd.concat([df, df_miy_onehot, df_tb_onehot], axis=1)
  df.drop(columns=['Timestamp', 'Month in Year', 'Time', 'Time Diff', 'Time Binned'], inplace=True)
  print("One-hot Encoded attribute in months and time of day: 'Timestamp'!")

  print('')
  print("Cleaning up attribute: 'Device Battery'...")
  df['Device Battery'] = df['Device Battery'].str.lower()
  df_db_onehot = pd.get_dummies(df['Device Battery'])
  df_db_onehot = df_db_onehot.astype(int)

  
  df = pd.concat([df, df_db_onehot], axis=1)
  df.drop(columns='Device Battery', inplace=True)
  print("One-hot Encoded attribute: 'Device Battery'!")

  df.drop(columns=['ID', 'Financial Loss'], inplace=True)


  return df