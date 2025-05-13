from collections import Counter  # 단어 빈도 계산을 위한 모듈

def load_corpus_from_csv(corpus_file, col_name):
    import pandas as pd
    data_df = pd.read_csv(corpus_file)            # CSV 파일 읽기
    result_list = list(data_df[col_name])         # 원하는 컬럼만 리스트로 추출
    return result_list

def tokenize_korean_corpus(corpus_list, tokenizer, tags, stopwords):
    text_pos_list = []
    for text in corpus_list:
        text_pos = tokenizer(text)                # 예: [('영화', 'Noun'), ('좋다', 'Adjective')]
        text_pos_list.extend(text_pos)            # 전체 문장에서 나온 형태소 모두 수집

    # 특정 품사만 남기고, 불용어 제거
    token_list = [token for token, tag in text_pos_list if tag in tags and token not in stopwords]
    return token_list

def analyze_word_freq(corpus_list, tokenizer, tags, stopwords):
    token_list = tokenize_korean_corpus(corpus_list, tokenizer, tags, stopwords)
    counter = Counter(token_list)  # 단어별 빈도수 계산
    return counter

def visualize_barchart(counter, title, xlabel, ylabel):
    most_common = counter.most_common(20)  # 상위 20개 단어
    word_list = [word for word, _ in most_common]
    count_list = [count for _, count in most_common]

    # 한글 폰트 설정 (맑은 고딕)
    from matplotlib import font_manager, rc
    font_path = "c:/Windows/Fonts/malgun.ttf"
    font_name = font_manager.FontProperties(fname=font_path).get_name()
    rc('font', family=font_name)

    import matplotlib.pyplot as plt

    # 수직 막대 그래프 (단어순 역순으로 출력)
    plt.bar(word_list[::-1], count_list[::-1])
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()

    
def visualize_wordcloud(counter):
    from wordcloud import WordCloud
    import matplotlib.pyplot as plt

    font_path = "c:/Windows/fonts/malgun.ttf"  # 한글 폰트 경로

    wordcloud = WordCloud(font_path,
                          width=600,
                          height=400,
                          max_words=50,
                          background_color='ivory')

    wordcloud = wordcloud.generate_from_frequencies(counter)
    plt.imshow(wordcloud)
    plt.axis('off')  # 축 숨기기
    plt.show()

    