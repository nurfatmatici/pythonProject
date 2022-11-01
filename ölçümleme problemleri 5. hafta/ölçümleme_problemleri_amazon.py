
import pandas as pd
import math
import scipy.stats as st
from intake.container import dataframe
from sklearn.preprocessing import MinMaxScaler

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 500)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

df = pd.read_csv("ölçümleme problemleri 5. hafta/amazon_review.csv")
df.head()
df.shape
df.info()


#Görev1
#region
#Adım1

df["overall"].mean()

#Adım2

df["reviewTime"]= pd.to_datetime(df["reviewTime"], dayfirst= True)
df.info()

current_date = df["reviewTime"].max()

df["days"] = (current_date -df["reviewTime"]).dt.days
df.head()

q1= df["days"].quantile(0.25)
q2= df["days"].quantile(0.50)
q3= df["days"].quantile(0.75)
df["days"].describe().T


def time_based_weighted_average(dataframe, w1=18, w2=22, w3=28, w4=32):
    return dataframe.loc[(dataframe["days"] <= q1), "overall"].mean() * w1 / 100 + \
           dataframe.loc[(dataframe["days"] > q1) & (dataframe["days"] <= q2), "overall"].mean() * w2 / 100 + \
           dataframe.loc[(dataframe["days"] > q2) & (dataframe["days"] <= q3), "overall"].mean() * w3 / 100 + \
           dataframe.loc[(dataframe["days"] > q3),"overall"].mean() * w4 / 100


time_based_weighted_average(df)


print(df.loc[(df["days"] <= q1), "overall"].mean() * 18 / 100 )
print(df.loc[(df["days"] > q1) & (df["days"] <= q2), "overall"].mean() * 22 / 100 )
print(df.loc[(df["days"] > q2) & (df["days"] <= q3), "overall"].mean() * 28 / 100 )
print(df.loc[(df["days"] > q3),"overall"].mean() * 32 / 100)


print(df.loc[(df["days"] <= q1), "overall"].mean())
print(df.loc[(df["days"] > q1) & (df["days"] <= q2), "overall"].mean())
print(df.loc[(df["days"] > q2) & (df["days"] <= q3), "overall"].mean())
print(df.loc[(df["days"] > q3),"overall"].mean())

#endregion


#Görev2
#region
#Adım1

df["helpful_no"] =df["total_vote"] - df["helpful_yes"]
df.head()

#Adım2

# score_pos_neg_diff
def score_pos_neg_diff(up, down):
    return up - down
df["score_pos_neg_diff"] = df.apply(lambda x: score_pos_neg_diff(x["helpful_yes"], x["helpful_no"]), axis=1)

# score_average_rating
def score_average_rating(up, down):
    if up + down == 0:
        return 0
    return up / (up + down)
df["score_average_rating"] = df.apply(lambda x: score_average_rating(x["helpful_yes"], x["helpful_no"]), axis=1)

# wilson_lower_bound
def wilson_lower_bound(up, down, confidence=0.95):
    n = up + down
    if n == 0:
        return 0
    z = st.norm.ppf(1 - (1 - confidence) / 2)
    phat = 1.0 * up / n
    return (phat + z * z / (2 * n) - z * math.sqrt((phat * (1 - phat) + z * z / (4 * n)) / n)) / (1 + z * z / n)
df["wilson_lower_bound"] = df.apply(lambda x: wilson_lower_bound(x["helpful_yes"], x["helpful_no"]), axis=1)

df.sort_values("wilson_lower_bound", ascending= False).head(20)

#endregion