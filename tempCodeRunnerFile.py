df["hour"]=pd.to_datetime(df["Time"],format="%H:%M:%S").dt.hour 
df
