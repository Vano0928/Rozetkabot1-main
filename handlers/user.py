from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters
from .open_json import read_json_data, write_register_json_data, write_json_data, check_if_logined, check_login_and_password
from .keyboards import login_reply_kb, start_reply_kb

async def cmd_register(update : Update, context : ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    data = read_json_data()
    if len(context.args) == 2:
        login_text = context.args[0]
        password_text = context.args[1]

    if len(context.args) != 2:
       await update.message.reply_text('Ви маєте ввести /reg <логін> <пароль>')

    elif login_text in data:
        await update.message.reply_text('Ви вже зареєстровані')

    elif check_if_logined(user_id) == False:
        write_register_json_data(login_text, password_text)
        await update.message.reply_text('Ви успішно зареєструвалися')

    else:
        await update.message.reply_text('Ви вже залогінені в свій акаунт, щоб зареєструватися, вам потрібно вийти з акаунта')


async def cmd_login(update : Update, context : ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if len(context.args) == 2:
        login = context.args[0]
        password = context.args[1]
    
    else:
        await update.message.reply_text("Ви неправильно написали команду, маєте ввести /login <логін> <пароль>")
        return
   
    if check_login_and_password(login, password):
        if check_if_logined(user_id) == False:
            data = read_json_data()
            data['logined tg users'][(str(user_id))] = login
            write_json_data(data)
            
            reply_kb = login_reply_kb()

            await update.message.reply_text("Ви успішно увійшли!", reply_markup=reply_kb)
        
        else: 
            await update.message.reply_text('Ви вже входили в акаунт')

    else:
        await update.message.reply_text("Неправильний логін або пароль.")


async def cmd_logout(update : Update, context : ContextTypes.DEFAULT_TYPE):

    user_id = str(update.effective_user.id)
    data = dict(read_json_data())

    if user_id in data['logined tg users']:
        data['logined tg users'].pop(user_id)
        write_json_data(data)

        reply_kb = start_reply_kb()
        await update.message.reply_text('Ви успішно вийшли з акаунту', reply_markup=reply_kb)
    else:
        await update.message.reply_text('Ви ще не ввійшли в акаунт, щоб вийти з нього')


def get_handlers():
    return [
        CommandHandler('register', cmd_register),
        CommandHandler('login', cmd_login),
        MessageHandler(filters.Text('Вийти з акаунту'), cmd_logout)
    ]
