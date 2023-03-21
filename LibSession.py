import requests
import json
import re
import random
'''
管理与学校图书馆服务器的会话
'''
class LibSession:
    seats = {}
    def __init__(self, cookie):
        self.cookie = cookie
        
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.27"
    }
    @staticmethod
    def initSeats():
        if not LibSession.seats:
            # 3楼和4楼的座位
            room_ids = ["100455356", "100455354", "100455352", "100455350"]
            for room_id in room_ids:
                url = f"https://libic.njfu.edu.cn/ClientWeb/pro/ajax/device.aspx?\
byType=devcls&classkind=8&display=fp&md=d&room_id={room_id}\
&purpose=&selectOpenAty=&cld_name=default&act=get_dev_coord&_=1669385403140"
                res = requests.get(url=url, headers=LibSession.headers)
                # res.encoding="utf8"
                # print(res.text)
                retJSON = json.loads(res.text)
                data = retJSON["data"]
                for room in data["objs"]:
                    LibSession.seats[room["name"]] = room["id"]
    
    # 获取所有座位
    @staticmethod
    def getAllSeats():
        LibSession.initSeats()
        return list(LibSession.seats.keys())
    
    @staticmethod
    def getSeatsByReg(reg:str, disorder:bool=False):
        valid = re.compile(reg)
        seats = [seats for seats in LibSession.getAllSeats() if valid.fullmatch(seats) ] 
        if disorder:
            random.shuffle(seats)
        return seats
    
    @staticmethod
    def getSeatId(seatName:str):
        LibSession.initSeats()
        if seatName in LibSession.seats:
            return LibSession.seats[seatName]
        return None
    
    def getLibSeat(self, seat:str, start_time:str, end_time:str):
        seat_id = self.getSeatId(seat)
        url = f"https://libic.njfu.edu.cn/ClientWeb/pro/ajax/reserve.aspx?\
dialogid=&dev_id={seat_id}&lab_id=&kind_id=&room_id=&type=dev&prop=&test_id=&term=&Vnumber=&classkind=&test_name=&\
start={start_time}&end={end_time}&start_time=730&end_time=1430&up_file=&memo=&act=set_resv&_=1669385403167"
        res = requests.get(url=url, headers=LibSession.headers ,cookies=self.cookie)
        ret = json.loads(res.text)
        return ret
    
    @staticmethod
    def getLibSession(id:str, pwd:str):
        login = "https://libic.njfu.edu.cn/ClientWeb/pro/ajax/login.aspx"
        data = {
            "id":id,
            "pwd":pwd,
            "act":"login"
        }
        res = requests.post(url=login, data=data, headers=LibSession.headers)
        ret = json.loads(res.text)
        if ret["ret"] == 1:
            return LibSession(res.cookies)
        else:
            return None
        
class LibSessionManager:
    sessions = {}
    def get(self, id:str, pwd:str):
        if id in self.sessions:
            if self.sessions[id]["pwd"] == pwd:
                return self.sessions[id]["libsession"]
        else:
            libsession = LibSession.getLibSession(id, pwd)
            if libsession:
                self.sessions[id] = {
                    "pwd":pwd,
                    "libsession":libsession
                }
                return libsession
        return None
