from lib2to3.pgen2.token import EQUAL
import logging
from settings import Token
from aiogram import Bot, Dispatcher, executor, types
from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
from aiogram.dispatcher.filters import Text

ua = UserAgent()

headers = {'user-agent': ua.random}
url = 'https://ru.investing.com/crypto/bitcoin/news/'

API_TOKEN = Token


# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands='start')
async def send_welcome(message: types.Message):
    start_buttons = 'Получить данные'
    keybord = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keybord.add(start_buttons)

    await message.answer('Please, press the button:', reply_markup=keybord)

@dp.message_handler(Text(equals='Получить данные'))
async def get_data(message: types.Message):
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    news_container = soup.find('div', class_='js-content-wrapper')
    news_list = news_container.find_all('div', class_='textDiv')
    for news in news_list:
        title = news.find('a').text.strip()
        href = news.find('a').get('href').strip()
        discripion = news.find('p').text.strip()
        
        if href.startswith('/'):
            href = 'https://ru.investing.com' + href

        await message.answer(f'Название: {title}\nСсылка: {href}\n Описание: {discripion}')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
