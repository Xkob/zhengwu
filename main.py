from bot import bot
from dbsql import delmsg,get_user,reguser,cxban,adp,is_user_invited,record_invitation,is_reg,chqd,set_user_vip,setban,getp,isvipu,sedtxt,get_invite_count,csmg,getsluser,getuserps,anpd,tsms,gec,mllb,get_all_today_command_count
import mysql.connector
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import random
import io
from frgn import *
from zfgn import *
from glygn import glygn
from queue import Queue
import ssl
from km import *
from dt import *
import threading
from telebot import types
from cfg import log_query,logger,TRON_WALLET_ADDRESS,TRONGRID_API_KEY,USDT_CONTRACT,RECHARGE_OPTIONS,MEMBERSHIP_OPTIONS,GN_ACTIONS,qid,MAX_DAILY_COMMANDS,USDTJG,ADMIN_IDS
from datetime import datetime,timedelta,date
import aiohttp
import asyncio
import time
from handlera import cmd1
from cmd2 import cmd2
from cfg import TARGET_CHAT_ID,KEYWORD,CHANNEL_ID,sendid,BUTTONS_PER_PAGE,CATEGORY_MAP
from dbsql import checkqd,generate_unique_random_amount,getqd,get_vip_level,is_today_holiday_or_weekend,next_holiday_or_weekend,mark_reminded_today,has_reminded_today,qrxxdqh
from dbsql import clear_user_qd,user_info,adusdt,getusdt
from kh.cfg2 import user_jobs,refresh_token,worker

import logging
logging.getLogger("mysql.connector").setLevel(logging.WARNING)


_background_loop = asyncio.new_event_loop()

def _start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()
def safe_ensure_async(coro):
    """在同步环境中安全调度异步协程，不堵主线程"""
    return asyncio.run_coroutine_threadsafe(coro, _background_loop)
threading.Thread(target=_start_loop, args=(_background_loop,), daemon=True).start()
clear_user_qd(8022175265)
bot_info = bot.get_me()
print(f"机器人ID: {bot_info.id}")
print(f"机器人用户名: @{bot_info.username}")
print(f"机器人全名: {bot_info.first_name}")
ksmarkup = InlineKeyboardMarkup()
ksmarkup.row_width = 1
btn1 = InlineKeyboardButton("大群", url="https://t.me/XiaoHaiGe_SGK")
btn2 = InlineKeyboardButton("备用", url="https://t.me/xiaohaigeleyuan")
btn3 = InlineKeyboardButton("政务频道", url="https://t.me/xhgzw")
btn4 = InlineKeyboardButton("频道", url="https://t.me/xiaohaigeSGK")
btn5 = InlineKeyboardButton("频道", url="https://t.me/xiaohaigechadang")
btn6 = InlineKeyboardButton("频道", url="https://t.me/yndbxc")
ksmarkup.add(btn1, btn2, btn3, btn4, btn5,btn6)
glygn(bot)
cmd1(bot)
cmd2(bot)
kmgn(bot)
gly(bot)
dt(bot)

frgn(bot)

start_frgn_worker(bot)


start_zf_worker(bot)
zhuanfan(bot)
def yaq(inviter_id):
    amarkup = InlineKeyboardMarkup()
    amarkup.row_width = 1
    btn1 = InlineKeyboardButton("大群", url="https://t.me/XiaoHaiGe_SGK")
    btn2 = InlineKeyboardButton("备用", url="https://t.me/xiaohaigeleyuan")
    btn3 = InlineKeyboardButton("政务频道", url="https://t.me/xhgzw")
    btn4 = InlineKeyboardButton("频道", url="https://t.me/xiaohaigeSGK")
    btn5 = InlineKeyboardButton("频道", url="https://t.me/xiaohaigechadang")
    btn6 = InlineKeyboardButton("⏺️进入频道后点击此处", url=f"https://t.me/{bot.get_me().username}?start={inviter_id}")
    amarkup.add(btn1, btn2, btn3, btn4, btn5,btn6)
    return amarkup
def generate_category_buttons():
    """生成一级分类按钮"""
    keyboard = types.InlineKeyboardMarkup()
    row = []
    for prefix, label in CATEGORY_MAP.items():
        btn = types.InlineKeyboardButton(
            text=label,
            callback_data=f"cat_{prefix}"
        )
        row.append(btn)
        if len(row) == 2:
            keyboard.row(*row)
            row = []
    if row:
        keyboard.row(*row)
    return keyboard


def generate_action_buttons(prefix: str, page: int = 0):
    """生成二级命令按钮"""
    keyboard = types.InlineKeyboardMarkup()
    items = [(cmd, value) for cmd, value in GN_ACTIONS.items() if cmd.startswith(prefix)]
    total_pages = (len(items) + BUTTONS_PER_PAGE - 1) // BUTTONS_PER_PAGE

    start = page * BUTTONS_PER_PAGE
    end = start + BUTTONS_PER_PAGE
    page_items = items[start:end]

    row = []
    for i, (cmd, value) in enumerate(page_items, 1):
        label = value[0]
        button = types.InlineKeyboardButton(
            text=label,
            callback_data=f"gn_{cmd}"
        )
        row.append(button)
        if i % 2 == 0:
            keyboard.row(*row)
            row = []
    if row:
        keyboard.row(*row)

    # 翻页
    nav_buttons = []
    if page > 0:
        nav_buttons.append(types.InlineKeyboardButton(
            text="⬅️ 上一页", callback_data=f"cat_{prefix}_page_{page-1}"
        ))
    if page < total_pages - 1:
        nav_buttons.append(types.InlineKeyboardButton(
            text="下一页 ➡️", callback_data=f"cat_{prefix}_page_{page+1}"
        ))
    if nav_buttons:
        keyboard.row(*nav_buttons)

    # 返回分类
    keyboard.row(types.InlineKeyboardButton(
        text="🔙 返回分类", callback_data="back_to_categories"
    ))

    return keyboard


def delete_notification(chat_id, message_id):
    time.sleep(10)
    delmsg(chat_id, message_id)

def yq(user_id, inviter_id):
    # 自邀 or 无效 inviter_id 直接跳过
    if str(user_id) == str(inviter_id):
        bot.send_message(user_id, "你不能邀请自己哦！")
        return

    if is_user_invited(user_id):
        bot.send_message(user_id, "你已经被邀请过了哦！")
        return

    # 二次验证关注（防止刷邀请）
    if not checkqd(user_id):
        bot.send_message(
            user_id,
            f"💁‍♂️你好, 请先关注频道后才能使用邀请码",
            parse_mode="html",
            reply_markup=yaq(inviter_id)
        )
        return

    # 记录邀请 & 加分
    record_invitation(user_id, inviter_id)
    adp(inviter_id, 2)
    bot.send_message(user_id, "🎉 注册成功！YNDBZW-2.0欢迎你 /start 点击加载机器人")
    bot.send_message(inviter_id, f"你成功邀请了用户 {user_id}，奖励1积分已发放 🎁")

@bot.message_handler(commands=['start'])
def handle_start(message):
    if message.chat.type != "private":
        delmsg(message.chat.id, message.message_id)
        return
    user_id = str(message.from_user.id)
    if tsms():
        if message.from_user.id not in ADMIN_IDS:
            delmsg(message.chat.id, message.message_id)
            bot.send_message(user_id, "当前正在检修中/添加功能中 机器人停止使用 稍安勿躁...")
            return
    args = message.text.split()
    inviter_id = args[1] if len(args) > 1 else None
    try:
        result = reguser(user_id)
        # 🎉 新注册用户
        if result != "0":
            bot.send_message(user_id, result)
            if inviter_id:
                yq(user_id, inviter_id)
        else:
            #概率触发人机验证
            if random.randint(1, 20) == 5:
                bot.send_message(user_id, "💁‍♂️你好, 已经触发人机认证 /start 👈点击完成认证")
                delmsg(message.chat.id, message.message_id)
                return
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(
                types.InlineKeyboardButton("✅️命令列表", callback_data="mllist"),
                types.InlineKeyboardButton("👤个人中心", callback_data="me")
            )
            keyboard.add(
                types.InlineKeyboardButton("💰️充值", callback_data="cz"),
            )
            keyboard.add(types.InlineKeyboardButton("💁‍主频道", url="https://t.me/xhgzw"))
            effect_id = random.choice(sendid)
            keyboard.add(types.InlineKeyboardButton("⭐使用卡密", callback_data="km"))
            if get_vip_level(user_id) == 2:
                bot.send_message(user_id, f"<a href='https://origin.picgo.net/2025/08/16/123321c7b5db4157eaa3.png'>🆕</a>你好尊贵的 {message.from_user.first_name} 少爷 欢迎回家", reply_markup=keyboard,parse_mode='HTML',message_effect_id=effect_id)
            elif get_vip_level(user_id) == 1:
                bot.send_message(user_id, "<a href='https://origin.picgo.net/2025/08/16/123321c7b5db4157eaa3.png'>📶</a>发现数据的价值,创造无限可能!", reply_markup=keyboard,parse_mode='HTML',message_effect_id=effect_id)
            elif get_vip_level(user_id) == 4:
                bot.send_message(user_id, "<a href='https://origin.picgo.net/2025/08/16/123321c7b5db4157eaa3.png'>📶</a>发现数据的价值,创造无限可能!", reply_markup=keyboard,parse_mode='HTML',message_effect_id=effect_id)
                bot.send_message(user_id, "⚠您的VIP已经过期 请尽快续费")
            else:
                bot.send_message(user_id, "<a href='https://origin.picgo.net/2025/08/16/123321c7b5db4157eaa3.png'>🆕</a>Hello Word!", reply_markup=keyboard,parse_mode='HTML',message_effect_id=effect_id)

        delmsg(message.chat.id, message.message_id)
    except Exception as e:
        print(f"start 错误: {e}")


@bot.message_handler(content_types=['document'])
def handle_file(message):
    try:
        if message.chat.type != "private":
            return
            # 限制文件类型为 txt
        if not message.document.file_name.endswith(".txt"):
            return
        user_id = message.from_user.id
        chat_id = message.chat.id
        file_info = bot.get_file(message.document.file_id)
        downloaded = bot.download_file(file_info.file_path)
        file_stream = io.StringIO(downloaded.decode("utf-8"))
        phone_numbers = [line.strip() for line in file_stream if line.strip()]
        phone_numbers2 = phone_numbers[:10]  # 限制前10个手机号
        if not isvipu(user_id):
            jf = getp(user_id)
            if jf < len(phone_numbers2):
                bot.send_message(user_id, "积分不足，请签到或充值获取")
                return
        if not phone_numbers2:
            bot.reply_to(message, "文件中没有手机号 ❌")
            return

        # 初始化用户任务
        user_jobs[chat_id] = {
            "queue": Queue(),
            "processed": set(),
            "results": [],
            "phones": phone_numbers2,
            "lock": threading.Lock()  # 每个用户自己的锁
        }

        # 创建确认按钮
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("手机号批量检测空号", callback_data=f"start_check_{chat_id}_{len(phone_numbers2)}"))

        bot.reply_to(
            message,
            f"📥 收到文件，共 {len(phone_numbers2)} 个手机号（机器人限制单次核验10个）。请点击下面按钮确认开始核验。",
            reply_markup=markup
        )

    except Exception as e:
        bot.reply_to(message, f"处理文件出错 请重上传 多次错误联系管理员")
        print("上传文件",e)
async def check_payment_and_update(bot, user_id, random_amount, original_amount, recharge_type, message_id):
    """
    检查支付并在确认后更新用户账户
    :param bot: Telebot实例
    :param user_id: 用户ID
    :param random_amount: 要检查的精确金额
    :param original_amount: 用户选择的原始金额
    :param recharge_type: 充值类型 (points/membership)
    :param message_id: 要更新的消息ID
    """
    max_retries = 120  # 10分钟，每5秒检查一次
    payment_successful = False

    # 创建支付跟踪ID
    payment_trace_id = f"{user_id}_{random_amount}_{int(time.time())}"
    logger.info(f"开始检查支付: {payment_trace_id}")

    for attempt in range(max_retries):
        try:
            if payment_successful:
                # 支付已处理，退出循环
                break

            # 检查支付状态
            paid = await check_tron_payment(TRON_WALLET_ADDRESS, random_amount)

            if paid and not payment_successful:
                payment_successful = True
                logger.info(f"用户 {user_id} 的支付成功，金额: {random_amount}，来源: TronGrid API")
                bot.send_message(qid,f"用户 {user_id} 的支付成功，金额: {random_amount}，来源: TronGrid API")

                # 记录充值日志
                await log_recharge_record(
                    user_id=user_id,
                    recharge_type=recharge_type,
                    amount=f"{original_amount} USDT ({random_amount})",
                    status="success"
                )

                # 根据充值类型更新用户账户
                if recharge_type == 'points':
                    points = RECHARGE_OPTIONS[original_amount]["points"]
                    bonus = RECHARGE_OPTIONS[original_amount]["bonus"]
                    total_points = points + int(points * bonus / 100)

                    # 将积分添加到用户账户
                    adp(user_id, total_points)
                    success_msg = f"<b>充值成功！</b>\n您获得了 <b>{total_points}</b> 积分（基础{points}+赠送{bonus}%）"
                elif recharge_type == 'usdt':
                    USDT = USDTJG[original_amount]["U"]
                    adusdt(user_id, USDT)
                    success_msg = f"<b>充值成功！</b>\n您获得了 <b>{USDT}</b> 绿宝石"
                    try:
                        bot.edit_message_text(
                            chat_id=user_id,
                            message_id=message_id,
                            text=success_msg,
                            parse_mode='HTML'
                        )
                    except Exception as edit_err:
                        logger.error(f"更新成功消息时出错: {edit_err}")
                    break
                elif recharge_type == 'membership':
                    days = MEMBERSHIP_OPTIONS[original_amount]["days"]
                    # 使用原始代码库中的set_vip函数
                    if days >= 36500:  # 如果是终身会员
                        set_user_vip(user_id,2)
                        success_msg = "<b>充值成功！</b>\n您获得了<b>终身SVIP会员</b>"
                    else:
                        set_user_vip(user_id,1,days)
                        if days >= 365:
                            success_msg = f"<b>充值成功！</b>\n您获得了 <b>{days // 365}年</b> VIP会员"
                        elif days >= 30:
                            success_msg = f"<b>充值成功！</b>\n您获得了 <b>{days // 30}个月</b> VIP会员"
                        else:
                            success_msg = f"<b>充值成功！</b>\n您获得了 <b>{days}天</b> VIP会员"
                else:
                    success_msg = "无效的充值类型选择"
                try:
                    bot.edit_message_text(
                        chat_id=user_id,
                        message_id=message_id,
                        text=success_msg,
                        parse_mode='HTML'
                    )
                except Exception as edit_err:
                    logger.error(f"更新成功消息时出错: {edit_err}")
                break
        except Exception as e:
            logger.error(f"检测支付状态或更新用户信息时出错: {e}")

        await asyncio.sleep(5)  # 每5秒检查一次

    if not payment_successful:
        # 记录超时日志
        await log_recharge_record(
            user_id=user_id,
            recharge_type=recharge_type,
            amount=f"{original_amount} USDT ({random_amount})",
            status="timeout"
        )

        timeout_msg = "<b>支付超时</b>\n请重新尝试充值或联系客服。"
        try:
            bot.edit_message_text(
                chat_id=user_id,
                message_id=message_id,
                text=timeout_msg,
                parse_mode="HTML"
            )
        except Exception as edit_err:
            logger.error(f"更新超时消息时出错: {edit_err}")
async def log_recharge_record(user_id, recharge_type, amount, status):
    """
    记录充值信息到日志文件
    :param user_id: 用户ID
    :param recharge_type: 充值类型 (points/membership/usd)
    :param amount: 充值金额（float或int）
    :param status: 充值状态 (success/failed/timeout)
    """
    try:
        expiry_time = datetime.now() + timedelta(minutes=10)
        expiry_time_str = expiry_time.strftime('%Y-%m-%d %H:%M:%S')
        msg = (f"🧾 用户ID: {user_id} | 类型: {recharge_type} | 金额: {amount} | 状态: {status} | 时间: {expiry_time_str}")
        logger.info(msg)
        print(f"✅ 充值记录已保存: {msg}")  # 可选调试输出
    except Exception as e:
        logger.error(f"记录充值日志时出错: {e}")


async def check_tron_payment(address, amount):
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    start_timestamp = int((datetime.now() - timedelta(minutes=30)).timestamp() * 1000)
    try:
        # TronGrid API请求配置
        trongrid_url = f"https://api.trongrid.io/v1/accounts/{address}/transactions/trc20"
        trongrid_params = {
            "limit": 50,  # 最多返回50条记录
            "contract_address": USDT_CONTRACT,  # USDT合约地址
            "min_timestamp": start_timestamp,  # 最小时间戳
            "only_confirmed": "true"  # 只返回已确认的交易
        }

        trongrid_headers = {
            "TRON-PRO-API-KEY": TRONGRID_API_KEY,
            "Accept": "application/json"
        }

        connector = aiohttp.TCPConnector(ssl=ssl_context)
        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.get(trongrid_url, params=trongrid_params, headers=trongrid_headers) as response:
                if response.status == 200:
                    data = await response.json()
                    if "data" in data and isinstance(data["data"], list):
                        tx_count = len(data["data"])
                        # 记录所有交易金额
                        all_tx_amounts = []

                        for tx in data["data"]:
                            # 只检查转入交易
                            if tx.get("to") == address:
                                # 验证合约是USDT
                                if tx.get("token_info", {}).get("address") != USDT_CONTRACT:

                                    continue

                                # 验证交易已确认
                                if not tx.get("block_timestamp"):

                                    continue
                                if tx.get("type") != "Transfer":

                                    continue
                                tx_value = int(tx.get("value", "0"))
                                tx_amount = tx_value / 1000000
                                tx_hash = tx.get("transaction_id", "未知")
                                tx_time_str = "未知"
                                if "block_timestamp" in tx:
                                    tx_time = datetime.fromtimestamp(int(tx.get("block_timestamp", 0)) / 1000)
                                    tx_time_str = tx_time.strftime("%Y-%m-%d %H:%M:%S")
                                all_tx_amounts.append(
                                    f"{tx_amount} USDT (交易ID: {tx_hash}, 时间: {tx_time_str})")
                                expected_amount = float(amount)
                                if abs(tx_amount - expected_amount) <= 0.000001:
                                    if tx_amount == expected_amount:
                                        pass
                                    else:
                                        logger.info(
                                            f"TronGrid找到近似匹配交易: {tx_hash} 金额: {tx_amount} USDT (期望: {expected_amount})")
                                    return True
                        if all_tx_amounts:
                            pass
                        else:
                            pass
                else:
                    logger.error(
                        f"TronGrid API请求失败: 状态码 {response.status}, 响应: {await response.text()}")

    except Exception as e:
        logger.error(f"TronGrid API检查出错: {e}")
    return False
@bot.callback_query_handler(lambda c: c.data.startswith("cat_") and "_page_" in c.data)
def process_category_page(call):
    try:
        parts = call.data.split("_")
        prefix = parts[1]
        page = int(parts[-1])
        keyboard = generate_action_buttons(prefix, page)
        bot.edit_message_reply_markup(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=keyboard
        )
    except Exception as e:
        print(f"分类翻页出错: {e}")


@bot.callback_query_handler(func=lambda call: call.data.startswith("gn_"))
def handle_gn_callback(call):
    try:
        user_id = call.message.from_user.id
        re3 = random.randint(1, 2)
        if re3 == 2:
            if not anpd(user_id):
                bot.answer_callback_query(call.id, "你点的我好爽，休息一下吧💦")
                return
        re1 = random.randint(1,5)
        if re1 == 2:
            if cxban(user_id):
                bot.answer_callback_query(call.id, "你点的我好爽，休息一下吧💦")
                delmsg(call.message.chat.id, call.message.message_id)
                return
        re2 = random.randint(1, 10)
        if re2 == 5:
            if not checkqd(user_id):
                bot.send_message(
                    user_id,
                    "💁‍♂️你好，请先关注以下频道后才能注册\n完成后点击 /start 重试",
                    parse_mode="HTML",
                    reply_markup=ksmarkup
                )
                delmsg(user_id, call.message.message_id)
                return

        if tsms() and user_id in ADMIN_IDS:
            bot.answer_callback_query(call.id, "当前正在检修中/添加功能中 机器人停止使用 稍安勿躁...", show_alert=True)
            return

        cmd_key = call.data[3:]  # 去掉 'gn_' 前缀
        if cmd_key in GN_ACTIONS:
            # 获取功能信息，最多 4 个元素
            item = GN_ACTIONS[cmd_key]
            name, example, price = item[:3]
            remark = item[3] if len(item) > 3 and item[3] else None

            bot.answer_callback_query(call.id)

            text = f"📌 <b>功能名称：</b>{name}\n"
            text += f"📎 <b>使用方法：</b><code>{example}</code>\n"
            text += f"💰 <b>所需积分：</b>{price} 分\n"
            if remark:
                text += f"📝 <b>备注：</b>{remark}"

            # 发送消息并自动删除
            mj = bot.send_message(call.message.chat.id, text, parse_mode="HTML")
            threading.Thread(
                target=delete_notification,
                args=(call.message.chat.id, mj.message_id)
            ).start()
        else:
            bot.answer_callback_query(call.id, "⚠️ 未知功能")
    except Exception as e:
        print("Callback query 已过期:", e)

@bot.callback_query_handler(lambda c: c.data.startswith("cat_") and "_page_" not in c.data)
def process_category(call):
    try:
        prefix = call.data.split("_", 1)[1]
        keyboard = generate_action_buttons(prefix, page=0)

        bot.edit_message_text(
            "请选择功能：",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=keyboard
        )
    except Exception as e:
        print(f"分类跳转出错: {e}")




@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    try:
        user_id = call.from_user.id
        data = call.data
        message_id = call.message.message_id
        re12 = random.randint(1, 5)
        if re12 == 2:
            if cxban(user_id):
                delmsg(call.message.chat.id, call.message.message_id)  # 改这里
                bot.answer_callback_query(call.id, "你点的我好爽，休息一下吧💦")
                return
        if not anpd(user_id):
            bot.answer_callback_query(call.id, "你点的我好爽，休息一下吧💦")
            return
        re1 = random.randint(1,10)
        if re1 == 2:
            if not checkqd(user_id):
                bot.send_message(
                    user_id,
                    "💁‍♂️你好，请先关注以下频道后才能注册\n完成后点击 /start 重试",
                    parse_mode="html",
                    reply_markup=ksmarkup
                )
                delmsg(call.message.chat.id,call.message.message_id)
                return
        if tsms():
            if user_id not in ADMIN_IDS:
                bot.answer_callback_query(call.id, "当前正在检修中/添加功能中 机器人停止使用 稍安勿躁...",show_alert=True)
                return

        if data == "me":

            user = get_user(user_id)
            if not user:
                return
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("邀请🔗", callback_data="getp"),
                       types.InlineKeyboardButton("📅签到", callback_data="qd"))
            markup.add(types.InlineKeyboardButton("❌关闭", callback_data="del"))
            if user['vip'] == 2:
                vip_status = "✅ 永久VIP"
            elif user['vip'] == 1 and user['VIPTIME'] and user['VIPTIME'] >= date.today():
                vip_status = "✅ 普通VIP"
            else:
                vip_status = "Free版"

            lines = [
                "👤 <b>我的账户</b>\n\n",
                "查询规则:",
                "<pre>• 有效期内会员: 查询不扣除积分",
                "• 普通积分用户: 有效使用扣除相应积分",
                "• 如你查询敏感身份 政务团队有权对你账号进行封禁</pre>",
                f"🪪 ID: <code>{user['userid']}</code>",
                f"👛 绿宝石:{getusdt(user_id)}",
                f"💯 积分: {user.get('points', 0)}",
                f"💎 会员: {vip_status}",
                f"<a href='https://origin.picgo.net/2025/08/16/123321c7b5db4157eaa3.png'>⏰</a> VIP到期: {user.get('VIPTIME') or '无'}",
                f"🛃今日上限：{gec(user_id)}/{MAX_DAILY_COMMANDS}"
                f"\n\n💁<u>‍需要客服支援？</u>"
                f"\n\n👉⌊ 联系 12 小时客服专员 @yndb08 ⌉"

            ]

            message_text = "\n".join(lines)

            bot.send_message(
                user_id,
                message_text,
                parse_mode="HTML",
                reply_markup=markup
            )
        elif data == "del":
            delmsg(call.message.chat.id, call.message.message_id)
        elif data.startswith("start_check_"):
            parts = call.data.split("_")
            chat_id = int(parts[-2])
            jf = int(parts[-1])
            delmsg(chat_id=call.message.chat.id, message_id=call.message.message_id)
            if not mllb(user_id):
                bot.send_message(chat_id,
                             f"⚠️ 使用过于频繁或已达上限，请稍后再试！\n🕐\n🛃今日上限：{gec(user_id)}/{MAX_DAILY_COMMANDS}")
                return
            if chat_id not in user_jobs:
                bot.answer_callback_query(call.id, "没有找到待核验的数据 ❌")
                return

            bot.answer_callback_query(call.id, "开始核验手机号 ✅")
            job = user_jobs[chat_id]

            # 初始化队列
            while not job["queue"].empty():
                job["queue"].get()
                job["queue"].task_done()
            job["processed"].clear()
            job["results"].clear()
            for phone in job["phones"]:
                job["queue"].put(phone)

            access_token = refresh_token()

            # 启动线程
            for i in range(10):
                t = threading.Thread(target=worker, args=(chat_id, access_token, i + 1))
                t.daemon = True
                t.start()

            def wait_and_send():
                job["queue"].join()
                result_text = "📋 核验结果:\n\n" + "\n".join(job["results"])
                bot.send_message(chat_id, result_text)
            if not isvipu(user_id):
                adp(user_id, -jf)
                txt = f"\n操作成功，已扣除{jf}积分,剩余积分：{getp(user_id)}"
                bot.send_message(chat_id,txt)

            threading.Thread(target=wait_and_send).start()
        elif data == "getp":
            text = f"偷偷告诉你\n邀请未注册主机器人的用户可获得3倍积分"
            mj = bot.send_message(user_id, text)
            threading.Thread(
                target=delete_notification,
                args=(user_id, mj.message_id)
            ).start()
            keyboard = types.InlineKeyboardMarkup()
            texta = f"{bot_info.first_name} 🏴‍☠️你的专属加入链接：https://t.me/{bot.get_me().username}?start={user_id}"
            button = types.InlineKeyboardButton(text="点击分享", url=f"https://t.me/share/url?url={texta}")
            keyboard.add(button)
            referral_link = f"🐟推广即可免费获得积分\n您的推广总数：{get_invite_count(user_id)}\n💡用户建议：在推特、脸书、INS、Github和TG公开群等地方发送以下广告词,推广成功率极大！\n🔗专属加入链接 https://t.me/{bot.get_me().username}?start={user_id}"
            bot.send_message(user_id, referral_link, parse_mode='html', reply_markup=keyboard)
        elif data =="qd":
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("⏺️确认签到",callback_data="qrqd"))
            markup.add(types.InlineKeyboardButton("❌取消",callback_data="del"))
            markup.add(types.InlineKeyboardButton("❓我不确定我是否添加全部",callback_data="qrpd"))
            bot.send_message(user_id,"关注频道后 @xsdqh 点击下方按钮立即签到\n签到过程中如果关注频道未关注将会扣除5积分😊\n正常签到将会获得1积分",reply_markup=markup)
        elif data =="qrpd":
            try:
                bot.send_message(chat_id=user_id,text="请确保加入了所有频道",reply_markup=ksmarkup)
            except Exception as e:
                print(f"⚠{e}")
        elif data == "cz":
            try:
                bot.delete_message(chat_id=user_id, message_id=message_id)
            except Exception as e:
                print(f"⚠️ 删除消息失败: {e}")
            markup = types.InlineKeyboardMarkup(row_width=4)
            points_buttons = []
            for amount, details in RECHARGE_OPTIONS.items():
                button_text = f"💰 {amount} USDT - {details['points']}积分"
                if details['bonus'] > 0:
                    button_text += f" (+{details['bonus']}%)"
                callback_data = f"points_{amount}"
                points_buttons.append(types.InlineKeyboardButton(button_text, callback_data=callback_data))

            vip_buttons = []
            for amount, details in MEMBERSHIP_OPTIONS.items():
                days = details['days']
                button_text = f"💎 {amount} USDT - "
                if days >= 36500:
                    button_text += "终身会员"
                elif days >= 365:
                    button_text += f"{days // 365}年会员"
                elif days >= 30:
                    button_text += f"{days // 30}个月会员"
                else:
                    button_text += f"{days}天会员"
                callback_data = f"vip_{amount}"
                vip_buttons.append(types.InlineKeyboardButton(button_text, callback_data=callback_data))

            # 初始化 markup
            markup = types.InlineKeyboardMarkup(row_width=2)

            # 添加 points_buttons（每行两个）
            for i in range(0, len(points_buttons), 2):
                markup.add(*points_buttons[i:i + 2])

            # 添加分隔符
            markup.add(types.InlineKeyboardButton("🔹 VIP会员充值 🔹", callback_data="separator"))

            # 添加 vip_buttons（每行两个）
            for i in range(0, len(vip_buttons), 2):
                markup.add(*vip_buttons[i:i + 2])

            # 添加取消按钮（单独一行）
            markup.add(types.InlineKeyboardButton("❌ 取消", callback_data="cancel_recharge"))

            # 发送充值选项消息
            recharge_text = (
                "📊 <b>充值选项</b>\n\n"
                "<pre>🔸 积分充值:\n"
                "- 10 USDT = 50积分\n"
                "- 20 USDT = 110积分 (+10%)\n"
                "- 50 USDT = 288积分 (+15%)\n"
                "- 100 USDT = 600积分 (+20%)\n"
                "- 300 USDT = 2000积分 (+33%)\n\n"
                "🔸 <b>会员充值:</b>\n"
                "- 20 USDT = 7天会员\n"
                "- 50 USDT = 30天会员\n"
                "- 100 USDT = 3个月会员\n"
                "- 300 USDT = 1年会员\n"
                "- 500 USDT = 终身会员\n\n</pre>"
                "-自助充值机器人 @xhgshop_bot- 支持微信 支付宝-\n"
                "-人工客服 @yndb08-\n"
                "<code>👇请选择充值选项👇</code>"
            )

            bot.send_message(user_id, recharge_text, reply_markup=markup, parse_mode='HTML')
            USDT_buttons = []
            for amount, details in USDTJG.items():
                button_text = f"💰 {amount} USDT - {details['U']}USDT"
                callback_data = f"usdt_{amount}"
                USDT_buttons.append(types.InlineKeyboardButton(button_text, callback_data=callback_data))
            markup = types.InlineKeyboardMarkup(row_width=2)

            # 添加 points_buttons（每行两个）
            for i in range(0, len(USDT_buttons), 2):
                markup.add(*USDT_buttons[i:i + 2])
            # 添加取消按钮（单独一行）
            markup.add(types.InlineKeyboardButton("❌ 取消", callback_data="cancel_recharge"))
            bot.send_message(user_id, "充值绿宝石-仅支持消费无法提现 可用于 大头 医疗 名下车项目", reply_markup=markup, parse_mode='HTML')



        elif data.startswith("points_") or data.startswith("vip_") or data.startswith("usdt_"):
            parts = data.split("_")
            if parts[0] == "points":
                recharge_type = "points"
            elif parts[0] == "vip":
                recharge_type = "membership"
            else:
                recharge_type = "usdt"
            amount = parts[1]

            # 生成带有随机小数的唯一金额
            random_amount = generate_unique_random_amount(amount)

            # 创建支付消息
            if recharge_type == "points":
                points = RECHARGE_OPTIONS[amount]["points"]
                bonus = RECHARGE_OPTIONS[amount]["bonus"]
                caption = f"<b>💞充值积分: {points}积分（送{bonus}%）</b>"
            elif recharge_type == "membership":  # membership
                days = MEMBERSHIP_OPTIONS[amount]["days"]
                if days >= 36500:
                    caption = "<b>💞充值会员: 终身会员</b>"
                elif days >= 365:
                    caption = f"<b>💞充值会员: {days // 365}年</b>"
                elif days >= 30:
                    caption = f"<b>💞充值会员: {days // 30}个月</b>"
                else:
                    caption = f"<b>💞充值会员: {days}天</b>"
            elif recharge_type == "usdt":
                usdt_real = USDTJG[amount]["U"]
                caption = f"<b>💞充值 绿宝石: {usdt_real} USDT</b>"

            # 添加支付说明
            expiry_time = datetime.now() + timedelta(minutes=10)
            expiry_time_str = expiry_time.strftime('%Y-%m-%d %H:%M:%S')

            caption += f"""
    请支付 <code>{random_amount}</code> USDT 到:
    <code>{TRON_WALLET_ADDRESS}</code>
    
    点击USDT地址或金额可复制 也可扫码支付！
    <b>到账金额一定要完全对应，否则无法到帐！</b>
    请在 <b>10 分钟</b>内完成转账，否则订单超时
    订单有效期: <code>{expiry_time_str}</code>
    <i>提示: 付款成功后系统自动到账！</i>"""


            # 创建带有取消按钮的键盘
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(types.InlineKeyboardButton("❌ 取消充值", callback_data="cancel_recharge"))
            user = get_user(user_id)
            if not user:
                return
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("❌关闭", callback_data="del"))
            if user['vip'] == 2:
                vip_status = "✅ 永久VIP"
            elif user['vip'] == 1 and user['VIPTIME'] and user['VIPTIME'] >= date.today():
                vip_status = "✅ 普通VIP"
            else:
                vip_status = "白嫖版"
            ban_status = "完蛋了你" if user['inban'] == 1 else "❌否"
            bot.send_message(qid,
                             f"""用户{user_id}创建了订单为 {random_amount} 金额\n到期时间{expiry_time_str}\n\n\n他的个人信息\n\n🆔 用户ID：<code>{user['userid']}</code>\n\nUSDT余额{user['USDT']}\n\n💰 积分：{user['points']}\n👑 VIP：{vip_status}\n⏰ VIP到期：{user['VIPTIME'] or '无'}\n🔒 是否封禁：{ban_status}\n🛃今日上限：{gec(user_id)}/{MAX_DAILY_COMMANDS}""",
                             reply_markup=markup, parse_mode="html")
            bot.send_message(qid, user_info(user_id))
            # 发送支付二维码
            sent_message = bot.send_message(
                user_id,
                text=caption,
                reply_markup=keyboard,
                parse_mode='HTML'
            )

            # 启动支付检查任务
            safe_ensure_async(
                check_payment_and_update(
                    bot=bot,
                    user_id=user_id,
                    random_amount=random_amount,
                    original_amount=amount,
                    recharge_type=recharge_type,
                    message_id=sent_message.message_id
                )
            )

        elif data == "cancel_recharge":
            try:
                bot.delete_message(call.message.chat.id, call.message.message_id)
            except Exception as e:
                print(f"⚠️ 删除消息失败: {e}")
        elif data == "mllist":
            try:
                bot.delete_message(call.message.chat.id, call.message.message_id)
            except Exception as e:
                print(f"⚠️ 删除消息失败: {e}")

            bot.send_message(user_id, "请选择要使用的功能：",reply_markup=generate_category_buttons())
        elif data == "back_to_categories":
            try:
                keyboard = generate_category_buttons()
                bot.edit_message_text(
                    "请选择分类：",
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    reply_markup=keyboard
                )
            except Exception as e:
                print(f"返回分类出错: {e}")
        elif data == "km":
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("👉免费卡密领取", url="https://t.me/xhgzw"))
            bot.send_message(user_id, "<b>卡密请从正规渠道购买 盗卖卡请联系客服处理</b>\n使用教程👇-点击可复制\n<code>/km 卡密</code>",parse_mode="html",reply_markup=markup)
        elif data =="qrqd":
            user_id = call.from_user.id
            user_name = call.from_user.first_name
            chat_id = call.message.chat.id




            if not is_today_holiday_or_weekend():
                days_left = next_holiday_or_weekend()
                bot.answer_callback_query(
                    call.id,
                    f"今天不是假期，{days_left} 天后才能签到哦~"
                )
                return

            # ✨ 正常签到流程
            try:
                re_msg = chqd(user_name, user_id)
                bot.send_message(chat_id, re_msg, parse_mode='html')
                if not qrxxdqh(user_id):
                    bot.send_message(
                        user_id,
                        "💁‍♂️你好,请先关注 @xsdqh",
                        parse_mode="html",
                        reply_markup=ksmarkup
                    )
                    return
                if not checkqd(user_id):
                    adp(user_id, -5)
                    bot.send_message(
                        user_id,
                        "💁‍♂️你好,感谢你对一诺家园贡献出5积分\n下次注意关注频道别耍小聪明",
                        parse_mode="html",
                        reply_markup=ksmarkup
                    )

            except Exception as e:
                print(f"签到失败: {e}")
        else:
            log_query(user_id, "用户点击了空的按钮", "空")
            return
    except Exception as e:
        print("Callback query 已过期:", e)






while True:
    try:
        bot.infinity_polling(
            timeout=60,
            long_polling_timeout=30,
            skip_pending=True
        )
    except Exception as e:
        print(f"⚠️ polling异常: {e}")
        time.sleep(5)