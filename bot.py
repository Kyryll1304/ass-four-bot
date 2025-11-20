import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Токен бота из переменной окружения
BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден! Создайте .env файл с BOT_TOKEN=your_token")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /start"""
    welcome_text = "Здравствуй,воин!Похоже что ты приобрел этот чудо-аппарат и теперь тебя мучают вопросы, связанные с его использованием. Самые первые владельцы этой машины покинули 3х мерный мир и теперь живут в квантовом пространстве.Они создали этот бот для того, чтобы помочь тебе разобраться в использовании этого аппарата.Для того чтобы начать пользоваться ботом, тебе нужно нажать на кнопку 'Начать'.Итак, начнем!"
    await update.message.reply_text(welcome_text)


async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /contact"""
    await update.message.reply_text("Последний пользующийся телефоном владелец этой машины: В ")


async def engine(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /engine"""
    await update.message.reply_text("Количество моторов:2")

async def key(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /key"""
    await update.message.reply_text("За второй ключ до сих пор ведется борьба в инстаграме с афроамериканцем который разпиздячил ее в СШП")


async def questions(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /questions"""
    # Массив ответов
    answers = [
        "Метки были пожертвованы друзьями и родственниками на память",
        "Мотор второй потому что ФИА запретило использование настолько мощного двигателя и прислали чуть менее мощный",
        "В коробку до сих пор залит солидол с водкой,просьба не вскрывать,пережила целый мотор",
        "НЕ дрифтить!Отьебет блок СРС!"
    ]
    response_text = "\n".join(answers)
    await update.message.reply_text(response_text)


async def last_price(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /lastPrice"""
    await update.message.reply_text("Последний раз ее купили за: 22000 usd")


def main() -> None:
    """Запуск бота"""
    # Создаем приложение
    application = Application.builder().token(BOT_TOKEN).build()

    # Регистрируем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("contact", contact))
    application.add_handler(CommandHandler("engine", engine))
    application.add_handler(CommandHandler("key", key))
    application.add_handler(CommandHandler("questions", questions))
    application.add_handler(CommandHandler("lastPrice", last_price))

    # Запускаем бота
    logger.info("Бот запущен...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()

