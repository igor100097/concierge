import telebot
import time
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("bot_log.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)

# Установка токена вашего бота
TOKEN = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
bot = telebot.TeleBot(TOKEN)

# Обработчик для команды /start (проверка работы бота)
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привет! Я консьерж-бот. Готов следить за порядком в чате!")
    logging.info(f"Отправлено приветственное сообщение для команды /start от пользователя {message.from_user.first_name}")

# Приветствие нового участника в группе
@bot.message_handler(content_types=['new_chat_members'])
def greet_new_member(message):
    for new_member in message.new_chat_members:
        welcome_message = f"Привет, сосед {new_member.first_name}! Напиши номер своей квартиры и этаж."
        bot.send_message(message.chat.id, welcome_message)
        logging.info(f"Приветствие для нового участника: {new_member.first_name}")

# Удаление сообщений со спамом или определенными словами
@bot.message_handler(func=lambda m: any(word in m.text.lower() for word in ['спам', 'реклама', 'оскорбление']))
def delete_spam(message):
    try:
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.chat.id, f"{message.from_user.first_name}, спам запрещен!")
        logging.info(f"Удалено спам-сообщение от {message.from_user.first_name}: {message.text}")
    except Exception as e:
        logging.error(f"Ошибка при удалении сообщения: {e}")

# Команда /help для отображения правил чата
@bot.message_handler(commands=['help'])
def send_rules(message):
    bot.reply_to(message, "Правила чата: \n1. Без спама.\n2. Без оскорблений.\n3. Уважение к участникам.\n4. ...")
    logging.info(f"Отправлены правила чата для команды /help от пользователя {message.from_user.first_name}")

# Обработчик для входящих текстовых сообщений
@bot.message_handler(content_types=['text'])
def handle_text_messages(message):
    logging.info(f"Получено сообщение от {message.from_user.first_name}: {message.text}")
    # Пример реакции на конкретное текстовое сообщение
    if "правила" in message.text.lower():
        bot.reply_to(message, "Пожалуйста, ознакомьтесь с правилами чата.")
    elif "привет" in message.text.lower():
        bot.reply_to(message, f"Привет, {message.from_user.first_name}! Чем могу помочь?")
    else:
        bot.reply_to(message, "Ваше сообщение получено! Если нужна помощь, введите /help.")
    logging.info(f"Обработано текстовое сообщение от {message.from_user.first_name}")

# Бесконечный цикл polling с обработкой ошибок
while True:
    try:
        logging.info("Бот запущен и ожидает сообщений...")
        bot.polling(none_stop=True)  # Запуск polling
    except Exception as e:
        logging.error(f"Произошла ошибка: {e}")
        time.sleep(5)  # Подождем перед перезапуском polling
