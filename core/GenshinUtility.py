import json
import os
import time
import datetime
import random
import hashlib
import requests

from core.settings import *


class GenshinID(object):
    def __init__(self, genshinID: str):
        self.GenshinID = genshinID

    def showGenshinID(self):
        print(self.GenshinID)

    def getDailyNote(self):
        cookie_txt = open("./config/cookie.txt", mode="r+")
        cookie = cookie_txt.read()
        cookie_txt.close()
        print("Cookie: " + cookie)
        print(DSGet("role_id=" + self.GenshinID + "&server=cn_gf01"))

        dailyNoteURL = "https://api-takumi.mihoyo.com/game_record/app/genshin/api/dailyNote?server=cn_gf01&role_id=" + self.GenshinID
        Header = {
            'Accept': 'application/json, text/plain, */*',
            'DS': DSGet("role_id=" + self.GenshinID + "&server=cn_gf01"),
            'Origin': 'https://webstatic.mihoyo.com',
            'x-rpc-app_version': mhyVersion,
            'User-Agent': 'Mozilla/5.0 (Linux; Android 9; Unspecified Device) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/39.0.0.0 Mobile Safari/537.36 miHoYoBBS/2.2.0',
            'x-rpc-client_type': client_type,
            'Referer': 'https://webstatic.mihoyo.com/app/community-game-records/index.html?v=6',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,en-US;q=0.8',
            'X-Requested-With': 'com.mihoyo.hyperion',
            "Cookie": cookie
        }
        print(dailyNoteURL)
        req = requests.get(dailyNoteURL, headers=Header)

        # 处理HTTP返回结果
        data = json.loads(req.text)
        if data["retcode"] != 0:
            if data["retcode"] == 10001:
                os.remove("cookie.txt")
                return {"result": "Cookie错误/过期，请重置Cookie"}
            retcode_error_report = "Api报错，返回内容为：\r\n"+ str(data) + "\r\n出现这种情况可能是UID输入错误 or 不存在"
            return {"result": retcode_error_report}
        else:
            pass
        data = data['data']
        # 当前原粹树脂值
        current_resin = data['current_resin']
        # 原粹树脂最大值
        max_resin = data['max_resin']
        # 原粹树脂补满剩余时间
        resin_recovery_time = data['resin_recovery_time']
        resin_recovery_time_hours = str(datetime.timedelta(seconds=int(resin_recovery_time)))
        expected_resin_recovery_time = str(
            datetime.datetime.now() + datetime.timedelta(seconds=int(resin_recovery_time)))

        # 每日任务完成数量
        finished_task_num = data['finished_task_num']
        # 每日任务最大数量
        total_task_num = data['total_task_num']

        # 周本树脂消耗减半剩余机会
        remain_resin_discount_num = data['remain_resin_discount_num']
        # 周本树脂消耗减半机会上限
        resin_discount_num_limit = data['resin_discount_num_limit']

        # 当前派遣任务数量
        current_expedition_num = data['current_expedition_num']
        # 派遣任务数量上限
        max_expedition_num = data['current_expedition_num']
        # 当前派遣
        current_expedition_list = data['expeditions']
        expedition_count = 1
        expedition_status_report = "派遣任务状态："
        # lowest_expedition_remain_time_hours: 默认轮询时间
        lowest_expedition_remain_time = default_roll_polling_time
        for expedition in current_expedition_list:
            expedition_status_report += ("派遣任务" + str(expedition_count) + "：\n")
            expedition_status_report += ("状态：" + str(expedition['status']) + "\n")
            if str(expedition['status']) != "Finished":
                expedition_remain_time = expedition['remained_time']
                if int(expedition_remain_time) < lowest_expedition_remain_time:
                    lowest_expedition_remain_time = int(expedition_remain_time)
                expedition_remain_time_hours = str(datetime.timedelta(seconds=int(expedition_remain_time)))
                expected_expedition_remain_time = str(
                    datetime.datetime.now() + datetime.timedelta(seconds=int(expedition_remain_time)))
                expedition_status_report += ("剩余时间：" + expedition_remain_time_hours + "\n")
                expedition_status_report += ("预计完成时间：" + expected_expedition_remain_time + "\n")
            expedition_status_report += "\n"
            expedition_count += 1

        # Reports
        resin_report = "原粹树脂当前状态：" + str(current_resin) + "/" + str(max_resin)
        resin_recovery_report = "原粹树脂恢复剩余时间：" + str(resin_recovery_time_hours) + "\n预计树脂恢复完成时间：" + str(
            expected_resin_recovery_time)
        daily_task_report = "每日任务完成状态：" + str(finished_task_num) + "/" + str(total_task_num)
        weekly_challenge_report = "周本树脂消耗减半机会：" + str(remain_resin_discount_num) + "/" + str(resin_discount_num_limit)
        expedition_report = "当前派遣任务数量：" + str(current_expedition_num) + "/" + str(max_expedition_num)

        report_string = resin_report + "\n" + resin_recovery_report + "\n" + daily_task_report + "\n" + weekly_challenge_report + "\n" + expedition_report + "\n" + expedition_status_report
        print(report_string)
        return_dict = {'result': "OK",
                       'resin_recovery_time_hours': resin_recovery_time,
                       'expedition_remain_time_hours': lowest_expedition_remain_time,
                       'report_string': report_string}
        return return_dict


def md5(text):
    md5 = hashlib.md5()
    md5.update(text.encode())
    return md5.hexdigest()


def DSGet(query: str):
    n = salt
    i = str(int(time.time()))
    r = str(random.randint(100001, 200000))
    b = ""
    q = query
    c = md5("salt=" + n + "&t=" + i + "&r=" + r + "&b=" + b + "&q=" + q)
    return i + "," + r + "," + c


def OSDSGet():
    n = os_salt
    i = str(int(time.time()))
    r = str(random.randint(100001, 200000))
    c = md5("salt=" + n + "&t=" + i + "&r=" + r)
    return i + "," + r + "," + c
