import os
import logging
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.error import Conflict, RetryAfter, TimedOut
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
    await update.message.reply_text("Последний пользующийся телефоном владелец этой машины: Дензел Вашингтон ")


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


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик ошибок"""
    logger.error(f"Exception while handling an update: {context.error}")
    
    # Обработка конфликтов (другой экземпляр бота запущен)
    if isinstance(context.error, Conflict):
        logger.error("Конфликт: другой экземпляр бота уже запущен. Остановите другие экземпляры.")
        # Можно попробовать подождать и перезапустить
        await asyncio.sleep(5)
    elif isinstance(context.error, RetryAfter):
        logger.warning(f"Rate limit exceeded. Retry after {context.error.retry_after} seconds")
    elif isinstance(context.error, TimedOut):
        logger.warning("Request timed out, retrying...")


async def post_init(application: Application) -> None:
    """Инициализация после создания приложения"""
    # Удаляем webhook если он был установлен (несколько попыток)
    bot = application.bot
    max_attempts = 3
    for attempt in range(max_attempts):
        try:
            await bot.delete_webhook(drop_pending_updates=True)
            logger.info("Webhook удален, pending updates очищены")
            break
        except Conflict as e:
            logger.warning(f"Попытка {attempt + 1}/{max_attempts}: Конфликт при удалении webhook. Ждем 5 секунд...")
            if attempt < max_attempts - 1:
                await asyncio.sleep(5)
            else:
                logger.error("Не удалось удалить webhook после нескольких попыток. Возможно, другой экземпляр бота все еще запущен.")
        except Exception as e:
            logger.warning(f"Ошибка при удалении webhook: {e}")
    
    # Дополнительное ожидание перед стартом polling
    logger.info("Ожидание 3 секунды перед запуском polling...")
    await asyncio.sleep(3)


def main() -> None:
    """Запуск бота"""
    # Создаем приложение с post_init для очистки webhook
    application = Application.builder().token(BOT_TOKEN).post_init(post_init).build()

    # Регистрируем обработчик ошибок
    application.add_error_handler(error_handler)

    # Регистрируем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("contact", contact))
    application.add_handler(CommandHandler("engine", engine))
    application.add_handler(CommandHandler("key", key))
    application.add_handler(CommandHandler("questions", questions))
    application.add_handler(CommandHandler("lastPrice", last_price))

    # Запускаем бота с drop_pending_updates=True для очистки очереди
    logger.info("Запуск бота...")
    application.run_polling(
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=True
    )


if __name__ == '__main__':
    main()

