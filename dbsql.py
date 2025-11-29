import mysql.connector
from cfg import DB_CONFIG,MIN_INTERVAL_SECONDS,MAX_DAILY_COMMANDS,COMMAND_COOLDOWN_SECONDS
from bot import bot
from decimal import Decimal
from datetime import datetime, timezone, timedelta,date
import os
from io import BytesIO
import telebot
import random
import re
import os
import chinese_calendar as calendar
from chinese_calendar import get_holiday_detail

REMIND_LOG_FILE = "remind_log.txt"  # 记录已提醒的日期
china_tz = timezone(timedelta(hours=8))
now = datetime.now(china_tz)

def qrxxdqh(user_id):
    if is_user_member('@xsdqh', user_id):
        return True
    else:
        return False



def user_info(user_id):
    try:
        user = bot.get_chat(user_id)

        info = f"""
👤 用户信息如下：

🆔 用户ID：{user.id}
🙋‍♂️ 姓名（first_name）：{getattr(user, 'first_name', '无')}
👨‍👩‍👧‍👦 姓氏（last_name）：{getattr(user, 'last_name', '无')}
🧑‍🤝‍🧑 用户名：@{getattr(user, 'username', '无')}
🗂️ 用户类型：{getattr(user, 'type', '未知')}
📛 显示名称（title）：{getattr(user, 'title', '无')}
🧾 个性签名（bio）：{getattr(user, 'bio', '无')}
🧑‍💼 活跃用户名列表：{', '.join(user.active_usernames) if getattr(user, 'active_usernames', None) else '无'}
💥 最大反应数：{getattr(user, 'max_reaction_count', '未知')}
🎨 主题色 ID：{getattr(user, 'accent_color_id', '无')}
🧵 是否是话题群组（is_forum）：{'是' if getattr(user, 'is_forum', False) else '否'}
🔒 是否允许私密转发：{'是' if getattr(user, 'has_private_forwards', False) else '否'}
"""
        return info

    except Exception as e:
        print(f"❌ 出错了：{e}")
        return "❌ 获取用户信息失败"

def is_user_member(channel_id, user_id):
    cannel_member = bot.get_chat_member(chat_id=channel_id, user_id=user_id)
    return cannel_member.status != 'left'
def checkqd(user_id):
    if is_user_member('@XiaoHaiGe_SGK', user_id) and is_user_member('@xiaohaigeleyuan', user_id)and is_user_member('@xhgzw', user_id)and is_user_member('@xiaohaigeSGK', user_id)and is_user_member('@xiaohaigechadang', user_id):
        return True
    else:
        return False
def generate_unique_random_amount(base_amount):
    """
    生成唯一金额，通过在基础金额上添加随机小数部分
    :param base_amount: 基础金额
    :return: 添加随机小数后的金额字符串
    """
    base = float(base_amount)
    # 生成0到0.5之间的随机小数
    random_decimal = random.random() * 0.500000
    # 将基础金额与随机小数相加，保留6位小数
    return f"{base + random_decimal:.6f}"
def sedtxt(bot: telebot.TeleBot, chat_id: int, text: str, filename: str = "1.txt"):
    """
    发送一段字符串为 .txt 文件
    :param bot: TeleBot 实例
    :param chat_id: 用户或群组的 chat_id
    :param text: 要发送的内容
    :param filename: 文件名，默认"1.txt"
    """
    file_data = BytesIO()
    file_data.write(text.encode('utf-8'))
    file_data.seek(0)
    bot.send_document(chat_id, file_data, visible_file_name=filename)
def tsms():
    return os.path.isfile("test.txt")
def delmsg(chat_id, message_id):
    try:
        bot.delete_message(chat_id, message_id)
    except Exception:
        pass
def get_db_conn():
    return mysql.connector.connect(**DB_CONFIG)

def gec(userid: int) -> int:
    conn = get_db_conn()
    cursor = conn.cursor(dictionary=True)
    today = datetime.now(timezone.utc).date()

    cursor.execute("SELECT today_count, last_reset_date FROM user_limits WHERE userid = %s", (userid,))
    user = cursor.fetchone()
    conn.close()

    if user and user["last_reset_date"] == today:
        return user["today_count"]
    return 0
def get_all_today_command_count() -> int:
    conn = get_db_conn()
    cursor = conn.cursor(dictionary=True)

    # 查询所有用户今天命令使用总次数
    cursor.execute("""
        SELECT SUM(today_count) AS total_today_usage
        FROM user_limits
        WHERE last_reset_date = CURDATE()
    """)
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result["total_today_usage"] or 0  # 如果为 None，则返回 0
def mllb(userid: int) -> bool:
    if cxban(userid):
        return False
    BEIJING_TZ = timezone(timedelta(hours=8))
    now = datetime.now(BEIJING_TZ)
    today = now.date()


    conn = get_db_conn()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM user_limits WHERE userid = %s", (userid,))
    user = cursor.fetchone()

    if user:


        # 判断是否跨天
        last_reset = user["last_reset_date"]
        if isinstance(last_reset, datetime):
            last_reset = last_reset.date()



        if last_reset != today:

            cursor.execute("""
                UPDATE user_limits
                SET today_count = 0, last_reset_date = %s
                WHERE userid = %s
            """, (today, userid))
            user["today_count"] = 0

        # 判断冷却时间
        last_time = user["last_command_time"]
        if last_time:
            if last_time.tzinfo is None:
                last_time = last_time.replace(tzinfo=BEIJING_TZ)

            cooldown = (now - last_time).total_seconds()


            if cooldown < COMMAND_COOLDOWN_SECONDS:

                conn.close()
                return False

        # 判断今日使用次数
        if user["today_count"] >= MAX_DAILY_COMMANDS:

            conn.close()
            return False

        # 更新使用时间和次数
        # print("✅ 通过检查，更新记录")
        cursor.execute("""
            UPDATE user_limits
            SET last_command_time = %s,
                today_count = today_count + 1,
                total_count = total_count + 1
            WHERE userid = %s
        """, (now, userid))

    else:
        # print("首次使用，插入新记录")
        cursor.execute("""
            INSERT INTO user_limits (userid, last_command_time, today_count, total_count, last_reset_date)
            VALUES (%s, %s, 1, 1, %s)
        """, (userid, now, today))

    conn.commit()
    conn.close()
    # print("✅ 操作完成，允许使用\n")
    return True
def getusdt(userid):
    conn = get_db_conn()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT USDT FROM users WHERE userid = %s", (userid,))
        result = cursor.fetchone()
        if result and result['USDT'] is not None:
            return Decimal(str(result['USDT']))  # 强制保留小数
        return Decimal('0')
    finally:
        cursor.close()
        conn.close()



BEIJING_TZ = timezone(timedelta(hours=8))

def anpd(userid):
    now = datetime.now(BEIJING_TZ)  # ✅ 获取北京时间
    conn = get_db_conn()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT last_button_time FROM user_limits WHERE userid = %s", (userid,))
    result = cursor.fetchone()

    if result:
        last_time = result['last_button_time']
        if last_time:
            # 防止 last_time 没有时区信息
            if last_time.tzinfo is None:
                last_time = last_time.replace(tzinfo=BEIJING_TZ)

            diff = (now - last_time).total_seconds()
            if diff < MIN_INTERVAL_SECONDS:
                cursor.close()
                conn.close()
                return False

        # 更新时间
        cursor.execute(
            "UPDATE user_limits SET last_button_time = %s WHERE userid = %s",
            (now, userid)
        )
    else:
        # 首次记录
        cursor.execute(
            "INSERT INTO user_limits (userid, last_button_time, last_reset_date) VALUES (%s, %s, %s)",
            (userid, now, now.date())
        )

    conn.commit()
    cursor.close()
    conn.close()
    return True


def set_user_vip(userid: str, vip_type: int, days: int = 0):
    try:
        conn = get_db_conn()
        cursor = conn.cursor()
        if vip_type == 2:
            # 永久VIP
            vip_time = datetime(2999, 12, 31, tzinfo=timezone.utc)
        elif vip_type == 1:
            # 普通VIP，计算到期时间
            vip_time = datetime.now(timezone.utc) + timedelta(days=days)
        else:
            # 免费用户
            vip_time = datetime(1997, 1, 1, tzinfo=timezone.utc)

        cursor.execute("UPDATE users SET vip = %s, VIPTIME = %s WHERE userid = %s", (vip_type, vip_time, userid))
        conn.commit()
        return f"✅ 设置成功！用户 {userid} 已设为 VIP {vip_type} 到期：{vip_time.strftime('%Y-%m-%d')}"
    except Exception as e:
        return f"❌ 设置失败: {e}"
    finally:
        cursor.close()
        conn.close()
def get_vip_level(userid):
    BEIJING = timezone(timedelta(hours=8))  # 北京时间

    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT vip, VIPTIME FROM users WHERE userid = %s", (userid,))
    row = cursor.fetchone()

    if not row:
        cursor.close()
        conn.close()
        return 0  # 默认免费用户

    vip, vip_time = row
    now = datetime.now(BEIJING)

    # 永久 VIP
    if vip == 2:
        result = 2

    # 普通 VIP，检查是否过期
    elif vip == 1:
        if vip_time:
            # vip_time 是 date 类型，需转为 datetime 加上时区
            vip_dt = datetime.combine(vip_time, datetime.min.time()).replace(tzinfo=BEIJING)
            if vip_dt > now:
                result = 1  # 有效 VIP
            else:
                # ⛔ 已过期，自动降级
                reset_time = datetime(1997, 1, 1, tzinfo=BEIJING)
                cursor.execute("UPDATE users SET vip = 0, VIPTIME = %s WHERE userid = %s", (reset_time, userid))
                conn.commit()
                result = 4
        else:
            result = 0
    else:
        result = 0

    cursor.close()
    conn.close()
    return result

# 注册用户
def get_invite_count(userid):
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM invites WHERE inviter_id = %s", (userid,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()

    if not row:
        return 0
    return row[0]


def getsluser():
    conn = get_db_conn()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return count
def get_avg_points():
    conn = get_db_conn()
    cursor = conn.cursor()

    # 只统计积分 ≥ 0 的用户
    cursor.execute("SELECT AVG(points) FROM users WHERE points >= 0")
    result = cursor.fetchone()[0] or 0

    cursor.close()
    conn.close()

    return result


def getuserps():
    conn = get_db_conn()
    cursor = conn.cursor()

    # 只计算 0 ≤ 积分 ≤ 1000 的
    cursor.execute("SELECT SUM(points) FROM users WHERE points BETWEEN 0 AND 1000")
    result = cursor.fetchone()[0] or 0  # 防止 None

    cursor.close()
    conn.close()

    return result



def reguser(user_id):
    conn = get_db_conn()
    cursor = conn.cursor()

    cursor.execute("SELECT userid FROM users WHERE userid = %s", (user_id,))
    if cursor.fetchone():
        msg = "0"
    else:
        cursor.execute(
            "INSERT INTO users (userid, points, USDT, vip, VIPTIME, inban) VALUES (%s, %s, %s, %s, %s, %s)",
            (user_id, 0, 0, 0, "1970-01-01 00:00:00", 0)
        )

        conn.commit()
        msg = "🎉 注册成功！XHGZW-2.0欢迎你 /start 点击加载机器人"

    cursor.close()
    conn.close()
    return msg


def cxban(user_id: int):
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT inban FROM users WHERE userid = %s", (user_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()

    # 如果没有该用户记录，默认不封禁
    if row is None:
        return False

    return row[0] == 1

# 查询用户信息
def get_user(user_id):
    conn = get_db_conn()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE userid = %s", (user_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result
def mask_name(name):
    if not name:
        return "匿名用户"
    if len(name) <= 1:
        return name + "****" + name
    return name[0] + "****" + name[-1]

def setban(user_id, inban):
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET inban = %s WHERE userid = %s", (inban, user_id))
    conn.commit()
    cursor.close()
    conn.close()
def clear_user_qd(user_id):
    conn = get_db_conn()
    cursor = conn.cursor()
    try:
        reset_date = date(2000, 1, 1)
        cursor.execute("UPDATE users SET qdtime = %s WHERE userid = %s", (reset_date, user_id))
        conn.commit()
        print(f"✅ 用户 {user_id} 的签到状态已设置为 2000-01-01")
    except Exception as e:
        print(f"❌ 清除失败：{e}")
    finally:
        cursor.close()
        conn.close()


def chqd(name,user_id):
    conn = get_db_conn()
    cursor = conn.cursor()
    today = date.today()
    cursor.execute("SELECT qdtime FROM users WHERE userid = %s", (user_id,))
    row = cursor.fetchone()
    if not row:
        cursor.close()
        conn.close()
        return "❌ 用户未注册，请先使用 /start 注册"
    last_qd_date = row[0]
    if last_qd_date == today:
        msg = "📝 你今天已经签到过啦，明天再来吧～"
    else:
        cursor.execute(
            "UPDATE users SET points = points + 1, qdtime = %s WHERE userid = %s",
            (today, user_id)
        )
        conn.commit()
        crqd()
        msg = f"签到成功！积分 +1 🎉"
    cursor.close()
    conn.close()
    return msg
def adp(userid, po):
    try:
        conn = get_db_conn()
        cursor = conn.cursor()

        # 查询当前积分
        cursor.execute("SELECT points FROM users WHERE userid = %s", (userid,))
        result = cursor.fetchone()
        if not result:
            return "❌ 用户不存在"

        current_points = result[0]
        new_points = current_points + po

        # ✅ 去掉“不允许负数”判断
        cursor.execute("UPDATE users SET points = %s WHERE userid = %s", (new_points, userid))
        conn.commit()
        return f"✅ 积分更新成功，当前积分为：{new_points}"
    except Exception as e:
        return f"❌ 更新失败：{e}"
    finally:
        cursor.close()
        conn.close()
from decimal import Decimal

def adusdt(userid, po):
    try:
        conn = get_db_conn()
        cursor = conn.cursor()

        # 查询当前积分
        cursor.execute("SELECT USDT FROM users WHERE userid = %s", (userid,))
        result = cursor.fetchone()
        if not result:
            return "❌ 用户不存在"

        current_points = result[0]  # Decimal
        # 强制把 po 转成 Decimal
        po = Decimal(str(po))

        new_points = current_points + po
        cursor.execute("UPDATE users SET USDT = %s WHERE userid = %s", (new_points, userid))
        conn.commit()
        return f"✅ 积分更新成功，当前积分为：{new_points}"
    except Exception as e:
        return f"❌ 更新失败：{e}"
    finally:
        if conn:
            cursor.close()
            conn.close()


def getup(userid):
    try:
        conn = get_db_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT points FROM users WHERE userid = %s", (userid,))
        result = cursor.fetchone()
        if result:
            return result[0]  # 返回积分数
        else:
            return None  # 用户不存在
    except Exception as e:
        print(f"获取积分失败：{e}")
        return None
    finally:
        cursor.close()
        conn.close()
#检查注册
def is_reg(user_id):
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM users WHERE userid = %s", (user_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result is not None
def is_user_invited(user_id):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM invites WHERE invited_id = %s", (user_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result is not None

from datetime import datetime

def record_invitation(invited_id, inviter_id):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO invites (inviter_id, invited_id, invited_time) VALUES (%s, %s, %s)",
        (inviter_id, invited_id, datetime.now())
    )
    conn.commit()
    cursor.close()
    conn.close()
def getp(user_id):
    try:
        conn = get_db_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT points FROM users WHERE userid = %s", (user_id,))
        result = cursor.fetchone()

        if result:
            return result[0]  # 返回积分数值
        else:
            return None  # 用户不存在
    except Exception as e:
        print(f"查询积分出错：{e}")
        return None
    finally:
        cursor.close()
        conn.close()

def isvipu(user_id):
    try:
        conn = get_db_conn()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT vip, VIPTIME FROM users WHERE userid = %s", (user_id,))
        user = cursor.fetchone()

        if not user:
            return False  # 用户不存在

        if user["vip"] == 2:
            return True  # 永久VIP
        elif user["vip"] == 1:
            return True
        return False
    except Exception as e:
        print(f"判断VIP出错：{e}")
        return False
    finally:
        cursor.close()
        conn.close()


def csmg(bot,qid,text,ban_id):
    try:
        with open("mingab.txt", 'r', encoding='utf-8') as f:
            content = f.read()
            if text in content:
                print(f"文本 [{text}] 存在于 mingab.txt 中，执行惩罚")
                bot.send_message(qid,f"用户{ban_id}输入了文本 [{text}] 存在于 敏感 中")
                setban(ban_id, 1)
                adp(ban_id, -9999)
                set_user_vip(ban_id, 0, "1970-01-01")
    except FileNotFoundError:
        print("文件未找到 mingab.txt")
        return False
    except Exception as e:
        print("读取文件出错:", e)
        return False

def crqd():
    today = datetime.now().date()
    conn = get_db_conn()
    cursor = conn.cursor(dictionary=True)

    # 插入或更新
    cursor.execute("""
        INSERT INTO daily_signin_stats (day, count)
        VALUES (%s, 1)
        ON DUPLICATE KEY UPDATE count = count + 1
    """, (today,))

    conn.commit()
    cursor.close()
    conn.close()


def getqd():
    conn = get_db_conn()
    cursor = conn.cursor()

    # 今日日期（北京时间）
    today = datetime.now(BEIJING_TZ).date()

    # 今日签到人数
    cursor.execute("SELECT count FROM daily_signin_stats WHERE day = %s", (today,))
    row = cursor.fetchone()
    today_count = row[0] if row else 0

    # 总签到人数
    cursor.execute("SELECT SUM(count) FROM daily_signin_stats")
    total = cursor.fetchone()[0] or 0

    cursor.close()
    conn.close()

    return today_count, total

def cxphone(phone_number):
    # 使用正则判断手机号合法性（中国11位手机号）
    if not re.fullmatch(r"1\d{10}", phone_number):
        return "❌ 非法手机号"

    segment = phone_number[:7]  # 提取前七位
    try:
        connection = get_db_conn()
        cursor = connection.cursor()

        sql = "SELECT province, city, operator FROM phone_segments WHERE segment = %s"
        cursor.execute(sql, (segment,))
        result = cursor.fetchone()

        if result:
            province, city, operator = result
            return f"📍 归属地：{province} {city}（{operator}）"
        else:
            return "❗ 未查询到号段归属地"

    except Exception as e:
        return f"⚠️ 查询失败: {e}"
    finally:
        if 'connection' in locals() and connection.is_connected():
            connection.close()



def is_today_holiday_or_weekend():
    today = date.today()
    return calendar.is_holiday(today) or today.weekday() >= 5

def next_holiday_or_weekend():
    today = date.today()
    for i in range(1, 365):
        next_day = today + timedelta(days=i)
        if calendar.is_holiday(next_day) or next_day.weekday() >= 5:
            return i
    return None

def get_holiday_end_info():
    today = date.today()
    holiday_name, is_holiday = get_holiday_detail(today)

    if not is_holiday:
        return None

    # 查找节假日结束的日期
    end_date = today
    while calendar.is_holiday(end_date + timedelta(days=1)):
        end_date += timedelta(days=1)

    days_left = (end_date - today).days + 1
    return holiday_name, end_date.strftime("%Y-%m-%d"), days_left

def has_reminded_today():
    today_str = date.today().isoformat()
    return os.path.exists(REMIND_LOG_FILE) and today_str in open(REMIND_LOG_FILE).read()

def mark_reminded_today():
    today_str = date.today().isoformat()
    with open(REMIND_LOG_FILE, "a") as f:
        f.write(today_str + "\n")
def generate_code(length=8):
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    return ''.join(random.choice(chars) for _ in range(length))





def update_card_used(table, code, user_id):
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute(
        f"UPDATE {table} SET used=1, user_id=%s, use_time=NOW() WHERE code=%s",
        (user_id, code)
    )
    conn.commit()
    conn.close()

def insert_cards(table, card_list, value_field, value, vip_type=None):
    conn = get_db_conn()
    cursor = conn.cursor()
    for code in card_list:
        if table == "vip_cards":
            cursor.execute(
                f"INSERT INTO {table}(code, {value_field}, vip_type, created_by) VALUES(%s,%s,%s,'admin')",
                (code, value, vip_type)
            )
        else:
            cursor.execute(
                f"INSERT INTO {table}(code, {value_field}, created_by) VALUES(%s,%s,'admin')",
                (code, value)
            )
    conn.commit()
    conn.close()

def fetch_all(table):
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table}")
    rows = cursor.fetchall()
    conn.close()
    return rows

def delete_unused(table):
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM {table} WHERE used=0")
    conn.commit()
    conn.close()

