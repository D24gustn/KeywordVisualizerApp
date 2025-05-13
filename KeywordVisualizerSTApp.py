#  필요한 라이브러리 import
import streamlit as st                    # 웹 인터페이스를 위한 streamlit
import pandas as pd                      # 데이터프레임 처리용
from konlpy.tag import Okt               # 형태소 분석기
from collections import Counter          # 단어 빈도 계산용
import lib.naverNewsCrawler as nnc       # 뉴스 검색 라이브러리
import lib.myTextMining as tm            # 형태소 분석 및 빈도 분석 라이브러리
import lib.STVisualizer as vis           # 시각화 라이브러리 (Streamlit용)

st.title(" 키워드 기반 뉴스 시각화 앱")

# --- 상태 변수 초기화 ---
if 'data' not in st.session_state:
    st.session_state['data'] = None

# --- 사이드바 입력 ---
st.sidebar.header("파일 선택")
uploaded_file = st.sidebar.file_uploader("Drag and drop file here", type=["csv"])  # 파일 업로드

st.sidebar.markdown("또는")
keyword = st.sidebar.text_input("뉴스 키워드 검색")  # 키워드 직접 입력

# --- 뉴스 검색 처리 ---
if keyword and st.sidebar.button("뉴스 검색"):
    resultAll = []
    start = 1
    display = 10
    resultJSON = nnc.searchNaverNews(keyword, start, display)

    while (resultJSON is not None) and (resultJSON['display'] > 0) and (start <= 1000):
        nnc.setNewsSearchResult(resultAll, resultJSON)     # 뉴스 결과 리스트에 저장
        start += resultJSON['display']
        if start > 1000:
            break
        resultJSON = nnc.searchNaverNews(keyword, start, display)

    data_df = pd.DataFrame(resultAll)  # 결과 DataFrame으로 변환
    nnc.saveSearchResult_CSV(resultAll, f"./data/{keyword}_naver_news.csv")  # CSV 저장
    st.session_state['data'] = data_df  # 세션에 저장
    st.success(f"{keyword} 뉴스 {len(data_df)}건 검색 완료")

# --- CSV 파일 업로드 처리 ---
elif uploaded_file is not None:
    data_df = pd.read_csv(uploaded_file)
    st.session_state['data'] = data_df
    st.success(f"CSV 파일 로딩 완료! 총 {len(data_df)}개 문서")

# --- 데이터 확인 및 분석 ---
data = st.session_state['data']

if data is not None:
    col_name = st.text_input("데이터가 들어있는 컬럼명", value="description")

    if col_name in data.columns:
        corpus = list(data[col_name].dropna())  # 결측값 제거한 텍스트 리스트

        st.sidebar.header("설정")

        show_bar = st.sidebar.checkbox("🌟 빈도수 그래프", value=True)
        bar_word_count = st.sidebar.slider("단어 수 (그래프)", 10, 50, 20)

        show_cloud = st.sidebar.checkbox("☁️ 워드클라우드", value=True)
        cloud_word_count = st.sidebar.slider("단어 수 (워드클라우드)", 20, 500, 100)

        if st.sidebar.button("분석 시작"):
            tokenizer = Okt().pos  # 형태소 분석기
            tags = ['Noun', 'Adjective', 'Verb']  # 사용할 품사
            stopwords = ['하며', '입', '하고', '로써', '하여', '애', '제', '한다', '그', '이', '할', '정', '수']  # 불용어

            counter = tm.analyze_word_freq(corpus, tokenizer, tags, stopwords)

            if show_bar:
                vis.visualize_barchart(counter, "키워드 빈도수", "빈도수", "단어", top_n=bar_word_count)

            if show_cloud:
                vis.visualize_wordcloud(counter, max_words=cloud_word_count)
    else:
        st.warning(f"⚠️ '{col_name}' 컬럼이 데이터에 없습니다.")
else:
    st.info("왼쪽 사이드바에서 CSV 업로드 또는 키워드를 입력해 주세요.")
