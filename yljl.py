import requests
import os
from dbsql import adp, getp, isvipu

def dowl(bot,userid, name, idcard):
    url = "http://154.64.230.27:8080/yljl"
    params = {
        "xm": name,
        "sfz": idcard,
        "key":"sanqiuchadang"
    }

    try:
        resp = requests.get(url, params=params, timeout=60)
        if '"code":0' in resp.text:
            bot.send_message(userid, "查询失败查询为空")
        if "success" in resp.text:
            bot.send_message(userid, "查询为空")
        if "记录" not in resp.text:
            bot.send_message(userid, "消息格式化失败 尝试重新查询")
        filename = f"{idcard}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(resp.text+"\n查询来源 一诺政务机器人 @xhgzw")
        bot.send_document(userid, open(filename, "rb"), caption=f"{name} 的查询结果")
        os.remove(filename)
        if not isvipu(userid):
            kcjf = 50
            adp(userid, -kcjf)
            bot.send_message(userid, f"已扣除 {kcjf} 积分")
        else:
            adp(userid, -1)
    except Exception as e:
        print("错误：", e)
        bot.send_message(userid, "查询失败，请稍后再试")
