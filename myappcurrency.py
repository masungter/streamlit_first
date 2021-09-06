import streamlit as st
from datetime import timedelta
import datetime
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from investingcom import *

#사이드바
st.sidebar.header('Choose')
my_button = st.sidebar.radio("기간", ('1주','1달','1분기','반년','1년'))

cal_date = date.today() - timedelta(days=365)
if my_button == '1주':
    cal_date = date.today() - timedelta(days=7)
elif my_button == '1달':
    cal_date = date.today() - timedelta(days=30)
elif my_button == '1분기':
    cal_date = date.today() - timedelta(days=91)
elif my_button == '반년':
    cal_date = date.today() - timedelta(days=183)
else:
    cal_date = date.today() - timedelta(days=365)


last_dollar_index = float(last_dollar_index())
df_dollar_index = dollar_index(cal_date)
df_dollar_index = df_dollar_index.sort_index(ascending=False)
st.write('''# 달러 인덱스 : {:.2f} ({:.2f}%)'''.format(last_dollar_index, (last_dollar_index-df_dollar_index['Price'].mean())/df_dollar_index['Price'].mean()*100 ))
st.write("min: {:.2f}, mean: {:.2f}, max: {:.2f}".format(df_dollar_index['Price'].min(), df_dollar_index['Price'].mean(), df_dollar_index['Price'].max()))

fig, ax = plt.subplots(figsize=(12, 2))
N, bins, patches = ax.hist(df_dollar_index['Price'], bins=20)
for bin_size, bin, patch in zip(N, bins, patches):
    if bin < df_dollar_index.iloc[0,0]:
        patch.set_facecolor("#ffe17d")
    elif bin > df_dollar_index.iloc[0,0]:
        patch.set_facecolor("#80b9ff")
ax.bar(df_dollar_index.iloc[0,0],max(N), color="#0000FF", width=0.1, alpha=0.1, label='today')
plt.legend()
st.pyplot(fig)

fig = plt.figure(figsize=(12, 2))
ax = plt.boxplot(df_dollar_index['Price'], whis=1, vert=False)
ax = plt.bar(df_dollar_index.iloc[0,0],2, color="#0000FF", width=0.1, alpha=0.1)
plt.ylim([0.8, 1.2])
st.pyplot(fig)


st.markdown("""---""")


last_usd_currency = float(last_usd_currency().replace(',',''))
df_usd_currency = usd_currency(cal_date)
df_usd_currency = df_usd_currency.sort_index(ascending=False)
st.write('''# 달러 환율 : {:.2f} ({:.2f}%)'''.format(last_usd_currency, (last_usd_currency-df_usd_currency['Price'].mean())/df_usd_currency['Price'].mean()*100 ))
st.write("min: {:.2f}, mean: {:.2f}, max: {:.2f}".format(df_usd_currency['Price'].min(), df_usd_currency['Price'].mean(), df_usd_currency['Price'].max()))

fig, ax = plt.subplots(figsize=(12, 2))
N, bins, patches = ax.hist(df_usd_currency['Price'], bins=20)
for bin_size, bin, patch in zip(N, bins, patches):
    if bin < df_usd_currency.iloc[0,0]:
        patch.set_facecolor("#ffe17d")
    elif bin > df_usd_currency.iloc[0,0]:
        patch.set_facecolor("#80b9ff")
ax.bar(df_usd_currency.iloc[0,0],max(N), color="#0000FF", width=1, alpha=0.1, label='today')
plt.legend()
st.pyplot(fig)

fig = plt.figure(figsize=(12, 2))
ax = plt.boxplot(df_usd_currency['Price'], whis=1, vert=False)
ax = plt.bar(df_usd_currency.iloc[0,0],2, color="#0000FF", width=1, alpha=0.1)
plt.ylim([0.8, 1.2])
st.pyplot(fig)


st.markdown("""---""")


dollar_gap = pd.DataFrame()
dollar_gap['Gap'] = df_dollar_index['Price'] / df_usd_currency['Price'] * 100
dollar_gap = dollar_gap.sort_index(ascending=False)
st.write('''# 달러 갭 : {:.3f} ({:.3f}%)'''.format(dollar_gap.iloc[0,0], (dollar_gap.iloc[0,0]-dollar_gap['Gap'].mean())/dollar_gap['Gap'].mean()*100 ))
st.write("min: {:.2f}, mean: {:.2f}, max: {:.2f}".format(dollar_gap['Gap'].min(), dollar_gap['Gap'].mean(), dollar_gap['Gap'].max()))

fig = plt.figure(figsize=(12, 2))
ax = plt.plot(dollar_gap['Gap'])
plt.axhline(y=dollar_gap['Gap'].mean(), color='r', linewidth=0.5)
plt.ylim([dollar_gap['Gap'].min()*0.999, dollar_gap['Gap'].max()*1.001])
plt.grid(True)
st.pyplot(fig)
