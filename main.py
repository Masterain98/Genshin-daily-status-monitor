import json
import time
from core import telegramBotUtility
from core import GenshinUtility

if __name__ == '__main__':
    last_finished_count = 23333
    with open('./config/config.json') as json_file:
        config_data = json.load(json_file)
    TG_BOT_API_URL = config_data['TG_BOT_API_URL']
    TG_BOT_TOKEN = config_data['TG_BOT_TOKEN']
    TG_USER_ID = config_data['TG_USER_ID']
    if TG_BOT_TOKEN != "" and TG_USER_ID != "":
        telegramBotUtility.pushNotification("派遣任务监控服务已启动")
    UID = GenshinUtility.GenshinID(config_data['Genshin_UID'])

    while last_finished_count >= 0:
        daily_report = GenshinUtility.GenshinID.getDailyNote(UID)
        if last_finished_count != daily_report['report_string'].count('Finished'):
            # TG BOT Push Notification
            if TG_BOT_TOKEN != "" and TG_USER_ID != "":
                telegramBotUtility.pushNotification(daily_report)
        else:
            pass
        last_finished_count = daily_report['report_string'].count('Finished')

        resin_recovery_time_hours = daily_report['resin_recovery_time_hours']
        expedition_remain_time_hours = daily_report['expedition_remain_time_hours']
        next_polling_time = min(int(resin_recovery_time_hours), int(expedition_remain_time_hours), 3600)
        print("下一次查询时间为"+next_polling_time+"秒后")
        time.sleep(next_polling_time)
    telegramBotUtility.pushNotification("未知错误，监控服务已停止")