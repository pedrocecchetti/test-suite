#! usr/bin/env python
import datetime
import argparse
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
    environment = results[1]
    summary_info_index = results.index('=========================== short test summary info ============================')
    summary = results[summary_info_index:-2]
    resume = results[-2].replace("=", '')
    return end_time, summary, resume, environment


def run(args):
    session = create_session()
    if args.run:
        test_run = TestRun(
            status='Running'
        )
        session.add(test_run)
        session.commit()

        created_at, started_at, results = run_all_tests()
        end_time, summary, resume, environment = treat_results(results.stdout.split('\n'))

        test_run.test = f"Test {str(created_at)}"
        test_run.created_at = created_at
        test_run.started_at = started_at
        test_run.finished_at = end_time
        test_run.status = resume
        test_run.logs = results.stdout
        test_run.environment = environment
        test_run.status = 'Done'

        session.add(test_run)
        session.commit()

        session.close()

    elif args.query:
        queryset = session.query(TestRun).all()
        list_of_tests = []
        for item in queryset:
            item_dict = {
                'name': item.test,
                'created_at': str(item.created_at),
                'started_at': str(item.started_at),
                'finished_at': str(item.finished_at),
                'status': item.status
            }
            list_of_tests.append(item_dict)

        print(list_of_tests)


def main():
    parser = argparse.ArgumentParser(
        description="Run tests from a test suite and save the information from the tests on a Database"
    )
    parser.add_argument(
        '--run',
        help='This option is used to run all the tests and store the info in the DB',
        action='store_const',
        const=True
    )
    parser.add_argument(
        '--query',
        help='This option is used to get the tests info from the DB',
        action='store_const',
        const=True
    )
    parser.set_defaults(func=run)
    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()