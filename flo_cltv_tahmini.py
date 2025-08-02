import pandas as pd
import datetime as dt
from lifetimes import BetaGeoFitter
from lifetimes import GammaGammaFitter
from lifetimes.plotting import plot_period_transactions
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

from CRM_Analytics.FLOMusteriSegmentasyonu.flo_rfm_analysis.floMusteriSeg import date_columns, analysis_date

df = pd.read_csv("CRM_Analytics/FLOMusteriSegmentasyonu/flo_rfm_analysis/flo_data_20k.csv")
df_copy = df
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.2f' % x)
pd.options.mode.chained_assignment =None

df.head()

# Adım 2: Aykırı değerleri baskılamak için gerekli olan outlier_thresholds ve replace_with_thresholds fonksiyonlarını tanımlayınız.
# Not: cltv hesaplanırken frequency değerleri integer olması gerekmektedir.Bu nedenle alt ve üst limitlerini round() ile yuvarlayınız.
def outlier_thresholds(dataframe, variable):
    quartile1 = dataframe[variable].quantile(0.01)
    quartile3 = dataframe[variable].quantile(0.99)
    interquantile_range = quartile3 - quartile1
    up_limit = quartile3 + 1.5 * interquantile_range
    low_limit = quartile1 - 1.5 * interquantile_range
    return low_limit, up_limit

def replace_with_thresholds(dataframe, variable):
    low_limit, up_limit = outlier_thresholds(dataframe, variable)
    dataframe.loc[(dataframe[variable] < low_limit), variable] = round(low_limit,0)
    dataframe.loc[(dataframe[variable] > up_limit), variable] = round(up_limit, 0)

# Adım 3: "order_num_total_ever_online", "order_num_total_ever_offline", "customer_value_total_ever_offline",
# "customer_value_total_ever_online" değişkenlerinin aykırı değerleri varsa baskıla.
columns = ["order_num_total_ever_online", "order_num_total_ever_offline", "customer_value_total_ever_offline","customer_value_total_ever_online" ]
for col in columns:
    replace_with_thresholds(df, col)

# Adım 4: Omnichannel müşterilerin hem online'dan hem de offline platformlardan alışveriş yaptığını ifade etmektedir. Her bir müşterinin toplam
# alışveriş sayısı ve harcaması için yeni değişkenler oluşturunuz.
df["order_num_total"] = df["order_num_total_ever_online"] + df["order_num_total_ever_offline"]
df["customer_value_total"] = df["customer_value_total_ever_online"] + df["customer_value_total_ever_offline"]

# Adım 5: Değişken tiplerini inceleyiniz. Tarih ifade eden değişkenlerin tipini date'e çeviriniz
df.info()
date_columns = df.columns[df.columns.str.contains("date")]
df[date_columns] = df[date_columns].apply(pd.to_datetime)
df.info()


## GÖREV 2: CLTV Veri Yapısının Oluşturulması
# Adım 1: Veri setindeki en son alışverişin yapıldığı tarihten 2 gün sonrasını analiz tarihi olarak alınız.
df["last_order_date"].max()
analysis_date = dt.datetime(2021,6,1)

# Adım 2: customer_id, recency_cltv_weekly, T_weekly, frequency ve monetary_cltv_avg değerlerinin yer aldığı yeni bir cltv dataframe'i oluşturunuz.
# Monetary değeri satın alma başına ortalama değer olarak, recency ve tenure değerleri ise haftalık cinsten ifade edilecek.
cltv = pd.DataFrame()
cltv["customer_id"] = df["master_id"]
cltv["recency_cltv_weekly"] = ((df["last_order_date"] - df["first_order_date"]).dt.days) / 7 # Müşterinin ilk alışverişinden son alışverişine kadar olan süredir. Bu değer müşterinin sistemde ne kadar süredir bulunduğunu gösterir.
cltv["T_weekly"] = ((analysis_date - df["first_order_date"]).dt.days) / 7 #Tenure değeri (müşterinin yaşını verir)
cltv["frequency"] = df["order_num_total"] -1
cltv["monetary_cltv_avg"] = df["customer_value_total"] / df["order_num_total"] #satınalma başına yapılan ortalama kazanç

# Sadece tekrar eden alım yapan müşterileri modele dahil et
cltv = cltv[cltv['frequency'] > 0]

cltv.head()


## GÖREV 3: BG/NBD, Gamma-Gamma Modellerinin Kurulması ve CLTV’nin Hesaplanması
# Adım 1: BG/NBD modelini fit ediniz
bgf = BetaGeoFitter(penalizer_coef=0.001)
bgf.fit(cltv['frequency'],
        cltv['recency_cltv_weekly'],
        cltv['T_weekly'])

# Bu grafik, modelin tahminlerinin gerçek verilerle ne kadar uyumlu olduğunu gösterir.
plot_period_transactions(bgf)
plt.show()

#  3 ay içerisinde müşterilerden beklenen satın almaları tahmin ediniz ve exp_sales_3_month olarak cltv dataframe'ine ekleyiniz.
cltv['exp_sales_3_month'] = bgf.predict(4*3,
                                        cltv['frequency'],
                                        cltv['recency_cltv_weekly'],
                                        cltv['T_weekly'])

#  6 ay içerisinde müşterilerden beklenen satın almaları tahmin ediniz ve exp_sales_6_month olarak cltv dataframe'ine ekleyiniz.
cltv['exp_sales_6_month'] = bgf.predict(4*6,
                                        cltv['frequency'],
                                        cltv['recency_cltv_weekly'],
                                        cltv['T_weekly'])


print("Correlation between frequency and monetary values:")
print(cltv[['frequency', 'monetary_cltv_avg']].corr())
# Korelasyon değeri küçüktür. Yani aralarında bariz bir korelasyon yok.


# Adım 2: Gamma-Gamma modelini fit ediniz. Müşterilerin ortalama bırakacakları değeri tahminleyip exp_average_value olarak cltv dataframe'ine ekleyiniz.
ggf = GammaGammaFitter(penalizer_coef=0.01)
ggf.fit(cltv['frequency'], cltv['monetary_cltv_avg'])
cltv['exp_average_value'] = ggf.conditional_expected_average_profit(cltv['frequency'], cltv['monetary_cltv_avg'])

cltv.head()

# Adım 3: 6 aylık CLTV hesaplayınız ve cltv ismiyle dataframe'e ekleyiniz.
cltv_value = ggf.customer_lifetime_value(bgf, cltv['frequency'], cltv['recency_cltv_weekly'], cltv['T_weekly'],
                                         cltv['monetary_cltv_avg'], time=4*6, freq="W", discount_rate=0.01)
cltv['cltv'] = cltv_value

#  • Cltv değeri en yüksek 20 kişiyi gözlemleyiniz
cltv.sort_values('cltv', ascending=False)[:20]


## GÖREV 4: CLTV Değerine Göre Segmentlerin Oluşturulması
# Adım 1: 6 aylık CLTV'ye göre tüm müşterilerinizi 4 gruba (segmente) ayırınız ve grup isimlerini veri setine ekleyiniz.
cltv['cltv_segment'] = pd.qcut(cltv['cltv'],4, labels=["D", "C", "B", "A"])
cltv.head()


print("Deatiled Analysis of Segments:")
print(cltv.groupby("cltv_segment").agg({
    "cltv": ["mean", "min", "max", "count"],
    "recency_cltv_weekly": "mean",
    "frequency": "mean",
    "monetary_cltv_avg": "mean"
}))