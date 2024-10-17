# Library Import
import streamlit as st, pandas as pd, numpy as np, matplotlib as plt, datetime

# Data Import 

## Data : Dividends
n = pd.read_csv('n.csv', encoding = 'EUC-KR')
s = pd.read_csv('s.csv', encoding = 'EUC-KR')
y = pd.read_csv('y.csv', encoding = 'EUC-KR')
d = pd.read_csv('d.csv', encoding = 'EUC-KR')

## Data : Stock Splits
y_splits = pd.read_csv('y_splits.csv', encoding = 'EUC-KR')
d_splits = pd.read_csv('d_splits.csv', encoding = 'EUC-KR')

## Data Pre-processing
def df_divide(df, gubun):

    df[gubun] = 'Y'

    for i in df.columns:
        if i in ['티커', '배당락일', gubun]:
            continue
        else:
            df = df.rename(columns = {i : i + '_' + gubun})

    f = df[pd.to_datetime(df['배당락일']) > pd.to_datetime(datetime.datetime.today())].reset_index(drop = True).copy()
    p = df[pd.to_datetime(df['배당락일']) <= pd.to_datetime(datetime.datetime.today())].reset_index(drop = True).copy()
    
    return f, p

n_future, n_past = df_divide(n, 'n')
s_future, s_past = df_divide(s, 's')
y_future, y_past = df_divide(y, 'y')
d_future, d_past = df_divide(d, 'd')

def div_unequal(n, s, y, d):

    total_future = \
        pd.merge(d, \
                 pd.merge(y, \
                          pd.merge(n, s, 'outer', ['티커', '배당락일']),\
                          'outer', ['티커', '배당락일']),\
                 'outer', ['티커', '배당락일'])

    # 정기배당만 남김
    total_future = total_future[total_future['배당유형_s'] == 'Regular'].reset_index(drop = True).copy()

    # nasdaq, seekingalpha, digrin 모두 갖고 있는 배당내역인 경우만 추출
    total_future_Y =\
        total_future[(total_future['n'] == 'Y') &
                    (total_future['s'] == 'Y') &
                    (total_future['d'] == 'Y')][total_future.columns.sort_values()].reset_index(drop = True)

def div_unequal(n, s, y, d):

	total_future = \
	pd.merge(d, \
		 pd.merge(y, \
			  pd.merge(n, s, 'outer', ['티커', '배당락일']),\
			  'outer', ['티커', '배당락일']),\
		 'outer', ['티커', '배당락일'])

	# 정기배당만 남김
	total_future = total_future[total_future['배당유형_s'] == 'Regular'].reset_index(drop = True).copy()

	# nasdaq, seekingalpha, digrin 모두 갖고 있는 배당내역인 경우만 추출
	total_future_Y =\
	total_future[(total_future['n'] == 'Y') &
		    (total_future['s'] == 'Y') &
		    (total_future['d'] == 'Y')][total_future.columns.sort_values()].reset_index(drop = True)

	total_future_Y[ ~((total_future_Y['배당금액_n'] == total_future_Y['수정배당금액_s']) &\
		  (total_future_Y['배당금액_n'] == total_future_Y['수정배당금액_d']) &\
		  (total_future_Y['수정배당금액_s'] == total_future_Y['수정배당금액_d']))]



total_splits = pd.merge(y_splits, d_splits, 'outer', ['티커', '권리락일'])
total_splits['분할/병합'] = total_splits['분할/병합_y']
# total_splits[total_splits['분할/병합_x'].isnull(), '분할/병합'] = total_splits['분할/병합_y']
total_splits.loc[total_splits['분할/병합_y'].isnull(), '분할/병합'] = total_splits['분할/병합_x']




# Dashboard 

## Page Full width
st.set_page_config(layout = "wide")

## Dashboard Title
st.title('배당성장주 배당내역 모니터링 대시보드')

## Caption
date = max(d['크롤링 날짜'].max(), n['크롤링 날짜'].max(), s['크롤링 날짜'].max(), y['크롤링 날짜'].max())
st.caption('(' + str(date) + ' 기준, 매일 정오 업데이트)')

## Tab name list
t = ['01.모니터링' , '02.배당내역', '03.분할/병합내역']

## Tabs
tab1, tab2, tab3 = st.tabs(t)

### 01.홈
with tab1:
	
	st.subheader('배당감소 의심 종목\n\n')
	st.caption('- 배당내역 크롤링 사이트 3곳 모두 해당 내역 존재\n- 주식분할/병합 여부\n- 배당지급 주기 변동 여부')
	st.dataframe(n, hide_index = True, width = 2000, height = 1000)

	st.subheader('배당내역 불일치 종목\n\n')
	st.caption('')
	
	st.subheader('주식 분할/병합 예정 종목\n\n')
	st.caption('')
	
### 02.배당내역
with tab2:

	# Chart - Upcoming Dividends
	

	
	# Select Box
	t1_r1c1_sb1, t1_r1c2_sb2, t1_r1c3_sb3 = st.columns(3)
	
	with t1_r1c1_sb1:
		t1_r1c1 = st.selectbox('- 사이트', ['Nasdaq.com', 'SeekingAlpha' ,'YahooFinance', 'Digrin.com'])
		if t1_r1c1 == 'Nasdaq.com':
			temp = n.copy()
		if t1_r1c1 == 'SeekingAlpha':
			temp = s.copy()
		if t1_r1c1 == 'YahooFinance':
			temp = y.copy()
		if t1_r1c1 == 'Digrin.com':
			temp = d.copy()
	
	with t1_r1c2_sb2:

		# Only User choose WebSite above
		if len(t1_r1c1) > 0:
		
			stock_select = ['전체']
			for x in range(ord('A'), ord('Z') + 1):
			    stock_select.append(chr(x))
			t1_r1c2 = st.selectbox('- 알파벳(티커 첫글자)', stock_select)

			if t1_r1c2 != '전체':
				temp = temp[temp['티커'].str[0] == t1_r1c2].reset_index(drop = True).copy()

		else:
			st.selectbox('- 알파벳', '사이트를 선택해주세요.')
	
	with t1_r1c3_sb3:

		t1_r1c3 = st.selectbox('- 티커', pd.unique(temp['티커']))
		temp = temp[temp['티커'] == t1_r1c3].reset_index(drop = True).copy()

	st.dataframe(temp, hide_index = True, width = 2000, height = 1000)


### 03.분할/병합내역
with tab3:

	# Select Box
	t3_r1c1_sb1, t3_r1c2_sb2, t3_r1c3_sb3 = st.columns(3)

	with t3_r1c1_sb1:
		t3_r1c1 = st.selectbox('- 사이트', ['YahooFinance', 'Digrin.com'])
		if t3_r1c1 == 'YahooFinance':
			temp_splits = y_splits.copy()
		if t3_r1c1 == 'Digrin.com':
			temp_splits = d_splits.copy()
	
	with t3_r1c2_sb2:

		# Only when user choose WebSite above
		if len(t3_r1c1) > 0:
		
			stock_select = ['전체']
			for x in range(ord('A'), ord('Z') + 1):
			    stock_select.append(chr(x))
			t3_r1c2 = st.selectbox('- 알파벳', stock_select)

			if t3_r1c2 != '전체':
				temp_splits = temp_splits[temp_splits['티커'].str[0] == t3_r1c2].reset_index(drop = True).copy()

		else:
			st.selectbox('- 알파벳', '사이트를 선택해주세요.')
	
	with t3_r1c3_sb3:

		t3_r1c3 = st.selectbox('- 티커', pd.unique(temp_splits['티커']))
		temp_splits = temp_splits[temp_splits['티커'] == t3_r1c3].sort_values(['티커', '권리락일'], ascending = [True, False]).reset_index(drop = True).copy()

	st.dataframe(temp_splits, hide_index = True, width = 2000, height = 300)
