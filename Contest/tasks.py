from apscheduler.schedulers.background import BackgroundScheduler
"""This File Is Used To Initlize the Worker Only"""
scheduler = BackgroundScheduler(max_workers=30)
scheduler.start()


