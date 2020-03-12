import asyncio
import datetime
import subprocess
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from model import TestRun, Base

# Configuring Database
def create_session():
    engine = create_engine('postgresql://postgres:postgres@localhost:5432')
    Session = sessionmaker(bind=engine)
    Session.configure(bind=engine)
    session = Session()

    Base.metadata.create_all(engine)
    return session

def execute_subprocess():
    started_at = datetime.datetime.now()
    return started_at, subprocess.run(["pytest -rA -v &"], shell=True, text=True, capture_output=True)

def run_all_tests():
    created_at = datetime.datetime.now()
    started_at, results = execute_subprocess()
    return created_at, started_at, results


def treat_results(results):
    end_time = datetime.datetime.now()
    summary_info_index = results.index('=========================== short test summary info ============================')
    summary = results[summary_info_index:-2]
    resume = results[-2].replace("=", '')
    return end_time, summary, resume

if __name__ == '__main__':
    session = create_session()
    created_at, started_at, results = run_all_tests()

    end_time, summary, resume = treat_results(results.stdout.split('\n'))

    test_run = TestRun(
        test="Teste 1",
        created_at=created_at,
        started_at=datetime.datetime.now(),
        finished_at=end_time,
        status=resume
    )

    session.add(test_run)
    session.commit()