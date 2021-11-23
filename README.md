프로그래머스 스터디를 위한 시간/공간 복잡도 파싱 및 통계화 하였음. (json 및 html 파일로 추출)
# parser4Study

(1) 각 파일은 문제명_이름.py으로 정의합니다.
 ex)
- 딕셔너리 빼기_김무천.py 
- 딕셔너리 빼기_김아무개.py
- 딕셔너리 빼기_이성진.py 

(2) 각각의 .py파일에 주석으로 프로그래머스 채점 결과를 붙여넣습니다.
- 테스트 27 〉	통과 (0.01ms, 10.2MB)
- 테스트 28 〉	통과 (0.01ms, 10.2MB)

(3) 위 파일들은 parser.py와 같은 폴더에 위치해야 합니다.

(4) 커맨드 창에서 문제명과 함께 parser.py를 실행합니다.  
- python parser.py "딕셔너리 빼기"
 
(5) 커맨드 결과 창에 각 풀이자의 시간/공간 복잡도의 평균 점수가 출력되고, json 형식의 원본 데이터와 html 형식의 집계 파일이 해당 폴더에 저장됩니다.

# 샘플 데이터 결과
[json 형식의 원본 데이터]

{
  "name": 
      {"0": "이성진",
       "1": "김무천",
       "2": "김아무개"
       },
  
  "time_complexity": 
      {
       "0": 1.02,
       "1": 0.02,
       "2": 0.04
       },
  "space_complexity":
       {
        "0": 20.5,
        "1": 20.4,
        "2": 20.5
       }
}

[html 형식의 집계 파일]
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>name</th>
      <th>time_complexity</th>
      <th>space_complexity</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1</th>
      <td>김무천</td>
      <td>0.02</td>
      <td>20.4</td>
    </tr>
    <tr>
      <th>2</th>
      <td>김아무개</td>
      <td>0.04</td>
      <td>20.5</td>
    </tr>
    <tr>
      <th>0</th>
      <td>이성진</td>
      <td>1.02</td>
      <td>20.5</td>
    </tr>
  </tbody>
</table>

