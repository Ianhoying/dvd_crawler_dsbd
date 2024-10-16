# Library Import
import streamlit as st, pandas as pd, numpy as np, matplotlib as plt, datetime

# Data Import 

## Dividends
n = pd.read_csv('n.csv', encoding = 'EUC-KR')
s = pd.read_csv('s.csv', encoding = 'EUC-KR')
y = pd.read_csv('y.csv', encoding = 'EUC-KR')
d = pd.read_csv('d.csv', encoding = 'EUC-KR')

## Stock Splits
y_splits = pd.read_csv('y_splits.csv', encoding = 'EUC-KR')
d_splits = pd.read_csv('d_splits.csv', encoding = 'EUC-KR')



# Dashboard 

## Page Full width
st.set_page_config(layout = "wide")

## Dashboard Title
st.title('배당성장주 배당내역 모니터링 대시보드')

## Caption
date = max(d['크롤링 날짜'].max(), n['크롤링 날짜'].max(), s['크롤링 날짜'].max(), y['크롤링 날짜'].max())
st.caption('(' + str(date) + ' 기준, 매일 정오 업데이트)')

## Tab name list
t = ['01.홈' , '02.배당내역', '03.분할/병합내역']

## Tabs
tab1, tab2, tab3 = st.tabs(t)

### 01.홈
with tab1:
	
	st.subheader('배당감소 의심 종목\n\n')

	st.subheader('배당내역 불일치 종목\n\n') 
	
	st.subheader('주식 분할/병합 예정 종목\n\n')
	
### 02.배당내역
with tab2:
	# Select Box
	t1_r1c1_sb1, t1_r1c2_sb2, t1_r1c3_sb3 = st.columns(3)
	
	with t1_r1c1_sb1:
		r1c1 = st.selectbox('- 사이트', ['Nasdaq.com', 'SeekingAlpha' ,'YahooFinance', 'Digrin.com'])
		if r1c1 == 'Nasdaq.com':
			temp = n.copy()
		if r1c1 == 'SeekingAlpha':
			temp = s.copy()
		if r1c1 == 'YahooFinance':
			temp = y.copy()
		if r1c1 == 'Digrin.com':
			temp = d.copy()
	
	with t1_r1c2_sb2:

		# Only User choose WebSite above
		if len(r1c1) > 0:
		
			stock_select = ['전체']
			for x in range(ord('A'), ord('Z') + 1):
			    stock_select.append(chr(x))
			r1c2 = st.selectbox('- 알파벳', stock_select)

			if r1c2 != '전체':
				temp = temp[temp['티커'].str[0] == r1c2].reset_index(drop = True).copy()

		else:
			st.selectbox('- 알파벳', '사이트를 선택해주세요.')
	
	with t1_r1c3_sb3:
		if r1c2 != '전체':
			r1c3 = st.selectbox('- 티커', pd.unique(temp['티커']))
			temp = temp[temp['티커'] == r1c3].reset_index(drop = True).copy()

	st.dataframe(temp, hide_index = True, width = 2000, height = 1000)


### 03.분할/병합내역
with tab3:
	st.subheader('Yahoo Finance')   
	st.dataframe(y_splits, hide_index = True, width = 2000, height = 300)
	st.subheader('\n\n') 
	st.subheader('Digrin')   
	st.dataframe(d_splits, hide_index = True, width = 2000, height = 300)
