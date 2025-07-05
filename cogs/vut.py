from utils.markups import vut_menu, exams_menu
from utils.custom_messages import *

from settings import EXAM_MAP   

def register(bot):
    # Define the start command
    @bot.message_handler(commands=['vut'])
    def start(message):
        bot.send_message(message.chat.id, DO_MESSAGE , reply_markup=vut_menu())


    # Define the callback function for the inline keyboard button
    @bot.callback_query_handler(func=lambda call: True)
    def callback_handler(call):
        if call.data == 'exams_callback':
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="...",
                reply_markup=exams_menu()
            )
        if call.data in EXAM_MAP:
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=f"{about_subject_message(call.data)}",
                parse_mode='MarkdownV2'  # or 'MarkdownV2' if you use that style
                
            )
        
        