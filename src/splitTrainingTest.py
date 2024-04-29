from sklearn.model_selection import train_test_split

def splitData(cleaned_df):
  df = cleaned_df
  seed = 4
  train, test = train_test_split(df, test_size=0.2, random_state=seed)

  return train, test