def register(bot):
    @bot.message_handler(func=lambda m: True)
    def fallback(message):
        bot.reply_to(message, "Sorry, I don't get that 🤷‍♂️")