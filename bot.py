import telebot
from settings import BOT_TOKEN, ENABLED_COGS
import importlib
import os 
import sys
import time

class SammyTelegramBot(telebot.TeleBot):
    """The main bot class, responsible bot management, such as loading cogs, disabling and enabling cogs

    Args:
        telebot (TeleBot): The TeleBot instance
    """
    def __init__(self, token) -> None:
        super().__init__(token)
        # All the cogs that are loaded
        self.activated_cogs = []
        self.all_commands = []
        # Load cogs on start
        self.load_cogs()

    def register_commands(self):
        print("Registering commands...")
        for handler in self.message_handlers:
            filters = handler.get('filters', {})
            commands = filters.get('commands')
            if commands:
                self.all_commands.append(commands[0])
                print(f'- {commands}')
        

    def load_cogs(self) -> None:
        for cog in ENABLED_COGS:
            module_name = f"cogs.{cog}"
            try:
                module = importlib.import_module(module_name)
                # Register the cog handlers
                module.register(self)
                self.activated_cogs.append(module_name)
                print(f"\n - {module_name} is loaded")
            except ImportError as e:
                print(f"\n - Failed to load {module_name}: {e}")
            except Exception as e:
                print(f"\n - Error in {module_name}: {e}")
        self.register_commands()

    def enable_cog(self, cog_name) -> bool:
        if cog_name not in ENABLED_COGS:
            ENABLED_COGS.append(cog_name)
            print(f"{cog_name} is enabled")
            return True
        else:
            print(f"{cog_name} is already enabled")
            return False
        
    def disable_cog(self, cog_name):
        if cog_name in ENABLED_COGS:
            ENABLED_COGS.remove(cog_name)
            print(f"{cog_name} is disabled")
            return True
        else:
            print(f"{cog_name} is not loaded or does not exist")
            return False
    def check_state(self) -> bool:
        is_restarted = os.getenv("RESTARTED")
        if is_restarted == "1":
            return True
        else:
            return False
    def reply_for_restart(self):
        # Send a message to the user who restarted the bot
        message_id = os.getenv("RESTART_CHAT_ID")
        if message_id:
            bot.send_message(int(message_id), "✅ Bot restarted!")
    
    def restart_bot(self):
        # Delay
        time.sleep(0.1)
        # Stop polling
        bot.stop_polling()
        # Set RESTARTED to 1
        os.environ["RESTARTED"] = "1"
        # Restart the bot
        os.execv(sys.executable, ['python'] + sys.argv)
    
    def start_bot(self):
        # Message based on state
        message = "✅ Bot started!" if not self.check_state() else "✅ Bot restarted!"
        print(message)
        # Send the message to the user
        self.reply_for_restart()
        self.polling()
        print("Bot stopped.")


if __name__ == "__main__":
    # Initialize the bot
    bot = SammyTelegramBot(BOT_TOKEN)
    # Set the bot commands
    bot.set_my_commands(commands=[
        telebot.types.BotCommand("/help", "Start the bot and get a welcome message"),
        telebot.types.BotCommand("/disable", "Disable a cog"),
        telebot.types.BotCommand("/enable", "Enable a cog"),
        ])
    # Start the bot
    bot.start_bot()

