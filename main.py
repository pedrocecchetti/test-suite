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
    summary_info_index = results.index('=========================== short test summary info ============================')
    summary = results[summary_info_index:-2]
    resume = results[-2].replace("=", '')
    return end_time, summary, resume


def run(args):
    session = create_session()
    if args.run:
        created_at, started_at, results = run_all_tests()
        end_time, summary, resume = treat_results(results.stdout.split('\n'))

        test_run = TestRun(
            test=f"Test {created_at.timestamp()}",
            created_at=created_at,
            started_at=started_at,
            finished_at=end_time,
            status=resume
        )

        session.add(test_run)
        session.commit()
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