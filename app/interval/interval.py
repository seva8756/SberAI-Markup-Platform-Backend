import atexit

from apscheduler.schedulers.background import BackgroundScheduler

jobs = []


def interval():
    try:
        for func in jobs:
            func()
    except Exception:
        pass


def register_interval(server):
    jobs.append(server.file_store_instance.Project().check_reserved)

    scheduler = BackgroundScheduler()
    interval()
    scheduler.add_job(interval, 'interval', seconds=60)
    atexit.register(lambda: scheduler.shutdown())
    scheduler.start()
