import os
EXAM_MAP = []

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", False)
ENABLED_COGS = ['admin', 'basic', 'vut', 'fallback']
VUT_ID = os.getenv("VUT_ID", False)
VUT_PASS = os.getenv("VUT_PASS", False)
AUTHORIZED_USERS = [993873472]