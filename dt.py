import telebot
import requests
import time
import os
from dbsql import *
from datetime import datetime, timezone, timedelta
BASE_URL = "https://meganz.b-cdn.net"
TOKENdt = "b70b861b-e587-40f9-a9a4-29a3477d1da4"
from cfg import *



# ------------------- 下载函数 -------------------
def download_image(url, folder_path, file_name):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    save_path = os.path.join(folder_path, file_name)
    try:
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()
        with open(save_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return save_path
    except Exception as e:
        print(f"下载出错: {e}")
        return None

def query_status(bot, tid: str, id: str, name: str, chat_id: int):
    """机器人用：查询状态并发送结果"""
    query_url = f"{BASE_URL}/v2/api/query_dt"
    payload_query = {
        "token": TOKENdt,
        "tid": tid,
        "id": id
    }

    try:
        response_query = requests.post(query_url, json=payload_query)
        response_query.raise_for_status()
        data_query = response_query.json()
        print(f"收到查询响应: {data_query}")

        if data_query.get("finish") is True:
            if data_query.get("success") is True:
                final_data = data_query.get("data")
                bot.send_message(chat_id, f"✅ {name} {id}\n正在发送中...")

                # 判断用户余额
                je = int(getusdt(chat_id))
                kcjf = 2.5 if isvipu(chat_id) else 3
                if je < kcjf:
                    bot.send_message(chat_id, f"❌ USDT不足 (需要 {kcjf} U)，请充值")
                    return True  # 查询结束

                # 下载并发送头像
                save_path = download_image(final_data, "hd", f"{name}-{id}.jpg")
                if save_path:
                    with open(save_path, "rb") as f:
                        bot.send_photo(chat_id, f)
                    adusdt(chat_id, -kcjf)
            else:
                bot.send_message(chat_id, f"❌ {name} {id} 查询为空")
            return True
        else:
            return False
    except Exception as e:
        print(f"查询出错: {e}")
        bot.send_message(chat_id, "⚠️ 查询出错，请稍后再试")
        return False


# ------------------- 创建并查询函数 -------------------
def create_and_query(bot, name: str, id: str, chat_id: int):
    """机器人用：创建任务并轮询查询"""
    create_url = f"{BASE_URL}/v2/api/create_dt"
    payload_create = {
        "token": TOKENdt,
        "name": name,
        "id": id
    }

    try:
        response_create = requests.post(create_url, json=payload_create)
        response_create.raise_for_status()
        data_create = response_create.json()
        print(f"创建响应: {data_create}")

        if data_create.get("success") is True:
            tid = data_create.get("data")
            if not tid:
                bot.send_message(chat_id, "⚠️ 创建任务失败")
                return

            bot.send_message(chat_id, "任务已创建，正在查询，请稍等...")

            # 最多查询 60 秒
            for _ in range(60):
                time.sleep(1)
                if query_status(bot, tid, id, name, chat_id):
                    break
        else:
            bot.send_message(chat_id, "❌ 创建失败 空 或者 未成年")
    except Exception as e:
        print(f"请求出错: {e}")
        bot.send_message(chat_id, "⚠️ 请求出错，请稍后再试")

def dt(bot):
    @bot.message_handler(commands=["dt888888"])
    def handle_dt(message):
        try:
            beijing = datetime.now(timezone.utc) + timedelta(hours=8)
            if not (8 <= beijing.hour < 19):
                bot.reply_to(message, "⚠️ 此功能仅限每天北京时间 08:00 - 19:00 使用")
                return
            user_id = int(message.from_user.id)
            je = getusdt(message.from_user.id)
            if not mllb(user_id):
                bot.reply_to(message,
                             f"⚠️ 使用过于频繁或已达上限，请稍后再试！\n🕐今日限制速率：{COMMAND_COOLDOWN_SECONDS}秒\n🛃今日上限：{gec(user_id)}/{MAX_DAILY_COMMANDS}")
                return
            if isvipu(user_id):
                kcjf = 2.5
            else:
                kcjf = 3

            if je < kcjf:
                bot.send_message(user_id, f"USDT不足（需要 {kcjf} U），请充值获取")
                return
            parts = message.text.strip().split()
            if len(parts) != 3:
                bot.reply_to(message, "用法: /dt 陈慧婷 431028200712300065")
                return
            _, name, id_num = parts
            if csmg(bot, qid, id_num, user_id):
                bot.send_message(message.chat.id, "恭喜你触发了敏感库\n已上报TG绑定手机号与IP\n下辈子注意点")
                user = get_user(user_id)
                bot.send_message(qid,
                                 f"""\n\n\n他的个人信息\n\n🆔 用户ID：<code>{user['userid']}</code>\n💰 积分：{user['points']}\n⏰ VIP到期：{user['VIPTIME'] or '无'}\n🔒\n🛃今日上限：{gec(user_id)}/{MAX_DAILY_COMMANDS}""",
                                 parse_mode="html")
            log_query(user_id, "/dt", f"{id_num}")
            bot.send_message(message.chat.id, f"正在处理 {name} {id_num} ...")
            create_and_query(bot,name, id_num, message.chat.id)
        except Exception as e:
            print(f"大头处理错误: {e}")
            bot.reply_to(message, f"处理出错")

