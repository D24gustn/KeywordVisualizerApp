# 네이버 검색 API 예제 기반으로 네이버 검색 API 동작 방식 확인 (검색 결과 모두 받기)
# rescode가 200인 동안 start를 증가시켜서 계속 검색 (테스트를 위해 start는 25이하로 제한)
import os
import sys
import urllib.request

client_id = "TAwwP_0w3dKgSO8K6ZV7" 
client_secret = "G1GkcF1B5C"

# 한글 검색어 안전하게 변환
encText = urllib.parse.quote("인공지능")

# url + query 생성
url = "https://openapi.naver.com/v1/search/news?query=" + encText # JSON 결과
start = 1
display = 10
rescode = 200
while rescode == 200 and start < 30:
    # request message 구성
    new_url = url + f"&start={start}&display={display}"
    request = urllib.request.Request(new_url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    
    # request ->response 받아오기
    response = urllib.request.urlopen(request)
    
    # 받아온 결과가 정상인지 확인
    rescode = response.getcode()
    if(rescode==200):
        # 정상이면 데이터 읽어오기
        response_body = response.read()
        # 한글이 있으면 utf-8 decoding
        print(response_body.decode('utf-8'))
    else:
        print("Error Code:" + rescode)
        
    start += display