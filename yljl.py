import requests
import os
from dbsql import adp, getp, isvipu

def dowl(bot, userid, name, idcard):
    """
    调用接口查询并下载图片结果，再发给 Telegram 用户。
    如果返回的不是图片或内容为空则提示“结果为空”。
    """
    url = "http://43.251.117.173:1013/yl"
    params = {
        "name": name,
        "sfz": idcard,
        "key": "3a77c673465b4fa3"
    }

    try:
        resp = requests.get(url, params=params, timeout=60)
        resp.raise_for_status()

        content_type = resp.headers.get("Content-Type", "")

        # 检查是否为图片
        if "image" not in content_type:
            bot.send_message(userid, "查询结果为空")
            return "空"

        # 检查大小
        if len(resp.content) < 1024:
            bot.send_message(userid, "查询结果为空")
            return "空"

        # 保存并发送图片
        ext = content_type.split("/")[-1].split(";")[0] or "png"
        filename = f"{name}_{idcard}.{ext}"
        with open(filename, "wb") as f:
            f.write(resp.content)

        with open(filename, "rb") as f:
            bot.send_document(userid, f, caption=f"{name}（{idcard}）查询结果")

        os.remove(filename)

        # 积分逻辑
        if not isvipu(userid):  # 非VIP扣积分
            kcjf = 50
            adp(userid, -kcjf)
            bot.send_message(userid, f"已扣除 {kcjf} 积分")
        else:
            adp(userid, -1)
    except Exception as e:
        print("错误：", e)
        bot.send_message(userid, "查询失败，请稍后再试")
