import urllib.request
import json

#  네이버 뉴스 검색 API를 호출해서 결과를 가져오는 함수
def searchNaverNews(keyword, start, display):
    # 네이버 개발자 센터에서 발급받은 클라이언트 ID, 시크릿
    client_id = "TAwwP_0w3dKgSO8K6ZV7" 
    client_secret = "G1GkcF1B5C"

    #  검색어가 한글일 경우 깨지지 않도록 URL 인코딩
    encText = urllib.parse.quote(keyword)

    #  API 요청용 URL 생성
    url = "https://openapi.naver.com/v1/search/news?query=" + encText
    new_url = url + f"&start={start}&display={display}"  # 페이지 시작 번호, 가져올 뉴스 개수 설정

    #  API 요청 객체 생성
    request = urllib.request.Request(new_url)
    request.add_header("X-Naver-Client-Id", client_id)           # 인증 헤더 추가
    request.add_header("X-Naver-Client-Secret", client_secret)

    resultJSON = None  # 결과 저장할 변수

    try:
        # 요청을 보내고 응답 받기
        response = urllib.request.urlopen(request)
        rescode = response.getcode()  # HTTP 응답 코드 확인

        if rescode == 200:
            # 응답이 200이면 성공 → 데이터 읽고 JSON 파싱
            response_body = response.read()
            resultJSON = json.loads(response_body.decode('utf-8'))
        else:
            print("Error Code:" + rescode)
    except Exception as e:
        # 에러 발생 시 메시지 출력
        print(e)
        print(f"Error : {new_url}")

    return resultJSON  # JSON 형태의 결과 리턴

#  JSON 데이터에서 뉴스 항목만 추출하여 리스트에 추가
def setNewsSearchResult(resultAll, resultJSON):
    for result in resultJSON['items']:
        resultAll.append(result)  # resultAll은 리스트, JSON의 'items' 안 뉴스 하나씩 추가


#  수집한 뉴스 데이터를 CSV 파일로 저장
def saveSearchResult_CSV(json_list, filename):
    import pandas as pd
    data_df = pd.DataFrame(json_list)     # 리스트를 DataFrame으로 변환
    data_df.to_csv(filename)              # CSV 파일로 저장
    print(f"{filename} SAVED")            # 저장 완료 메시지 출력