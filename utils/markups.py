from telebot import types
from services.parsers import vut_parser
from settings import EXAM_MAP
# Vut menu layout
def vut_menu():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("ℹ️ Exams", callback_data="exams_callback"))
    return markup

# Settings menu layout
def exams_menu():
    markup = types.InlineKeyboardMarkup()
    for exam in vut_parser.get_exam_names():
        EXAM_MAP.append(exam)
        markup.add(types.InlineKeyboardButton(exam, callback_data=exam))
    return markup