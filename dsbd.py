# Library Import
import streamlit as st, pandas as pd, numpy as np, matplotlib.pyplot as plt, datetime

# Data Import 

## Data : Dividends
n = pd.read_csv('n.csv', encoding = 'EUC-KR')
s = pd.read_csv('s.csv', encoding = 'EUC-KR')
y = pd.read_csv('y.csv', encoding = 'EUC-KR')
d = pd.read_csv('d.csv', encoding = 'EUC-KR')

## Data : Stock Splits
y_splits = pd.read_csv('y_splits.csv', encoding = 'EUC-KR')
d_splits = pd.read_csv('d_splits.csv', encoding = 'EUC-KR')

## Data : Stock Splits
div_cut = pd.read_csv('div_cut.csv', encoding = 'EUC-KR')
div_check = pd.read_csv('div_check.csv', encoding = 'EUC-KR')
total_splits = pd.read_csv('total_splits.csv', encoding = 'EUC-KR')

split_yn = pd.merge(div_cut, total_splits, 'left', '티커')
split_yn = split_yn.loc[(split_yn['배당락일'] >= split_yn['권리락일']) &\
(split_yn['직전_배당락일'] <= split_yn['권리락일'])].reset_index(drop = True)

div_cut.loc[div_cut['티커'].isin(split_yn['티커']), '분할/병합 여부'] = 'Y'
div_cut.loc[~div_cut['티커'].isin(split_yn['티커']), '분할/병합 여부'] = 'N'

div_cut = pd.merge(div_cut, split_yn[['티커', '분할/병합', '권리락일']], 'left', '티커')

# Div cut check
div_cut['구분'] = '기타(오류)'
# div_cut.loc[ (div_cut['분할/병합 여부'] > 0) & (), '구분'] = '분할/병합'
# div_cut.loc[ (div_cut['지급주기 변동'] == 'Y') & (), '구분'] = '분할/병합'

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
	
	st.subheader('배당감소 모니터링\n\n')
	st.caption('🚩 기준 : 조회일자 기준 과거 배당내역 1건 & 다음 배당내역 1건 비교 (단, 다음 배당내역이 없는 경우 과거 배당내역 2건)')
	st.caption('\n✅ 체크리스트\n- 주식분할/병합 여부\n- 배당지급 주기 변동 여부')

	# t1_r1c1, t1_r1c2 = st.columns(2)

	# with t1_r1c1:
	# 	t1_r1c1_sb1 = st.selectbox('배당감소 종목 수 : '+str(len(div_cut))+' 개', ['배당컷', '주기변동', '분할/병합', '기타(오류 등)'])
	
	# with t1_r1c2:
	# 	t1_r1c1_sb1 = st.selectbox('배당감소 종목 수 : '+str(len(div_cut))+' 개', ['배당컷', '주기변동', '분할/병합'])

	t1_r2c1, t1_r2c2 = st.columns(2)

	with t1_r2c1:
		cnt = str(len(div_cut))
		# st.markdown('배당감소 종목 수 : :blue-background{cnt}개')
		st.markdown(
		f"""
		  #### "배당감소 종목 수 : :blue-background{cnt} 개"  
		"""
		)
		
		# st.markdown('''
		#     :red[Streamlit] :orange[can] :green[write] :blue[text] :violet[in]
		#     :gray[pretty] :rainbow[colors] and :blue-background[highlight] text.''')
		st.dataframe(div_cut, hide_index = True, width = 2000, height = 300, column_order = ('티커', '지급주기 변동', '분할/병합 여부', '분할/병합', '권리락일',\
												     '직전_배당락일', '배당락일',\
												     '직전_배당금액_n', '배당금액_n', '직전_배당금액_s', '배당금액_s',\
												     '직전_수정배당금액_d', '수정배당금액_d'))
		
	with t1_r2c2:

		# 각 항목별 건수 Bar chart (주기변동, 분할/병합, 배당컷)
		# chart_data = pd.DataFrame(
		#     {
		#         "감소 사유": list(['주기변동', '분할/병합' ,'배당컷', '기타(오류 등)']),
		#         "종목 수": [0, 0, 0, 6]
		#     }
		# )
		div_cut_count = div_cut.groupby('구분')[['티커']].count().reset_index().rename(columns = {'티커' : '종목 수'})
		st.bar_chart(div_cut_count, x = '구분', y = '종목 수', color = '#F08080')
		

	st.divider()
	# st.subheader('배당내역 불일치 종목\n\n')
	# st.caption('- 배당내역 크롤링 사이트 3곳 모두 해당 내역 존재\n- 주식분할/병합 여부\n- 배당지급 주기 변동 여부')

	# t1_r3c1, t1_r3c2 = st.columns(2)

	# with t1_r3c2:
	# 	t1_r1c1_sb1 = st.selectbox('', ['Nasdaq.com', 'SeekingAlpha' ,'YahooFinance', 'Digrin.com'])
		
	# t1_r4c1, t1_r4c2 = st.columns(2)

	# with t1_r4c1:
	# 	# 각 사이트별 건수 Bar chart ()
	# 	chart_data = pd.DataFrame(
	# 	    {
	# 	        "사이트": list(['Nasdaq.com', 'SeekingAlpha' ,'YahooFinance', 'Digrin.com']),
	# 	        "배당내역 불일치 건수": [3,2,1,1]
	# 	    }
	# 	)
	# 	st.bar_chart(chart_data, x = '사이트', y = '배당내역 불일치 건수', color = '#808080')
		

	# with t1_r4c2:
	# 	st.dataframe(div_check, hide_index = True, width = 2000, height = 300)
	
	# st.subheader('주식 분할/병합 예정 종목\n\n')
	# st.caption('')
	# st.dataframe(total_splits, hide_index = True, width = 2000, height = 200)

	
### 02.배당내역
with tab2:

	# Chart - Upcoming Dividends
	

	
	# Select Box
	t1_r1c1_sb1, t1_r1c2_sb2, t1_r1c3_sb3 = st.columns(3)
	
	with t1_r1c1_sb1:
		t1_r1c1 = st.selectbox('- 사이트', ['Nasdaq.com', 'SeekingAlpha' ,'YahooFinance', 'Digrin.com'])
		if t1_r1c1 == 'Nasdaq.com':
			temp = n.copy()
			y_axis = '배당금액'
		if t1_r1c1 == 'SeekingAlpha':
			temp = s.copy()
			y_axis = '수정배당금액'
		if t1_r1c1 == 'YahooFinance':
			temp = y.copy()
			y_axis = '수정배당금액'
		if t1_r1c1 == 'Digrin.com':
			temp = d.copy()
			y_axis = '수정배당금액'
	
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
		
	st.subheader('(주의 : 특별배당 포함)')
	st.bar_chart(temp, x = '배당락일', y = y_axis, color = '#F08080')
	st.divider()
	st.dataframe(temp, hide_index = True, width = 2000, height = 500)


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
		
	st.line_chart(temp_splits, x = '권리락일', y = '분할/병합', color = '#F08080')
	st.divider()
	st.dataframe(temp_splits, hide_index = True, width = 2000, height = 200)
