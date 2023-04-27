import nasapy
from aiogram import Bot, Dispatcher, executor, types
from datetime import datetime
import random
import requests
from data import db_session
from data.users import User
from data.links import Links
from config import BOT_TOKEN
from datetime import datetime, timedelta
db_session.global_init("db/bot_data.db")
NASA_API_KEY = 'fNkARpRKqsFjsvNwX90bIsEjdseRUp4GfhTdO5Qx'
img_request = 'https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos'
array = open('img.marsLisr', mode='a')
DB_SESSION = db_session.create_session()
bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)
RUN = True
admins = ["1428507394", "1525377107"]
commands = ["/en", "/ru", "/bk", "/fr", "/mars", "/rover", "/rovers", "/today", "/apod", "/Apod", "/popular",
            "марс:12", "adop:2001-01-01"]


class Timer:
    def __init__(self, tick):
        self.tick, self.last = tick, datetime.now()

    def tk(self):
        if (datetime.now() - self.last) > timedelta(seconds=self.tick):
            self.last = datetime.now()
            return True
        return False


def distance(a, b):
    n, m = len(a), len(b)
    if n > m:
        a, b = b, a
        n, m = m, n
    current_row = range(n + 1)
    for i in range(1, m + 1):
        previous_row, current_row = current_row, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete, change = previous_row[j] + 1, current_row[j - 1] + 1, previous_row[j - 1]
            if a[j - 1] != b[i - 1]:
                change += 1
            current_row[j] = min(add, delete, change)
    return current_row[n]


def nearest_com(com):
    global distance, commands
    return f"Do you mean {sorted(commands, key=lambda x: distance(x, com))[0]} ?"


def user_exist(uid):
    return len(list(DB_SESSION.query(User).filter(User.uid == uid))) == 1


def register_user(uid):
    if not user_exist(uid):
        user = User(uid=uid)
        DB_SESSION.add(user)
        DB_SESSION.commit()


def link_exist(key):
    return len(list(DB_SESSION.query(Links).filter(Links.key == key))) >= 1


def add_link(key, link):
    link = Links(key=key, link=link, asks=1)
    DB_SESSION.add(link)
    DB_SESSION.commit()


def plus_link(key):
    for i in DB_SESSION.query(Links).filter(Links.key == key):
        i.asks += 1
    DB_SESSION.commit()


def get_asks(key):
    return DB_SESSION.query(Links).filter(Links.key == key).first().asks


def get_link(key):
    return DB_SESSION.query(Links).filter(Links.key == key).first().link


def jodict(di):
    return ''.join('{}{}'.format(key, val) for key, val in di.items())


def most_popular():
    mes, ask, key = "NO REZULT", 1, ""
    for i in DB_SESSION.query(Links).filter(Links.asks > 2):
        if i.asks > ask:
            ask, mes, key = i.asks, i.link + f"\nCALLS: {i.asks}", i.key
    if link_exist(key):
        plus_link(key)
    return mes


@dp.message_handler(commands=['start'])
async def _start(message: types.Message):
    register_user(message.chat.id)
    await message.answer('''
            To start help command, use:
            /en - on english
            /ru - on russian
            /bk - on bashkort
            /fr - on french.''')


@dp.message_handler(commands=['ru'])
async def ru_start(message: types.Message):
    await message.answer('''
Здравствуй, этот бот нужен для получения фото из NASA API.
Бот может:
- присылать рандомное фото марсианского ровера.
    Для этого нужно послать команду /mars, /rover, /rovers.
- присылать фото конкретного дня марсианского ровера.
    Для этого нужно послать сообщения "марс:день(доступнодо 1700 дня)".
- присылать текущее изображение или фотоснимок из нашей Вселенной,
 а также краткое пояснение к нему, написанное профессиональным астрономом.
    Для этого нужно послать команду /today, /apod, /Apod.
- присылать изображение или фотоснимок из нашей Вселенной, а также краткое пояснение к нему,
 написанное профессиональным астрономом конкретного дня.
    Для этого нужно послать сообщения "apod:год-месяц-день".
- присылать самый популярный запрос среди пользователей
    Для этого пошлите команду /popular''')


@dp.message_handler(commands=['en'])
async def en_start(message: types.Message):
    await message.answer('''
Hello, this bot is needed to get photos from the NASA API.
The bot can:
- send a random photo of the Mars rover.
    To do this, send the command /mars, /rover, /rover.
- send photos of a specific day of the Mars rover.
    To do this, you need to send messages "Mars: day (available until 1700 days)".
- send the current image or photograph from our universe,
 as well as a brief explanation to it, written by a professional astronomer.
    To do this, send the command /today, /ipad, /iPod.
- send an image or photograph from our universe, as well as a brief explanation to it
, written by a professional astronomer of a particular day.
    To do this, you need to send messages "apod:year-month-day".
- send the most popular request among users
 To do this, send the command /popular
''')


@dp.message_handler(commands=['bk'])
async def bk_start(message: types.Message):
    await message.answer('''
Сәләм, БЫЛ бот NASA API-нан фото алыу өсөн кәрәк.
Бот ала:
 марс роверының осраҡлы фотоһын ебәрергә.
Бының өсөн /mars, /rover, /rovers командаларын ебәрергә кәрәк.
 марс роверының билдәле бер көнөнөң фотоһын ебәрергә.
  Бының өсөн "марс:көн(1700 көнгә тиклем)"тигән хәбәрҙәр ебәрергә кәрәк.
 Хәҙерге һүрәтте йәки фотоһүрәтте Беҙҙең Ғаләмдән ебәрергә,
  шулай уҡ профессиональ астроном яҙған ҡыҫҡаса аңлатманы ебәрергә.
Бының өсөн /today, /ipod, /Ipod командаларын ебәрергә кәрәк.
- Беҙҙең Ғаләмдән һүрәт йәки фотоһүрәт ебәрергә, шулай уҡ уға ҡыҫҡаса аңлатма ебәрергә,
 уны профессиональ астроном конкрет көн яҙған.
Бының өсөн "apod:йыл-ай-көн"тигән хәбәрҙәр ебәрергә кәрәк.
 ҡулланыусылар араһында иң популяр запрос ебәрергә
 Бының өсөн команда ебәрегеҙ /popular
''')


@dp.message_handler(commands=['fr'])
async def bk_start(message: types.Message):
    await message.answer('''
Bonjour, ce bot est nécessaire pour obtenir une photo de l'API de la NASA.
Le bot peut:
- envoyer une photo aléatoire d'un Rover martien.
 Pour ce faire, vous devez envoyer la commande / mars, /rover, / rovers.
- envoyer une photo d'un jour particulier d'un Rover martien.
 Pour ce faire, vous devez envoyer des messages "mars: jour (disponible 1700 jours)".
- envoyer une image ou une photo actuelle de notre Univers,
 et aussi une brève explication écrite par un astronome professionnel.
 Pour ce faire, vous devez envoyer la commande / today, / apod, / Apod.
- envoyer une image ou une photo de notre Univers, ainsi qu'une brève explication,
 écrit par un astronome professionnel.
 Pour ce faire, vous devez envoyer des messages "apod: année-mois-jour".
- envoyer la demande la plus populaire parmi les utilisateurs
 Pour ce faire, envoyez la commande / popular
''')


def get_nice_img_(date_now, date=''):
    nasa = nasapy.Nasa(key=NASA_API_KEY)
    # Get today's date in YYYY-MM-DD format:

    d = datetime.today().strftime('%Y-%m-%d') if date_now else date if date != '' else '2001-01-01'
    # Get the image data:
    if link_exist(d):
        plus_link(d)
        rez = get_link(d) + f"\n CALLS: {get_asks(d)}"
    else:
        apod = nasa.picture_of_the_day(date=d, hd=True)
        rez = f"<b>{apod['title']}</b> \n <b>Date:</b> {apod['date']} \n \n {apod['explanation']} \n {apod['hdurl']}"
        add_link(d, rez)
    return rez


def get_my_mars_(params):
    par = jodict(params)
    if link_exist(par):
        rez = get_link(par)
        plus_link(par)
        return rez + f"\n CALLS: {get_asks(par)}"
    response = requests.get(img_request, params=params)
    if response:
        json_response = response.json()
        if json_response:
            rez = 'Camera: ' + json_response['photos'][0]['camera']['full_name'] + '\n' + 'Day: ' \
                   + str(json_response['photos'][0]['sol']) + '\n' + json_response['photos'][0]['img_src']
            add_link(par, rez)
        else:
            rez = 'Sorry, response is empty'
    else:
        rez = 'Sorry, response is empty'

    return rez


@dp.message_handler(commands=['mars', 'rover', 'rovers'])
async def mars_(message: types.Message):
    await message.answer('Wait...')
    sol = random.randint(0, 1722)
    paramsi = {'sol': sol, 'api_key': NASA_API_KEY}
    rez = get_my_mars_(paramsi)
    print(rez)
    await message.answer(rez)


@dp.message_handler(commands=['today', 'Apod', 'apod'])
async def cmd_start(message: types.Message):
    await message.answer('Wait...')
    rez = get_nice_img_(True)
    print(rez)
    await message.answer(rez)


@dp.message_handler(commands=['shutdown'])
async def finish(message: types.Message):
    if message.chat.id in admins:
        await bot.send_message(message.chat.id, "goodbuy")
        RUN = False
        exit()


@dp.message_handler(commands=['popular'])
async def popular(message: types.Message):
    await message.answer(most_popular())


@dp.message_handler()
async def welcome(my_message):
    await my_message.answer('Wait...')
    message = my_message.text.split(':')
    try:
        if message[0].lower() == 'марс':
            if abs(int(message[1])) < 1700:
                sol = abs(int(message[1]))
                paramsi = {'sol': sol, 'api_key': NASA_API_KEY}
                await my_message.answer(get_my_mars_(paramsi))
            else:
                await my_message.answer('В этот день снимка нет :(')
        elif message[0].lower() == 'apod':
            try:
                await my_message.answer(get_nice_img_(False, message[1]))
            except Exception as ex:
                await my_message.answer(f'!!!Error!!! \n {ex}')
        else:
            await my_message.answer('Неправильный формат ввода.')
            await bot.send_message(my_message.chat.id, nearest_com(my_message.text))
    except Exception as ex:
        await my_message.answer(f'!!!Error!!! \n {ex}')
        await bot.send_message(my_message.chat.id, nearest_com(my_message.text))


if __name__ == "__main__":
    timeC = Timer(10)
    while RUN:
        if timeC.tk():
            try:
                executor.start_polling(dp, skip_updates=True)
            except Exception as ex:
                print(ex)
