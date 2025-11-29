import json
import os
import time
import threading
import requests
from telebot import TeleBot
from dbsql import adp, getp, isvipu
QUEUE_FILE = "zf.json"
LOCK = threading.Lock()
import re
from urllib.parse import quote
# =================== 存醋队列 ===================

def load_queue():
    """读取排队数据"""
    if not os.path.exists(QUEUE_FILE):
        return {"mode": {}, "queue": [], "data": {}}
    with open(QUEUE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_queue(data):
    """保存排队数据"""
    with open(QUEUE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
def extract_id_message(messages):
    id_pattern = re.compile(r"\b\d{17}[\dXx]\b")
    for msg in messages:
        if id_pattern.search(msg):
            return msg
    return "格式化错误"


def clean_points_lines(text: str) -> str:
    text = re.sub(r"已经扣除你的\d+积分", "", text)
    text = re.sub(r"您的剩余积分[:：]\s*\d+", "", text)
    cleaned_lines = []
    for line in text.split("\n"):
        if "小助手" in line:
            continue
        if line.strip():
            cleaned_lines.append(line)
    return "\n".join(cleaned_lines)


# 主函数：自动提取 + 自动清理
def parse_response(data: dict) -> str:
    messages = data["response"]["response_messages"]
    msg = extract_id_message(messages)
    msg = clean_points_lines(msg)
    return msg







# =================== 主功能注册 ===================

def zhuanfan(bot: TeleBot):
    @bot.message_handler(commands=["yhk3"])
    def handle_fr2(message):
        parts = message.text.split()
        if message.chat.type != "private":
            return
        if len(parts) < 2:
            bot.reply_to(message, "⚠️ 用法：<code>/yhk3 名字 身份证 银行卡</code>", parse_mode="html")
            return
        user_id = message.from_user.id
        if not isvipu(user_id):
            jf = getp(user_id)
            if jf < 5:
                bot.send_message(user_id, "积分不足，请签到或充值获取")
                return
        user_id = message.from_user.id
        nsrsbh = f"{parts[1]},{parts[2]},{parts[3]}"

        with LOCK:
            data = load_queue()
            queue = data.get("queue", [])
            user_data = data.get("data", {})
            mode = data.get("mode", {})
            # 检查是否重复排队
            if user_id in queue:
                bot.reply_to(message, "⚠️ 你已经在排队中，请耐心等待")
                return
            # 队伍上限10
            if len(queue) >= 10:
                bot.reply_to(message, "🚫 排队人数已满（含正在查询的用户），请稍后再试。")
                return

            # 入队
            user_data[str(user_id)] = nsrsbh
            queue.append(user_id)
            data["queue"] = queue
            data["mode"] = parts[0]
            data["data"] = user_data
            save_queue(data)

            position = len(queue)
            bot.reply_to(message, f"✅ 已加入排队（当前第 {position}/10 位），功能：{parts[0]}", parse_mode="html")

    @bot.message_handler(commands=["yxq"])
    def handle_yxqhy(message):
        parts = message.text.split()
        if message.chat.type != "private":
            return
        if len(parts) < 5:
            bot.reply_to(message, "⚠️ 用法：<code>/yxq 名字 身份证 起始日 结束日</code>", parse_mode="html")
            return
        user_id = message.from_user.id
        if not isvipu(user_id):
            jf = getp(user_id)
            if jf < 5:
                bot.send_message(user_id, "积分不足，请签到或充值获取")
                return
        user_id = message.from_user.id
        nsrsbh = f"{parts[1]},{parts[2]},{parts[3]},{parts[4]}"

        with LOCK:
            data = load_queue()
            queue = data.get("queue", [])
            user_data = data.get("data", {})
            mode_data = data.get("mode", {})
            # 检查是否重复排队
            if user_id in queue:
                bot.reply_to(message, "⚠️ 你已经在排队中，请耐心等待")
                return
            # 队伍上限10
            if len(queue) >= 10:
                bot.reply_to(message, "🚫 排队人数已满（含正在查询的用户），请稍后再试。")
                return

            # 入队
            user_data[str(user_id)] = nsrsbh
            mode_data[str(user_id)] = parts[0]
            queue.append(user_id)
            data["queue"] = queue
            data["mode"] = mode_data
            data["data"] = user_data
            save_queue(data)
            position = len(queue)
            bot.reply_to(message, f"✅ 已加入排队（当前第 {position}/10 位），功能：{parts[0]}", parse_mode="html")


# =================== 后台线程逻辑 ===================
def process_queue(bot: TeleBot):
    #进入处理判断需处理内容
    while True:
        with LOCK:
            data = load_queue()
            queue = data.get("queue", [])
            mode_data = data.get("mode", {})
            user_data = data.get("data", {})

        if not queue:
            time.sleep(5)
            continue
        user_id = queue[0]
        nsrsbh = user_data.get(str(user_id))
        try:
            if "yhk" in mode_data.get(str(user_id)):
                    bot.send_message(user_id, "🎯开始核验，请稍候...", parse_mode="html")
                    a = nsrsbh.split(",")
                    name = quote(a[0])
                    id_card = quote(a[1])
                    bank = quote(a[2])

                    url = f"http://103.207.68.203:5551/yhk_2?name={name}&id_card={id_card}&bank_card={bank}"
                    print(url)
                    # 请求
                    resp = requests.get(url, timeout=200)
                    try:
                        data = resp.json()
                    except:
                        bot.send_message(user_id, "⚠️ 接口返回格式错误，请稍后再试")
                        return
                    # 扣积分逻辑
                    if not isvipu(user_id):
                        jf = getp(user_id)
                        if jf < 5:
                            bot.send_message(user_id, "积分不足，请签到或充值获取")
                            with LOCK:
                                queue.pop(0)
                                data["queue"] = queue
                                save_queue(data)
                            continue
                        adp(user_id, -5)
                    result_text = parse_response(data)
                    bot.send_message(user_id, result_text)



            elif "yxq" in mode_data.get(str(user_id)):
                bot.send_message(user_id, "🎯开始核验，请稍候...", parse_mode="html")
                a = nsrsbh.split(",")
                name = quote(a[0])
                id_card = quote(a[1])
                start_time = quote(a[2])
                end_time = quote(a[3])
                url = f"http://103.207.68.203:5551/yxq_hy_1?name={name}&id_card={id_card}&start_date={start_time}&end_date={end_time}"
                print(url)
                # 请求
                resp = requests.get(url, timeout=200)
                try:
                    data = resp.json()
                except:
                    bot.send_message(user_id, "⚠️ 接口返回格式错误，请稍后再试")
                    return
                # 扣积分逻辑
                if not isvipu(user_id):
                    jf = getp(user_id)
                    if jf < 5:
                        bot.send_message(user_id, "积分不足，请签到或充值获取")
                        with LOCK:
                            queue.pop(0)
                            data["queue"] = queue
                            save_queue(data)
                        continue
                    adp(user_id, -5)
                result_text = parse_response(data)
                bot.send_message(user_id, result_text)
        except Exception as e:
            bot.send_message(user_id, "⚠️ 查询失败，请稍后再试")
            print("转发核验出错：", e)
        finally:
            with LOCK:
                data = load_queue()
                queue = data.get("queue", [])
                if queue and queue[0] == user_id:
                    queue.pop(0)
                    data["queue"] = queue
                    save_queue(data)

            # 每个用户查询间隔一分钟
            time.sleep(200)


def start_zf_worker(bot: TeleBot):
    threading.Thread(target=process_queue, args=(bot,), daemon=True).start()