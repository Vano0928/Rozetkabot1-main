from telegram.ext import Application
from handlers import get_all_handlers

BOT_TOKEN = '6352444129:AAElfiNTmjetfMGAuBCHLzZEgtIXLvnNTEo'


def main():
    aplication_builder =  Application.builder()
    aplication_token = aplication_builder.token(BOT_TOKEN)
    aplication = aplication_token.build()

    for handler in get_all_handlers():
        aplication.add_handler(handler)

    aplication.run_polling()


if __name__ == '__main__':
    main()