"""
- 터미널에서 작업할 때는 파이썬 가상 환경으로 설정한 sandbox를 활성화 시키고 명령한다.
source ~/sandbox/bin/activate

- ask를 작성하고 테스트 할 수 있다.
airflow tasks test DAG_id task_id start_date
"""


from logging import log
from airflow.models import DAG
"""
사용하려는 Operator는 airflow 공식 문서에서 찾아서 설치할 수 있다.
  - Airflow 2.0 이전에는 새로운 버전의 operator를 추가하기 위해 Airflow를 업데이트 해야했지만 이제는 따로 설치할 수 있다.
  - 라이브러리를 설치하고, task를 정의한 다음에 UI의 connection으로 가서 새로운 connection을 정의한다.
   이때, Conn Type으로 라이브러리 설치를 통해 생겨난 타입을 선택한다.
  - Conn Type으로 새로운 타입이 안생기는 오류가 발생할 수 있다. 
   이 때는 webserver와 scheduler를 재시작하면 UI의 connection -> add -> Conn Type에 새로운 타입이 생긴다.
"""
from airflow.providers.sqlite.operators.sqlite import SqliteOperator
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.http.operators.http import SimpleHttpOperator


# PythonOperator는 Airflow를 설치할 때 기본으로 포함되어 있다. 그래서 airflow.providers가 아닌! airflow.operators로 시작한다.
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator

from pandas import json_normalize
from datetime import datetime
import json


"""
1. AirFlow에서 기본 시간은 UTC를 따른다.
airflow.cfg에서 UI 및 기본 timezone을 변경할 수는 있지만, UTC로 두는 것을 추천한다
UTC를 기본으로 두고, 현지 시각을 UTC로 계산해서 두는 것이 낫다!

2. 시작 시간이 2021/1/1 10:00이고 time interval이 10분이라면, Dag이 처음 시작되는 시간은 2021/1/1 10:10이다.
"""
default_args = {
    'start_date': datetime(2021, 12, 13)
}


def _processing_user(ti):
    """
    - /airflow/sample_data에 원본 샘플 데이터 뒀음. 참고해서 코드 분석할 것.
    - task 인스턴스를 통해 Xcom에 접근할 수 있다. 여기에서는 xcom에 있는 데이터를 가져오는 하는 함수를 사용했다.
    - Xcom은 태스크 간에 데이ㅣ터를 공유하는 장소라고 생각하면 된다.
    """
    users = ti.xcom_pull(task_ids=['extracting_user'])
    if not len(users) or not 'results' in users[0]:
        raise ValueError("User is empty")

    user = users[0]['results'][0]
    processed_user = json_normalize({
        "firstname":user['name']['first'],
        'lastname':user['name']['last'],
        'country':user['location']['country'],
        'username':user['login']['username'],
        'password':user['login']['password'],
        'email':user['email']
    })

    processed_user.to_csv('/tmp/processed_user.csv', header=False, index=None)
    return

"""
catchup 인자는 backfill을 위해 사용된다.
catchup의 인자는 기본 값으로 True를 갖는다.

만약 2020년 1월 1일부터 매일 트리거 되는 DAG이 있다고 가정해보자.
1월 3일에 DAG을 중지 했다면 다시 시작할 때까지 트리거되지 않을 것이다.
1월 10일에 DAG을 재시작 했다면, AirFlow는 3일부터 10일에 시작되지 않았던 DAG을 순차대로 트리거한다.

여러 개의 DAG이 작동 또는 작동 예정인 것을 보기 위해서는 UI의 Tree view 우측 그래프를 확인하면 된다.
"""
with DAG('user_processing', schedule_interval='@daily',
    default_args=default_args,
    catchup=False) as dag:

    creating_table = SqliteOperator(
        task_id='creating_table',
        sqlite_conn_id='db_sqlite',
        sql='''
            CREATE TABLE IF NOT EXISTS users (
                firstname TEXT NOT NULL,
                lastname TEXT NOT NULL,
                country TEXT NOT NULL,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                email TEXT NOT NULL PRIMARY KEY
            );
        '''

    )

    """
    Sensor는 상태를 나타내는 Operator다. 예를 들어, 특정 경로의 폴더에 파일이 생겼는지를 확인한다.
    여기서 정의한 task는 user_api가 사용 가능한지 확인하는 용도다.

    http_conn_id는 요청보낼 url을 의미한다. UI의 connection에서 정의할 수 있다.
    UI에 http_conn_id를 정의하면 해당 url의 endpoint인 'api/'로 요청을 보낸다.
    """
    is_api_available = HttpSensor(
        task_id='is_api_available',
        http_conn_id='user_api',
        endpoint='api/'
    )

    """
    logs_response는 로그로 응답 내용을 나타냄.
    """
    extracting_user = SimpleHttpOperator(
        task_id = 'extracting_user',
        http_conn_id = 'user_api',
        endpoint = 'api/',
        method = 'GET',
        response_filter = lambda response: json.loads(response.text),
        log_response = True
    )
    
    """
    - python_callable에 호출할 파이썬 함수명을 넣는다. 
    """
    processing_user = PythonOperator(
        task_id = 'processing_user',
        python_callable=_processing_user
    )


    """
    /tmp/processed_user.csv를 읽어서 쉼표를 구분자로 데이터 추출한다. 
    /home/airflow/airflow/airflow.db의 users 테이블에 데이터를 넣는다.
    """
    storing_user = BashOperator(
        task_id = 'storing_user',
        bash_command='echo -e ".separator ","\n.import /tmp/processed_user.csv users" | sqlite3 /home/airflow/airflow/airflow.db'
    )

    """
    Task의 실행 순서 정하기!
    '>>'로 Dependancy를 정의할 수 있다.
    UI의 graph view에서 각각의 태크스가 화살표로 표시된다.
    """
    creating_table >> is_api_available >> extracting_user >> processing_user >> storing_user