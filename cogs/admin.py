from utils import custom_decorators
import os
# TODO: More detailed messages for errors
# TODO: Add authorization for admin commands
# * Done, but needs to be polished



def check_cog_name(msg_array, message, bot):
    """Checks wheather the cog name is valid
    """
    if len(msg_array) <= 1:
        bot.reply_to(message, "Please provide a cog name to disable.")
        return False
    return True


def register(bot):        
    @bot.message_handler(commands=["disable"])
    def handle_disable(message):
        msg_array = message.text.split()
        if not check_cog_name(msg_array, message, bot):
            return
        if bot.disable_cog(message.text.split()[1]):
            bot.reply_to(message, "✅ Cog disabled!")
        else:
            bot.reply_to(message, "❌ Cog not disabled! Check logs for more info.")
            
    @bot.message_handler(commands=["enable"])
    def handle_enable(message):
        msg_array = message.text.split()
        if not check_cog_name(msg_array, message, bot):
            return
        if bot.enable_cog(message.text.split()[1]):
            bot.reply_to(message, "✅ Cog enabled!")
        else:
            bot.reply_to(message, "❌ Cog not disabled! Check logs for more info.")

    @bot.message_handler(commands=["restart"])
    def restart_bot(message):
        os.environ["RESTART_CHAT_ID"] = str(message.chat.id)
        bot.restart_bot()
        bot.reply_to(message, "✅ Bot restarted!")
        

        
                
    