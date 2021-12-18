from airflow.models import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta

meet_date = datetime.today()
while meet_date.weekday() != 1:
    meet_date += timedelta(days=1)
meet_date = meet_date.strftime('%y%m%d')

default_args = {
    'start_date': datetime(2021, 12, 18)
}

with DAG('rank_update', schedule_interval='*/10 * * * *',
    default_args=default_args,
    catchup=False) as dag:

    pull_from_git = BashOperator(
        task_id = 'pull_from_git',
        bash_command='git -C /home/airflow/AlgorithmStudy_211124 pull'
    )    

    make_indicator = BashOperator(
        task_id = 'make_indicator',
        bash_command=f'python3 /home/airflow/parser4Study/multiple_parser.py /home/airflow/AlgorithmStudy_211124/{meet_date}/'
    )   

    mv_indicator_to_repo = BashOperator(
        task_id = 'mv_indicator_to_repo',
        bash_command=f'mv /tmp/result/html/rank.html /home/airflow/AlgorithmStudy_211124/{meet_date}/rank.md'
    )   

    git_add = BashOperator(
        task_id = 'git_add',
        bash_command = f'git -C /home/airflow/AlgorithmStudy_211124/{meet_date}/ add rank.md'
    )   

    git_commit = BashOperator(
        task_id = 'git_commit',
        bash_command = 'git --git-dir=/home/airflow/AlgorithmStudy_211124/.git/ --work-tree=/home/airflow/AlgorithmStudy_211124/.git/ commit -m "Auto-update for rank"'
    )

    git_push = BashOperator(
        task_id = 'git_push',
        bash_command = 'git -C /home/airflow/AlgorithmStudy_211124 push'
        
    )

    pull_from_git >> make_indicator >> mv_indicator_to_repo >> git_add >> git_commit >> git_push