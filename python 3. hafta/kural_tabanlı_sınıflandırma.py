# GÖREV 1: Aşağıdaki soruları yanıtlayınız.
#############################################
#region
# Soru 1: persona.csv dosyasını okutunuz ve veri seti ile ilgili genel bilgileri gösteriniz.
import pandas as pd
pd.set_option("display.max_rows", None)
df = pd.read_csv("persona.csv")
df.info()
df.head()

# Soru 2: Kaç unique SOURCE vardır? Frekansları nedir?
df["SOURCE"].nunique()
df["SOURCE"].value_counts()

# Soru 3: Kaç unique PRICE vardır?
df["PRICE"].nunique()

# Soru 4: Hangi PRICE'dan kaçar tane satış gerçekleşmiş?
df["PRICE"].value_counts()

# Soru 5: Hangi ülkeden kaçar tane satış olmuş?

df["COUNTRY"].value_counts()
df.groupby("COUNTRY")["PRICE"].count()


# Soru 6: Ülkelere göre satışlardan toplam ne kadar kazanılmış?

df.groupby("COUNTRY")["PRICE"].sum()
df.groupby("COUNTRY").agg({"PRICE": "sum"})


# Soru 7: SOURCE türlerine göre göre satış sayıları nedir?

df["SOURCE"].value_counts()

# Soru 8: Ülkelere göre PRICE ortalamaları nedir?

df.groupby(by=['COUNTRY']).agg({"PRICE": "mean"})

# Soru 9: SOURCE'lara göre PRICE ortalamaları nedir?

df.groupby(by=['SOURCE']).agg({"PRICE": "mean"})

# Soru 10: COUNTRY-SOURCE kırılımında PRICE ortalamaları nedir?

df.groupby(by=["COUNTRY", 'SOURCE']).agg({"PRICE": "mean"})

#endregion

#############################################
# GÖREV 2: COUNTRY, SOURCE, SEX, AGE kırılımında ortalama kazançlar nedir?
#############################################
#region

df.groupby(["COUNTRY", 'SOURCE', "SEX", "AGE"]).agg({"PRICE": "mean"}).head()

#endregion


#############################################
# GÖREV 3: Çıktıyı PRICE'a göre sıralayınız.
#############################################
# Önceki sorudaki çıktıyı daha iyi görebilmek için sort_values metodunu azalan olacak şekilde PRICE'a uygulayınız.
# Çıktıyı agg_df olarak kaydediniz.
#region

agg_df = df.groupby(by=["COUNTRY", 'SOURCE', "SEX", "AGE"]).agg({"PRICE": "mean"}).sort_values("PRICE", ascending=False)
agg_df.head()
#endregion



# GÖREV 4: Indekste yer alan isimleri değişken ismine çeviriniz.
#############################################
# Üçüncü sorunun çıktısında yer alan PRICE dışındaki tüm değişkenler index isimleridir.
# Bu isimleri değişken isimlerine çeviriniz.
# İpucu: reset_index()
#region

agg_df = agg_df.reset_index()
agg_df.head()
#endregion


# GÖREV 5: AGE değişkenini kategorik değişkene çeviriniz ve agg_df'e ekleyiniz.
#############################################
# Age sayısal değişkenini kategorik değişkene çeviriniz.
# Aralıkları ikna edici olacağını düşündüğünüz şekilde oluşturunuz.
# Örneğin: '0_18', '19_23', '24_30', '31_40', '41_70'

#region

agg_df["age_cat"] = pd.cut(agg_df["AGE"], bins=[0, 18, 23, 30, 40, 66], labels=['0_18', '19_23', '24_30', '31_40', '41_66'])
agg_df.head()
#endregion



# GÖREV 6: Yeni level based müşterileri tanımlayınız ve veri setine değişken olarak ekleyiniz.
#############################################
# customers_level_based adında bir değişken tanımlayınız ve veri setine bu değişkeni ekleyiniz.
# Dikkat!
# list comp ile customers_level_based değerleri oluşturulduktan sonra bu değerlerin tekilleştirilmesi gerekmektedir.
# Örneğin birden fazla şu ifadeden olabilir: USA_ANDROID_MALE_0_18
# Bunları groupby'a alıp price ortalamalarını almak gerekmektedir.

#region
#1.yöntem
agg_df["customers_level_based"] = [row[0].upper() + "_" + row[1].upper() + "_" + row[2].upper() + "_" + row[5].upper() for row in agg_df.values]
agg_df.head()

#2.YÖNTEM

cat_cols = [col for col in agg_df.columns if str(agg_df[col].dtype) in ["category", "object", "bool"]]
agg_df["customers_level_based"] = ["_".join(col).upper() for col in agg_df[cat_cols].values]
agg_df.head()
agg_df["customers_level_based"].value_counts()
agg_df=agg_df.groupby("customers_level_based").agg({"PRICE": "mean"})
agg_df.reset_index(inplace= True)
agg_df.value_counts()

#endregion


# GÖREV 7: Yeni müşterileri (USA_ANDROID_MALE_0_18) segmentlere ayırınız.
#############################################
# PRICE'a göre segmentlere ayırınız,
# segmentleri "SEGMENT" isimlendirmesi ile agg_df'e ekleyiniz,
# segmentleri betimleyiniz,

#region
agg_df["SEGMENT"] = pd.qcut(agg_df["PRICE"], 4, labels=["D", "C", "B", "A"])
agg_df.groupby("SEGMENT").agg({"PRICE": ("count","mean","min","max","sum")})
#endregion



# GÖREV 8: Yeni gelen müşterileri sınıflandırınız ne kadar gelir getirebileceğini tahmin ediniz.
#############################################
# 33 yaşında ANDROID kullanan bir Türk kadını hangi segmente aittir ve ortalama ne kadar gelir kazandırması beklenir?
#region
user1 = "TUR_ANDROID_FEMALE_31_40"
agg_df[agg_df["customers_level_based"] == user1]

# 35 yaşında IOS kullanan bir Fransız kadını hangi segmente ve ortalama ne kadar gelir kazandırması beklenir?

user2 = "FRA_IOS_FEMALE_31_40"
agg_df[agg_df["customers_level_based"] == user2]

#endregion
