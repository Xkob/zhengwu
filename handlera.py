from cfg import log_query,COMMAND_COOLDOWN_SECONDS,error_keywords,qid,MAX_DAILY_COMMANDS
from shuju import gtqfjg,yss,cx_jzinfo,hljym,zjqy,eys,cyh,fr4,jnqy,tjfc,hbfc,cd,hljyt,nmgxl,tjcz,hlj,submit_code_sync,hbyxq,bjzyz,jyb,sys2,yhkdiqu
from shuju import hyhy,xjcd,fr4y2,zjeys,xl,mxc
from dbsql import get_user,adp,getp,isvipu,sedtxt,csmg,mllb,gec,cxphone,delmsg
from yljl import dowl
import re
from dbsql import *
from konhao import PhoneGetzt
from fr import extract_info
def remove_personal_info(text: str) -> str:
    """
    去掉文本中 【性别 | 出生日期 | 年龄 | 地区】 格式的内容
    """
    return re.sub(r"【.*?】", "", text).strip()
def cmd1(bot):
    @bot.message_handler(commands=['sys'])
    def handle_sys(message):
        user_id = message.from_user.id
        kcjf = 2
        if message.chat.type != "private":
            delmsg(message.chat.id, message.message_id)
            return
        if not isvipu(user_id):
            jf = getp(user_id)
            if jf < kcjf:
                bot.send_message(user_id, "积分不足，请签到或充值获取")
                return
        args = message.text.split(maxsplit=3)
        if len(args) < 4:
            bot.reply_to(message, "❗ 请输入完整参数，例如 /sys 刘艳阳 232303200008271830 18245079091")
            return
        user_id = message.from_user.id
        if not mllb(user_id):
            bot.reply_to(message,
                         f"⚠️ 使用过于频繁或已达上限，请稍后再试！\n🕐今日限制速率：{COMMAND_COOLDOWN_SECONDS}秒\n🛃今日上限：{gec(user_id)}/{MAX_DAILY_COMMANDS}")
            return
        jf = getp(user_id)
        if jf is None:
            bot.send_message(user_id, "用户未注册，请先注册")
            return
        if csmg(bot, qid, args[2], user_id):
            bot.send_message(message.chat.id, "恭喜你触发了敏感库\n已上报TG绑定手机号与IP\n下辈子注意点")
            user = get_user(user_id)
            bot.send_message(qid,
                             f"""\n\n\n他的个人信息\n\n🆔 用户ID：<code>{user['userid']}</code>\n💰 积分：{user['points']}\n⏰ VIP到期：{user['VIPTIME'] or '无'}\n🔒\n🛃今日上限：{gec(user_id)}/{MAX_DAILY_COMMANDS}""",
                             parse_mode="html")
            if not isvipu(user_id):
                jf = getp(user_id)
                if jf < 2:
                    bot.send_message(user_id, "积分不足，请签到或充值获取")
                    return
        log_query(user_id, args[0], f"{args[1]}-{args[2]}-{args[3]}")
        bot.reply_to(message, f"机器人收到了你的命令请等待返回\n{args[1]}-{args[2]}-{args[3]}", parse_mode="html")
        re = sys2(args[1], args[2], args[3])

        txt = f"{re}"
        response_text = re
        if any(keyword in response_text for keyword in error_keywords):
            bot.send_message(user_id, f"查询接口返回空 或 错误 ")
            return
        if not isvipu(user_id):
            adp(user_id, -2)
            txt += f"\n操作成功，已扣除2积分,剩余积分：{getp(user_id)}"
        bot.send_message(user_id, txt)


    @bot.message_handler(commands=['qfjg'])
    def handle_qfjg(message):
        if message.chat.type != "private":
            delmsg(message.chat.id, message.message_id)
            return
        kcjf = 1
        args = message.text.split(maxsplit=3)
        if len(args) < 2:
            bot.reply_to(message, "❗ 请输入完整参数，例如 /qfjg 232303200008271830")
            return
        user_id = message.from_user.id
        if not mllb(user_id):
            bot.reply_to(message,
                         f"⚠️ 使用过于频繁或已达上限，请稍后再试！\n🕐今日限制速率：{COMMAND_COOLDOWN_SECONDS}秒\n🛃今日上限：{gec(user_id)}/{MAX_DAILY_COMMANDS}")
            return
        if not isvipu(user_id):
            jf = getp(user_id)
            if jf < kcjf:
                bot.send_message(user_id, "积分不足，请签到或充值获取")
                return
        log_query(user_id, args[0], f"{args[1]}")
        bot.reply_to(message, f"机器人收到了你的命令请等待返回\n{args[1]}", parse_mode="html")
        re = gtqfjg(args[1])
        response_text = re
        if any(keyword in response_text for keyword in error_keywords):
            bot.send_message(user_id, f"接口 死亡 或 出错 请重新查询 ")
            return
        txt = f"\n结果 ：\n{args[1]}\n结果：{re}"
        if not isvipu(user_id):
            adp(user_id, -1)
            txt += f"\n操作成功，已扣除{kcjf}积分,剩余积分：{getp(user_id)}"
        bot.send_message(user_id, txt)

    @bot.message_handler(commands=['sjh'])
    def handle_111yys(message):
        if message.chat.type != "private":
            delmsg(message.chat.id, message.message_id)
            return
        kcjf = 1
        args = message.text.split(maxsplit=3)
        if len(args) < 2:
            bot.reply_to(message, "❗ 请输入完整参数，例如 /sjh 13377572388")
            return
        user_id = message.from_user.id
        if not mllb(user_id):
            bot.reply_to(message,
                         f"⚠️ 使用过于频繁或已达上限，请稍后再试！\n🕐今日限制速率：{COMMAND_COOLDOWN_SECONDS}秒\n🛃今日上限：{gec(user_id)}/{MAX_DAILY_COMMANDS}")
            return
        jf = getp(user_id)
        if jf < kcjf:
            bot.send_message(user_id, "积分不足，请签到或充值获取")
            return
        log_query(user_id, args[0], f"{args[1]}")
        bot.reply_to(message, f"机器人收到了你的命令请等待返回\n{args[1]}", parse_mode="html")
        re = cxphone(args[1])
        response_text = re
        if any(keyword in response_text for keyword in error_keywords):
            bot.send_message(user_id, f"接口 死亡 或 出错 请重新查询 ")
            return
        txt = f"\n结果 ：\n{args[1]}\n结果：{re}"
        if not isvipu(user_id):
            adp(user_id, -1)
            txt += f"\n操作成功，已扣除{kcjf}积分,剩余积分：{getp(user_id)}"
        bot.send_message(user_id, txt)


    @bot.message_handler(commands=['mhcd'])
    def handle_cd(message):
        if message.chat.type != "private":
            delmsg(message.chat.id, message.message_id)
            return
        kcjf = 5
        args = message.text.split(maxsplit=3)
        if len(args) < 2:
            bot.reply_to(message, "❗ 请输入完整参数，例如 /mhcd 京A99999")
            return
        user_id = message.from_user.id
        if not mllb(user_id):
            bot.reply_to(message,
                         f"⚠️ 使用过于频繁或已达上限，请稍后再试！\n🕐今日限制速率：{COMMAND_COOLDOWN_SECONDS}秒\n🛃今日上限：{gec(user_id)}/{MAX_DAILY_COMMANDS}")
            return
        jf = getp(user_id)
        if jf < kcjf:
            bot.send_message(user_id, "积分不足，请签到或充值获取")
            return
        log_query(user_id, args[0], f"{args[1]}")
        bot.reply_to(message, f"机器人收到了你的命令请等待返回\n{args[1]}", parse_mode="html")
        re = cd(args[1])
        response_text = re
        if any(keyword in response_text for keyword in error_keywords):
            bot.send_message(user_id, f"接口 死亡 或 出错 请重新查询 ")
            return
        txt = f"\n结果 ：\n{args[1]}\n结果：{re}"
        if not isvipu(user_id):
            adp(user_id, -5)
            txt += f"\n操作成功，已扣除{kcjf}积分,剩余积分：{getp(user_id)}"
        bot.send_message(user_id, txt)


    @bot.message_handler(commands=['dqmh'])
    def handle_ahqh(message):
        kcjf = 4
        if message.chat.type != "private":
            delmsg(message.chat.id, message.message_id)
            return
        args = message.text.split(maxsplit=3)
        if len(args) < 2:
            bot.reply_to(message, "❗ 请输入完整参数，例如 /dqmh 手机号")
            return
        user_id = message.from_user.id
        if not mllb(user_id):
            bot.reply_to(message,
                         f"⚠️ 使用过于频繁或已达上限，请稍后再试！\n🕐今日限制速率：{COMMAND_COOLDOWN_SECONDS}秒\n🛃今日上限：{gec(user_id)}/{MAX_DAILY_COMMANDS}")
            return
        jf = getp(user_id)
        if jf < kcjf:
            bot.send_message(user_id, "积分不足，请签到或充值获取")
            return
        log_query(user_id, args[0], f"{args[1]}")
        bot.reply_to(message, f"机器人收到了你的命令请等待返回\n{args[1]}", parse_mode="html")
        try:
            re = cx_jzinfo(args[1])
            if "暂不支持" in re:
                bot.send_message(message.from_user.id, re)
                return
            if "失败" in re:
                bot.send_message(message.from_user.id, re)
                return
            if " 非法手机号" in re:
                bot.send_message(message.from_user.id, re)
                return
            if "请求失败" in re:
                bot.send_message(message.from_user.id, "空")
                return
            txt = f"\n结果 ：\n{args[1]}\n结果：{re}"
            if not isvipu(user_id):
                adp(user_id, -4)
                txt += f"\n操作成功，已扣除{kcjf}积分,剩余积分：{getp(user_id)}"
        except Exception as e:
            print(f"⚠️ 消息失败: {e}")
            bot.send_message(user_id, txt)


    @bot.message_handler(commands=['hljym'])
    def handle_ahqh(message):
        if message.chat.type != "private":
            delmsg(message.chat.id, message.message_id)
            return
        kcjf = 5
        args = message.text.split(maxsplit=3)
        if len(args) < 2:
            bot.reply_to(message, "❗ 请输入完整参数，例如 /hljym 身份证")
            return
        user_id = message.from_user.id
        if not mllb(user_id):
            bot.reply_to(message,
                         f"⚠️ 使用过于频繁或已达上限，请稍后再试！\n🕐今日限制速率：{COMMAND_COOLDOWN_SECONDS}秒\n🛃今日上限：{gec(user_id)}/{MAX_DAILY_COMMANDS}")
            return
        if csmg(bot, qid, args[1], user_id):
            bot.send_message(message.chat.id, "恭喜你触发了敏感库\n已上报TG绑定手机号与IP\n下辈子注意点")
            user = get_user(user_id)
            bot.send_message(qid,
                             f"""\n\n\n他的个人信息\n\n🆔 用户ID：<code>{user['userid']}</code>\n💰 积分：{user['points']}\n⏰ VIP到期：{user['VIPTIME'] or '无'}\n🔒\n🛃今日上限：{gec(user_id)}/{MAX_DAILY_COMMANDS}""",
                             parse_mode="html")

        jf = getp(user_id)
        if jf < kcjf:
            bot.send_message(user_id, "积分不足，请签到或充值获取")
            return
        log_query(user_id, args[0], f"{args[1]}")
        bot.reply_to(message, f"机器人收到了你的命令请等待返回\n{args[1]}", parse_mode="html")
        re = hljym(args[1])

        response_text = re
        if any(keyword in response_text for keyword in error_keywords):
            bot.send_message(user_id, f"接口 死亡 或 出错 请重新查询 ")
            return
        if re == "总接种次数: 0":
            bot.send_message(user_id, f"身份证错误 或 无接种记录 ")
            return

        if not isvipu(user_id):
            adp(user_id, -4)
            txt = f"\n操作成功，已扣除{kcjf}积分,剩余积分：{getp(user_id)}"
            bot.send_message(user_id, txt)
        sedtxt(bot, user_id, re, f"{args[1]}.txt")


    @bot.message_handler(commands=['eys'])
    def handle_eys(message):
        if message.chat.type != "private":
            delmsg(message.chat.id, message.message_id)
            return
        args = message.text.split(maxsplit=3)
        if len(args) < 3:
            bot.reply_to(message, "❗ 请输入完整参数，例如 /eys 刘艳阳 232303200008271830")
            return
        user_id = message.from_user.id
        if not mllb(user_id):
            bot.reply_to(message,
                         f"⚠️ 使用过于频繁或已达上限，请稍后再试！\n🕐今日限制速率：{COMMAND_COOLDOWN_SECONDS}秒\n🛃今日上限：{gec(user_id)}/{MAX_DAILY_COMMANDS}")
            return
        jf = getp(user_id)
        if jf is None:
            bot.send_message(user_id, "用户未注册，请先注册")
            return
        if not isvipu(user_id):
            jf = getp(user_id)
            if jf < 2:
                bot.send_message(user_id, "积分不足，请签到或充值获取")
                return
        if csmg(bot, qid, args[2], user_id):
            bot.send_message(message.chat.id, "恭喜你触发了敏感库\n已上报TG绑定手机号与IP\n下辈子注意点")
            return
        log_query(user_id, args[0], f"{args[1]}-{args[2]}")
        bot.reply_to(message, f"机器人收到了你的命令请等待返回\n{args[1]}-{args[2]}", parse_mode="html")
        re = eys(args[1], args[2])
        txt = f"\n核验结果 ：\n{args[1]}-{args[2]}\n结果：{re}"
        response_text = re
        if response_text and any(keyword in response_text for keyword in error_keywords):
            bot.send_message(user_id, f"查询接口返回空 或 错误 ")
            return
        if not isvipu(user_id):
            adp(user_id, -2)
            txt += f"\n操作成功，已扣除2积分,剩余积分：{getp(user_id)}"
        bot.send_message(user_id, txt)

    @bot.message_handler(commands=['jzys'])
    def handle_jzeys(message):
        if message.chat.type != "private":
            delmsg(message.chat.id, message.message_id)
            return
        args = message.text.split(maxsplit=3)
        if len(args) < 3:
            bot.reply_to(message, "❗ 请输入完整参数，例如 /jzys 刘艳阳 13377572399")
            return
        user_id = message.from_user.id
        if not mllb(user_id):
            bot.reply_to(message,
                         f"⚠️ 使用过于频繁或已达上限，请稍后再试！\n🕐今日限制速率：{COMMAND_COOLDOWN_SECONDS}秒\n🛃今日上限：{gec(user_id)}/{MAX_DAILY_COMMANDS}")
            return
        jf = getp(user_id)
        if jf is None:
            bot.send_message(user_id, "用户未注册，请先注册")
            return
        if not isvipu(user_id):
            jf = getp(user_id)
            if jf < 2:
                bot.send_message(user_id, "积分不足，请签到或充值获取")
                return
        log_query(user_id, args[0], f"{args[1]}-{args[2]}")
        bot.reply_to(message, f"机器人收到了你的命令请等待返回\n{args[1]}-{args[2]}", parse_mode="html")
        yys,jg = zjeys(args[1], args[2])
        txt = f"\n核验结果 ：\n{args[1]}-{args[2]}\n运营商：{yys}\n核验结果：{jg}"
        if not isvipu(user_id):
            adp(user_id, -2)
            txt += f"\n操作成功，已扣除2积分,剩余积分：{getp(user_id)}"
        bot.send_message(user_id, txt)










    @bot.message_handler(commands=['eys'])
    def handle_eys(message):
        if message.chat.type != "private":
            delmsg(message.chat.id, message.message_id)
            return
        args = message.text.split(maxsplit=3)
        if len(args) < 3:
            bot.reply_to(message, "❗ 请输入完整参数，例如 /eys 刘艳阳 232303200008271830")
            return
        user_id = message.from_user.id
        if not mllb(user_id):
            bot.reply_to(message,
                         f"⚠️ 使用过于频繁或已达上限，请稍后再试！\n🕐今日限制速率：{COMMAND_COOLDOWN_SECONDS}秒\n🛃今日上限：{gec(user_id)}/{MAX_DAILY_COMMANDS}")
            return
        jf = getp(user_id)
        if jf is None:
            bot.send_message(user_id, "用户未注册，请先注册")
            return
        if not isvipu(user_id):
            jf = getp(user_id)
            if jf < 2:
                bot.send_message(user_id, "积分不足，请签到或充值获取")
                return
        if csmg(bot, qid, args[2], user_id):
            bot.send_message(message.chat.id, "恭喜你触发了敏感库\n已上报TG绑定手机号与IP\n下辈子注意点")
            user = get_user(user_id)
            bot.send_message(qid,
                             f"""\n\n\n他的个人信息\n\n🆔 用户ID：<code>{user['userid']}</code>\n💰 积分：{user['points']}\n⏰ VIP到期：{user['VIPTIME'] or '无'}\n🔒\n🛃今日上限：{gec(user_id)}/{MAX_DAILY_COMMANDS}""",
                             parse_mode="html")

        log_query(user_id, args[0], f"{args[1]}-{args[2]}")
        bot.reply_to(message, f"机器人收到了你的命令请等待返回\n{args[1]}-{args[2]}", parse_mode="html")
        re = eys(args[1], args[2])
        txt = f"\n核验结果 ：\n{args[1]}-{args[2]}\n结果：{re}"
        response_text = re
        if any(keyword in response_text for keyword in error_keywords):
            bot.send_message(user_id, f"查询接口返回空 或 错误 ")
            return
        if not isvipu(user_id):
            adp(user_id, -2)
            txt += f"\n操作成功，已扣除2积分,剩余积分：{getp(user_id)}"
        bot.send_message(user_id, txt)




    @bot.message_handler(commands=['yys'])
    def handle_yys(message):
        if message.chat.type != "private":
            delmsg(message.chat.id, message.message_id)
            return
        kcjf = 1
        args = message.text.split(maxsplit=3)
        if len(args) < 2:
            bot.reply_to(message, "❗ 请输入完整参数，例如 /yys 232303200008271830")
            return
        user_id = message.from_user.id
        if not mllb(user_id):
            bot.reply_to(message,
                         f"⚠️ 使用过于频繁或已达上限，请稍后再试！\n🕐今日限制速率：{COMMAND_COOLDOWN_SECONDS}秒\n🛃今日上限：{gec(user_id)}/{MAX_DAILY_COMMANDS}")
            return
        if not isvipu(user_id):
            jf = getp(user_id)
            if jf < kcjf:
                bot.send_message(user_id, "积分不足，请签到或充值获取")
                return
        log_query(user_id, args[0], f"{args[1]}")
        bot.reply_to(message, f"机器人收到了你的命令请等待返回\n{args[1]}", parse_mode="html")
        re = yss(args[1])
        response_text = re
        if any(keyword in response_text for keyword in error_keywords):
            bot.send_message(user_id, f"接口 死亡 或 出错 请重新查询 ")
            return
        txt = f"\n结果 ：\n{args[1]}\n结果：{re}"
        if not isvipu(user_id):
            adp(user_id, -1)
            txt += f"\n操作成功，已扣除{kcjf}积分,剩余积分：{getp(user_id)}"
        bot.send_message(user_id, txt)


    @bot.message_handler(commands=['frhy'])
    def handle_qfjg(message):
        if message.chat.type != "private":
            delmsg(message.chat.id, message.message_id)
            return
        args = message.text.split(maxsplit=5)
        if len(args) < 5:
            bot.reply_to(message,
                         "❗ 请输入完整参数，例如 /frhy 方大炭素新材料科技股份有限公司大酒店分公司 91620111665428781D 张伟 620111197305151013")
            return
        user_id = message.from_user.id
        if not mllb(user_id):
            bot.reply_to(message,
                         f"⚠️ 使用过于频繁或已达上限，请稍后再试！\n🕐今日限制速率：{COMMAND_COOLDOWN_SECONDS}秒\n🛃今日上限：{gec(user_id)}/{MAX_DAILY_COMMANDS}")
            return
        jf = getp(user_id)
        if jf is None:
            bot.send_message(user_id, "用户未注册，请先注册")
            return
        if not isvipu(user_id):
            jf = getp(user_id)
            if jf < 3:
                bot.send_message(user_id, "积分不足，请签到或充值获取")
                return
        log_query(user_id, args[0], args[1])
        bot.reply_to(message, f"机器人收到了你的命令请等待返回\n{args[1]}", parse_mode="html")
        re = fr4(args[1], args[2], args[3], args[4])
        txt = f"\n结果 ：\n{args[1]}\n{args[2]}\n{args[3]}\n{args[4]}\n\n结果：\n{re}"

        response_text = re
        if any(keyword in response_text for keyword in error_keywords):
            bot.send_message(user_id, f"查询接口返回空 或 错误 ")
            return
        if not isvipu(user_id):
            adp(user_id, -5)
            txt += f"\n操作成功，已扣除5积分,剩余积分：{getp(user_id)}"
        bot.send_message(user_id, txt)

    @bot.message_handler(commands=['frhy2'])
    def handle_frhy2(message):
        if message.chat.type != "private":
            delmsg(message.chat.id, message.message_id)
            return
        args = message.text.split(maxsplit=5)
        if len(args) < 5:
            bot.reply_to(message,
                         "❗ 请输入完整参数，例如 /frhy2 91620111665428781D 方大炭素新材料科技股份有限公司大酒店分公司  张伟 620111197305151013")
            return
        user_id = message.from_user.id
        if not mllb(user_id):
            bot.reply_to(message,
                         f"⚠️ 使用过于频繁或已达上限，请稍后再试！\n🕐今日限制速率：{COMMAND_COOLDOWN_SECONDS}秒\n🛃今日上限：{gec(user_id)}/{MAX_DAILY_COMMANDS}")
            return
        jf = getp(user_id)
        if jf is None:
            bot.send_message(user_id, "用户未注册，请先注册")
            return
        if not isvipu(user_id):
            jf = getp(user_id)
            if jf < 5:
                bot.send_message(user_id, "积分不足，请签到或充值获取")
                return
        log_query(user_id, args[0], args[1])
        bot.reply_to(message, f"机器人收到了你的命令请等待返回\n{args[1]}", parse_mode="html")
        re = fr4y2(args[1], args[2], args[3], args[4])
        txt = f"\n结果 ：\n{args[1]}\n{args[2]}\n{args[3]}\n{args[4]}\n\n结果：\n{re}"

        response_text = re
        if any(keyword in response_text for keyword in error_keywords):
            bot.send_message(user_id, f"查询接口返回空 或 错误 ")
            return
        if not isvipu(user_id):
            adp(user_id, -5)
            txt += f"\n操作成功，已扣除5积分,剩余积分：{getp(user_id)}"
        bot.send_message(user_id, txt)










    @bot.message_handler(commands=['hljyt'])
    def handle_cyh(message):
        if message.chat.type != "private":
            delmsg(message.chat.id, message.message_id)
            return
        args = message.text.split(maxsplit=2)
        if len(args) < 2:
            bot.reply_to(message, "❗ 请输入完整参数，例如 /hljyt 230624199701090457")
            return
        user_id = message.from_user.id
        if not mllb(user_id):
            bot.reply_to(message,
                         f"⚠️ 使用过于频繁或已达上限，请稍后再试！\n🕐今日限制速率：{COMMAND_COOLDOWN_SECONDS}秒\n🛃今日上限：{gec(user_id)}/{MAX_DAILY_COMMANDS}")
            return
        jf = getp(user_id)
        if jf is None:
            bot.send_message(user_id, "用户未注册，请先注册")
            return
        if not isvipu(user_id):
            jf = getp(user_id)
            if jf < 7:
                bot.send_message(user_id, "积分不足，请签到或充值获取")
                return
        if csmg(bot, qid, args[1], user_id):
            bot.send_message(message.chat.id, "恭喜你触发了敏感库\n已上报TG绑定手机号与IP\n下辈子注意点")
            user = get_user(user_id)
            bot.send_message(qid,
                             f"""\n\n\n他的个人信息\n\n🆔 用户ID：<code>{user['userid']}</code>\n💰 积分：{user['points']}\n⏰ VIP到期：{user['VIPTIME'] or '无'}\n🔒\n🛃今日上限：{gec(user_id)}/{MAX_DAILY_COMMANDS}""",
                             parse_mode="html")

        log_query(user_id, args[0], f"{args[1]}")
        bot.reply_to(message, f"机器人收到了你的命令请等待返回\n{args[1]}", parse_mode="html")
        re = hljyt(args[1])
        if re == "空":
            bot.send_message(user_id, "结果为空不扣分")
            return
        txt = f"\n结果 ：\n{args[1]}\n结果：{re}"
        response_text = re
        if any(keyword in response_text for keyword in error_keywords):
            bot.send_message(user_id, f"查询接口返回空 或 错误")
            return
        if not isvipu(user_id):
            adp(user_id, -7)
            txt += f"\n操作成功，已扣除7积分,剩余积分：{getp(user_id)}"
        bot.send_message(user_id, txt)


    @bot.message_handler(commands=['frhy'])
    def handle_qfjg(message):
        if message.chat.type != "private":
            delmsg(message.chat.id, message.message_id)
            return
        args = message.text.split(maxsplit=5)
        if len(args) < 5:
            bot.reply_to(message,
                         "❗ 请输入完整参数，例如 /frhy 方大炭素新材料科技股份有限公司大酒店分公司 91620111665428781D 张伟 620111197305151013")
            return
        user_id = message.from_user.id
        if not mllb(user_id):
            bot.reply_to(message,
                         f"⚠️ 使用过于频繁或已达上限，请稍后再试！\n🕐今日限制速率：{COMMAND_COOLDOWN_SECONDS}秒\n🛃今日上限：{gec(user_id)}/{MAX_DAILY_COMMANDS}")
            return
        jf = getp(user_id)
        if jf is None:
            bot.send_message(user_id, "用户未注册，请先注册")
            return
        if jf < 3:
            bot.send_message(user_id, "积分不足，请签到或充值获取")
            return
        log_query(user_id, args[0], args[1])
        bot.reply_to(message, f"机器人收到了你的命令请等待返回\n{args[1]}", parse_mode="html")
        re = fr4(args[1], args[2], args[3], args[4])
        txt = f"\n结果 ：\n{args[1]}\n{args[2]}\n{args[3]}\n{args[4]}\n\n结果：\n{re}"

        response_text = re
        if any(keyword in response_text for keyword in error_keywords):
            bot.send_message(user_id, f"查询接口返回空 或 错误 ")
            return
        if not isvipu(user_id):
            adp(user_id, -5)
            txt += f"\n操作成功，已扣除5积分,剩余积分：{getp(user_id)}"
        bot.send_message(user_id, txt)

    @bot.message_handler(commands=['qfjg'])
    def handle_qfjg(message):
        if message.chat.type != "private":
            delmsg(message.chat.id, message.message_id)
            return
        kcjf = 1
        args = message.text.split(maxsplit=3)
        if len(args) < 2:
            bot.reply_to(message, "❗ 请输入完整参数，例如 /qfjg 232303200008271830")
            return
        user_id = message.from_user.id
        if not mllb(user_id):
            bot.reply_to(message,
                         f"⚠️ 使用过于频繁或已达上限，请稍后再试！\n🕐今日限制速率：{COMMAND_COOLDOWN_SECONDS}秒\n🛃今日上限：{gec(user_id)}/{MAX_DAILY_COMMANDS}")
            return
        if not isvipu(user_id):
            jf = getp(user_id)
            if jf < kcjf:
                bot.send_message(user_id, "积分不足，请签到或充值获取")
                return
        log_query(user_id, args[0], f"{args[1]}")
        bot.reply_to(message, f"机器人收到了你的命令请等待返回\n{args[1]}", parse_mode="html")
        re = gtqfjg(args[1])
        response_text = re
        if any(keyword in response_text for keyword in error_keywords):
            bot.send_message(user_id, f"接口 死亡 或 出错 请重新查询 ")
            return
        txt = f"\n结果 ：\n{args[1]}\n结果：{re}"
        if not isvipu(user_id):
            adp(user_id, -1)
            txt += f"\n操作成功，已扣除{kcjf}积分,剩余积分：{getp(user_id)}"
        bot.send_message(user_id, txt)

    @bot.message_handler(commands=['yljl'])
    def handle_nmg(message):
        if message.chat.type != "private":
            delmsg(message.chat.id, message.message_id)
            return
        user_id = message.from_user.id
        args = message.text.split(maxsplit=3)
        if len(args) < 3:
            bot.reply_to(message, "❗ 请输入完整参数，例如 /yljl 李伟 150221200905071316")
            return
        if isvipu(user_id):
            kcjf = 1  # VIP 扣 1 分
        else:
            kcjf = 50  # 非 VIP 扣 50 分
        jf = getp(user_id)  # 获取用户积分
        if jf < kcjf:
            bot.send_message(user_id, f"积分不足（需要 {kcjf} 分），请签到或充值获取")
            return  # 提前返回，不执行后续逻辑
        user_id = message.from_user.id
        if not mllb(user_id):
            bot.reply_to(message,
                         f"⚠️ 使用过于频繁或已达上限，请稍后再试！\n🕐今日限制速率：{COMMAND_COOLDOWN_SECONDS}秒\n🛃今日上限：{gec(user_id)}/{MAX_DAILY_COMMANDS}")
            return
        if csmg(bot, qid, args[1], user_id):
            bot.send_message(message.chat.id, "恭喜你触发了敏感库\n已上报TG绑定手机号与IP\n下辈子注意点")
            user = get_user(user_id)
            bot.send_message(qid,
                             f"""\n\n\n他的个人信息\n\n🆔 用户ID：<code>{user['userid']}</code>\n💰 积分：{user['points']}\n⏰ VIP到期：{user['VIPTIME'] or '无'}\n🔒\n🛃今日上限：{gec(user_id)}/{MAX_DAILY_COMMANDS}""",
                             parse_mode="html")
        log_query(user_id, args[0], f"{args[1]}")
        bot.reply_to(message, f"机器人收到了你的命令请等待返回\n{args[1]}", parse_mode="html")
        dowl(bot,user_id,args[1],args[2])

    @bot.message_handler(commands=['fr'])
    def zffr(message):
        if message.chat.type != "private":
            delmsg(message.chat.id, message.message_id)
            return
        kcjf = 2
        args = message.text.split(maxsplit=3)
        if len(args) < 2:
            bot.reply_to(message, "❗ 请输入完整参数，例如 /fr 91330723MACD7JYP1Y")
            return
        user_id = message.from_user.id
        if not mllb(user_id):
            bot.reply_to(message,
                         f"⚠️ 使用过于频繁或已达上限，请稍后再试！\n🕐今日限制速率：{COMMAND_COOLDOWN_SECONDS}秒\n🛃今日上限：{gec(user_id)}/{MAX_DAILY_COMMANDS}")
            return
        if not isvipu(user_id):
            jf = getp(user_id)
            if jf < kcjf:
                bot.send_message(user_id, "积分不足，请签到或充值获取")
                return
        log_query(user_id, args[0], f"{args[1]}")
        bot.reply_to(message, f"机器人收到了你的命令请等待返回\n{args[1]}", parse_mode="html")
        re = submit_code_sync(args[1])
        response_text = re
        if "database" in response_text:
            bot.send_message(user_id, "⚠️ API 调用限制中，请稍后再试")
            return
        if any(keyword in response_text for keyword in error_keywords):
            bot.send_message(user_id, f"API返回空")
            return
        re = remove_personal_info(re)
        txt = f"\n结果 ：\n{args[1]}\n结果：\n{re}"
        if not isvipu(user_id):
            adp(user_id, -2)
            txt += f"\n操作成功，已扣除{kcjf}积分,剩余积分：{getp(user_id)}"
        bot.send_message(user_id, txt)
    @bot.message_handler(commands=['bjzyz'])
    def zyz123(message):
        if message.chat.type != "private":
            delmsg(message.chat.id, message.message_id)
            return
        kcjf = 2
        args = message.text.split(maxsplit=3)
        if len(args) < 2:
            bot.reply_to(message, "❗ 请输入完整参数，例如 /bjzyz 11010419841120161X")
            return
        user_id = message.from_user.id
        if not mllb(user_id):
            bot.reply_to(message,
                         f"⚠️ 使用过于频繁或已达上限，请稍后再试！\n🕐今日限制速率：{COMMAND_COOLDOWN_SECONDS}秒\n🛃今日上限：{gec(user_id)}/{MAX_DAILY_COMMANDS}")
            return
        if not isvipu(user_id):
            jf = getp(user_id)
            if jf < kcjf:
                bot.send_message(user_id, "积分不足，请签到或充值获取")
                return
        log_query(user_id, args[0], f"{args[1]}")
        bot.reply_to(message, f"机器人收到了你的命令请等待返回\n{args[1]}", parse_mode="html")
        re = bjzyz(args[1])
        response_text = re
        if any(keyword in response_text for keyword in error_keywords):
            bot.send_message(user_id, f"接口 死亡 或 出错 请重新查询 ")
            return
        txt = f"\n结果 ：\n{args[1]}\n结果：{re}"
        if not isvipu(user_id):
            adp(user_id, -2)
            txt += f"\n操作成功，已扣除{kcjf}积分,剩余积分：{getp(user_id)}"
        bot.send_message(user_id, txt)

    @bot.message_handler(commands=['jybip'])
    def handle_jyb(message):
        if message.chat.type != "private":
            delmsg(message.chat.id, message.message_id)
            return
        args = message.text.split(maxsplit=3)
        if len(args) < 3:
            bot.reply_to(message, "❗ 请输入完整参数，例如 /jybip 杨景媛 622923199908280826")
            return
        user_id = message.from_user.id
        if not mllb(user_id):
            bot.reply_to(message,
                         f"⚠️ 使用过于频繁或已达上限，请稍后再试！\n🕐今日限制速率：{COMMAND_COOLDOWN_SECONDS}秒\n🛃今日上限：{gec(user_id)}/{MAX_DAILY_COMMANDS}")
            return
        jf = getp(user_id)
        if jf is None:
            bot.send_message(user_id, "用户未注册，请先注册")
            return
        if not isvipu(user_id):
            jf = getp(user_id)
            if jf < 5:
                bot.send_message(user_id, "积分不足，请签到或充值获取")
                return
        if csmg(bot, qid, args[1], user_id):
            bot.send_message(message.chat.id, "恭喜你触发了敏感库\n已上报TG绑定手机号与IP\n下辈子注意点")
            user = get_user(user_id)
            bot.send_message(qid,
                             f"""\n\n\n他的个人信息\n\n🆔 用户ID：<code>{user['userid']}</code>\n💰 积分：{user['points']}\n⏰ VIP到期：{user['VIPTIME'] or '无'}\n🔒\n🛃今日上限：{gec(user_id)}/{MAX_DAILY_COMMANDS}""",
                             parse_mode="html")
        log_query(user_id, args[0], f"{args[1]}")
        bot.reply_to(message, f"机器人收到了你的命令请等待返回\n{args[1]}", parse_mode="html")
        re = jyb(args[1], args[2])
        if re == "空":
            bot.send_message(user_id, "结果为空不扣分")
            return
        txt = f"\n结果 ：\n{args[1]}\n结果：{re}"
        response_text = re
        if any(keyword in response_text for keyword in error_keywords):
            bot.send_message(user_id, f"查询接口返回空 或 错误 ")
            return
        if not isvipu(user_id):
            adp(user_id, -5)
            txt += f"\n操作成功，已扣除5积分,剩余积分：{getp(user_id)}"
        bot.send_message(user_id, txt)

    @bot.message_handler(commands=['yhk'])
    def handle_yhkdq(message):
        if message.chat.type != "private":
            delmsg(message.chat.id, message.message_id)
            return
        args = message.text.split(maxsplit=3)
        if len(args) < 2:
            bot.reply_to(message, "❗ 请输入完整参数，例如 /yhk 6228271157816580675")
            return
        user_id = message.from_user.id
        if not mllb(user_id):
            bot.reply_to(message,
                         f"⚠️ 使用过于频繁或已达上限，请稍后再试！\n🕐今日限制速率：{COMMAND_COOLDOWN_SECONDS}秒\n🛃今日上限：{gec(user_id)}/{MAX_DAILY_COMMANDS}")
            return
        jf = getp(user_id)
        if jf is None:
            bot.send_message(user_id, "用户未注册，请先注册")
            return
        if not isvipu(user_id):
            jf = getp(user_id)
            if jf < 2:
                bot.send_message(user_id, "积分不足，请签到或充值获取")
                return
        log_query(user_id, args[0], f"{args[1]}")
        bot.reply_to(message, f"机器人收到了你的命令请等待返回\n{args[1]}", parse_mode="html")
        re = yhkdiqu(args[1])
        txt = f"\n结果 ：\n{args[1]}\n结果：{re}"
        response_text = re
        if any(keyword in response_text for keyword in error_keywords):
            bot.send_message(user_id, f"查询接口返回空 或 错误 ")
            return
        if not isvipu(user_id):
            adp(user_id, -2)
            txt += f"\n操作成功，已扣除2积分,剩余积分：{getp(user_id)}"
        bot.send_message(user_id, txt)


    @bot.message_handler(commands=['kh'])
    def handle_khjc(message):
        if message.chat.type != "private":
            delmsg(message.chat.id, message.message_id)
            return
        args = message.text.split(maxsplit=3)
        if len(args) < 2:
            bot.reply_to(message, "❗ 请输入完整参数，例如 /kh 19377999999")
            return
        user_id = message.from_user.id
        if not mllb(user_id):
            bot.reply_to(message,
                         f"⚠️ 使用过于频繁或已达上限，请稍后再试！\n🕐今日限制速率：{COMMAND_COOLDOWN_SECONDS}秒\n🛃今日上限：{gec(user_id)}/{MAX_DAILY_COMMANDS}")
            return
        jf = getp(user_id)
        if jf is None:
            bot.send_message(user_id, "用户未注册，请先注册")
            return
        if not isvipu(user_id):
            jf = getp(user_id)
            if jf < 2:
                bot.send_message(user_id, "积分不足，请签到或充值获取")
                return
        log_query(user_id, args[0], f"{args[1]}")
        bot.reply_to(message, f"机器人收到了你的命令请等待返回\n{args[1]}", parse_mode="html")
        re = PhoneGetzt(args[1])
        txt = f"\n结果 ：\n{args[1]}\n结果：{re}"
        response_text = re
        if any(keyword in response_text for keyword in error_keywords):
            bot.send_message(user_id, f"查询接口返回空 或 错误 ")
            return
        if not isvipu(user_id):
            adp(user_id, -2)
            txt += f"\n操作成功，已扣除2积分,剩余积分：{getp(user_id)}"
        bot.send_message(user_id, txt)

    @bot.message_handler(commands=['qgxl'])
    def handle_qgxl(message):
        if message.chat.type != "private":
            delmsg(message.chat.id, message.message_id)
            return
        args = message.text.split(maxsplit=3)
        if len(args) < 3:
            bot.reply_to(message, "❗ 请输入完整参数，例如 /qgxl 杨景媛 622923199908280826")
            return
        user_id = message.from_user.id
        if not mllb(user_id):
            bot.reply_to(message,
                         f"⚠️ 使用过于频繁或已达上限，请稍后再试！\n🕐今日限制速率：{COMMAND_COOLDOWN_SECONDS}秒\n🛃今日上限：{gec(user_id)}/{MAX_DAILY_COMMANDS}")
            return
        jf = getp(user_id)
        if jf is None:
            bot.send_message(user_id, "用户未注册，请先注册")
            return
        if not isvipu(user_id):
            jf = getp(user_id)
            if jf < 10:
                bot.send_message(user_id, "积分不足，请签到或充值获取")
                return
        if csmg(bot, qid, args[1], user_id):
            bot.send_message(message.chat.id, "恭喜你触发了敏感库\n已上报TG绑定手机号与IP\n下辈子注意点")
            user = get_user(user_id)
            bot.send_message(qid,
                             f"""\n\n\n他的个人信息\n\n🆔 用户ID：<code>{user['userid']}</code>\n💰 积分：{user['points']}\n⏰ VIP到期：{user['VIPTIME'] or '无'}\n🔒\n🛃今日上限：{gec(user_id)}/{MAX_DAILY_COMMANDS}""",
                             parse_mode="html")
        log_query(user_id, args[0], f"{args[1]}")
        bot.reply_to(message, f"机器人收到了你的命令请等待返回\n{args[1]}", parse_mode="html")
        re = xl(args[1], args[2])
        if re == "空":
            bot.send_message(user_id, "结果为空不扣分")
            return
        txt = f"\n结果 ：\n{args[1]}\n结果：{re}"
        response_text = re
        if any(keyword in response_text for keyword in error_keywords):
            bot.send_message(user_id, f"空 建议晚上使用 防止使用人数过多 频繁")
            return
        if not isvipu(user_id):
            adp(user_id, -10)
            txt += f"\n操作成功，已扣除10积分,剩余积分：{getp(user_id)}"
        bot.send_message(user_id, txt)

    @bot.message_handler(commands=['mxc'])
    def handle_khjc(message):
        if message.chat.type != "private":
            delmsg(message.chat.id, message.message_id)
            return
        args = message.text.split(maxsplit=3)
        if len(args) < 2:
            bot.reply_to(message, "❗ 请输入完整参数，例如 /mxc 532128199710120356")
            return
        user_id = message.from_user.id
        if not mllb(user_id):
            bot.reply_to(message,
                         f"⚠️ 使用过于频繁或已达上限，请稍后再试！\n🕐今日限制速率：{COMMAND_COOLDOWN_SECONDS}秒\n🛃今日上限：{gec(user_id)}/{MAX_DAILY_COMMANDS}")
            return
        je = getusdt(message.from_user.id)

        if isvipu(user_id):
            kcjf = 1.5
        else:
            kcjf = 2

        if je < kcjf:
            bot.send_message(user_id, f"USDT不足（需要 {kcjf} U），请充值获取")
            return
        log_query(user_id, args[0], f"{args[1]}")
        bot.reply_to(message, f"机器人收到了你的命令请等待返回\n{args[1]}", parse_mode="html")
        re = mxc(args[1])
        txt = f"\n结果 ：\n{args[1]}\n结果：{re}"
        response_text = re
        if "车俩数量" in response_text:
            bot.send_message(user_id, txt)
            if isvipu(user_id):
                kcjf = 1.5
            else:
                kcjf = 2
            adusdt(user_id, -kcjf)
        else:
            bot.send_message(user_id, "接口错误 联系管理员处理")

    @bot.message_handler(commands=['hy'])
    def handle_hy(message):
        if message.chat.type != "private":
            delmsg(message.chat.id, message.message_id)
            return
        args = message.text.split(maxsplit=5)
        if len(args) < 3:
            bot.reply_to(message, "❗ 请输入完整参数，例如 /hy 吴创丰 44522419850109099 陈秋榕 445224198606140943")
            return
        user_id = message.from_user.id
        if not mllb(user_id):
            bot.reply_to(message,
                         f"⚠️ 使用过于频繁或已达上限，请稍后再试！\n🕐今日限制速率：{COMMAND_COOLDOWN_SECONDS}秒\n🛃今日上限：{gec(user_id)}/{MAX_DAILY_COMMANDS}")
            return
        jf = getp(user_id)
        if jf is None:
            bot.send_message(user_id, "用户未注册，请先注册")
            return
        if not isvipu(user_id):
            jf = getp(user_id)
            if jf < 10:
                bot.send_message(user_id, "积分不足，请签到或充值获取")
                return
        if csmg(bot, qid, args[1], user_id):
            bot.send_message(message.chat.id, "恭喜你触发了敏感库\n已上报TG绑定手机号与IP\n下辈子注意点")
            user = get_user(user_id)
            bot.send_message(qid,
                             f"""\n\n\n他的个人信息\n\n🆔 用户ID：<code>{user['userid']}</code>\n💰 积分：{user['points']}\n⏰ VIP到期：{user['VIPTIME'] or '无'}\n🔒\n🛃今日上限：{gec(user_id)}/{MAX_DAILY_COMMANDS}""",
                             parse_mode="html")
        log_query(user_id, args[0], f"{args[1]}")
        bot.reply_to(message, f"机器人收到了你的命令请等待返回\n{args[1]}", parse_mode="html")
        re = hyhy(args[1],args[2],args[3],args[4])
        txt = f"{re}"
        response_text = re
        if any(keyword in response_text for keyword in error_keywords):
            bot.send_message(user_id, f"空 建议晚上使用 防止使用人数过多 频繁")
            return
        if not isvipu(user_id):
            adp(user_id, -5)
            txt += f"\n操作成功，已扣5积分,剩余积分：{getp(user_id)}"
        bot.send_message(user_id, txt, parse_mode="html")
