import streamlit as st, pandas as pd, numpy as np, matplotlib as plt


st.title("미국 배당성장주 배당내역 크롤링 모니터링 대시보드")

n = pd.read_csv('n.csv', encoding = 'EUC-KR').groupby('티커').head(5).copy()
s = pd.read_csv('s.csv', encoding = 'EUC-KR').groupby('티커').head(5).copy()
y = pd.read_csv('y.csv', encoding = 'EUC-KR').groupby('티커').head(5).copy()
d = pd.read_csv('d.csv', encoding = 'EUC-KR').groupby('티커').head(5).copy()

# details = pd.read_csv('update_details.csv', encoding = 'EUC-KR')




st.dataframe(n)
st.dataframe(s)
st.dataframe(y)
st.dataframe(d)


