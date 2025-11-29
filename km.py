from dbsql import *
import random
from cfg import *
import csv
from datetime import datetime, timedelta
import string
def generate_code(length=12):
    """生成随机卡密，只包含大写字母和数字"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
def kmgn(bot):
    @bot.message_handler(commands=["adhelp"])
    def admin_help(message):
        if message.chat.id != qid:
            return
        help_text = (
            "🤖 管理员帮助菜单\n\n"
            "/addkm 数量 - 生成积分卡密\n"
            "/gykm 数量 - 生成公益卡密\n"
            "/delkm - 删除所有未使用卡密\n"
            "/vipkm 天数 类型 - 设置用户 VIP\n"
            "/lb - 导出卡密 (CSV)\n"
            "/help - 查看管理员命令帮助\n"
        )
        bot.send_message(message.chat.id, help_text, parse_mode="HTML")

    @bot.message_handler(commands=['km'])
    def use_km(message):
        user_id = message.from_user.id
        parts = message.text.strip().split()
        if message.chat.type != "private":
            delmsg(message.chat.id, message.message_id)
            return
        if len(parts) < 2:
            bot.reply_to(message, "用法: /km 卡密")
            return

        code = parts[1]

        conn = get_db_conn()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 'point' AS t FROM point_cards WHERE code=%s
            UNION
            SELECT 'vip' FROM vip_cards WHERE code=%s
            UNION
            SELECT 'charity' FROM charity_cards WHERE code=%s
            UNION
            SELECT 'usdt' FROM usdt_cards WHERE code=%s
        """, (code, code, code, code))
        exist = cursor.fetchone()
        conn.close()

        # 校验卡密格式
        if not code.isalnum() or len(code) > 30:
            bot.reply_to(message, "❌ 非法卡密格式")
            return

        # 判断是否存在
        if not exist:
            bot.reply_to(message, "❌ 卡密错误")
            return

        # 公益卡
        if "XHGGY" in code :
            # 先查卡密是否存在及是否已使用
            conn = get_db_conn()
            cursor = conn.cursor()
            cursor.execute("SELECT points, used FROM charity_cards WHERE code=%s", (code,))
            row = cursor.fetchone()
            conn.close()

            if not row:
                bot.reply_to(message, "❌ 公益卡不存在")
                return

            points, used = row
            if used:
                bot.reply_to(message, "❌ 公益卡已使用")
                return

            # 再检查24小时限制
            conn = get_db_conn()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT use_time FROM charity_cards WHERE used=1 AND user_id=%s ORDER BY use_time DESC LIMIT 1",
                (user_id,)
            )
            last = cursor.fetchone()
            conn.close()

            if last and last[0] > datetime.now() - timedelta(hours=24):
                bot.reply_to(
                    message,
                    "\n<pre>公益卡密24小时仅能使用一张</pre>\n看起来你想耍小聪明 🤡 扣你5积分",
                    parse_mode="HTML"
                )
                adp(user_id, -5)
                return

            # 更新卡密状态，增加积分
            update_card_used("charity_cards", code, user_id)
            adp(user_id, points)
            bot.reply_to(message, f"✅ 公益卡使用成功，获得 {points} 积分")
            bot.send_message(qid, f"用户 {user_id} 使用公益卡成功，获得 {points} 积分")
            return
        # ===========================
        # USDT卡
        # ===========================
        conn = get_db_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT amount, used FROM usdt_cards WHERE code=%s", (code,))
        row = cursor.fetchone()
        conn.close()

        if row:
            amount, used = row
            if used:
                bot.reply_to(message, "USDT卡已使用")
                return
            update_card_used("usdt_cards", code, user_id)
            adusdt(user_id, amount)
            bot.reply_to(message, f"USDT卡使用成功，获得 {amount} USDT")
            bot.send_message(qid, f"用户 {user_id} 使用USDT卡成功，获得 {amount} USDT")
            return


        # ===========================
        # 积分卡
        # ===========================
        conn = get_db_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT points, used FROM point_cards WHERE code=%s", (code,))
        row = cursor.fetchone()
        conn.close()

        if row:
            points, used = row
            if used:
                bot.reply_to(message, "积分卡已使用")
                return
            update_card_used("point_cards", code, user_id)
            adp(user_id, points)
            bot.reply_to(message, f"积分卡使用成功，获得 {points} 积分")
            bot.send_message(qid, f"用户 {user_id} 使用积分卡成功，获得 {points} 积分")
            return

        # ===========================
        # VIP卡
        # ===========================
        conn = get_db_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT days, used, vip_type FROM vip_cards WHERE code=%s", (code,))
        row = cursor.fetchone()
        conn.close()

        if row:
            days, used, vip_type = row
            if used:
                bot.reply_to(message, "VIP卡已使用")
                return
            update_card_used("vip_cards", code, user_id)
            set_user_vip(user_id, vip_type, days)
            bot.reply_to(message, f"VIP卡使用成功，开通 {days} 天 VIP")
            bot.send_message(qid, f"用户 {user_id} 使用VIP卡成功，开通 {days} 天 VIP")
            return
def gly(bot):
    @bot.message_handler(commands=['vipkm'])
    def add_vip(message):
        if message.chat.id != qid:
            return
        parts = message.text.strip().split()
        if len(parts) < 4:
            bot.reply_to(message, "用法: /vip 数量 天数 VIP类型")
            return
        num = int(parts[1])
        days = int(parts[2])
        vip_type = int(parts[3])
        codes = [generate_code() for _ in range(num)]
        insert_cards("vip_cards", codes, "days", days, vip_type)
        # 拼接卡密
        text = f"已生成 {num} 张 VIP卡\n"
        text += "\n".join(codes)

        # 避免超过 4096 字符限制
        for i in range(0, len(text), 4000):
            bot.send_message(message.chat.id, text[i:i + 4000])

    @bot.message_handler(commands=['addkm'])
    def add_km(message):
        if message.chat.id != qid:
            return
        parts = message.text.strip().split()
        if len(parts) < 3:
            bot.reply_to(message, "用法: /addkm 数量 积分")
            return
        num = int(parts[1])
        points = int(parts[2])
        codes = [generate_code() for _ in range(num)]
        insert_cards("point_cards", codes, "points", points)
        # 拼接卡密
        text = f"已生成 {num} 张 卡\n"
        text += "\n".join(codes)

        # 避免超过 4096 字符限制
        for i in range(0, len(text), 4000):
            bot.send_message(message.chat.id, text[i:i + 4000])


    @bot.message_handler(commands=['delkm'])
    def del_km(message):
        if message.chat.id != qid:
            return
        delete_unused("point_cards")
        delete_unused("vip_cards")
        delete_unused("charity_cards")
        bot.reply_to(message, "所有未使用卡密已删除")

    @bot.message_handler(commands=['usdtkm'])
    def add_usdtkm(message):
        if message.chat.id != qid:
            return
        parts = message.text.strip().split()
        if len(parts) < 3:
            bot.reply_to(message, "用法: /usdtkm 数量 金额")
            return

        num = int(parts[1])
        amount = float(parts[2])  # 支持小数金额
        codes = [generate_code() for _ in range(num)]

        conn = get_db_conn()
        cursor = conn.cursor()
        for code in codes:
            cursor.execute(
                "INSERT INTO usdt_cards(code, amount, used) VALUES(%s,%s,0)",
                (code, amount)
            )
        conn.commit()
        cursor.close()
        conn.close()

        # 拼接卡密
        text = f"已生成 {num} 张 USDT卡，每张 {amount} USDT\n"
        text += "\n".join(codes)

        # 避免超过 4096 字符限制
        for i in range(0, len(text), 4000):
            bot.send_message(message.chat.id, text[i:i + 4000])

    @bot.message_handler(commands=['lb'])
    def export_km(message):
        if message.chat.id != qid:
            return

        conn = get_db_conn()
        cursor = conn.cursor()
        files = {}

        # 积分卡
        cursor.execute("SELECT code, points, used FROM point_cards")
        rows = cursor.fetchall()
        files["未使用积分卡.csv"] = [r for r in rows if r[2] == 0]
        files["已使用积分卡.csv"] = [r for r in rows if r[2] == 1]

        # VIP卡
        cursor.execute("SELECT code, days, used FROM vip_cards")
        rows = cursor.fetchall()
        files["未使用VIP卡.csv"] = [r for r in rows if r[2] == 0]
        files["已使用VIP卡.csv"] = [r for r in rows if r[2] == 1]

        # 公益卡
        cursor.execute("SELECT code, used FROM charity_cards")
        rows = cursor.fetchall()
        files["未使用公益卡.csv"] = [r for r in rows if r[1] == 0]
        files["已使用公益卡.csv"] = [r for r in rows if r[1] == 1]

        # USDT卡
        cursor.execute("SELECT code, amount, used FROM usdt_cards")
        rows = cursor.fetchall()
        files["未使用USDT卡.csv"] = [r for r in rows if r[2] == 0]
        files["已使用USDT卡.csv"] = [r for r in rows if r[2] == 1]

        cursor.close()
        conn.close()

        # 生成并发送文件
        for fname, data in files.items():
            with open(fname, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                if "VIP" in fname:
                    writer.writerow(["卡密", "天数", "是否使用"])
                elif "积分" in fname:
                    writer.writerow(["卡密", "积分", "是否使用"])
                elif "USDT" in fname:
                    writer.writerow(["卡密", "金额", "是否使用"])
                else:
                    writer.writerow(["卡密", "是否使用"])
                for row in data:
                    writer.writerow(row)

            with open(fname, "rb") as f:
                bot.send_document(message.chat.id, f)

            os.remove(fname)  # 清理临时文件

    # 公益卡生成
    @bot.message_handler(commands=['gykm'])
    def add_gykm(message):
        if message.chat.id != qid:
            return
        conn = get_db_conn()
        cursor = conn.cursor()
        parts = message.text.strip().split()
        if len(parts) < 2:
            bot.reply_to(message, "用法: /gykm 数量")
            return
        num = int(parts[1])
        codes = []  # 用来保存所有生成的卡密
        for _ in range(num):
            code = "XHGGY"+ generate_code()
            points = random.randint(1, 5)  # 随机积分
            cursor.execute(
                "INSERT INTO charity_cards(code, points, created_by) VALUES(%s,%s,'XHGZWGY')",
                (code, points)
            )
            codes.append(code)  # 保存卡密

        conn.commit()

        # 拼接卡密
        text = f"已生成 {num} 张 公益卡\n"
        text += "\n".join(codes)

        # 避免超过 4096 字符限制
        for i in range(0, len(text), 4000):
            bot.send_message(message.chat.id, text[i:i + 4000])