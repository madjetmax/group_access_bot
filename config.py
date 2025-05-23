import os
from dotenv import load_dotenv
import json
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
GROUP_ID = os.getenv("GROUP_ID")


GROP_LINK_LIFE_TIME = 15 # час доступу посилання (у хвилинах)

# texts
TEXTS_FOLDER = "texts" # папка для всіх текстів, в тому числі і питань

START_TEST_BUTTON_TEXT = "Начать тест" # текст для кнопки для початку тесту яка з'являється після /start
START_TEST_MESSAGE_TEXT = "Теперь пройдите небольшой тест на знание правил." # текст для повідомлення для початку тесту яке з'являється після /start


TEST_FAIL_TEXT = "Ответ неверный, попробуйте заново" # текст при не правильній відповіді на запитання

START_TEST_AGAIN_TEXT = "Вы уже начали проходить тест" # текст якщо користувач ще раз хоче пройти тест

LINK_LIFETIME_TEXT = f"Ссылка на втупление в наш чат активна {GROP_LINK_LIFE_TIME} минут" # текст для повідомдлення, для входу в чат
CHAT_BUTTON_TEXT = "Чат" # текст для кнопки, для входу в чат


# load rulers and questions
with open(f"{TEXTS_FOLDER}/rules.txt", "rb") as file:
    RULES = file.read()

with open(f"{TEXTS_FOLDER}/questions.json", "rb") as file:
    ALL_QUESTIONS = json.load(file)