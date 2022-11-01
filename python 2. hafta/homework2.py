#ÖDEV1
#region

import seaborn as sns
df = sns.load_dataset("car_crashes")
df.columns

["NUM_" + col.upper()  if df[col].dtype != "O" else col.upper() for col in df.columns]

#endregion



#ÖDEV2
#region

import seaborn as sns
df = sns.load_dataset("car_crashes")
df.columns

[col.upper()+ "_FLAG" if "no" not in col else col.upper() for col in df.columns]

#endregion



#ÖDEV3
#region

import seaborn as sns
df = sns.load_dataset("car_crashes")
df.columns

og_list=["abbrev","no_previous"]

new_cols=[col for col in df.columns if col not in og_list]
new_cols

new_df=df[new_cols]
new_df

#endregion


#ÖDEV4
#region

#1.soru

import seaborn as sns
df1=sns.load_dataset("titanic")
df1


#2.soru

df1["sex"].value_counts()

#3.soru

df1.nunique()

#4.soru

df1["pclass"].unique()

#5.soru

df1[["pclass", "parch"]].nunique()

#6.soru

df1["embarked"].dtypes
df1["embarked"]=df1["embarked"].astype("category")
df1["embarked"].dtypes


#7.soru

df1[df1["embarked"] == "C"].head()

#8.soru

df1[df1["embarked"] != "S"].head()

#9.soru

df1.loc[(df1["age"] < 30) & (df1["sex"] == "female")]

#10.soru

df1.loc[(df1["fare"] > 500) | (df1["age"] > 70)]

#11.soru

df1.isnull().sum()

#12.soru

df1.drop("who", axis=1, inplace=True)
df1.columns

#13.soru

import seaborn as sns
df1=sns.load_dataset("titanic")
df1

df1["deck"].isnull().sum()

df1["deck"] = df1["deck"].fillna(df1["deck"].mode()[0])
df1["deck"]

df1["deck"].isnull().sum()

#14.soru

import seaborn as sns
df1=sns.load_dataset("titanic")
df1

df1["age"].isnull().sum()

df1["age"].median()

df1["age"]=df1["age"].fillna(df1["age"].median())
df1["age"]

df1["age"].isnull().sum()

#15.soru

df1.groupby(["pclass","sex"]).agg({"survived":["sum","count","mean"]})

#16.soru

def age_func(age):
    if age < 30:
        return 1
    else:
        return 0
df1["age_flag"]=df1["age"].apply(lambda x:age_func(x))
df1["age_flag"]

#17.soru

import seaborn as sns
df2= sns.load_dataset("tips")
df2

#18.soru

df2.groupby("time").agg({"total_bill": (["sum","min","max","mean"])})

#19.soru

df2.groupby(["time","day"]).agg({"total_bill": (["sum","min","max","mean"])})

#2.yöntem
df2.pivot_table("total_bill", "time", "day", aggfunc=["sum","min","mean","max"])

#20.soru


df2[(df2["time"]== "Lunch") & (df2["sex"] == "Female")].groupby("day").agg({"total_bill" : (["sum","min","max","mean"]),
                                                                           "tip" : (["sum","min","max","mean"])})

#21.soru

df2.loc[(df2["size"] < 3) & (df2["total_bill"] >10),"total_bill"].mean()

#22.soru

df2["total_bill_tip_sum"]=df2["total_bill"]+ df2["tip"]
df2["total_bill_tip_sum"]

#23.soru

df2["total_bill_tip_sum"]=df2["total_bill"]+ df2["tip"]
df2["total_bill_tip_sum"]

df3 = df2.sort_values("total_bill_tip_sum", ascending=False)[:30]
df3

#2.yöntem
df3=df2["total_bill_tip_sum"].sort_values(ascending=False)[:30]
df3
#endregion








import pandas as pd
pd.set_option('display.max_columns', None)


#uyarı kodu
import warnings
warnings.filterwarnings("ignore")