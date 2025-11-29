import requests
import json
import brotli
import random
# 身份证生成函数
def generate_valid_id():
    areas = ["110101", "310101", "440101", "440301", "120101"]  # 简化
    address = random.choice(areas)
    year = random.randint(1950, 2005)
    month = random.randint(1, 12)
    if month in [1, 3, 5, 7, 8, 10, 12]:
        day = random.randint(1, 31)
    elif month in [4, 6, 9, 11]:
        day = random.randint(1, 30)
    else:
        if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
            day = random.randint(1, 29)
        else:
            day = random.randint(1, 28)
    birth_date = f"{year:04d}{month:02d}{day:02d}"
    sequence = random.randint(1, 999)
    gender_digit = random.choice([1, 3, 5, 7, 9])
    id_17 = f"{address}{birth_date}{sequence:03d}"[:-1] + str(gender_digit)
    weights = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    check_codes = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']
    total = sum(int(id_17[i]) * weights[i] for i in range(17))
    return id_17 + check_codes[total % 11]

# 随机姓名
def generate_random_name():
    surnames = ["李", "王", "张", "刘", "陈"]
    name_chars = ["伟", "芳", "娜", "磊", "洋", "勇", "军", "杰", "霞", "鹏"]
    return random.choice(surnames) + "".join(random.sample(name_chars, 2))

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
    url = "https://backend.shwoody.com/ms-common/api/auth/mobileAuth"
    headers = {
        "Authorization": access_token,
        "content-type": "application/json"
    }
    payload = {
        "name": name,
        "mobile": mobile,
        "idCard": id_card,
        "openId": "obHbp4vyWDqPI0UiJGB22lkOqDqA",
        "openid": "obHbp4vyWDqPI0UiJGB22lkOqDqA"
    }
    r = requests.post(url, headers=headers, json=payload)
    if r.headers.get("Content-Encoding") == "br":
        try:
            text = brotli.decompress(r.content).decode()
        except:
            text = r.text
    else:
        text = r.text

    try:
        data = r.json() if text == r.text else __import__("json").loads(text)
        pd =data.get("message", data)
        if "不符合规则" in pd:
            return "空号(不符合手机号规则)"
        elif "查询无结果" in pd:
            return "空号"
        elif "验证不一致" in pd:
            return "号码存活"
        else:
            return "返回不在预期"
    except Exception as e:
        print(e)

def PhoneGetzt(first_phone):
    if not first_phone:
        return "无手机号"
    print("手机号:", first_phone)
    token = refresh_token()
    if not token:
        return "Token过期或不存在"
    name = generate_random_name()
    id_card = generate_valid_id()
    result = mobile_auth(token, name, id_card, first_phone)
    return result
