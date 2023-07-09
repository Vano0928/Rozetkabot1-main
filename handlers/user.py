from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from .utils import read_json_data, write_register_json_data

async def cmd_start(update : Update, context : ContextTypes.DEFAULT_TYPE):
    print(update.effective_chat.id)
    # await context.bot.send_message()
    await update.message.reply_text('start')


async def register(update : Update, context : ContextTypes.DEFAULT_TYPE):
    
    data = read_json_data()
    user_data = str(update.effective_message.text).split()
    login_text = user_data[1]
    password_text = user_data[2]

    print(user_data)
    if len(user_data) != 3:
       await update.message.reply_text('Ви маєте ввести /reg <логін> <пароль>')

    elif login_text in data:
        await update.message.reply_text('Ви вже зареєстровані')

    elif ' ' in password_text:
        await update.message.reply_text('Ви ввели пароль неправильно')
    else:
        write_register_json_data(login_text, password_text)



def get_handlers():
    return [
        CommandHandler('start', cmd_start),
        CommandHandler('reg', register)
    ]
