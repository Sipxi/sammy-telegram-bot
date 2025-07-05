from utils.custom_decorators import is_enabled
from utils.custom_messages import HELP_MESSAGE
import time

def register(bot):    
    
    
    @bot.message_handler(commands=["help"])
    @is_enabled
    def handle_help(message):
        bot.reply_to(message, HELP_MESSAGE, parse_mode='MarkdownV2')

    # TODO: Latency test?
    @bot.message_handler(commands=['ping'])
    def send_welcome(message):
        start_tiome = time.time()
        pong_message = "🚀Pong!"
        bot.reply_to(message, pong_message)

    @bot.message_handler(commands=['hello'])
    def hello(message):
        start_tiome = time.time()
        pong_message = "hello"
        bot.reply_to(message, pong_message)
        
        