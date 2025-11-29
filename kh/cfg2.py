import os
import threading
import json
import time
import random
import brotli
import requests
from queue import Queue
from collections import defaultdict

user_jobs = defaultdict(lambda: {
    "queue": Queue(),
    "results": [],
    "processed": set(),
    "lock": threading.Lock()
})
def generate_valid_id():
    """生成有效的18位身份证号"""
    # 区域代码（前6位，这里使用一些常见的区域代码）
    areas = [
        "110101", "110102", "110105", "110106",  # 北京市
        "310101", "310104", "310105", "310106",  # 上海市
        "440101", "440103", "440104", "440106",  # 广州市
        "440301", "440303", "440304", "440305",  # 深圳市
        "120101", "120102", "120103", "120104",  # 天津市
    ]

    # 随机选择一个区域代码
    address = random.choice(areas)

    # 生成出生日期（1950-2005年之间）
    year = random.randint(1950, 2005)
    month = random.randint(1, 12)

    # 根据月份确定最大天数
    if month in [1, 3, 5, 7, 8, 10, 12]:
        day = random.randint(1, 31)
    elif month in [4, 6, 9, 11]:
        day = random.randint(1, 30)
    else:  # 2月
        if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
            day = random.randint(1, 29)  # 闰年
        else:
            day = random.randint(1, 28)  # 平年

    # 格式化日期部分
    birth_date = f"{year:04d}{month:02d}{day:02d}"

    # 生成顺序码（3位）
    sequence = random.randint(1, 999)

    # 生成性别码（奇数男，偶数女）
    gender_digit = random.choice([1, 3, 5, 7, 9])  # 随机选择奇数（男）

    # 组合前17位
    id_17 = f"{address}{birth_date}{sequence:03d}"[:-1] + str(gender_digit)

    # 计算校验码
    weights = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    check_codes = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']

    total = 0
    for i in range(17):
        total += int(id_17[i]) * weights[i]

    check_code = check_codes[total % 11]

    # 返回完整的身份证号
    return id_17 + check_code


# 姓名生成函数
def generate_random_name():
    """生成随机三字姓名"""
    # 常见姓氏
    surnames = ["李", "王", "张", "刘", "陈", "杨", "赵", "黄", "周", "吴",
                "徐", "孙", "胡", "朱", "高", "林", "何", "郭", "马", "罗"]

    # 常见名字用字
    name_chars = ["伟", "芳", "娜", "秀英", "敏", "静", "磊", "洋", "艳", "勇",
                  "军", "杰", "娟", "强", "霞", "鹏", "宇", "超", "婷", "明",
                  "平", "雪", "鑫", "亮", "建", "波", "林", "华", "刚", "红"]

    # 随机选择姓氏和两个字组成名字
    surname = random.choice(surnames)
    name = "".join(random.sample(name_chars, 2))

    return surname + name






def refresh_token():
    refresh_url = "https://backend.shwoody.com/wd-base-user/o/api/refreshToken"
    refresh_params = {
        "refreshToken": "69d12fe3-bcf1-4776-83dd-7ef97c5370f3",
        "openId": "obHbp4vyWDqPI0UiJGB22lkOqDqA",
        "openid": "obHbp4vyWDqPI0UiJGB22lkOqDqA"
    }
    refresh_headers = {
        "Host": "backend.shwoody.com",
        "content-type": "application/json",
        "Authorization": "xxx"  # 旧的 token
    }

    r = requests.get(refresh_url, params=refresh_params, headers=refresh_headers)
    if r.headers.get("Content-Encoding") == "br":
        try:
            text = brotli.decompress(r.content).decode()
        except:
            text = r.text
    else:
        text = r.text

    try:
        data = json.loads(text)
        if data.get("code") == 0:
            return data["data"]["accessToken"]
    except:
        pass
    return None

def mobile_auth(access_token, name, id_card, mobile):
    """发送认证请求并解析结果"""
    auth_url = "https://backend.shwoody.com/ms-common/api/auth/mobileAuth"
    auth_headers = {
        "content-type": "application/json",
        "Authorization": access_token,
        "User-Agent": "Mozilla/5.0",
    }
    auth_data = {
        "name": name,
        "mobile": mobile,
        "idCard": id_card,
        "openId": "obHbp4vyWDqPI0UiJGB22lkOqDqA",
        "openid": "obHbp4vyWDqPI0UiJGB22lkOqDqA"
    }

    try:
        r = requests.post(auth_url, headers=auth_headers, json=auth_data, timeout=10)
        text = r.text
        # 解压 br
        if r.headers.get("Content-Encoding") == "br":
            try:
                text = brotli.decompress(r.content).decode("utf-8")
            except:
                pass

        try:
            data = r.json() if text == r.text else json.loads(text)
        except Exception:
            return "解析失败"

        pd = data.get("message", data)

        if "不符合规则" in pd:
            return "空号(不符合手机号规则)"
        elif "查询无结果" in pd:
            return "空号"
        elif "验证不一致" in pd:
            return "号码存活"
        else:
            return "返回不在预期"

    except Exception as e:
        return f"请求出错: {e}"


def worker(chat_id, access_token, thread_id):
    job = user_jobs[chat_id]
    while not job["queue"].empty():
        try:
            mobile = job["queue"].get_nowait()
            with job["lock"]:
                if mobile in job["processed"]:
                    job["queue"].task_done()
                    continue
                job["processed"].add(mobile)
            name = generate_random_name()
            id_card = generate_valid_id()
            auth_result = mobile_auth(access_token, name, id_card, mobile)
            with job["lock"]:
                if len(job["results"])<10:
                    job["results"].append(f"{mobile} → {auth_result}")
            job["queue"].task_done()
            time.sleep(0.5)
        except Exception as e:
            print(f"线程错误: {e}")
            time.sleep(1)