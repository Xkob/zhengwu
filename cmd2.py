from dbsql import isvipu
import base64
import requests
import os
import uuid
from cfg import TOKEN,log_query
from telebot import types

API_URL = "http://103.239.244.99:51276/rlhy"
QUALITY_THRESHOLD = 70  # 相似度阈值


def cmd2(bot):
    @bot.message_handler(content_types=['photo'])
    def handle_photo(message):
        if message.chat.type != "private":
            return

        user_id = message.from_user.id
        if not isvipu(user_id):
            markup = types.InlineKeyboardMarkup()
            markup.add(
                types.InlineKeyboardButton("💰立即开通会员", callback_data="cz"),
                types.InlineKeyboardButton("❌关闭", callback_data="del")
            )
            bot.send_message(
                message.chat.id,
                "🚫 <b>权限不足</b>\n\n"
                "抱歉！你不是尊贵会员，无法使用这个牛逼功能 😎\n\n"
                "💎 <b>开通会员后即可享受全部高级功能</b>\n"
                "✨ 会员特权包括：\n"
                "🔹 快速身份验证\n"
                "🔹 使用不扣除积分\n"
                "🔹 优先体验新功能\n\n",
                parse_mode="HTML", reply_markup=markup
            )
            return

        caption = message.caption or ""
        parts = caption.strip().split()
        if len(parts) != 2:
            bot.reply_to(message, "请在标题中输入：名字 身份证 例如：李伟 460200198909255332")
            return
        bot.reply_to(message, f"已经收到了{message.caption}")
        name, idcard = parts
        file_id = message.photo[-1].file_id
        file_info = bot.get_file(file_id)
        file_url = f"https://api.telegram.org/file/bot{TOKEN}/{file_info.file_path}"

        temp_file_path = f"{uuid.uuid4().hex}.jpg"

        try:
            # 下载原图
            resp = requests.get(file_url)
            resp.raise_for_status()
            with open(temp_file_path, "wb") as f:
                f.write(resp.content)

            # 转 Base64
            with open(temp_file_path, "rb") as f:
                image_base64 = base64.b64encode(f.read()).decode("utf-8")
            payload = {
                "name": name,
                "sfz": idcard,
                "photo": image_base64
            }
            r = requests.post(API_URL, json=payload)
            r.raise_for_status()
            data = r.json()

            quality = data.get("second_request", {}).get("data", {}).get("realPersonAuthQuality")
            if quality is not None:
                if quality >= QUALITY_THRESHOLD:
                    result = f"通过 ✅ 相似度: {quality}"
                else:
                    result = f"不通过 ❌ 相似度: {quality}"
            else:
                result = "API调用失败"

            bot.reply_to(message, result)
            log_query(user_id, "人脸",message.caption)

        except Exception as e:
            bot.reply_to(message, "处理失败")
            print("错误：", e)

        finally:
            if os.path.exists(temp_file_path):
                try:
                    os.remove(temp_file_path)
                except Exception as e:
                    print(f"删除临时文件失败: {e}")
