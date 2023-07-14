from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from .open_json import get_orders_data, check_if_logined, get_login, get_orders_msg, read_json_data, write_json_data
from .keyboards import get_orders_kb, back_inline_kb, start_reply_kb
from random import randint


async def cmd_start(update : Update, context : ContextTypes.DEFAULT_TYPE):
    reply_kb = start_reply_kb()
    await update.message.reply_text('Привіт! Це бот інтернет магазину розетка. У цьому боті ви можете зайти в свій акаунт розетки, і подивитися інформацію про своє замовлення. Напишіть команду /help щоб подивитися всі інші команди.',
                                    reply_markup=reply_kb)


async def help(update : Update, context : ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('''
Ось список команд, які вам можуть бути потробні:
1) /register <логін> <пароль> - зареєструвати свій акаунт;
2) /login <логін> <пароль> - увійти в свій акаунт;
3) Мої замовлення - це кнопка знизу, під клавіатурою щоб подивитися інформацію про свої замовлення.''')


async def send_order_data(update : Update, context : ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    login = get_login(user_id)
    order_id = update.callback_query.data.split()[1]

    order_data = get_orders_data(login)[str(order_id)]

    item_name = order_data['item_name']
    arrival_time = order_data['arrival_time']
    price = order_data['price']
    delivery_price = order_data['delivery_price']


    msg = f'Назва товару - {item_name}, ціна(з доставкою) - {price + delivery_price}, орієнтовна дата прибуття - {arrival_time}'
    query = update.callback_query
    inline_kb = back_inline_kb()

    await query.edit_message_text(text = msg, reply_markup=inline_kb)



async def send_orders(update : Update, context : ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    if get_orders_msg(user_id) != False:
        msg = get_orders_msg(user_id)[0]

    else:
        await update.message.reply_text('Ви ще не ввійшли в акаунт')
        return ...

    orders = get_orders_msg(user_id)[1]
    reply_kb_markup = get_orders_kb(orders, user_id)
    query = update.callback_query

    if query == None:
        await update.message.reply_text(msg, reply_markup= reply_kb_markup)
    
    else:
        await query.edit_message_text(msg, reply_markup= reply_kb_markup)


async def add_order(update : Update, context : ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    item_name = context.args[0]

    if check_if_logined(user_id):
        login = get_login(user_id)

    data = read_json_data()

    new_order = {randint(1, 10000) : {
                "item_name": f"{item_name}",
                "item_id": f'{randint(1, 10000)}',
                "arrival_time": "16.07.2023",
                "price": randint(100, 10000),
                "delivery_price": 100}}

    data[login]['orders'].update(new_order)

    write_json_data(data)

    await update.message.reply_text('Ви успішно додали нове замовлення')


def cmd_tech_break(update : Update, context : ContextTypes.DEFAULT_TYPE):
    ...


async def unknown_user_message(update : Update, context : ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Незрозуміле повідомлення')



def get_handlers():

    return [
        CommandHandler('start', cmd_start),
        CommandHandler('help', help),
        CommandHandler('add_order', add_order),
        MessageHandler(filters.Text('Подивитися свої замовлення'), send_orders),
        MessageHandler(filters.TEXT, unknown_user_message),
        CallbackQueryHandler(callback= send_orders, pattern='back'),
        CallbackQueryHandler(callback= send_order_data)


    ]
