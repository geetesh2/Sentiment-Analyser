import pandas as pd
from collection import comments
from analysis import final_data
from analysis import polarity

dataframe = {"Comment":comments,"Sentiment_type" : final_data,"Polarity":polarity}
df = pd.DataFrame.from_dict(dataframe, orient='index')
df1= df.transpose()
df1.columns = ["Comment","Sentiment_type","Polarity"]

df1.to_csv("data.csv",header = True, encoding = 'utf-8', index = False)