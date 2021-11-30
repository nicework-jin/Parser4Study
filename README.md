### 프로그램 목적

프로그래머스 스터디를 위한 시간/공간 복잡도 파싱 및 통계화 하였음. (json 및 html 파일로 추출)

### 파이썬 버전 / 설치해야 하는 라이브러리

- Python 3.8
- Pandas

### 대상 파일

1. 프로그래머스 풀이 파일

2. 파일 형식: 문제명_이름.py 
- 딕셔너리 빼기_김무천.py
- 딕셔너리 빼기_김아무개.py
- 딕셔너리 빼기_이성진.py

3. 파일 내용: 프로그래머스 결과로 시간/공간 복잡도가 들어간 파일<br>
--------------------------------- <br>
테스트 27 〉	통과 (0.01ms, 10.2MB) <br> 
테스트 28 〉	통과 (0.01ms, 10.2MB) <br> 
테스트 28 〉	통과 (0.01ms, 10.2MB) <br>
--------------------------------- 


## parser.py (한 문제씩 파싱하기)
1. [parser.py]가 위치한 폴더로 이동한 후 [cmd]에 2번 또는 3번과 같이 입력합니다.

2. [현재 폴더]에 "딕셔너리 빼기" 문제가 있는 경우
- python parser.py "딕셔너리 빼기"

3. [~/AlgorithmStudy_211124/211130/] 경로의 폴더에 "딕셔너리 빼기"문제가 있는 경우
- python parser.py "딕셔너리 빼기" ~/AlgorithmStudy_211124/211130/

4. 출력 결과는 [parser.py]이 위치한 경로에 두 파일로 저장됩니다.
- "./result/문제명/문제명.json"
- "./result/문제명/문제명.html"

![image](https://user-images.githubusercontent.com/42059680/143489072-f463cb75-be74-4d7e-b198-4b8e73627145.png)


## multiple_parer.py (지정한 경로에 모든 문제 파싱하기)

1. [multiple_parser.py]와 [parser.py]가 위치한 폴더로 이동합니다.

2. cmd에 다음과 같이 입력합니다.
- python multiple_parser.py ~/AlgorithmStudy_211124/211130/

3. 출력 결과는 [multiple_parser.py]가 위치한 경로에 세 폴더로 나뉘어 저장됩니다.
- "./result/문제명01/문제명01.html", "./result/문제명02/문제명02.html" , ...
- "./result/문제명01/문제명01.json", "./result/문제명02/문제명02.json", ...
- "./result/html/연월일.html"
    - 여러 개의 html 파일을 하나로 묶은 파일입니다. 

![image](https://user-images.githubusercontent.com/42059680/143489429-37f591cf-6740-4e5a-ac4d-007f1eeba9b0.png)

### 버전 업데이트 정보
#### version 1. 
> parser.py 개발
- 개별 문제에 대해 시간/공간 복잡도를 계산함.

#### version 2.
> parser.py의 사용 범위 확장
- 기존에는 parser.py과 동일한 위치에 있는 문제만 파싱이 가능했는데, 다른 경로에 문제도 파싱이 가능해짐. 
  
> multiple_parser.py 기능 추가
- parser.py를 이용하여 특정 경로에 위치한 "모든 문제"를 파싱함
 
#### version 2.5
> 검색어에 대한 유연성 제공
- 띄어쓰기 
- 영어 대소문자
- "이중 순위 큐.py"를 실수로 "이중순위.py"로 저장한 경우를 고려하여 두 결과를 가까운 위치에 배치
- "가장 큰 수 != "가장 큰 수"인 현상 해결 <a href="https://github.com/nicework-jin/StudyOrTest/blob/main/Python/같은%20두%20한글이%20다르다고%20할%20때.py"> - [링크]</a>
