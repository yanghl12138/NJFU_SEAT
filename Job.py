import datetime
from LibSession import *
from myEmail import *
import time
import random
from SettingManager import *
import pymysql

'''
管理一次完整的业务流程
'''
class Job:
    def __init__(self, user:LibSession, To_addr:str, seats:list, start:str, end:str):
        self.user = user
        self.email_settings = SettingManager.getSettings("email_settings")
        self.email = myEmail(addr=self.email_settings["mail"] , code=self.email_settings["code"], 
                              smtp_url=self.email_settings["smtp_url"], smtp_port=self.email_settings["smtp_port"])
        self.seats = seats
        self.seat_time = {
            "start":start,
            "end":end
        }
        self.To_addr = To_addr
        self.sleep_time = 0.3
    def do(self) -> bool:
        print("\033[1;33mNow: {}\033[0m".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
        print("----------------------------------------------")
        flag = False
        final_seat = ""
        for seat in self.seats:
            ret = self.user.getLibSeat(seat=seat, start_time=self.seat_time["start"], end_time=self.seat_time["end"])
            print(f"\033[0;31m{seat} {self.seat_time}\033[0m")
            print(ret)
            if ret["ret"] == 1:
                final_seat = seat
                flag = True
                break
            time.sleep(self.sleep_time)
        seader = InfoSender(self.email, sendername=self.email_settings["sendername"])
        if flag:
            seader.seadOKmail(seat=final_seat, start=self.seat_time["start"], end=self.seat_time["end"], To_addr=self.To_addr)
        else:
            seader.seadFailmail(To_addr=self.To_addr)
        return flag
            

def readJobsFromDB(date:str):
    manager = LibSessionManager()
    db_settings = SettingManager.getSettings("db_settings")
    connection = pymysql.connect(host=db_settings["host"],
                         port=db_settings["port"],
                         user=db_settings["user"],
                         password=db_settings["pwd"],
                         database=db_settings["db"])
    with connection: 
        with connection.cursor() as cursor: 
            sql = "select id, email, seats, start, end from info;"
            cursor.execute(sql)
            records = cursor.fetchall()
            # print(records)
            sql = "select id, pwd from users;"
            cursor.execute(sql)
            users = dict(cursor.fetchall())
            # print(users)
    
    jobs_list = []
    # 缓存
    seats_cache = {}
    for record in records: 
        user = manager.get(id=record[0], pwd=users[record[0]])
        if record[2] in seats_cache:
            seats = seats_cache[record[2]]
        else:
            seats = LibSession.getSeatsByReg(reg=record[2], disorder=True)
            seats_cache[record[2]] = seats
        jobs_list.append(Job(user=user,
                             To_addr=record[1],
                             seats=seats,
                             start=f"{date}+{record[3]}", end=f"{date}+{record[4]}"))
    return jobs_list
    