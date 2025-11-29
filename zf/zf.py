from flask import Flask, request, jsonify
from telethon import TelegramClient
import asyncio
import re
import os
import nest_asyncio
nest_asyncio.apply()
# ===== Telegram 配置 =====
api_id = '2040'
api_hash = 'b18441a1ff607e10a989891a5462e627'
bot_username = "ynsgkBot"
app = Flask(__name__)
def extract_record(text: str) -> str:
    match = re.search(r"真全国企业法人.*?▎记录\s*1\s*(.*?)查询完成。", text, re.S)
    if match:
        return match.group(1).strip()
    return ""
# 删除最近的 N 条消息
async def clear_bot_messages(client, bot_username, limit=20):
    msgs = await client.get_messages(bot_username, limit=limit)
    for m in msgs:
        try:
            await m.delete()
        except Exception as e:
            # 无法删除就跳过
            print(f"删除消息失败: {e}")

# ===== Telethon 异步查询 =====
async def _fetch_record(法人代码: str) -> str:
    async with TelegramClient("my_account", api_id, api_hash) as client:
        # 1. 发送法人代码
        await clear_bot_messages(client, bot_username, limit=20)
        await client.send_message(bot_username, 法人代码)

        # 2. 等待带按钮或提示消息
        msg = None
        while True:
            response = await client.get_messages(bot_username, limit=5)
            for m in response:
                # 如果出现提示消息，直接返回空
                if "没有找到相关信息，请尝试重新查询或等待数据更新" in (m.text or ""):
                    return "空"
                # 如果有按钮，说明可以导出
                if m.buttons:
                    msg = m
                    break
            if msg:
                break
            await asyncio.sleep(2)

        # 3. 点击导出TXT按钮
        try:
            await msg.click(text="✨导出TXT✨")
        except Exception as e:
            return f"点击按钮失败: {e}"

        # 4. 等待 TXT 文件消息
        file_msg = None
        while True:
            msgs = await client.get_messages(bot_username, limit=5)
            for m in msgs:
                if m.file and m.file.name.endswith(".txt"):
                    file_msg = m
                    break
            if file_msg:
                break
            await asyncio.sleep(2)

        # 5. 下载文件
        filename = await file_msg.download_media(file="result.txt")

        # 6. 解析文件
        with open(filename, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        os.remove(filename)

        if "真全国企业法人" not in content:
            return "空"
        return extract_record(content)

# ===== 同步接口调用 =====
def fetch_record_sync(法人代码: str) -> str:
    try:
        return asyncio.run(_fetch_record(法人代码))
    except Exception as e:
        return f"Error: {e}"

# ===== Flask 接口 =====
@app.route("/fetch", methods=["GET"])
def fetch():
    code = request.args.get("code", "")
    if not code:
        return jsonify({"error": "请提供法人代码"}), 400

    result = fetch_record_sync(code)
    return jsonify({"code": code, "result": result})


# ===== 运行 =====
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
