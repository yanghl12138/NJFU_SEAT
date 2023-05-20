
import datetime
import random
from Job import readJobsFromDB
from LibSession import *
from SettingManager import *

'''
使用数据库的版本
'''

if __name__ == "__main__":
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    jobs = readJobsFromDB(tomorrow)
    for job in jobs:
        job.do()