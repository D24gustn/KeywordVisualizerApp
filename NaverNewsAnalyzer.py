# 필요한 모듈과 사용자 정의 라이브러리 불러오기
import lib.naverNewsCrawler as nnc       # 뉴스 검색 및 저장 기능
import lib.myTextMining as tm            # 형태소 분석, 빈도 분석, 시각화 기능
from konlpy.tag import Okt               # 형태소 분석기 (Okt)

# 사용자로부터 검색어 입력받기 (예: 인공지능)
keyword = input("검색어 : ").strip()

resultAll = []             # 수집된 뉴스 결과 저장할 리스트
start = 1                  # 검색 시작 위치
display = 10               # 한 번에 가져올 뉴스 수
resultJSON = nnc.searchNaverNews(keyword, start, display)  # 첫 요청

# 최대 1000개까지 반복해서 뉴스 수집
while (resultJSON is not None) and (resultJSON['display'] > 0) and (start <= 1000):
    nnc.setNewsSearchResult(resultAll, resultJSON)  # 뉴스 결과 리스트에 저장

    start += resultJSON['display']  # 다음 페이지로 이동
    if start > 1000:
        break  # 1000개 넘으면 종료

    resultJSON = nnc.searchNaverNews(keyword, start, display)  # 다음 뉴스 요청

    # 요청 결과 상태 출력
    if resultJSON is not None:
        print(f"{keyword} [{start}] : Search Request Success")
    else:
        print(f"{keyword} [{start}] : Error ~~~~")

# 3. CSV 저장
filename = f"./data/{keyword}_naver_news.csv"  # 저장할 파일 경로
nnc.saveSearchResult_CSV(resultAll, filename)  # 파일 저장

# 4. CSV 불러오기
corpus_list = tm.load_corpus_from_csv(filename, "description")  # 'description' 컬럼 텍스트만 불러옴
print("🔹 상위 10개 뉴스 설명:")
print(corpus_list[:10])  # 앞 10개만 확인

# 5. 형태소 분석기 설정
my_tokenizer = Okt().pos                     # 형태소 분석기: POS 태깅 포함
my_tags = ['Noun', 'Adjective', 'Verb']      # 명사, 형용사, 동사만 사용
my_stopwords = ['하며', '입', '하고', '로써', '하여', '애', '제', '한다', '그', '이', '할', '정', '수']  # 불용어

# 6. 단어 빈도 분석
counter = tm.analyze_word_freq(corpus_list, my_tokenizer, my_tags, my_stopwords)  # 분석 수행
print("🔹 단어 빈도 상위 20개:")
print(list(counter.items())[:20])  # 상위 20개 출력

# 7. 시각화
tm.visualize_barchart(counter, "뉴스 키워드 분석", "빈도수", "키워드")      # 수평 막대 그래프
tm.visualize_wordcloud(counter) # 워드클라우드
