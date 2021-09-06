import streamlit as st
import yfinance as yf
import pandas as pd

st.write("""
# Simple 주식 price APP
about GOOGLE \n
## wow신기신기
""")

tickerSymbol = 'GOOGL'
tickerData = yf.Ticker(tickerSymbol)
tikerDF = tickerData.history(period='1d', start='2010-5-31', end='2020-5-31')

st.write("""
# Close
""")
st.line_chart(tikerDF.Close)

st.write("""
# Volume
""")
st.line_chart(tikerDF.Volume)
