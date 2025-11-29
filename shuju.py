import requests
import urllib.parse
import json
import urllib3
from urllib3.exceptions import InsecureRequestWarning
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import os
import httpx
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import urllib.parse
from datetime import datetime
from sjk.shujuk import data
import re
import os
from datetime import date
import datetime
import json
from io import BytesIO
from PIL import Image
qjkey = 'xhgkey.1'



def gtqfjg(id_numb):
    area_code = id_numb[:6]
    if area_code in data:
        return data[area_code]
    else:
        return "身份证号错误"

# ---- 预加载地区数据库 ----
def load_id_database(json_path="sjk/id.json"):
    if not os.path.exists(json_path):
        raise FileNotFoundError("缺少 id.json 文件，请确保地区数据库存在。")
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


# 初始化加载数据库（只加载一次）
ID_DATA = load_id_database()


# ---- 工具函数们 ----

def get_location_by_id(id_code: int) -> str:
    for item in ID_DATA:
        if item["id"] == id_code:
            parts = [item["provinceName"], item["cityName"], item["countName"]]
            return "".join(filter(None, parts))
    return "未知地区"


def get_sex(id_card: str) -> str:
    return "男" if int(id_card[16]) % 2 == 1 else "女"


def get_birth(id_card: str) -> str:
    return f"{id_card[6:10]}-{id_card[10:12]}-{id_card[12:14]}"


def get_age(id_card: str) -> int:
    from datetime import datetime

    try:
        if len(id_card) >= 18:
            id_card = id_card[:18]  # 截断前18位
        birth_str = id_card[6:14]
        if not birth_str.isdigit():
            return -1
        birth_date = datetime.strptime(birth_str, "%Y%m%d")
        today = datetime.today()

        age = today.year - birth_date.year
        if (today.month, today.day) < (birth_date.month, birth_date.day):
            age -= 1
        return age
    except Exception:
        return -1



def is_valid_id(id_card: str) -> bool:
    if len(id_card) != 18 or not id_card[:17].isdigit():
        return False
    weights = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    check_map = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']
    total = sum(int(id_card[i]) * weights[i] for i in range(17))
    return id_card[17].upper() == check_map[total % 11]
def yss(id_card: str) -> str:
    id_card = id_card.strip().upper()
    if len(id_card) != 18 or not id_card[:17].isdigit():
        return f"身份证号：{id_card}\n格式非法\n"

    lines = [
        f"身份证号：{id_card}",
        f"地区：{get_location_by_id(int(id_card[:6]))}",
        f"出生：{get_birth(id_card)}",
        f"年龄：{get_age(id_card)}",
        f"性别：{get_sex(id_card)}",
        f"是否合法：{'合法' if is_valid_id(id_card) else '非法'}"
    ]
    return "\n".join(lines)
def ahqy(phone):
    url = "http://103.239.244.99:11452/ahjz"
    params = {
        "phone": phone,
        "key": qjkey
    }
    try:
        resp = requests.get(url, params=params)
        return resp.text if resp.status_code == 200 else "请求失败"
    except Exception as e:
        return f"null"
def hljym(phone):
    url = "http://103.239.244.99:11452/hljym"
    params = {
        "phone": phone,
        "key": qjkey
    }
    try:
        resp = requests.get(url, params=params)
        return resp.text if resp.status_code == 200 else "请求失败"
    except Exception as e:
        return f"null"
def eys(name,ids):
    url = "http://103.239.244.99:56912/eys"
    params = {
        "name": name,
        "id_num": ids
    }

    # 发送 GET 请求
    response = requests.get(url, params=params)
    # 检查响应
    if response.status_code == 200:
        try:
            data = response.json()  # 转换为字典
            return data.get("result")
        except ValueError:
            return "返回错误"
    else:
       return "返回错误"



def cyh(phone):
    url = "http://103.239.244.99:11452/phone/sfz"
    params = {
        "key": qjkey,
        "id": phone,
    }
    try:
        resp = requests.get(url, params=params, timeout=10)
        if resp.status_code != 200:
            return "请求失败"

        data = resp.json()

        # 判断接口结构和状态
        if data.get("success") and "data" in data:
            phone_value = data["data"]["result"].get("phone", "无")
            name_value = data["data"]["result"].get("name", "无")
            if phone_value != "无":
                return f"模糊名字：{name_value}\n模糊手机号：{phone_value}"
            else:
                return "无"
        else:
            return "接口返回错误"
    except Exception as e:
        return "null"

def jxfr(public_key, data):
    key = RSA.import_key(public_key)
    cipher = PKCS1_v1_5.new(key)
    max_length = key.size_in_bytes() - 11
    encrypted_data = b""
    for i in range(0, len(data), max_length):
        chunk = data[i:i + max_length].encode('utf-8')
        encrypted_chunk = cipher.encrypt(chunk)
        encrypted_data += encrypted_chunk
    return base64.b64encode(encrypted_data).decode('utf-8')
def fr4(corp_name, credit_code, legal_name, legal_id):

    url = "https://user.mct.gov.cn/idm/publickey"

    # 请求头
    headers = {
        "Host": "user.mct.gov.cn",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.4 Mobile/15E148 Safari/604.1",
        "Accept": "*/*",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "https://user.mct.gov.cn/idm/corp/reg;jsessionid=5FA3160151D3BA995FD0CD8EABE20F01?servicecode=zwfw&gourl=http%3A//zwfw.mct.gov.cn%3A80/%3Ftype%3Dcorp",
        "Origin": "https://user.mct.gov.cn",
        "Accept-Language": "zh-CN,zh-Hans;q=0.9",
        "Priority": "u=5, i",
        "Accept-Encoding": "gzip, deflate, br",
        "Cookie": "JSESSIONID=5FA3160151D3BA995FD0CD8EABE20F01; session_extargs=; sso_gourl=431172A472E90D1701FD776F70FD0BCC71CE56622F8FDFE1D9D13DF20E47D335D685D380AB876F27A237CC12D6486FEF; _trs_uv=mbuv4dj5_4419_h139; zwfwToken=MmY1YzM4NzUtOTg2ZC00NDM2LTlmYTUtOTY2MjRiNTIzNjc0",
        "Connection": "keep-alive"
    }

    # 发送 POST 请求
    response = requests.post(url, headers=headers, data="")

    # 解析响应 JSON
    if response.status_code == 200:
        try:
            data = response.json()
            attr_value = data.get("attr")


            public_key = (
                    "-----BEGIN PUBLIC KEY-----\n"
                    + attr_value.strip()
                    + "\n-----END PUBLIC KEY-----"
            )

        except json.JSONDecodeError:
            return "失败"
    else:
        return "失败"

    # 根据信用代码开头设置corptype
    if credit_code.startswith("91"):
        corptype = "1"  # 企业法人
    elif credit_code.startswith("92"):
        corptype = "4"  # 个体工商户
    elif credit_code.startswith("93"):
        corptype = "2"  # 社团法人(示例,可根据实际需求调整)
    elif credit_code.startswith("94"):
        corptype = "3"  # 机关事业单位法人(示例,可根据实际需求调整)
    else:
        return "失败"

    # 构造参数(仅加密用户输入)
    raw_params = {
        "corptype": corptype,
        "corpname": jxfr(public_key, corp_name),
        "certificatesno": jxfr(public_key, credit_code),
        "legalname": jxfr(public_key, legal_name),
        "legalcertno": jxfr(public_key, legal_id),
        "legalcerttype": "1",
        "legalsex": "",
        "legalnation": ""
    }
    request_body = urllib.parse.urlencode(raw_params)

    # 请求头(保持不变)
    headers = {
        "Host": "user.mct.gov.cn",
        "Accept": "*/*",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://user.mct.gov.cn",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.4 Mobile/15E148 Safari/604.1",
        "Referer": "https://user.mct.gov.cn/idm/corp/reg;jsessionid=5FA3160151D3BA995FD0CD8EABE20F01?servicecode=zwfw&gourl=http%3A//zwfw.mct.gov.cn%3A80/%3Ftype%3Dcorp",
        "Content-Length": "847",
        "X-Requested-With": "XMLHttpRequest",
        "Accept-Language": "zh-CN,zh-Hans;q=0.9",
        "Priority": "u=5, i",
        "Accept-Encoding": "gzip, deflate, br",
        "Cookie": "JSESSIONID=5FA3160151D3BA995FD0CD8EABE20F01; session_extargs=; sso_gourl=431172A472E90D1701FD776F70FD0BCC71CE56622F8FDFE1D9D13DF20E47D335D685D380AB876F27A237CC12D6486FEF; _trs_uv=mbuv4dj5_4419_h139; zwfwToken=MmY1YzM4NzUtOTg2ZC00NDM2LTlmYTUtOTY2MjRiNTIzNjc0",
        "Connection": "keep-alive"
    }

    url = "https://user.mct.gov.cn/idm/corp/regFillcorp"
    try:
        response = requests.post(url, data=request_body, headers=headers, timeout=10)
    except requests.exceptions.RequestException as e:
        print(f"请求异常: {e}")
        return "失败"

    # 打印完整响应(保持不变)

    for key, value in response.headers.items():
        print(f"{key}: {value}")

    try:
        response_json = response.json()
        msg = response_json.get("msg", "")
        if msg == "成功":
            return "核验成功✅"
        elif msg == "法人信息认证失败":
            return "法人四要素比对不一致❌"
        elif msg == "统一社会信用代码验证失败":
            return "统一社会信用代码不正确"
        elif msg =="失败":
            return "法人四要素比对不一致"
        else:
            return "失败"
    except ValueError:
        print("响应非JSON格式,原始正文如下:")
        return "失败"
def kys(MZ, SFZ, YHK):
    url = "http://qinghe.uc0.cn/yubei/yhk3ys.php"
    params = {
        "xm": MZ,
        "sfz": SFZ,
        "yhk": YHK
    }
    # 发送GET请求
    response = requests.get(url, params=params)

    if response.status_code == 200:
        try:
            data = response.json()
            # 👇 关键判断部分
            if isinstance(data, dict):
                desc = data.get("desc", "错误")
            elif isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
                desc = data[0].get("desc", "错误")
            else:

                desc = "错误"
            return desc
        except ValueError:
            return "错误"
    else:
        return "错误"



def jnqy(id_card):
    url = "http://103.239.244.99:11452/jinan/vaccine"
    params = {
        "key": qjkey,
        "id": id_card
    }

    try:
        response = requests.get(url, params=params)
        if response.status_code != 200:
            return {"success": False, "error": f"请求失败，状态码：{response.status_code}"}

        data = response.json()
        if not data.get("success"):
            return {"success": False, "error": data.get("message", "接口返回失败")}

        user = data['data'][0]
        raw = user.get("raw_data", {})

        result = (
            f"姓名：{user.get('name')}\n"
            f"身份证号：{user.get('id_card')}\n"
            f"手机号：{user.get('phone')}\n"
            f"性别：{user.get('gender')}\n"
            f"户籍地址：{user.get('huji_address')}\n"
            f"居住地址：{user.get('home_address')}\n"
            f"出生日期：{raw.get('chilBirthday')}\n"
            f"登记日期：{raw.get('jdrq')}\n"
            f"上报时间：{raw.get('sjscsj')}"
        )
        return result

    except Exception as e:
        return "错误"





def tjfc(name: str, id_card: str):
    base_url = "http://103.239.244.99:45456/tianjin/"
    params = {
        "xm": name,
        "sfz": id_card
    }

    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.encoding = 'utf-8'

        data = response.json()

        records = data.get("data", {}).get("data", {}).get("bdcdyxx", [])

        if not records:
            return "空"

        msg = f"🏠 共查询到 {len(records)} 条房产记录：\n"

        for i, info in enumerate(records, 1):
            qlrmc = info.get("qlrmc", "未知")
            zl = info.get("zl", "未知地址")
            fwmj = info.get("fwmj", "未知")
            fwyt = info.get("fwyt", "未知")
            fwxz = info.get("fwxz", "未知")

            msg += (
                f"\n【第{i}套】\n"
                f"🏷️ 权利人：{qlrmc}\n"
                f"📍 地址：{zl}\n"
                f"📐 面积：{fwmj}㎡\n"
                f"🏠 用途：{fwyt} | 性质：{fwxz}\n"
            )

        return msg

    except requests.RequestException as e:
        return f"请求失败"
    except Exception as e:
        return f"解析失败"


def hbfc(id_card: str):
    url = "http://103.239.244.99:45456/estate/"
    params = {"sfz": id_card}
    try:
        response = requests.get(url, params=params, timeout=10)
        response.encoding = 'utf-8'
        data = response.json()

        results = data.get("data", {}).get("result", [])

        if not results:
            return "空"

        msg = f"🏠 共查询到 {len(results)} 条房产信息：\n"

        for i, item in enumerate(results, 1):
            zl = item.get("zl", "未知地址")
            mj = item.get("fwjzmj", "未知面积")
            msg += f"\n【第{i}套】\n📍 地址：{zl}\n📐 面积：{mj}㎡\n"

        return msg

    except requests.RequestException as e:
        return f"请求失败"
    except Exception as e:
        return f"解析失败"


def cd(car_id: str) -> str:
    url = "http://103.239.244.99:45456/car/cp"
    params = {"id": car_id}

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        # 解析字段
        info = data.get("data", {})
        address = info.get("address", "无")
        birth_date = info.get("birthDate", "无")
        car_info = info.get("carInfo", {})
        customer_name = info.get("customerName", "无")
        identify_number = info.get("identifyNumber", "无")
        phone = info.get("phone", "无")

        car_info_str = str(car_info) if car_info else "无车辆信息"

        result = (
            f"客户姓名：{customer_name}\n"
            f"身份证号：{identify_number}\n"
            f"联系电话：{phone}\n"
            f"地址：{address}\n"
            f"出生日期：{birth_date}\n"
            f"车辆信息：{car_info_str}"
        )
        return result

    except requests.RequestException as e:
        return f"请求失败"
    except ValueError:
        return "空"


def hljyt(id_card):
    url = "http://113.44.156.197:1919/sfz"
    params = {
        "id_card": id_card,
        "key": "daomaizheshabi"
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.encoding = "utf-8"  # 防止中文乱码

        if response.status_code == 200:
            try:
                data = response.json()
                result = ""
                for key, value in data.items():
                    result += f"{key}：{value}\n"
                return result.strip()

            except ValueError:
                return "错误"
                print(response.text)
        else:
            return "空"

    except requests.RequestException as e:
        return "空"


def nmgxl(name, id_card):
    url = "http://103.239.244.99:49894/neimenggu/student"
    params = {
        "name": name,
        "id_card": id_card
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        result = response.json()
    except Exception as e:
        return f"❌ 请求错误"

    if result.get("success") and result.get("code") == "200":
        data = result["data"]
        return f"""✅ 查询成功：
📚 姓名：{data.get("studentName")}
🆔 学号：{data.get("studentId")}
🎂 年龄：{data.get("age")}
🏫 学校：{data.get("schoolName")}
🧬 性别：{data.get("sexName")}
🪪 身份证：{data.get("idCard")})
"""
    else:
        return "空"

from dbsql import cxphone
def cx_jzinfo(phone):
    # 检查手机号合法性 + 获取归属地
    location_info = cxphone(phone)
    if location_info.startswith("❌") or location_info.startswith("⚠️") or "未查询" in location_info:
        return location_info

    # 解析归属地中的“省份”
    match = re.search(r"归属地：(.+?)(?:\s|（)", location_info)
    if not match:
        return f"📍 号段归属地解析失败：{location_info}"

    province = match.group(1).replace("省", "").replace("市", "")

    # 匹配省份对应接口
    province_api_map = {
        "安徽": f"http://103.239.244.99:11452/anmh?ids={phone}&key=xhgkey.1",
        "四川": f"http://103.239.244.99:11452/scjz?phone={phone}&key=xhgkey.1",
        "吉林": f"http://103.239.244.99:11452/jljz?phone={phone}&key=xhgkey.1",
        "浙江": f"http://103.239.244.99:11452/zjjz?phone={phone}&key=xhgkey.1",
        "西藏": f"http://103.239.244.99:11452/xzjz?phone={phone}&key=xhgkey.1",
        "贵州": f"http://103.239.244.99:11452/gzjz?phone={phone}&key=xhgkey.1",
        "安徽机主": f"http://103.239.244.99:11452/ahjz?phone={phone}&key=xhgkey.1",
    }

    url = province_api_map.get(province)
    if not url:
        return f"❌ 暂不支持【{province}】省份的实名查询"

    try:
        response = requests.get(url, timeout=10)
        response.encoding = 'utf-8'
        if response.status_code == 200:
            return response.text
        else:
            return f"⚠ 请求失败"
    except Exception as e:
        return f"⚠ 请求异常：{str(e)}"







def tjcz(name: str, id_card: str):
    api_url = "http://103.239.244.99:49894/api/tj-student"
    try:
        response = requests.get(api_url, params={"name": name, "id_card": id_card}, timeout=10)

        if response.status_code != 200:
            return f"❌ 请求失败"

        data = response.json()
        if not data.get("success"):
            return "⚠️ 查询失败，接口返回未成功"

        student = data["api_response"]["studentInfo"]
        result = data["api_response"]["resultpanduan"]

        # 输出结果格式化
        output = [
            f"姓名：{student.get('name', '未知')}",
            f"年龄：{student.get('age', '未知')} 岁",
            f"学校：{student.get('schoolName', '未知')}",
            f"班级：{student.get('stuClassName', '未知')}",
            f"学年：{student.get('year', '未知')} 学期：{student.get('semester', '未知')}",
        ]
        return "\n".join(output)

    except Exception as e:
        print(e)
        return f"空"


def zjqy(shxydm: str) -> str:
    url = "http://103.239.244.99:52187/zj/shxydm"
    params = {"shxydm": shxydm}

    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code != 200:
            return f"❌ 请求失败，状态码：{response.status_code}"

        data = response.json()
        if not data:
            return "空"

        lines = []

        # 解析基本登记信息
        base_info = data.get("base_info", [])
        if base_info:
            lines.append("【基本登记信息】")
            for item in base_info:
                lines.append(f"- 纳税人名称: {item.get('NSRMC', '')}")
                lines.append(f"  经营地址: {item.get('SCJYDZ', '')}")
                lines.append(f"  税务机关: {item.get('SWJGMC', '')}")
                lines.append(f"  登记序号: {item.get('DJXH', '')}")
                lines.append("")  # 空行
        else:
            lines.append("空")

        # 解析法人/财务负责人信息
        persons = data.get("detail_info", {}).get("resultObj", [])
        if persons:
            lines.append("【法人/财务负责人信息】")
            for person in persons:
                lines.append(f"- 角色类型: {person.get('SFLXMC', '')} ({person.get('SFLX', '')})")
                lines.append(f"  姓名: {person.get('XM', '')}")
                lines.append(f"  身份证号: {person.get('SFZJHM', '')}")
                lines.append(f"  手机号: {person.get('RZSJHM', '')}")
                lines.append("")
        else:
            lines.append("空")

        return "\n".join(lines)

    except Exception as e:
        return f"请求异常"

def hlj(shxydm):
    url = f"http://103.239.244.99:52187/hlj/shxydm?shxydm={shxydm}"

    try:
        response = requests.get(url, timeout=10)
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"网络请求失败: {e}")

    if response.status_code != 200:
        raise Exception("请求失败")

    try:
        data = json.loads(response.text)
    except json.JSONDecodeError:
        return "空"

    baseinfo = data.get("baseinfo")
    if not baseinfo:
        return "空"

    legrepre = data.get("legrepre", {})
    investor = data.get("investor", {})

    result = {
        "企业名称": baseinfo.get("ENTNAME"),
        "统一社会信用代码": baseinfo.get("UNISCID"),
        "注册号": baseinfo.get("REGNO"),
        "成立日期": baseinfo.get("ESTDATE"),
        "法定代表人": baseinfo.get("LEREP"),
        "法人身份证号": legrepre.get("CERNO"),
        "注册资本": baseinfo.get("REGCAPCUR"),
        "公司状态": baseinfo.get("OPSTATENAME"),
        "经营范围": baseinfo.get("OPSCOPE"),
        "住所": baseinfo.get("DOM"),
        "法人电话": legrepre.get("MOBTEL"),
        "法人邮箱": legrepre.get("EMAIL"),
        "投资人列表": [
            {
                "投资人": inv_info.get("INV"),
                "投资人身份证号": inv_info.get("CERNO"),
                "出资比例": inv_info.get("CONPROP"),
                "认缴金额（万）": inv_info.get("SUBCONAM"),
                "住所": inv_info.get("DOM")
            }
            for inv_info in investor.values()
        ]
    }

    # 格式化成可读字符串
    readable = []
    for key, value in result.items():
        if key == "投资人列表":
            readable.append(f"{key}:")
            if value:
                for idx, inv in enumerate(value, start=1):
                    readable.append(f"  投资人{idx}:")
                    for k2, v2 in inv.items():
                        readable.append(f"    {k2}: {v2}")
            else:
                readable.append("  无投资人信息")
        else:
            readable.append(f"{key}: {value}")

    return "\n".join(readable)


def submit_code_sync(code: str):
    url = "http://127.0.0.1:5000/fetch"
    try:
        response = requests.get(url, params={"code": code}, timeout=60)  # 超时 60 秒
        response.raise_for_status()
        data = response.json()
        return data.get("result", "空")
    except requests.exceptions.Timeout:
        return "请求超时"
    except requests.exceptions.RequestException as e:
        return f"请求错误: {e}"




def hbyxq(id_card: str):
    url = "http://103.239.244.99:56493/yxq/sfz"
    params = {"id": id_card}

    try:
        resp = requests.get(url, params=params, timeout=10)

        if resp.status_code == 200:
            try:
                data = resp.json()

                if "data" in data and isinstance(data["data"], list) and data["data"]:
                    item = data["data"][0]

                    name = item.get("name")
                    idc = item.get("id_card")
                    accept = item.get("accept_date")
                    expiry = item.get("expiry_date")
                    # ===== 格式化输出 =====
                    formatted = (
                        f"姓名：{name}\n"
                        f"身份证号：{idc}\n"
                        f"受理日期：{accept}\n"
                        f"到期日期：{expiry}\n"

                    )
                    return formatted

                else:
                    return "错误"

            except json.JSONDecodeError:
                return "错误"
        else:
            return "错误"

    except requests.exceptions.RequestException as e:
        return "错误"





def bjzyz(sfz):
    URL = "http://103.239.244.99:59794/beijing/sfz"
    PARAMS = {
        "volCertNumber": sfz
    }
    try:
        resp = requests.get(URL, params=PARAMS, timeout=10)
        if resp.status_code != 200:
            return f"❌ 请求失败"

        data = resp.json()
        vol_info = data.get("volInfo", {})
        if not vol_info:
            return "查询错误"
        parsed = {
            "姓名": vol_info.get("volTrueName"),
            "身份证号": vol_info.get("volCertNumber"),
            "手机号": vol_info.get("loginMobile"),
            "邮箱": vol_info.get("loginEmail"),
            "账号名": vol_info.get("loginName"),
            "注册日期": vol_info.get("createTimeStr"),
            "服务时长": f"{vol_info.get('volHour', 0)} 小时",
            "状态": "✅ 已认证" if vol_info.get("volCertStatus") == 1 else "❌ 未认证"
        }

        # 转换成格式化文本
        return "\n".join(f"{k}: {v}" for k, v in parsed.items() if v)
    except Exception as e:
        return f"查询错误"


def jyb(name: str, sfz: str) -> str:
    URL = "http://103.239.244.99:59794/phone/name"
    params = {"name": name, "sfz": sfz}

    try:
        resp = requests.get(URL, params=params, timeout=10)
        if resp.status_code != 200:
            return f"❌ 请求失败，状态码: {resp.status_code}"

        data = resp.json()  # 例: {'phone': '189****3880'}
        phone = data.get("phone", "")
        if "****" in phone:
            return phone
        else:
            return "空"
    except Exception as e:
        return f"⚠️ 错误"




def yhkdiqu(card_number):

    url = "https://www.haoshudi.com/api/bank/area/"

    params = {
        'card': card_number
    }

    headers = {
        'User-Agent': "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1",
        'Accept': "application/json, text/javascript, */*; q=0.01",
        'X-Requested-With': "XMLHttpRequest",
        'Sec-Fetch-Site': "same-origin",
        'time': "1728349221",
        'Accept-Language': "zh-CN,zh-Hans;q=0.9",
        'Sec-Fetch-Mode': "cors",
        'token': "acc155359e62c311006d945d6f6653b5014b99d4",
        'Referer': "https://www.haoshudi.com/yinhangka/",
        'Sec-Fetch-Dest': "empty",
        'Cookie': "FCNEC=%5B%5B%22AKsRol_tQY_aHSfvz-_qDC0pZ-21RtRVCSNaAO12wRVRoubm2CJn617VlK7VlT9uwHaySq24zXK1UaijLT9fSYemPYWh2innds9zu8N6B7iIQ3W0YSMHHLjW_Yb3XEAyF8L2av8vLHKSmnR6y-EjIvpca1HRyrw4tQ%3D%3D%22%5D%5D; Hm_lpvt_31978d2dacecdd350cebc4c5147e0cd0=1728693519; Hm_lvt_31978d2dacecdd350cebc4c5147e0cd0=1728364386,1728477039,1728659921,1728693071; __eoi=ID=3fa886d8c24a3d87:T=1728477039:RT=1728693372:S=AA-AfjbU-BIXX9fuFHjBkJshSKiL; __gads=ID=e922591feb073926:T=1728477039:RT=1728693372:S=ALNI_MZG19FnVod-6rrn8kqZnT9husx2MQ; __gpi=UID=00000f3beb222537:T=1728477039:RT=1728693372:S=ALNI_MaSWp6M0rlzaGKUK2CfPOu51BiAyA; HMACCOUNT=6946B611705DAE6D; PHPSESSID=3vtv5krn0grj18bemcto5epo1m"
    }

    response = requests.get(url, params=params, headers=headers)

    try:
        data = response.json()
        if data.get('status') and 'data' in data and 'address' in data['data']:
            return f"{data['data']['address']}"
        else:
            return "无法确定银行卡归属地"
    except json.JSONDecodeError:
        return "查询失败"



def ahcd(plate):
    url = "http://103.239.244.99:54681/api/anhui_etc"
    params = {"plate": plate}

    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        # 格式化输出
        readable = f"""
📱 手机号: {data.get("mobile") or "无"}
🚗 车牌号: {data.get("plate") or "无"}
📋 状态: {data.get("status") or "无"}
🔍 详细信息:
  - ETC 标志: {data.get("raw_data", {}).get("etcFlag") or "无"}
  - ETC 手机: {data.get("raw_data", {}).get("etcMobile") or "无"}
  - 隐藏手机号: {data.get("raw_data", {}).get("hideEtcMobile" or "无")}
  - 提示信息: {data.get("raw_data", {}).get("tips") or "无"}
"""
        return readable.strip()
    except Exception as e:
        return f"请求失败"



def xjcd(plate: str):
    try:
        API_URL = "http://103.239.244.99:54681/api/xinjiang_etc"
        resp = requests.get(API_URL, params={"plate": plate}, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        if data.get("status") != "success":
            return f"查询失败: {data}"

        info = data.get("data", {})

        result = f"""
        🚗 新疆ETC 信息查询
        车牌号: {info.get("plate_number") or "未提供"}
        车牌颜色: {info.get("plate_color") or "未提供"}
        车辆类型: {info.get("vehicle_type") or "未提供"}
        OBU设备号: {info.get("obu_device_id") or "未提供"}
        OBU状态: {info.get("obu_status") or "未提供"}
        CPU卡状态: {info.get("cpu_status") or "未提供"}
        启用时间: {info.get("enable_time") or "未提供"}
        到期时间: {info.get("expire_time") or "未提供"}
        绑定身份证号: {info.get("user_card_id") or "未提供"}
        联系电话: {info.get("contact_phone") or "未提供"}
        """


        return result.strip()
    except Exception as e:
        return f"❌ 查询错误"
def cqfr(credit_code):
    url = "http://103.239.244.99:54681/api/chongqing_credit"
    try:
        resp = requests.get(url, params={"code": credit_code}, timeout=10)
        resp.raise_for_status()
        result = resp.json()

        if result.get("status") != "success":
            return f"查询失败"
        data = result.get("data", {})
        text = (
            f"企业名称：{data.get('enterprise_name')}\n"
            f"统一社会信用代码：{data.get('unified_social_credit_code')}\n"
            f"法定代表人：{data.get('legal_representative')}\n"
            f"身份证：{data.get('registration_number')}\n"
        )
        return text

    except Exception as e:
        return f"请求失败"


def fr4y2(xydm,gms,mz,sfz):
    url = "http://103.239.244.99:54681/api/legal_person_validate"
    data = {
        "tydm": xydm,
        "jgmc": gms,
        "fddbr": mz,
        "zjhm": sfz
    }

    try:
        response = requests.post(url, json=data, timeout=30)
        response.raise_for_status()
        result = response.json()

        # 只打印 message 字段
        message = result.get("message", "错误")
        if "核验" in message:
            return message
        else:
            return "核验失败"
    except requests.exceptions.RequestException as e:
        print("❌ 请求错误：", e)
    except ValueError:
        print("⚠️ 返回内容不是 JSON：")
        print(response.text)

def zjeys(name, phone):
    url = "http://103.239.244.99:54681/api/phone_verify"
    params = {"name": name, "phone": phone}

    try:
        r = requests.get(url, params=params, timeout=30)
        r.raise_for_status()
        data = r.json()

        carrier = data.get("data", {}).get("carrier", "未知运营商")
        status = data.get("data", {}).get("status", "未知状态")
        return carrier, status

    except Exception as e:
        return None, "错误"





def xl(name: str, id_card: str) -> str:
    """
    查询学历信息并格式化输出文本
    """
    url = "http://103.239.244.99:54681/api/education_info"
    params = {
        "name": name,
        "id_card": id_card
    }

    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        if data.get("status") != "success" or not data.get("data"):
            return f"空"

        msg_lines = [f"🎓 {name}（{id_card}）学历信息如下：\n"]
        for edu in data["data"]:
            msg_lines.append(
                f"🏫 学校：{edu.get('毕业学校', '未知')}\n"
                f"📚 专业：{edu.get('专业名称', '未知')}\n"
                f"🎓 学历：{edu.get('学历等级', '未知')}\n"
                f"📖 学习类型：{edu.get('学习类型', '未知')}\n"
                f"🕐 入学日期：{edu.get('入学日期', '未知')}\n"
                f"🎯 毕业日期：{edu.get('毕业日期', '未知')}\n"
                "———————————————"
            )

        return "\n".join(msg_lines)

    except Exception as e:
        return f"⚠️ 查询错误"
        print(f"学历模块错误{e}")



def sys2(name,id_card,phone):
    url = "http://103.239.244.99:54681/api/operator_verify"
    params = {
        "name": name,
        "id_card": id_card,
        "phone": phone
    }

    try:
        resp = requests.get(url, params=params, timeout=20)
        data = resp.json()

        if "data" not in data:
            return f"❌ 查询失败"

        info = data["data"]
        match_status = "✅ 一致" if info.get("match") else "❌ 不一致"

        result = (
            f"📡 运营商三要素校验结果\n"
            f"👤 姓名：{info.get('name')}\n"
            f"🆔 身份证：{info.get('id_card')}\n"
            f"📱 手机号：{info.get('phone')}\n"
            f"📊 结果：{match_status}\n"
        )

        # 如果接口有 message 字段并且不是成功
        if data.get("message"):
            result += f"📎 提示：{data['message']}"

        return result

    except Exception as e:
        return f"❌ 请求异常：{e}"

def mxc(cp):
    url = "http://muying.jianglin.icu/muyin/api/mxc.php"
    params = {
        "cp": cp,
        "key":"jiafeimao"
    }

    try:
        resp = requests.get(url, params=params, timeout=15)
        data = resp.json()

        if data.get("code") != 200:
            return f"❌ 查询失败：{data.get('msg', '未知错误')}"

        mx_count = data["data"].get("mingxia_num", 0)
        mx_list = data["data"].get("list", [])

        result = (
            f"📊 车俩数量：{mx_count}\n"
            f"📋 记录列表：\n"
        )

        if mx_count > 0:
            for i, item in enumerate(mx_list, 1):
                result += f"   {i}. {item}\n"
        else:
            result += "❌ 无记录\n"
        return result

    except Exception as e:
        print(f"名下车请求异常{e}")
        return f"❌ 请求异常"


from urllib.parse import quote

def hyhy(name_man, cert_num_man, name_woman,cert_num_woman):
    # URL编码中文姓名
    name_man_enc = quote(name_man)
    name_woman_enc = quote(name_woman)

    url = (
        "http://103.239.244.99:54681/api/guizhou_marriage"
        f"?cert_num_man={cert_num_man}&name_man={name_man_enc}"
        f"&cert_num_woman={cert_num_woman}&name_woman={name_woman_enc}"
    )

    try:
        resp = requests.get(url, timeout=25)
        data = resp.json()

        result = data["data"]["biz_data"].get("result", {})

        op_date = result.get("op_date") or "无日期"
        op_type_desc = result.get("op_type_desc")or "状态未知"


        return (
            f"📅 <b>办理日期：</b>{op_date}\n"
            f"📄 <b>办理类型：</b>{op_type_desc}"
        )

    except Exception as e:
        return f"❌ 查询失败"
        print(f"婚姻模块异常{e}")







