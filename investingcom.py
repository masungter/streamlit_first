import requests
from bs4 import BeautifulSoup
import pandas as pd
from html_table_parser import parser_functions as parser
import streamlit as st
from dateutil.parser import parse
from datetime import date

formdata = {
        "curr_id": "8827",
        "smlID": "400001",
        "header": "US Dollar Index Futures Historical Data",
        "st_date": "01/30/2019",
        "end_date": "09/01/2021",
        "interval_sec": "Daily",
        "sort_col": "date",
        "sort_ord": "DESC",
        "action":"historical_data"
    }

today = date.today()
today = "{}/{}/{}".format(today.month,today.day,today.year)

@st.cache
def crawling_investing(formdata):
    url = 'https://www.investing.com/instruments/HistoricalDataAjax'

    headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'X-Requested-With' : 'XMLHttpRequest'
    }

    r = requests.post(url, data=formdata, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    containers = soup.find('table', {'id' : "curr_table"})

    table = parser.make2d(containers)
    df = pd.DataFrame(table[1:], columns=table[0])

    #날짜 형 조정하기
    days=[]
    for i in df['Date']:
        days.append(parse(i).date())
    df['Date'] = days
    df = df.set_index(['Date'])

    df['Price'] = df['Price'].apply(lambda x: x.replace(',', '')).astype('float')
    df['Open'] = df['Open'].apply(lambda x: x.replace(',', '')).astype('float')
    df['High'] = df['High'].apply(lambda x: x.replace(',', '')).astype('float')
    df['Low'] = df['Low'].apply(lambda x: x.replace(',', '')).astype('float')

    return df

@st.cache
def dollar_index(cal_date):
    formdata["end_date"] = today
    formdata["curr_id"] = "942611"
    formdata["smlID"] = "2067751"
    formdata["header"] = "US Dollar Index Historical Data"

    dollar_index = crawling_investing(formdata)
    dollar_index_from_cal_date = dollar_index.loc[:cal_date]

    return dollar_index_from_cal_date

@st.cache
def usd_currency(cal_date):
    formdata["end_date"] = today
    formdata["curr_id"] = "650"
    formdata["smlID"] = "106816"
    formdata["header"] = "USD/KRW Historical Data"

    usd_currency = crawling_investing(formdata)
    usd_currency_from_cal_date = usd_currency.loc[:cal_date]
    return usd_currency_from_cal_date



def last_dollar_index():
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Content-Type': 'text/html; charset=utf-8'
    }
    response = requests.get("https://www.investing.com/indices/usdollar", headers=headers)
    content = BeautifulSoup(response.content, 'html.parser')
    containers = content.find('span', {'data-test': 'instrument-price-last'})
    current_dollar_index = containers.text

    return current_dollar_index

def last_usd_currency():
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Content-Type': 'text/html; charset=utf-8'
    }
    response = requests.get("https://www.investing.com/currencies/usd-krw", headers=headers)
    content = BeautifulSoup(response.content, 'html.parser')
    containers = content.find('span', {'id': 'last_last'})
    current_dollar_index = containers.text
    
    return current_dollar_index
