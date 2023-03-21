
import datetime
import random
from Job import Job
from LibSession import *

'''
不使用数据库的版本
'''

if __name__ == "__main__":
    manager = LibSessionManager()
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    
    job_list = []
    seats = LibSession.getSeatsByReg("4F-A[0-9]{3}", True)
    random.shuffle(seats)
    job_list.append(Job(user=manager.get(id="<Your Student ID>", pwd="<Your Password>"), 
                        To_addr="<Your Email>", seats=seats, 
                        start=f"{today}+14:00", end=f"{today}+22:00"))
    for job in job_list:
        job.do()