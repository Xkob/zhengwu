import json
import os
import time
import threading
import requests
from telebot import TeleBot
from dbsql import adp, getp, isvipu
QUEUE_FILE = "queue.json"
LOCK = threading.Lock()
# =================== 队列存储逻辑 ===================

def load_queue():
    """读取排队数据"""
    if not os.path.exists(QUEUE_FILE):
        return {"queue": [], "data": {}}
    with open(QUEUE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_queue(data):
    """保存排队数据"""
    with open(QUEUE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# =================== 主功能注册 ===================

def frgn(bot: TeleBot):
    """注册 /fr2 查询命令"""
    @bot.message_handler(commands=["fr2"])
    def handle_fr2(message):
        parts = message.text.split()
        if message.chat.type != "private":
            return
        if len(parts) < 2:
            bot.reply_to(message, "⚠️ 用法：<code>/fr2 企业代码</code>", parse_mode="html")
            return
        user_id = message.from_user.id
        if not isvipu(user_id):
            jf = getp(user_id)
            if jf < 10:
                bot.send_message(user_id, "积分不足，请签到或充值获取")
                return
        user_id = message.from_user.id
        nsrsbh = parts[1].strip()

        with LOCK:
            data = load_queue()
            queue = data.get("queue", [])
            user_data = data.get("data", {})
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
            data["data"] = user_data
            save_queue(data)

            position = len(queue)
            bot.reply_to(message, f"✅ 已加入排队（当前第 {position}/10 位），企业号：{nsrsbh}", parse_mode="html")


# =================== 后台线程逻辑 ===================

def process_queue(bot: TeleBot):
    """后台队列处理"""
    while True:
        with LOCK:
            data = load_queue()
            queue = data.get("queue", [])
            user_data = data.get("data", {})

        if not queue:
            time.sleep(5)
            continue

        user_id = queue[0]
        nsrsbh = user_data.get(str(user_id))

        try:
            bot.send_message(user_id, f"🎯 正在查询：{nsrsbh}...", parse_mode="html")
            url = f"http://103.239.244.104:57820/api/query?nsrsbh={nsrsbh}"
            resp = requests.get(url, timeout=200)

            try:
                data_json = resp.json()
                if not isvipu(user_id):
                    jf = getp(user_id)
                    if jf < 10:
                        bot.send_message(user_id, "积分不足，请签到或充值获取")
                        return
                if not isvipu(user_id):
                    adp(user_id, -10)
                # ✅ 只有 status == success 才视为成功结果
                if data_json.get("status") == "success" and "data" in data_json:
                    data = data_json["data"]
                    name = data.get("法人姓名", "未知")
                    id_card = data.get("法人证件号", "未知")
                    company = data.get("纳税人名称", "未知")
                    code = data.get("统一社会信用代码", "未知")

                    text = (
                        f"📄 查询成功：\n"
                        f"👤 法人姓名：{name}\n"
                        f"🪪 法人证件号：{id_card}\n"
                        f"🏢 纳税人名称：{company}\n"
                        f"🔢 统一社会信用代码：{code}"
                    )
                else:
                    text = "❌ 查询失败或无结果"

            except json.JSONDecodeError:
                text = "⚠️ 返回数据格式错误"
            jf = getp(user_id)

            bot.send_message(user_id, text)

        except Exception as e:
            bot.send_message(user_id, f"⚠️ 查询失败")
            print(f"法人代理出 {e}")

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


def start_frgn_worker(bot: TeleBot):
    threading.Thread(target=process_queue, args=(bot,), daemon=True).start()