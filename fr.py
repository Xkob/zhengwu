import re
import time
import requests
from collections import deque



def extract_info(text: str) -> str:
    """
    提取姓名和模糊身份证号，如果失败返回空字符串
    """

    # 匹配姓名
    name_match = re.search(r"姓名[:：]\s*([^\s]+)", text)
    name = name_match.group(1) if name_match else ""

    # 匹配身份证（可能带*）
    id_match = re.search(r"证件号码[:：]\s*([0-9Xx*]+)", text)
    idcard = id_match.group(1) if id_match else ""

    if name and idcard:
        return f"{name}-{idcard}"
    return "未知"








