#GÖREV1
#region
#Adım1
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 500)
pd.set_option('display.float_format',lambda x: '%.3f' % x)
df_=pd.read_csv("crm analitiği 4. hafta/flo_data_20k.csv.csv")
df=df_.copy()
df



#Adım2
#a)
df.head(10)
#b)
df.columns
#c)
df.describe().T
#d)
df.isnull().sum()
#e)
df.info()

df.dtypes

for i in  df.columns:
    print(i , df[i].dtype)



#Adım3

df["total_order"] = df["order_num_total_ever_online"] + df["order_num_total_ever_offline"]
df["total_order"]

df["total_price"] = df["customer_value_total_ever_online"] + df["customer_value_total_ever_offline"]
df["total_price"]


#Adım4

df.info()
df.head()
date =["first_order_date","last_order_date","last_order_date_online","last_order_date_offline"]
df[date] = df[date].apply(pd.to_datetime)
df[date]


#Adım5

df.groupby("master_id").agg({"total_order":"sum",
                                    "total_price":"sum"})


#Adım6

df.groupby("master_id").agg({"total_price": "sum"}).sort_values(by="total_price", ascending=False).head(10)


#Adım7
df["total_order"]=df["total_order"].astype(int)
df.groupby("master_id").agg({"total_order": "sum"}).sort_values(by="total_order", ascending=False).head(10)

#Adım8

def data_preparation_process(df):
    df["total_order"] = df["order_num_total_ever_online"] + df["order_num_total_ever_offline"]
    df["total_order"]

    df["total_price"] = df["customer_value_total_ever_online"] + df["customer_value_total_ever_offline"]
    df["total_price"]


    date = ["first_order_date", "last_order_date", "last_order_date_online", "last_order_date_offline"]
    df[date] = df[date].apply(pd.to_datetime)
    df.info()

    return df
data_preparation_process(df)
#endregion


#Görev2
#region


last_time = df["last_order_date"].max()
type(last_time)

import datetime as dt
today_date = dt.datetime(2021,6,1)
type(today_date)

rfm = df.groupby('master_id').agg({"last_order_date":lambda last_order_date: (today_date - last_order_date.max()).days,
                                    "total_order" : lambda x:int(x),
                                    "total_price": lambda x:x})


rfm.columns = ["recency", "frequency", "monetary"]
rfm


#endregion



#Görev3
#region

rfm["recency_score"] = pd.qcut(rfm["recency"],5,labels = [5,4,3,2,1])
rfm["frequency_score"] = pd.qcut(rfm["frequency"].rank(method = "first"), 5, labels = [1,2,3,4,5])
rfm["monetary_score"] = pd.qcut(rfm["monetary"], 5, labels = [1,2,3,4,5])

rfm["RF_SCORE"] = (rfm['recency_score'].astype(str) + rfm['frequency_score'].astype(str))
rfm
#endregion


#Görev4
#region

seg_map = {
    r'[1-2][1-2]': 'hibernating',
    r'[1-2][3-4]': 'at_Risk',
    r'[1-2]5': 'cant_loose',
    r'3[1-2]': 'about_to_sleep',
    r'33': 'need_attention',
    r'[3-4][4-5]': 'loyal_customers',
    r'41': 'promising',
    r'51': 'new_customers',
    r'[4-5][2-3]': 'potential_loyalists',
    r'5[4-5]': 'champions'
}

rfm['segment'] = rfm['RF_SCORE'].replace(seg_map, regex = True)
rfm

#endregion

#Görev5
#region

rfm[["segment", "recency", "frequency","monetary"]].groupby("segment").agg(["mean","count"])
new= rfm.loc[(rfm["segment"] == "champions") | (rfm["segment"] == "loyal_customers")]
new


df_cats= df[["master_id","interested_in_categories_12"]].merge(right=new, on="master_id", how="right")
df_cats
df[["master_id","interested_in_categories_12"]].merge(right=new, on="master_id", how="inner")

df_cats_a = df_cats[df_cats["interested_in_categories_12"].str.contains("KADIN")]

df_cats_a["master_id"].to_csv("new.csv")





#Adım2

new1 = rfm.loc[((rfm["segment"] == "cant_loose") | (rfm["segment"] == 'about_to_sleep') | (rfm["segment"] == 'new_customers'))]
new1

df_cats_1= df[(df["interested_in_categories_12"]).str.contains("ERKEK|COCUK")]
df_cats_1

df_cats_b = pd.merge(new1,df_cats_1[["interested_in_categories_12","master_id"]],on=["master_id"])
df_cats_b

df_cats_c= df_cats_b.drop(df_cats_b.loc[:,'recency':'interested_in_categories_12'].columns,axis=1)
df_cats_c
new1.reset_index(inplace=True)
new1
new1["master_id"].to_csv("new1.csv")
#endregion