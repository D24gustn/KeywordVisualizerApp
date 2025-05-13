# STVisualizer.py
#  시각화를 위한 필수 라이브러리 불러오기
import matplotlib.pyplot as plt                         # 그래프 그리기용
from matplotlib import font_manager, rc                # 한글 폰트 설정용
from wordcloud import WordCloud                        # 워드클라우드 생성용
import streamlit as st                                 # Streamlit에 그래프 출력용

font_path = "c:/Windows/Fonts/malgun.ttf"  # 윈도우용 한글 폰트 경로
font_name = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font_name)  # matplotlib에서 한글이 깨지지 않도록 설정

def visualize_barchart(counter, title, xlabel, ylabel, top_n=20):
    most_common = counter.most_common(top_n)       # 상위 단어 n개 추출
    words = [word for word, _ in most_common]      # 단어만 추출
    counts = [count for _, count in most_common]   # 빈도만 추출

    fig, ax = plt.subplots()
    ax.barh(words[::-1], counts[::-1])             # 역순 정렬 (빈도 높은 게 위로)
    ax.set_title(title)                            # 그래프 제목
    ax.set_xlabel(xlabel)                          # x축 라벨
    ax.set_ylabel(ylabel)                          # y축 라벨
    st.pyplot(fig)                                 # Streamlit에서 그래프 출력

def visualize_wordcloud(counter, max_words=100):
    wordcloud = WordCloud(
        font_path=font_path,
        background_color='ivory',                  # 배경 색
        width=800,
        height=400,
        max_words=max_words)                        # 단어 수 제한
    wordcloud = wordcloud.generate_from_frequencies(counter)  # 빈도로부터 생성

    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation='bilinear')  # 부드럽게 이미지 렌더링
    ax.axis("off")                                  # 축 숨김
    st.pyplot(fig)                                  # Streamlit에 출력
