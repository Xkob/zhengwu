from cfg import *
from dbsql import *
import psutil
import time
start_time = time.time()
def format_duration(seconds):
    delta = timedelta(seconds=int(seconds))
    days = delta.days
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{days}天 {hours}小时 {minutes}分 {seconds}秒"
def get_server_status():
    # CPU 使用率
    cpu_percent = psutil.cpu_percent(interval=1)

    # 内存信息
    mem = psutil.virtual_memory()
    total_mem = mem.total / (1024 ** 3)
    used_mem = mem.used / (1024 ** 3)
    free_mem = mem.available / (1024 ** 3)
    mem_percent = mem.percent

    # 网络信息
    net = psutil.net_io_counters()
    sent = net.bytes_sent / (1024 ** 2)
    recv = net.bytes_recv / (1024 ** 2)

    # 系统运行时间
    boot_time = psutil.boot_time()
    uptime = format_duration(time.time() - boot_time)


    # 脚本运行时间
    script_uptime = format_duration(time.time() - start_time)
    today_qd, total_qd = getqd()
    info = (
        "▎<b>服务器运行情况</b>：\n"
        f"🧠 CPU 使用率: <b>{cpu_percent:.1f}%</b>\n"
        f"💾 内存总量: <b>{total_mem:.2f} GB</b>\n"
        f"📦 已用内存: <b>{used_mem:.2f} GB</b>\n"
        f"📭 剩余内存: <b>{free_mem:.2f} GB</b>\n"
        f"📊 内存使用率: <b>{mem_percent:.1f}%</b>\n"
        f"📤 发送数据: <b>{sent:.2f} MB</b>\n"
        f"📥 接收数据: <b>{recv:.2f} MB</b>\n"
        f"⏱️ 系统运行时间: <b>{uptime}</b>\n"
        f"🐍 脚本运行时间: <b>{script_uptime}</b>\n"
        f"💁🏼 系统总用户: <b>{getsluser()}</b>\n"
        f"🛃 今日系统总用户指令使用次数: <b>{get_all_today_command_count()}</b>\n"
        f"✅ 系统总积分(不包括大于1000): <b>{getuserps()}</b>\n"
        f"➡️ 今日签到人数: {today_qd}，总签到人数: {total_qd}\n"
    )

    return info
def glygn(bot):
    @bot.message_handler(commands=['addusdt'])
    def add_usdt_command(message):
        if message.chat.type == "private":
            return
        if message.chat.id != qid:
            return
        args = message.text.split()
        if len(args) < 2:
            bot.reply_to(message, "❗ 请指定目标用户，例如 /addusdt uid 5 或 /addusdt 123456789 -2")
            return
        # 获取加分数量
        try:
            points = float(args[2]) if len(args) > 2 else 1.0
        except ValueError:
            bot.reply_to(message, "❗ 金额格式错误，请输入数字，例如 2.5")
            return

        # 执行加分
        success = adusdt(args[1], points)

        if success:

            bot.send_message(qid, f"管理员 {message.from_user.id} 为 {args[1]} 修改积分\n金额: {points}")
            bot.send_message(args[1],
                             f"XHG-✅收款成功\n\n转账用户：XHG Admin\n收款金额： {points} USDT")
        else:
            bot.reply_to(message, "⚠️ 操作失败，用户不存在或数据库错误")

    @bot.message_handler(commands=['add'])
    def add_points_command(message):
        if message.chat.type == "private":
            return
        if message.chat.id != qid:
            return
        args = message.text.split()
        if len(args) < 2:
            bot.reply_to(message, "❗ 请指定目标用户，例如 /add uid 5 或 /add 123456789 2")
            return
        # 获取加分数量
        try:
            points = int(args[2]) if len(args) > 2 else 1
        except:
            points = 1

        # 执行加分
        success = adp(args[1], points)

        if success:

            bot.send_message(qid, f"管理员 {message.from_user.id} 为 {args[1]} 修改积分\n金额: {points}")
            bot.send_message(args[1],
                             f"XHG-✅收款成功\n\n转账用户：XHG Admin\n收款金额： {points} 积分")
        else:
            bot.reply_to(message, "⚠️ 操作失败，用户不存在或数据库错误")

    @bot.message_handler(commands=['ban'])
    def ban_command(message):
        if message.chat.type == "private":
            return
        if message.chat.id != qid:
            return

        args = message.text.split(maxsplit=2)
        if len(args) < 2:
            bot.reply_to(message, "⚠️ 参数格式错误，请使用 /ban 用户ID")
            return

        ban_id = args[1]

        try:
            # 调用你的 setban 封禁函数
            setban(ban_id, 1)

            # 扣除所有积分
            adp(ban_id, -99999999)

            # 清除 VIP
            set_user_vip(ban_id, 0, "1970-01-01")

            bot.reply_to(message, f"✅ 成功封禁 {ban_id}")
        except Exception as e:
            bot.reply_to(message, f"❌ 封禁失败：{e}")

    @bot.message_handler(commands=['uban'])
    def banuucommand(message):
        if message.chat.type == "private":
            return
        if message.chat.id != qid:
            return

        args = message.text.split(maxsplit=2)
        if len(args) < 2:
            bot.reply_to(message, "⚠️ 参数格式错误，请使用 /ban 用户ID")
            return

        ban_id = args[1]

        try:
            # 调用你的 setban 封禁函数
            setban(ban_id, 0)

            # 扣除所

            # 清
            bot.reply_to(message, f"✅ 成功解禁 {ban_id}")
        except Exception as e:
            bot.reply_to(message, f"❌ 封禁失败：{e}")

    @bot.message_handler(commands=['webinfo'])
    def webinfo1(message):
        if message.chat.type == "private":
            return
        if message.chat.id != qid:
            return
        status = get_server_status()
        bot.send_message(message.chat.id, status, parse_mode='HTML')

    @bot.message_handler(commands=['info'])
    def banuucand(message):
        if message.chat.type == "private":
            return
        if message.chat.id != qid:
            return

        args = message.text.split(maxsplit=2)
        if len(args) < 2:
            bot.reply_to(message, "⚠️ 参数格式错误，请使用 /info 用户ID")
            return

        user = get_user(args[1])
        if not user:
            return
        if user['vip'] == 2:
            vip_status = "✅ 永久VIP"
        elif user['vip'] == 1 and user['VIPTIME'] and user['VIPTIME'] >= date.today():
            vip_status = "✅ 普通VIP"
        else:
            vip_status = "白嫖版"
        ban_status = "封号中" if user['inban'] == 1 else "❌否"
        bot.send_message(message.chat.id,
                         f"""🆔 用户ID：{user['userid']}\n💰 积分：{user['points']}\n👑 VIP：{vip_status}\n⏰ VIP到期：{user['VIPTIME'] or '无'}\n🔒 是否封禁：{ban_status}\nUSDT：{getusdt(args[1])}""")
        bot.send_message(message.chat.id, user_info(args[1]))

    @bot.message_handler(commands=['vip'])
    def handle_vip_command(message):
        # 群聊限制
        if message.chat.type != "supergroup" and message.chat.type != "group":
            return

        # 只允许特定群使用（如限定群 ID）
        if message.chat.id != qid:  # qid 为你设定的管理群 ID
            return

        # 检查是否是管理员
        if message.from_user.id not in ADMIN_IDS:
            bot.reply_to(message, "❌ 你没有权限使用该命令")
            return

        args = message.text.split()
        if len(args) < 3:
            bot.reply_to(message, "❗ 使用格式：/vip 用户ID 类型 [天数（普通VIP需填）]")
            return

        try:
            userid = args[1]
            vip_type = int(args[2])
            days = int(args[3]) if vip_type == 1 and len(args) >= 4 else 0  # 永久VIP无需天数

            result = set_user_vip(userid, vip_type, days)
            bot.reply_to(message, result)
        except Exception as e:
            bot.reply_to(message, f"❌ 设置失败：{e}")