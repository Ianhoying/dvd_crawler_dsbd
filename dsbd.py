import streamlit as st, pandas as pd, numpy as np, matplotlib as plt

# Data Import

## Dividends
n = pd.read_csv('n.csv', encoding = 'EUC-KR').groupby('티커').head(5).copy()
s = pd.read_csv('s.csv', encoding = 'EUC-KR').groupby('티커').head(5).copy()
y = pd.read_csv('y.csv', encoding = 'EUC-KR').groupby('티커').head(5).copy()
d = pd.read_csv('d.csv', encoding = 'EUC-KR').groupby('티커').head(5).copy()

## Stock Splits
y_splits = pd.read_csv('y_splits.csv', encoding = 'EUC-KR')
d_splits = pd.read_csv('d_splits.csv', encoding = 'EUC-KR')



# Dashboard 

## Page Full width
st.set_page_config(layout = "wide")

## Dashboard Title
st.title('배당성장주 배당내역 모니터링 대시보드')

# 탭명
t = ['01.홈' , '02.배당내역', '03.분할/병합내역']

# 대시보드 항목별 탭 분리 생성
tab1, tab2, tab3 = st.tabs(t)

with tab1:

with tab2:
  st.dataframe(n)
  st.dataframe(s)
  st.dataframe(y)
  st.dataframe(d)
with tab3:
  st.dataframe(y_splits)
  st.dataframe(d_splits)
