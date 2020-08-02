import sched
import time
import requests
import json
import sqlite3


def login():
    cookie = open('static/cookie').read()
    try:
        qq = cookie.split("; uin=")[1].split(";")[0]
        skey = cookie.split("skey=")[1].split(";")[0]
    except IndexError:
        print("error input")
    return qq, skey


def getGTK(key):
    hashValue = 5381
    for index in key:
        hashValue += (hashValue << 5) + ord(index)
    return str(hashValue & 0x7fffffff)


def getDataByPage(uin: str, key: str, page: int):
    url = "https://quic.yundong.qq.com/pushsport/cgi/rank/friends?g_tk="
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; TNY-AL00 Build/HUAWEITNY-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/045114 Mobile Safari/537.36 V1_AND_SQ_8.2.7_1334_YYB_D PA QQ/8.2.7.4410 NetType/WIFI WebP/0.3.0 Pixel/1080 StatusBarHeight/72 SimpleUISwitch/0",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://quic.yundong.qq.com",
        "Cookie": "uin=" + uin + ";skey=" + key + ";"
    }
    data = {
        "dcapiKey": "user_rank",
        "l5apiKey": "rank_friends",
        "params": "{\"cmd\":1,\"pno\":" + str(page) + ",\"dtype\":1,\"pnum\":50}"
    }
    response = requests.post(url=url + getGTK(key), headers=headers, data=data)
    return response.text


def sortData(res: str, c):
    rankList = json.loads(res)["data"]["list"]
    for friend in rankList:
        c.execute('''insert into Walk (id, name, point) 
        values ({}, "{}", {})'''.format(friend["uin"], friend["name"], friend["points"]))


def refresh():
    qq, skey = login()
    conn = sqlite3.connect('walk.db')
    c = conn.cursor()
    for ind in range(1, 5):
        raw = getDataByPage(qq, skey, ind)
        sortData(raw, c)
    conn.commit()
    conn.close()


def task():
    refresh()


def perform(inc):
    s.enter(inc, 0, perform, (inc,))
    task()


if __name__ == '__main__':
    s = sched.scheduler(time.time, time.sleep)
    s.enter(0, 0, perform, (15*60,))
    s.run()
