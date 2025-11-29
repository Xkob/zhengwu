#配置文件
from datetime import datetime, date,timedelta,timezone
import logging
TRON_WALLET_ADDRESS = "TWNFxq9BqhkkadiBgErgpBW48V4jEvsbGE"  # 示例地址充值地址
USDT_CONTRACT = "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"  # USDT合约地址
TRONGRID_API_KEY = "d1ffb3ff-bfa5-490e-a6ce-b4ff7a46d105"  # TronGrid API密钥
# mysql配置
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'root',
    'database': 'zwuser',
}
rewu = {}
ADMIN_IDS = [8022175265,899444996,7527185734,7445300717]
CHANNEL_ID = -1001866840961
# 充值日志路径预防有恶意充值成功没发现
RECHARGE_LOG_PATH = "recharge_logs.txt"
qid = -4838257369
TARGET_CHAT_ID = -1001971287812
KEYWORD = "签到"
MIN_INTERVAL_SECONDS = 1
MAX_DAILY_COMMANDS = 200
COMMAND_COOLDOWN_SECONDS = 3
error_keywords = ['失败', '错误','None','异常',"null"]
# 充值选项
RECHARGE_OPTIONS = {
    "10": {"points": 50, "bonus": 0},    # 10 USDT = 50积分，无赠送
    "20": {"points": 110, "bonus": 10},  # 20 USDT = 110积分，送10%
    "50": {"points": 288, "bonus": 15},  # 50 USDT = 288积分，送15%
    "100": {"points": 600, "bonus": 20}, # 100 USDT = 600积分，送20%
    "300": {"points": 2000, "bonus": 33} # 300 USDT = 2000积分，送33%
}
CATEGORY_MAP = {
    "jc": "核验类",
    "dq": "地区类",
    "fr": "法人类",
    "qg": "全国类"
}

GN_ACTIONS = {
    # "qg_qgdt":("全国大头", "/dt 名字 身份证 ", "扣除usdt 会员 2.5 非会员 3 不扣除积","限制 未成年 可使用时间 早上8:00之后到下午7:00前"),
    "jc_kh":("空号检测", "/kh 手机号", 2),
    "jc_hy":("核验", "/hy 男方姓名 男身份证 女方名字 女身份证", 5),
    "jc_yhkdq":("空号检测", "/kh 手机号", 2),
    "qg_mxc":("全国名下车", "/mxc 身份证 ", "扣除绿宝石 会员 1.5 非会员 2 不扣除积","无论空还是有都扣款"),
    "jc_khpl":("空号批量检测", "发送txt文件", "更具条数扣分","使用教程 https://t.me/ZZZTTTS/1029"),
    "jc_sys": ("三要素", "/sys 名字 身份证 手机号", 2, "单次三要素 多次核验会出现错误"),
    "jc_zjhy":("机主二要素","/jzys 名字 手机号",2),
    "jc_eys": ("二要素", "/eys 名字 身份证", 2),
    "jc_yys":("一要素","/yys 身份证",1),
    "jc_frhy":("法人核验","/frhy 企业名称 社会统一信用代码 法人姓名 法人身份证",3," 注销个体 个体独资 都可以核验 "),
    "zx_sjh": ("手机号解析", "/sjh 手机号", 1),
    "zx_yhkdq":("银行卡地区","/yhk 银行卡",2,"核验多次会出现错误"),
    "qg_mhcd": ("模糊车挡", "/mhcd 车牌号", 5,"异常不一定是接口死了可能是空 "),
    "zx_qfjg": ("签发机关", "/qfjg 身份证", 1),
    "fr_fr": ("全国法人2", "/fr2 社会信用代码", 10, "排队机制"),
    "fr_fr2": ("全国法人", "/fr 社会信用代码", 5, "1分钟限制次 限制就排队"),
    "jc_yhk3": ("银行卡3要素", "/yhk3 名字 身份证 银行卡", 5, "接口限制需要排队"),
    "jc_yxq": ("身份证有效期核验", "/yxq 名字 身份证 起始日 结束日", 5, "日期填写如 2024年7日12日写为 20240712 /yxq 名字 身份证 20240712 20240713 "),
    "jc_rlhy": ("人脸核验[VIP]", "仅限VIP使用", "无需", "发送格式 https://t.me/ZZZTTTS/1025"),
    # "qg_yljl": ("医疗记录", "/yljl 名字 身份证", "非 VIP 50 分 VIP 1  ", "非 VIP 50 分 VIP 1分"),
    "dq_bjzyz":("北京志愿者","/bjzyz 身份证",5,""),
    "qg_jybyl":("教育部预留","/jybip 名字 身份证",5,""),
    "qg_qgxl": ("全国学历", "/qgxl 名字 身份证", 10, "建议晚上使用 只有大学毕业可查询"),
    "dq_dqmh":("地区模糊","/dqmh 手机号",4),
    "dq_hljym":("黑龙江疫苗","/hljym 身份证",5),
    "dq_hljyt": ("黑龙江一体化", "/hljyt 身份证", 6),
}
BUTTONS_PER_PAGE = 15
# 会员选项
MEMBERSHIP_OPTIONS = {
    "20": {"days": 7},      # 20 USDT = 7天会员
    "50": {"days": 30},     # 50 USDT = 30天会员
    "100": {"days": 90},    # 100 USDT = 90天会员（3个月）
    "300": {"days": 365},   # 300 USDT = 365天会员（1年）
    "500": {"days": 36500}  # 500 USDT = 终身会员（100年）
}
USDTJG = {
    "10": {"U": 10},
    "50": {"U": 50},
    "100": {"U": 100},
    "300": {"U": 300},
    "500": {"U": 500}
}
sendid = [
    "5104841245755180586",  # 🔥
    "5046509860389126442",  # 🎉
]
TOKEN = "8137250326:AAG6D9Lg5al48iN80Vb6wmI7wCS8or1ihQs"
# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
def log_query(user_id, command, args):
    timestamp = datetime.now(timezone.utc).isoformat()
    log_line = f"时间 {timestamp}用户 {user_id}执行 {command} 参数: {args}"
    logging.info(log_line)

