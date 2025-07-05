from services.parsers import vut_parser
import re

def escape_md(text):
    """Escape Telegram MarkdownV2 reserved characters."""
    return re.sub(r'([_*\[\]()~`>#+\-=|{}.!\\])', r'\\\1', str(text))


def format_exam_info(exam: dict) -> str:
    rooms = escape_md(exam['room']).replace(", ", "\n") if exam['room'] else "N/A"
    return f"""\
📘 *{escape_md(exam['subject'])}*
*Typ:* {escape_md(exam['type'])}  
🗓️ *Datum:* {escape_md(exam['date'])}  
🏆 *Výsledek:* {escape_md(exam['result'])}  
👨‍🏫 *Zkoušející:* {escape_md(exam['lecturer'])}  
🏫 *Místnosti:*  
{rooms}  
👥 *Zapsaní:* {escape_md(exam['num_of_registered_people'])}  
📝 *Registrován:* {"Ano" if exam['is_registered']['status'] else "Ne"}  
"""


def get_subject_data(callback_data):
    # Get subject data
    index = int(callback_data[0])
    text = callback_data.split(")", 1)[1].strip()
    filtered = vut_parser.search(text, "subject")

    return filtered[index-1]