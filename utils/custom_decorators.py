import os
from settings import ENABLED_COGS

def is_enabled(func):
    """ 
    Decorator to check if the cog is enabled
    
    Example usage:

    @bot.message_handler(commands=["help"])
!   @is_enabled         SHOULD BE USED AFTER ALL OTHER DECORATORS 
    def func(arg):
        func...

    """
    def wrapper(*args, **kwargs):
        filename = os.path.basename(func.__code__.co_filename).split(".")[0]
        if filename not in ENABLED_COGS:
            print(f"{filename} is disabled")
            return
        result = func(*args, **kwargs)  
        return result
    return wrapper

