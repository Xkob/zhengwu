from telebot import TeleBot
from cfg import TOKEN

bot = TeleBot(TOKEN,parse_mode="HTML",skip_pending=False,)
