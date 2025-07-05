from services.parsers import vut_parser
from utils.util_funcs import get_subject_data, format_exam_info

def about_subject_message(callback_data):
    subject = get_subject_data(callback_data)
    return format_exam_info(subject)


HELP_MESSAGE = """
*👋 Hello there\\!*  
I'm *Sammy*, your friendly Telegram bot — crafted with care by Sipxi  💖

📦 Version: `1\\.0\\.0`

📚 Available Commands:
• /start \\- Start the bot
• /help \\- Show this help message
• /about \\- Learn more about me


💡 Tip: Just ask me anything, and I'll do my best to assist you\\!

📩 For support or feedback, reach out to us on GitHub   
"""

DO_MESSAGE = 'Hey! Please choose what you want to do 👇'