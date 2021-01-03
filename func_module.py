import datetime
import json
import os
import socket
import threading
import time
import requests
import urllib3
import vk_api
from dotenv import load_dotenv
from googletrans import Translator
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id
import AnimeGoParser
import Dict
import db_module
import KinoPoisk
import random
from newsapi import NewsApiClient

# Init
newsapi = NewsApiClient(api_key='4e44257f0c7c4d51a8efb0c7a0361e1c')

load_dotenv()
# Функция обработки ошибок

API_GROUP_KEY = os.environ.get("API_GROUP_KEY")
API_USER_KEY = os.environ.get("API_USER_KEY")
API_SERVICE_KEY = os.environ.get("API_SERVICE_KEY")
client_secret = os.environ.get("client_secret")
vk_app_id = int(os.environ.get("vk_app_id"))
print("Бот запускается...")
group_id = '196288744'  # Указываем id сообщества
threads = list()
eventhr = []
kolpot = -1
group_sob = "@bratikbot"  # Указываем короткое имя бота (если нет то id)
group_name = "Братик"  # Указываем название сообщества
translator = Translator()

# Авторизация под именем сообщества
vk_session = vk_api.VkApi(token=API_GROUP_KEY)
longpoll = VkBotLongPoll(vk_session, group_id)
vk = vk_session.get_api()

# Авторизация под именем пользователя
vk_session_user = vk_api.VkApi(token=API_USER_KEY)
vk_polzovat = vk_session_user.get_api()

# Авторизация сервисным токеном
vk_session_SERVISE = vk_api.VkApi(app_id=vk_app_id, token=API_SERVICE_KEY, client_secret=client_secret)
vk_session_SERVISE.server_auth()
vk_SERVISE = vk_session_SERVISE.get_api()
vk_session_SERVISE.token = {'access_token': API_SERVICE_KEY, 'expires_in': 0}

global photo_loli, photo_neko, photo_arts, photo_hent, photo_aheg, photo_stik, photo_mart, video_coub, photo_bdsm, \
    photo_ur18, video_hent, video_tikt, photo_etti, video_tikt2, photo_gitl, oboiv_tele


# Отправка запросов на информацию об фотографиях и видео в группе
def zapros_ft_vd():
    global photo_loli, photo_neko, photo_arts, photo_hent, photo_aheg, photo_stik, photo_mart, video_coub, \
        photo_bdsm, photo_ur18, video_hent, video_tikt, photo_etti, video_tikt2, photo_gitl, oboiv_tele
    photo_loli = vk_SERVISE.photos.get(owner_id='-' + '196288744', album_id=271418270, count=1000)  # Тут находятся
    photo_neko = vk_SERVISE.photos.get(owner_id='-' + '196288744', album_id=271449419, count=1000)  # альбомы группы
    photo_arts = vk_SERVISE.photos.get(owner_id='-' + '196288744', album_id=271418213, count=1000)  # и их id
    photo_hent = vk_SERVISE.photos.get(owner_id='-' + '196288744', album_id=271418234, count=1000)  # по которым внизу
    photo_aheg = vk_SERVISE.photos.get(owner_id='-' + '196288744', album_id=271421874, count=1000)  # будут отбираться
    photo_stik = vk_SERVISE.photos.get(owner_id='-' + '196288744', album_id=271599613, count=1000)  # фото + 10 сек
    photo_mart = vk_SERVISE.photos.get(owner_id='-' + '196288744', album_id=271761499, count=1000)  # к запуску
    photo_bdsm = vk_SERVISE.photos.get(owner_id='-' + '196288744', album_id=272201504, count=1000)  #
    photo_ur18 = vk_SERVISE.photos.get(owner_id='-' + '196288744', album_id=272411793, count=1000)  #
    video_coub = vk_polzovat.video.get(owner_id='-' + '196288744', album_id=1, count=200)  #
    video_hent = vk_polzovat.video.get(owner_id='-' + '196288744', album_id=3, count=200)  #
    video_tikt = vk_polzovat.video.get(owner_id='-' + '196288744', album_id=4, count=200)  #
    video_tikt2 = vk_polzovat.video.get(owner_id='-' + '196288744', album_id=5, count=200)  #
    oboiv_tele = vk_polzovat.video.get(owner_id='-' + '196288744', album_id=6, count=200)  #
    photo_etti = vk_SERVISE.photos.get(owner_id='-' + '196288744', album_id=273079952, count=1000)  #
    photo_gitl = vk_SERVISE.photos.get(owner_id='-' + '196288744', album_id=273184565, count=1000)


print('Импортируем список онгоингов...')
AnimeOngoing = AnimeGoParser.AnimeGo('ongoing').random_anime()
print('Импортируем список всех аниме...')
AnimeFinish = AnimeGoParser.AnimeGo('finish').random_anime()
print('Импортируем фото из альбомов...')
zapros_ft_vd()

try:
    def listing_new_anime_series():
        while True:
            New_Anime = AnimeGoParser.AnimeGo('ongoing').ongoing_search_series()
            people = db_module.sql_fetch_from_all_id(db_module.con, 'anime_ongoings', '0')
            for anime in New_Anime:
                for k in range(len(people)):
                    if anime[0] in people[k][1].split(':|:'):
                        send_msg_new(people[k][0], 'Вышла новая серия аниме: ' + anime[0])
                        if not anime[1]:
                            anime = anime[0].replace("'", "")
                            anime_list_people = \
                            db_module.sql_fetch_from_money(db_module.con, 'anime_ongoings', people[k][0])[0][0]
                            animesh = ':|:' + anime
                            anime_list_people = anime_list_people.replace(animesh, '')
                            db_module.sql_update_from_money_text(db_module.con, 'anime_ongoings', anime_list_people,
                                                                 people[k][0])
                            send_msg_new(people[k][0], 'Это была последняя серия - удаляю аниме из вашего календаря:\n' + anime)
            time.sleep(60)

    def anime_ongoings_list(*args):
        peer_id = args[0]
        mess = '***Список онгоингов***:\n'
        for i in range(len(AnimeOngoing)):
            mess += str(i) + ') ' + AnimeOngoing[i][0] + '\n'
        send_msg_new(peer_id, mess + '\nЧтобы бот присылал вам информацию о новых сериях напишите "смотрю (номер '
                                     'онгоинга)", например: "смотрю 12", тоже самое чтобы отписаться от информирования')

    def anime_ongoing_pesonal_list(*args):
        peer_id = args[0]
        from_id = args[1]
        mess = '***Ваш календарь***\n'
        personal_anime = db_module.sql_fetch_from_money(db_module.con, 'anime_ongoings', from_id)[0][0].split(":|:")
        for i in range(len(personal_anime)):
            if i != 0:
                mess += str(i) + ') ' + personal_anime[i] + '\n'
        send_msg_new(peer_id, mess)

    def add_anime_ongoing_listing(*args):
        peer_id = args[0]
        from_id = args[1]
        if args[2][1].isdigit():
            if int(args[2][1]) < len(AnimeOngoing):
                anime = AnimeOngoing[int(args[2][1])][0].replace("'", "")
                anime_list_people = db_module.sql_fetch_from_money(db_module.con, 'anime_ongoings', from_id)[0][0]
                if anime not in anime_list_people.split(":|:"):
                    anime_list_people += ':|:' + anime
                    db_module.sql_update_from_money_text(db_module.con, 'anime_ongoings', anime_list_people, from_id)
                    send_msg_new(from_id, 'Аниме успешно добавлено в ваш календарь:\n' + anime)
                else:
                    animesh = ':|:' + anime
                    anime_list_people = anime_list_people.replace(animesh, '')
                    db_module.sql_update_from_money_text(db_module.con, 'anime_ongoings', anime_list_people, from_id)
                    send_msg_new(from_id, 'Аниме успешно удалено из вашего календаря:\n' + anime)
            else:
                send_msg_new(peer_id, 'Вы ввели неверный номер онгоинга')
        else:
            send_msg_new(peer_id, 'Вы ввели неверный номер онгоинга')

    def info_for_user(*args):
        event_func = args[4]
        vk_reg_data = vk_register_date(event_func.message.from_id)
        vk_reg_now = datetime.datetime.now()
        vk_reg_datas = datetime.datetime.strptime(vk_reg_data[0], "%Y-%m-%d")
        vk_reg_date_time = (vk_reg_now - vk_reg_datas).days
        vk_reg_years = int(vk_reg_date_time // 365.25)
        vk_reg_mount = int((vk_reg_date_time - vk_reg_years * 365.25) // 30.4167)
        vk_reg_days = int((vk_reg_date_time - vk_reg_years * 365.25 - vk_reg_mount * 30.4167) // 1)
        people = vk.users.get(user_ids=event_func.message.from_id,
                              fields=['photo_id', 'verified', 'sex', 'bdate', 'city', 'country', 'home_town',
                                      'has_photo',
                                      'photo_400_orig', 'photo_max', 'photo_max_orig', 'online', 'domain', 'has_mobile',
                                      'contacts', 'site', 'education', 'universities', 'schools', 'status', 'last_seen',
                                      'followers_count', 'occupation', 'nickname', 'relatives', 'relation', 'personal',
                                      'connections', 'exports', 'activities', 'interests', 'music', 'movies', 'tv',
                                      'books',
                                      'games', 'about', 'quotes', 'can_post', 'can_see_all_posts', 'can_see_audio',
                                      'can_write_private_message', 'can_send_friend_request', 'is_favorite',
                                      'is_hidden_from_feed', 'timezone', 'screen_name', 'maiden_name', 'crop_photo',
                                      'is_friend', 'friend_status', 'career', 'military', 'blacklisted',
                                      'blacklisted_by_me',
                                      'can_be_invited_group'])[0]
        first_name = people['first_name']
        last_name = people['last_name']
        pol = ''
        if str(people['sex']) == '1':
            pol = '\n&#128698;Пол: ' + 'женский'
        elif str(people['sex']) == '2':
            pol = '\n&#128697;Пол: ' + 'мужской'
        try:
            city = '\n&#127988;Город: ' + str(people['city']['title'])
        except KeyError:
            city = ''
        try:
            country = '\n&#127884;Страна: ' + str(people['country']['title'])
        except KeyError:
            country = ''
        try:
            photo_max = people['photo_max']
        except KeyError:
            photo_max = ''
        try:
            photo_id = people['photo_id']
        except KeyError:
            photo_id = '1'
        try:
            site = '\n&#127538;Сайт: ' + str(people['site'])
        except KeyError:
            site = ''
        try:
            status = '\n&#127545;Статус: ' + str(people['status'])
        except KeyError:
            status = ''
        try:
            verified = people['verified']
            if str(verified) == '0':
                verified = '\n&#10060;Верифицированная страница: ' + 'нет'
            elif str(verified) == '1':
                verified = '\n&#10004;Верифицированная страница: ' + 'да'
        except KeyError:
            verified = ''
        try:
            followers_count = '\n&#128106;Количество подписчиков: ' + str(people['followers_count'])
        except KeyError:
            followers_count = ''
        try:
            occupation_type = people['occupation']['type']
        except KeyError:
            occupation_type = 'Неизвестно'
        try:
            occupation_name = '\n&#128736;Место работы: ' + str(people['occupation']['name'])
        except KeyError:
            occupation_name = ''
        try:
            university_name = '\n&#128213;Университет: ' + str(people['university_name'])
        except KeyError:
            university_name = ''
        try:
            faculty_name = '\n&#128215;Факультет: ' + str(people['faculty_name'])
        except KeyError:
            faculty_name = ''
        try:
            personal_langs = '\n&#128483;Разговаривает на: ' + str(people['personal']['langs'])
        except KeyError:
            personal_langs = ''
        try:
            schools = ''
            for i in range(len(people['schools'])):
                schools = '\n&#128216;Школа: ' + str(people['schools'][i]['name'])
        except KeyError:
            schools = ''
        try:
            about = '\n&#8505;Обо мне: ' + str(people['about'])
        except KeyError:
            about = ''
        try:
            quotes = '\n&#127378;Девиз по жизни: ' + str(people['quotes'])
        except KeyError:
            quotes = ''

        experience = exp_count(event_func.message.from_id)
        level = 0
        level_porog = 0
        if experience < 100:
            level_porog = 100
            level = 1
        elif experience < 500:
            level_porog = 500
            level = 2
        elif experience < 1500:
            level_porog = 1500
            level = 3
        elif experience < 5000:
            level_porog = 5000
            level = 4
        elif experience < 10000:
            level_porog = 10000
            level = 5
        elif experience < 25000:
            level_porog = 25000
            level = 6
        elif experience < 75000:
            level_porog = 75000
            level = 7
        elif experience < 300000:
            level_porog = 300000
            level = 8
        elif experience < 1000000:
            level_porog = 1000000
            level = 9
        elif experience < 5000000:
            level_porog = 5000000
            level = 10
        elif experience >= 5000000:
            level_porog = 999999999
            level = 11

        level = str(level) + ' [' + str(experience) + '/' + str(level_porog) + ' EXP]'
        level_persent = round((experience / level_porog) * 10)
        level_line = '|'
        for persent in range(10):
            if level_persent > persent:
                level_line += '='
            elif level_persent == persent:
                level_line += '>'
            else:
                level_line += '-'
        level_line += '|'

        ms_g = '&#128221;' + str(first_name) + ' ' + str(last_name) + pol + country + city + site + status + verified + \
               followers_count + occupation_name + university_name + faculty_name + personal_langs + schools + \
               about + quotes + '\n&#8987;День регистрации: ' + str(vk_reg_data[0]) + '\n&#9203;Время регистрации: ' + \
               str(vk_reg_data[1]) + '\n&#128342;Времени со дня регистрации: ' + str(vk_reg_years) + ' лет ' + \
               str(vk_reg_mount) + ' месяц ' + str(vk_reg_days) + ' дней' + '\n&#128214;Уровень: ' + str(level) + ' ' + \
               str(level_line)

        vk.messages.send(peer_id=event_func.message.peer_id, random_id=0, message=ms_g,
                         attachment='photo' + str(photo_id))


    def vk_register_date(from_id):
        url = 'https://vk.com/foaf.php?id=' + str(from_id)
        response = requests.get(url).text.split()
        for i in range(len(response)):
            if response[i] == '<ya:created':
                reg_data = response[i + 1]
                for j in reg_data:
                    if j == '"':
                        reg_date, reg_time, reg_chas = '', '', ''
                        for k in range(10):
                            reg_date += reg_data[9 + k]
                        for k in range(8):
                            reg_time += reg_data[20 + k]
                        for k in range(6):
                            reg_chas += reg_data[28 + k]
                        return [reg_date, reg_time, reg_chas]
                return None
        return None


    def Davai_poboltaem(*args):
        event_func = args[4]
        import os
        import dialogflow
        send_msg_new(event_func.message.peer_id,
                     'Запущен режим общения с ботом, для того чтобы остановить болтавню бота напишите "стоп"')
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "google.json"
        project_id = "small-talk-xqju"
        session_id = str(random.randint(0, 1000000))
        language_code = "ru"
        session_client = dialogflow.SessionsClient()
        session = session_client.session_path(project_id, session_id)
        for event in longpoll.listen():  # Постоянный листинг сообщений
            if event.type == VkBotEventType.MESSAGE_NEW:  # Проверка на приход сообщения
                if event.message.peer_id == event_func.message.peer_id:
                    if event.message.text == 'стоп':
                        send_msg_new(event.message.peer_id, 'Всё! Больше не болтаем!')
                        break
                    else:
                        stop_msg = ''
                        stop_on = random.randint(0, 3)
                        if stop_on == 1:
                            stop_msg = '\n\nЧтобы остановить болтавню бота, напишите "стоп"'

                        text_input = dialogflow.types.TextInput(text=event.message.text, language_code=language_code)
                        query_input = dialogflow.types.QueryInput(text=text_input)
                        response_dialogflow = session_client.detect_intent(
                            session=session, query_input=query_input).query_result.fulfillment_text
                        # Если есть ответ от бота - присылаем юзеру, если нет - бот его не понял
                        if response_dialogflow:
                            vk.messages.send(peer_id=event.message.peer_id, random_id=0, message=response_dialogflow)
                        else:
                            vk.messages.send(peer_id=event.message.peer_id, random_id=0,
                                             message='Б-бака!!! Не хочу понимать тебя!' + stop_msg)


    # Инфа о человеке
    def people_info(people_id):
        if int(people_id) > 0:
            people = vk.users.get(user_ids=people_id)
            people = str(people[0]['first_name']) + ' ' + str(people[0]['last_name'])
            return people
        return 'НАЧАЛОСЬ ВОССТАНИЕ МАШИН'


    def add_exp(*args):
        m_count = int(db_module.sql_fetch_from_money(db_module.con, 'm_count', args[1])[0][0])
        m_count += 1
        db_module.sql_update_from_money_int(db_module.con, 'm_count', str(m_count), args[1])


    def exp_count(people_id):
        return db_module.sql_fetch_from_money(db_module.con, 'm_count', people_id)[0][0]


    def Film_popular(*args):
        film = KinoPoisk.get_random_popular()
        # Загрузка фото на комп
        p = requests.get(film[4])
        out = open("film.jpg", "wb")
        out.write(p.content)
        out.close()

        # Отправка фото в ВК:
        upload = vk_api.VkUpload(vk)
        photo = upload.photo_messages('film.jpg')
        owner_id = photo[0]['owner_id']
        photo_id = photo[0]['id']
        access_key = photo[0]['access_key']
        attachment = f'photo{owner_id}_{photo_id}_{access_key}'

        film_janr = ''
        for i in film[6]:
            film_janr += i + ', '

        vk.messages.send(peer_id=args[4].message.peer_id, random_id=0, attachment=attachment,
                         message='Название: ' + film[0] + '\nРейтинг: ' + str(film[5]) + '\nДата премьеры: ' +
                                 str(film[2]) + '\nЖанры: ' + film_janr + '\n\n' + 'Описание:\n' + film[1] +
                                 '\n\nСсылка на фильм: ' + film[7])


    def AnimeGo_Search(*args):
        text = args[4].message.text.split()
        del text[0]
        text_s = ''
        for i in text:
            text_s += i + ' '
        Anime_searched = AnimeGoParser.search(text_s)
        name = Anime_searched[0]
        pict = Anime_searched[1]
        url = Anime_searched[2]
        anime_type = Anime_searched[3]
        anime_year = Anime_searched[4]
        anime_reit = Anime_searched[5]
        # Загрузка фото на комп
        p = requests.get(pict)
        out = open("temp.jpg", "wb")
        out.write(p.content)
        out.close()

        # Отправка фото в ВК:
        upload = vk_api.VkUpload(vk)
        photo = upload.photo_messages('temp.jpg')
        owner_id = photo[0]['owner_id']
        photo_id = photo[0]['id']
        access_key = photo[0]['access_key']
        attachment = f'photo{owner_id}_{photo_id}_{access_key}'
        vk.messages.send(peer_id=args[4].message.peer_id, random_id=0, attachment=attachment,
                         message='Название: ' + name + '\nРейтинг: ' + anime_reit + '⭐\nКоличество серий: ' +
                                 AnimeGoParser.series(url) + '\nТип аниме: ' + anime_type +
                                 '\nГод показа: ' + anime_year + '\nСсылка на аниме: ' + url)
        anime_keyboard(args[4].message.peer_id)


    def anime_keyboard(my_peer):
        settings = dict(one_time=False, inline=True)
        keyboard_nabor = VkKeyboard(**settings)
        keyboard_nabor.add_button(label='посоветуй аниме', color=VkKeyboardColor.POSITIVE)
        keyboard_nabor.add_button(label='посоветуй онгоинг', color=VkKeyboardColor.POSITIVE)
        vk.messages.send(
            random_id=get_random_id(),
            peer_id=my_peer,
            keyboard=keyboard_nabor.get_keyboard(),
            message='Так же я могу:')


    # Вывод случайного аниме
    def AnimeGo_Finish(*args):
        id_anime = random.randint(0, len(AnimeFinish) - 1)
        name = AnimeFinish[id_anime][0]
        pict = AnimeFinish[id_anime][1]
        url = AnimeFinish[id_anime][2]
        dics = AnimeFinish[id_anime][3]
        anime_type = AnimeFinish[id_anime][4]
        anime_year = AnimeFinish[id_anime][5]
        anime_janrs = AnimeFinish[id_anime][6]
        anime_janr = ''
        for i in anime_janrs:
            anime_janr += i + ', '
        anime_reit = AnimeFinish[id_anime][7]

        # Загрузка фото на комп
        p = requests.get(pict)
        out = open("temp.jpg", "wb")
        out.write(p.content)
        out.close()

        # Отправка фото в ВК:
        upload = vk_api.VkUpload(vk)
        photo = upload.photo_messages('temp.jpg')
        owner_id = photo[0]['owner_id']
        photo_id = photo[0]['id']
        access_key = photo[0]['access_key']
        attachment = f'photo{owner_id}_{photo_id}_{access_key}'

        vk.messages.send(peer_id=args[4].message.peer_id, random_id=0, attachment=attachment,
                         message='Название: ' + name + '\nРейтинг: ' + anime_reit + '⭐\nКоличество серий: ' +
                                 AnimeGoParser.series(url) + '\nТип аниме: ' + anime_type +
                                 '\nГод показа: ' + anime_year +
                                 '\nЖанр: ' + anime_janr + '\n\n' + dics + '\n\nСсылка на аниме: ' + url)
        anime_keyboard(args[4].message.peer_id)


    # Вывод случайного онгоинга
    def AnimeGo_Ongoings(*args):
        id_anime = random.randint(0, len(AnimeOngoing) - 1)
        pict = AnimeOngoing[id_anime][1]
        name = AnimeOngoing[id_anime][0]
        dics = AnimeOngoing[id_anime][3]
        url = AnimeOngoing[id_anime][2]
        anime_type = AnimeOngoing[id_anime][4]
        anime_year = AnimeOngoing[id_anime][5]
        anime_janrs = AnimeOngoing[id_anime][6]
        anime_janr = ''
        for i in anime_janrs:
            anime_janr += i + ', '
        anime_reit = AnimeFinish[id_anime][7]

        # Загрузка фото на комп
        p = requests.get(pict)
        out = open("temp.jpg", "wb")
        out.write(p.content)
        out.close()

        # Отправка фото в ВК:
        upload = vk_api.VkUpload(vk)
        photo = upload.photo_messages('temp.jpg')
        owner_id = photo[0]['owner_id']
        photo_id = photo[0]['id']
        access_key = photo[0]['access_key']
        attachment = f'photo{owner_id}_{photo_id}_{access_key}'

        vk.messages.send(peer_id=args[4].message.peer_id, random_id=0, attachment=attachment,
                         message='Название: ' + name + '\nРейтинг: ' + anime_reit + '⭐\nКоличество серий: ' +
                                 AnimeGoParser.series(url) + '\nТип аниме: ' + anime_type +
                                 '\nГод показа: ' + anime_year +
                                 '\nЖанр: ' + anime_janr + '\n\n' + dics + '\n\nСсылка на аниме: ' + url)
        anime_keyboard(args[4].message.peer_id)


    # Переводчик
    def translate(text, lang):
        try:
            result = translator.translate(str(text), dest=lang).text
            return result
        except Exception as error:
            print(error)


    # Отправка в чат id беседы относительно бота
    def dialog_id(*args):
        event = args[4]
        send_msg_new(event.message.peer_id, 'ID этой беседы относительно меня: ' + str(event.message.peer_id))


    # Информация о коронавирусе
    def covid(*args):
        event = args[4]
        words = event.message.text.lower().split()
        if len(words) > 1:
            if words[1] == 'америка':
                country = 'USA'
            else:
                country = translate(words[1], 'en')
        else:
            country = 'Russia'
        url = "https://covid-193.p.rapidapi.com/statistics"

        headers = {
            'x-rapidapi-host': "covid-193.p.rapidapi.com",
            'x-rapidapi-key': "5a42fd676cmsh120861aa5715a2cp16f89ejsn6269c9e5abc8"
        }

        response = requests.request("GET", url, headers=headers)
        data = response.json()['response']
        a = False
        for i in range(len(data)):
            if data[i]['country'] == country:
                send_msg_new(event.message.peer_id, '&#9763;' + translate(str(data[i]['country']), 'ru') +
                             ' - информация по коронавирусу на ' +
                             data[i]['day'] + '&#9763;' +
                             '\n&#128106;Население страны: ' + str(data[i]['population']) +
                             '\n\n&#128554;Заболевших сегодня: ' + str(data[i]['cases']['new']) +
                             '\n&#128567;Болеющих данный момент: ' + str(data[i]['cases']['active']) +
                             '\n&#128583;Выздоровело: ' + str(data[i]['cases']['recovered']) +
                             '\n\n&#128565;Умерло: ' +
                             '\n&#128534;-сегодня: ' + str(data[i]['deaths']['new']) +
                             '\n&#128555;-всего: ' + str(data[i]['deaths']['total']) +
                             '\n\n&#9762;Всего: ' + str(data[i]['cases']['total']) + '&#9762;' +
                             '\n\nДля получения информации о конкретной стране, напишите "коронавирус (страна)"' +
                             '\nАктуальные данные предоставлены сайтом https://rapidapi.com/')
                a = True
        if not a:
            send_msg_new(event.message.peer_id, 'Извините, но информация о ситуации в данной стране мне неизвестна')


    # Курс евро и доллара
    def curs_value(*args):
        peer_id = args[0]
        link = "https://www.cbr-xml-daily.ru/daily_json.js"
        data = requests.get(link)
        USD = round(data.json()['Valute']["USD"]["Previous"] / data.json()['Valute']["USD"]["Nominal"], 2)
        EUR = round(data.json()['Valute']["EUR"]["Previous"] / data.json()['Valute']["EUR"]["Nominal"], 2)
        JPY = round(data.json()['Valute']["JPY"]["Previous"] / data.json()['Valute']["JPY"]["Nominal"], 2)
        forex = 'Курс валюты на утро ' + str(datetime.datetime.now().date()) + '\n\n' + \
                '&#128181; 1 USD = ' + str(USD) + ' Российских рублей\n' + \
                '&#128182; 1 EUR = ' + str(EUR) + ' Российский рублей\n' + \
                '&#128180; 1 JPY = ' + str(JPY) + ' Российский рублей'
        send_msg_new(peer_id, forex)


    # Погода
    def weather(*args):
        event_func = args[4]
        stop = False
        s_city = ''
        if len(event_func.message.text.split()) > 1:
            s_city = event_func.message.text.split()[1]
        else:
            send_msg_new(event_func.message.peer_id, '&#9925;Для получения информации о погоде напишите'
                                                     ' "погода (город)"&#127777;')
            stop = True
        if not stop:
            appid = 'a8051039c6443539398bac146ab24206'
            city_id = 0
            try:
                res = requests.get("http://api.openweathermap.org/data/2.5/find",
                                   params={'q': s_city, 'type': 'like', 'units': 'metric', 'APPID': appid})
                data = res.json()
                city_id = data['list'][0]['id']
            except Exception as error:
                print("Exception (find):", error)
                pass
            try:
                res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                                   params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
                data = res.json()
                Osadki = data['weather'][0]['description']
                Temp = data['main']['temp']
                Temp_fel = data['main']['feels_like']
                Wind_speed = data['wind']['speed']
                Wind_deg = data['wind']['deg']
                sunrise = time.ctime(data['sys']['sunrise'] + 10800).split()[3]  # Восход
                sunset = time.ctime(data['sys']['sunset'] + 10800).split()[3]  # Закат
                if 0 <= Wind_deg <= 22:
                    Wind_deg = 'северный'
                elif 23 <= Wind_deg <= 66:
                    Wind_deg = 'северо-восточный'
                elif 67 <= Wind_deg <= 112:
                    Wind_deg = 'восточный'
                elif 113 <= Wind_deg <= 158:
                    Wind_deg = 'юго-восточный'
                elif 159 <= Wind_deg <= 203:
                    Wind_deg = 'южный'
                elif 204 <= Wind_deg <= 248:
                    Wind_deg = 'юго-западный'
                elif 249 <= Wind_deg <= 293:
                    Wind_deg = 'западный'
                elif 294 <= Wind_deg <= 338:
                    Wind_deg = 'северо-западный'
                elif 339 <= Wind_deg <= 360:
                    Wind_deg = 'северный'
                send_msg_new(event_func.message.peer_id, '&#127961;Погода в ' + str(data['name']) + '\n' +
                             '&#9925;Осадки: ' + str(Osadki) + '\n&#127777;Температура: ' + str(Temp) + '°C\n' +
                             '&#128583;ощущается как: ' + str(Temp_fel) + '°C\n&#127788;ветер: ' + Wind_deg + ' ' +
                             str(Wind_speed) + ' м/с' + '\n&#127749;рассвет: ' + str(
                    sunrise) + '\n&#127748;закат: ' + str(
                    sunset))
            except Exception as error:
                print("Exception (weather):", error)
                send_msg_new(event_func.message.peer_id, 'Извините, но я не знаю о таком месте...')
                pass


    # Создание клана
    def clan_create(*args):
        my_peer = args[0]
        my_from = args[1]
        clan_name = args[4].message.text.split()[2]
        clan_name = clan_name.replace("'", "&#039;")
        if len(clan_name) >= 3:
            cln_name = str(db_module.sql_fetch_from_money(db_module.con, 'clan_name', my_from)[0][0])
            if (cln_name == 'NULL') or (cln_name is None) or (cln_name == 'None'):
                if db_module.sql_fetch_clan_info(db_module.con, 'clan_name', clan_name) == 'NULL':
                    if int(db_module.sql_fetch_from_money(db_module.con, 'money', my_from)[0][0]) >= 5000:
                        db_module.sql_update_from_money_text(db_module.con, 'clan_name', clan_name, str(my_from))
                        db_module.sql_update_from_money_int(db_module.con, 'clan_rank', '5', str(my_from))
                        add_balans(my_from, '-5000')
                        entities = str(clan_name), '0', str(my_from)
                        db_module.sql_insert_clan_info(db_module.con, entities)
                        db_module.sql_update_clan_info(db_module.con, 'clan_admin', my_from, clan_name)
                        send_msg_new(my_peer, 'Клан ' + clan_name + ' успешно создан!')
                    else:
                        send_msg_new(my_peer, people_info(my_from) + ', у вас недостаточно монет!')
                else:
                    send_msg_new(my_peer, people_info(my_from) + ', клан с таким названием уже существует!')
            else:
                send_msg_new(my_peer, people_info(my_from) + ', вы уже состоите в клане!')
        else:
            send_msg_new(my_peer, 'Для создания клана напишите "Клан создать "название_клана""\n'
                                  'Стоимость создания клана - 5000 монет')


    # Проверка на число
    def chislo_li_eto(chto):  # Определяет, является ли данный аргумент числом или нет
        a = ''
        odna_tochka = 0
        for i in str(chto):
            if '0' <= str(i) <= '9':
                a += str(i)
            elif str(i) == '-':
                a += str('-')
            elif str(i) == '.':
                if not odna_tochka:
                    a += str('.')
                    odna_tochka = 1
                else:
                    return False
            else:
                return False
        if a == '':
            return False
        else:
            return True


    # Снятие денег с баланса клана rank 4+
    def clan_rem_balance(*args):
        if len(args[2]) > 2:
            my_peer = args[0]
            my_from = args[1]
            money = args[2][2]
            clan_name = db_module.sql_fetch_from_money(db_module.con, 'clan_name', my_from)[0][0]
            if clan_name != 'NULL' and clan_name is not None:
                if int(db_module.sql_fetch_from_money(db_module.con, 'clan_rank', str(my_from))[0][0]) >= 4:
                    if chislo_li_eto(money):
                        clan_bals = db_module.sql_fetch_clan_info(db_module.con, 'clan_money', clan_name)[0]
                        if int(clan_bals) >= int(money):
                            clan_add_balance(my_peer, my_from, ['', '', int(-int(money))])
                            send_msg_new(my_peer, people_info(my_from) + ' вывел из казны клана ' + money + ' монет')
                        else:
                            send_msg_new(my_peer, people_info(my_from) + ', в казне недостаточно монет!')
                    else:
                        send_msg_new(my_peer, people_info(my_from) + ', введите правильное число!')
                else:
                    send_msg_new(my_peer, people_info(my_from) + ', вы не обладаете достаточными привелегиями для '
                                                                 'выполнения данной команды!')
            else:
                send_msg_new(my_peer, people_info(my_from) + ', вы не состоите в клане!')


    # Пополнение баланса клана
    def clan_add_balance(*args):
        if len(args[2]) > 2:
            my_peer = args[0]
            my_from = args[1]
            money = args[2][2]
            clan_name = db_module.sql_fetch_from_money(db_module.con, 'clan_name', my_from)[0][0]
            if clan_name != 'NULL' and clan_name is not None:
                if chislo_li_eto(money):
                    if int(db_module.sql_fetch_from_money(db_module.con, 'money', my_from)[0][0]) >= int(money):
                        money_clan = int(db_module.sql_fetch_clan_info(db_module.con, 'clan_money', clan_name)[0]) + \
                                     int(money)
                        db_module.sql_update_clan_info(db_module.con, 'clan_money', money_clan, clan_name)
                        add_balans(my_from, int(-int(money)))
                        if int(money) > 0:
                            send_msg_new(my_peer, 'Казна клана ' + clan_name + ' пополнена на ' + str(money) + ' монет')
                    else:
                        send_msg_new(my_peer, people_info(my_from) + ', у вас недостаточно монет!')
                else:
                    send_msg_new(my_peer, people_info(my_from) + ', введите правильное число!')
            else:
                send_msg_new(my_peer, people_info(my_from) + ', вы не состоите в клане!')


    # Баланс клана rank 1+
    def clan_balance(*args):
        my_peer = args[0]
        if len(args[2]) == 2:  # Если длина сообщения 2 слова \клан инфо\
            if args[3] == '':  # Если имя упомянутого пустое (не упоминали)
                my_from = args[1]  # Присвоить имя отправителя
            else:
                my_from = args[3]  # Присвоить имя упомянутого
        else:
            id2 = args[2][2]  # Присвоить имя кого-то
            my_from = ''
            for i in id2:
                if '0' <= i <= '9':
                    my_from += i
                if i == '|':
                    break
        if my_from != '':
            clan_name = db_module.sql_fetch_from_money(db_module.con, 'clan_name', my_from)[0][0]
            if clan_name != 'NULL' and clan_name is not None:
                if int(db_module.sql_fetch_from_money(db_module.con, 'clan_rank', str(my_from))[0][0]) >= 1:
                    money = db_module.sql_fetch_clan_info(db_module.con, 'clan_money', clan_name)[0]
                    send_msg_new(my_peer, 'В казне клана ' + str(clan_name) + ' ' + str(money) + ' монет')
                else:
                    send_msg_new(my_peer, people_info(my_from) + ', вы не обладаете достаточными привелегиями для '
                                                                 'выполнения данной команды!')
            else:
                send_msg_new(my_peer, people_info(my_from) + ', вы не состоите в клане!')


    # Инфо о клане
    def clan_info(*args):
        my_peer = args[0]
        if len(args[2]) == 2:  # Если длина сообщения 2 слова \клан инфо\
            if args[3] == '':  # Если имя упомянутого пустое (не упоминали)
                my_from = args[1]  # Присвоить имя отправителя
            else:
                my_from = args[3]  # Присвоить имя упомянутого
        else:
            id2 = args[2][2]  # Присвоить имя кого-то
            my_from = ''
            for i in id2:
                if '0' <= i <= '9':
                    my_from += i
                if i == '|':
                    break
        if my_from != '' and int(my_from) > 0:
            clan_name = db_module.sql_fetch_from_money(db_module.con, 'clan_name', my_from)[0][0]
            if clan_name != 'NULL' and clan_name is not None:
                first_all = (db_module.sql_fetch_from_money_clan(db_module.con, 'first_name', str(clan_name)))
                last_all = (db_module.sql_fetch_from_money_clan(db_module.con, 'last_name', str(clan_name)))
                rank_all = (db_module.sql_fetch_from_money_clan(db_module.con, 'clan_rank', str(clan_name)))
                mess = ''
                people = []
                for i in range(len(rank_all)):
                    people.append([first_all[i][0], last_all[i][0], rank_all[i][0]])
                people = sorted(people, key=lambda peoples: (-peoples[2]))
                for i in range(len(people)):
                    if int(people[i][2]) == 5:
                        mess += '⭐⭐⭐⭐⭐'
                    elif int(people[i][2]) == 4:
                        mess += '⭐⭐⭐⭐'
                    elif int(people[i][2]) == 3:
                        mess += '⭐⭐⭐'
                    elif int(people[i][2]) == 2:
                        mess += '⭐⭐'
                    elif int(people[i][2]) == 1:
                        mess += '⭐'
                    else:
                        mess += 'Холоп-'
                    mess += str(people[i][0]) + ' ' + str(people[i][1]) + '\n'
                send_msg_new(my_peer, people_info(my_from) + ' состоит в клане ' + clan_name + '\n\n' + mess)
            else:
                send_msg_new(my_peer, people_info(my_from) + ' не состоит в клане!')


    # Баланс клана топ
    def clan_balance_top(*args):
        my_peer = args[0]
        idall = db_module.sql_fetch_clan_all(db_module.con, 'clan_name')
        monall = db_module.sql_fetch_clan_all(db_module.con, 'clan_money')
        mess = ''
        clan = []
        for i in range(len(idall)):
            a = ''
            b = ''
            for j in (idall[i]):
                a += str(j)
            for k in (monall[i]):
                if '0' <= str(k) <= '9':
                    b += str(k)
            if chislo_li_eto(b):
                clan.append([str(a), int(b)])
        clan = sorted(clan, key=lambda peoples: (-peoples[1]))
        for i in range(len(clan)):
            if int(clan[i][1]) > 0 and i <= 30:
                if i == 0:
                    mess += '&#128142;'
                elif i == 1:
                    mess += '&#128176;'
                elif i == 2:
                    mess += '&#128179;'
                else:
                    mess += '&#128182;'
                mess += str(i + 1) + '. ' + clan[i][0] + ' - ' + str(clan[i][1]) + ' монет\n'
        send_msg_new(my_peer, mess)


    # rank 2+
    def clan_kick(*args):
        my_peer = args[0]
        my_from = args[1]
        if len(args[2]) == 2:
            our_from = args[3]
        else:
            id2 = args[2][2]
            our_from = ''
            for i in id2:
                if '0' <= i <= '9':
                    our_from += i
                if i == '|':
                    break
        clan_name = db_module.sql_fetch_from_money(db_module.con, 'clan_name', my_from)[0][0]
        if clan_name != 'NULL' and clan_name is not None:
            if db_module.sql_fetch_from_money(db_module.con, 'clan_name', our_from)[0][0] == clan_name:
                if int(db_module.sql_fetch_from_money(db_module.con, 'clan_rank', str(my_from))[0][0]) > \
                        int(db_module.sql_fetch_from_money(db_module.con, 'clan_rank', str(our_from))[0][0]) >= 2:
                    db_module.sql_update_from_money_text(db_module.con, 'clan_name', 'NULL', our_from)
                    db_module.sql_update_from_money_int(db_module.con, 'clan_rank', '0', our_from)
                    send_msg_new(my_peer, people_info(our_from) + ' исключен из клана!')
                else:
                    send_msg_new(my_peer, people_info(my_from) + ', вы не обладаете достаточными привелегиями для '
                                                                 'выполнения данной команды!')
            else:
                send_msg_new(my_peer, people_info(my_from) + ', данный человек не состоит в вашем клане!')
        else:
            send_msg_new(my_peer, people_info(my_from) + ', вы не состоите в клане!')


    # rank 5
    def clan_disvorse(*args):
        my_peer = args[0]
        my_from = args[1]
        clan_name = db_module.sql_fetch_from_money(db_module.con, 'clan_name', my_from)[0][0]
        if clan_name != 'NULL' and clan_name is not None:
            if int(db_module.sql_fetch_from_money(db_module.con, 'clan_rank', str(my_from))[0][0]) == 5:
                clan_members = db_module.sql_fetch_from_money_clan(db_module.con, 'from_id', clan_name)
                db_module.sql_delite_clan_info(db_module.con, clan_name)
                for i in clan_members:
                    db_module.sql_update_from_money_text(db_module.con, 'clan_name', 'NULL', i[0])
                    db_module.sql_update_from_money_int(db_module.con, 'clan_rank', '0', i[0])
                send_msg_new(my_peer, 'Клан ' + clan_name + ' распался')
            else:
                send_msg_new(my_peer, people_info(my_from) + ', вы не являетесь администратором клана!')
        else:
            send_msg_new(my_peer, people_info(my_from) + ', вы не состоите в клане!')


    # Покинуть клан
    def clan_leave(*args):
        my_peer = args[0]
        my_from = args[1]
        clan_name = db_module.sql_fetch_from_money(db_module.con, 'clan_name', my_from)[0][0]
        if clan_name != 'NULL' and clan_name is not None:
            clan_adm = db_module.sql_fetch_clan_info(db_module.con, 'clan_admin', clan_name)
            if str(clan_adm[0]) == str(my_from):
                send_msg_new(my_peer, people_info(my_from) + ', вы не можете покинуть клан, так как являетесь главой')
            else:
                db_module.sql_update_from_money_text(db_module.con, 'clan_name', 'NULL', my_from)
                db_module.sql_update_from_money_int(db_module.con, 'clan_rank', '0', my_from)
                send_msg_new(my_peer, people_info(my_from) + ', вы покинули клан ' + clan_name)
        else:
            send_msg_new(my_peer, people_info(my_from) + ', вы не состоите в клане!')


    # rank 2+
    def clan_invite(*args):
        my_peer = args[0]
        my_from = args[1]
        if len(args[2]) == 2:
            our_from = args[3]
        else:
            id2 = args[2][2]
            our_from = ''
            for i in id2:
                if '0' <= i <= '9':
                    our_from += i
                if i == '|':
                    break
        clan_name_my = db_module.sql_fetch_from_money(db_module.con, 'clan_name', my_from)[0][0]
        if our_from != '' and int(our_from) > 0:
            clan_name_our = db_module.sql_fetch_from_money(db_module.con, 'clan_name', our_from)[0][0]
            if clan_name_my != 'NULL' and clan_name_my != 'None':
                a = (db_module.sql_fetch_from_money(db_module.con, 'clan_rank', str(my_from))[0][0])
                if int(a) >= 2:
                    if my_from != our_from:
                        if clan_name_our == 'NULL' or clan_name_our is None:
                            timing = time.time()
                            keyboard = VkKeyboard(inline=True)
                            keyboard.add_button('да', color=VkKeyboardColor.PRIMARY)
                            keyboard.add_button('нет', color=VkKeyboardColor.NEGATIVE)
                            vk.messages.send(peer_id=my_peer, random_id=get_random_id(),
                                             keyboard=keyboard.get_keyboard(),
                                             message=people_info(our_from) +
                                                     ', вы были приглашены в клан ' + clan_name_my +
                                                     '\nВступить в клан?\nПриглашение действует в течении 60 секунд')
                            for eventhr[kolpot] in longpoll.listen():
                                if time.time() - timing > 60.0:
                                    send_msg_new(my_peer, 'Срок действия приглашения истек...')
                                    break
                                if eventhr[kolpot].type == VkBotEventType.MESSAGE_NEW:
                                    if str(eventhr[kolpot].message.peer_id) == str(my_peer) and str(
                                            eventhr[kolpot].message.from_id) == str(our_from):
                                        slova_m = eventhr[kolpot].message.text.split()
                                        if len(slova_m) == 2:
                                            if slova_m[1] == "да":
                                                db_module.sql_update_from_money_text(db_module.con, 'clan_name',
                                                                                     clan_name_my, our_from)
                                                db_module.sql_update_from_money_int(db_module.con, 'clan_rank', '1',
                                                                                    our_from)
                                                send_msg_new(my_peer, people_info(our_from) + ', вы вступили в клан ' +
                                                             clan_name_my)
                                                break
                                            elif slova_m[1] == "нет":
                                                send_msg_new(my_peer, 'Увы, но ' + people_info(our_from) +
                                                             ' не желает вступать в клан')
                                                break
                        else:
                            send_msg_new(my_peer, people_info(our_from) + ' уже состоит в клане ' + clan_name_our)
                    else:
                        send_msg_new(my_peer, people_info(my_from) + ', вы не можете пригласить в клан самого себя!')
                else:
                    send_msg_new(my_peer, people_info(my_from) + ', вы не обладаете достаточными привелегиями для '
                                                                 'выполнения данной команды!')
            else:
                send_msg_new(my_peer, people_info(my_from) + ', вы не состоите в клане!')


    def clan_up_down(*args):
        my_peer = args[0]
        my_from = args[1]
        if len(args[2]) == 2:
            our_from = args[3]
        else:
            id2 = args[2][2]
            our_from = ''
            for i in id2:
                if '0' <= i <= '9':
                    our_from += i
                if i == '|':
                    break
        up_or_down = args[2][1]
        if up_or_down == 'повысить':
            up_or_down = True
        else:
            up_or_down = False
        clan_name = db_module.sql_fetch_from_money(db_module.con, 'clan_name', my_from)[0][0]
        if clan_name != 'NULL' and clan_name is not None:
            if db_module.sql_fetch_from_money(db_module.con, 'clan_name', our_from)[0][0] == clan_name:
                my_rank = int(db_module.sql_fetch_from_money(db_module.con, 'clan_rank', str(my_from))[0][0])
                our_rank = int(db_module.sql_fetch_from_money(db_module.con, 'clan_rank', str(our_from))[0][0])
                if my_rank > our_rank:
                    if my_rank >= 3:
                        if up_or_down:
                            db_module.sql_update_from_money_int(db_module.con, 'clan_rank', str(our_rank + 1), our_from)
                            send_msg_new(my_peer, people_info(my_from) + ' повысил ранг ' + people_info(our_from) + '!')
                        else:
                            if our_rank > 0:
                                db_module.sql_update_from_money_int(db_module.con, 'clan_rank', str(our_rank - 1),
                                                                    our_from)
                                send_msg_new(my_peer,
                                             people_info(my_from) + ' понизил ранг ' + people_info(our_from) + '!')
                            else:
                                send_msg_new(my_peer, 'У ' + people_info(our_from) + ' нисший ранг!')
                    else:
                        send_msg_new(my_peer, people_info(my_from) + ', вы не обладаете достаточными привелегиями для '
                                                                     'выполнения данной команды!\n'
                                                                     'У вас должен быть минимум 3-ий ранг')
                else:
                    send_msg_new(my_peer, people_info(my_from) + ', вы не обладаете достаточными привелегиями для '
                                                                 'выполнения данной команды!\n'
                                                                 'Вы не можете присвоить кому-либо ранг своего '
                                                                 'уровня или выше')
            else:
                send_msg_new(my_peer, people_info(my_from) + ', данный человек не состоит в вашем клане!')
        else:
            send_msg_new(my_peer, people_info(my_from) + ', вы не состоите в клане!')


    # Статус брака
    def marry_status(*args):
        my_peer = args[0]
        if len(args[2]) == 2:  # Если длина сообщения 2 слова \клан инфо\
            if args[3] == '':  # Если имя упомянутого пустое (не упоминали)
                my_from = args[1]  # Присвоить имя отправителя
            else:
                my_from = args[3]  # Присвоить имя упомянутого
        else:
            id2 = args[2][2]  # Присвоить имя кого-то
            my_from = ''
            for i in id2:
                if '0' <= i <= '9':
                    my_from += i
                if i == '|':
                    break
        if my_from != '' and int(my_from) > 0:
            marry_id = str(db_module.sql_fetch_from(db_module.con, 'marry_id', my_peer, my_from)[0][0])
            if marry_id == 'None' or marry_id == '0':
                send_msg_new(my_peer, people_info(my_from) + ' не состоит в браке')
            else:
                send_msg_new(my_peer, people_info(my_from) + ' состоит в браке с ' + people_info(marry_id))


    # Развод
    def marry_disvorse(*args):
        my_peer = args[0]
        my_from = args[1]
        marry_id = str(db_module.sql_fetch_from(db_module.con, 'marry_id', my_peer, my_from)[0][0])
        if str(marry_id) == 'None' or str(marry_id) == '0':
            send_msg_new(my_peer, 'Вы не состоите в браке!')
        else:
            db_module.sql_update_from(db_module.con, 'marry_id', str('0'), str(my_peer), str(my_from))
            db_module.sql_update_from(db_module.con, 'marry_id', str('0'), str(my_peer), str(marry_id))
            send_msg_new(my_peer, people_info(my_from) + ' разводится с ' + people_info(marry_id))


    # Создание брака
    def marry_create(*args):
        my_peer = args[0]
        my_from = args[1]
        if len(args[2]) == 1:
            our_from = args[3]
        else:
            id2 = args[2][1]
            our_from = ''
            for i in id2:
                if '0' <= i <= '9':
                    our_from += i
                if i == '|':
                    break
        if str(my_from) == str(our_from) or our_from < 0:
            send_msg_new(my_peer, 'Ты чо? Дебил? Одиночество? Да? Иди лучше подрочи...')
        else:
            marry_id = str(db_module.sql_fetch_from(db_module.con, 'marry_id', my_peer, my_from)[0][0])
            marry_id2 = str(db_module.sql_fetch_from(db_module.con, 'marry_id', my_peer, our_from)[0][0])
            if (marry_id == 'None' or marry_id == '0') and (marry_id2 == 'None' or marry_id2 == '0'):
                chel = people_info(my_from)
                chel2 = people_info(our_from)
                timing = time.time()
                keyboard = VkKeyboard(inline=True)
                keyboard.add_button('💝да', color=VkKeyboardColor.PRIMARY)
                keyboard.add_button('💔нет', color=VkKeyboardColor.NEGATIVE)
                vk.messages.send(peer_id=my_peer, random_id=get_random_id(),
                                 keyboard=keyboard.get_keyboard(), message='💍' + chel2 +
                                                                           ', готов ли ты выйти за ' +
                                                                           chel + ' ?')
                for eventhr[kolpot] in longpoll.listen():
                    if time.time() - timing > 60.0:
                        send_msg_new(my_peer, 'Время заключения брака истекло...')
                        break
                    if eventhr[kolpot].type == VkBotEventType.MESSAGE_NEW:
                        if str(eventhr[kolpot].message.peer_id) == str(my_peer) and str(
                                eventhr[kolpot].message.from_id) == str(our_from):
                            slova_m = eventhr[kolpot].message.text.split()
                            if len(slova_m) == 2:
                                if slova_m[1] == "💝да":
                                    db_module.sql_update_from(db_module.con, 'marry_id', str(our_from), str(my_peer),
                                                              str(my_from))
                                    db_module.sql_update_from(db_module.con, 'marry_id', str(my_from), str(my_peer),
                                                              str(our_from))
                                    send_msg_new(my_peer, 'Брак успешно заключен!')
                                    break
                                elif slova_m[1] == "💔нет":
                                    send_msg_new(my_peer, 'Увы, но брак не будет заключен')
                                    break
            else:
                send_msg_new(my_peer, 'Один из вас уже находится в браке!')


    def balans_status(*args):
        my_peer = args[0]
        my_from = args[1]
        balans = str(db_module.sql_fetch_from_money(db_module.con, 'money', my_from)[0][0])
        send_msg_new(my_peer, people_info(my_from) + ', ваш баланс : ' + str(balans) + ' бро-коинов')


    # Баланс топ
    def balans_top(*args):
        my_peer = args[0]
        people = (db_module.sql_fetch_from_all(db_module.con, '*', str(my_peer)))
        people = sorted(people, key=lambda peoples: (-peoples[1]))
        mess = ''
        col = 0
        for i in range(len(people)):
            if col < 15:
                if i == 0:
                    mess += '&#128142;'
                elif i == 1:
                    mess += '&#128176;'
                elif i == 2:
                    mess += '&#128179;'
                else:
                    mess += '&#128182;'
                col += 1
                mess += str(i + 1) + '. ' + str(people[i][4]) + ' ' + str(people[i][5]) + ' - ' + \
                        str(people[i][1]) + ' монет\n'
        send_msg_new(my_peer, mess)


    # Отправка денег от одного участника к другому
    def money_send(*args):
        try:
            my_peer = args[0]
            my_from = args[1]
            if len(args[2]) == 2:
                our_from = args[3]
                money = args[2][1]
            else:
                id2 = args[2][1]
                money = args[2][2]
                our_from = ''
                for i in id2:
                    if '0' <= i <= '9':
                        our_from += i
                    if i == '|':
                        break
            if our_from != '':
                if int(our_from) > 0:
                    if int(str(db_module.sql_fetch_from_money(db_module.con, 'money',
                                                              str(my_from))[0][0])) >= int(money) > 0:
                        add_balans(str(my_from), '-' + str(money))
                        add_balans(str(our_from), str(money))
                        send_msg_new(my_peer, people_info(my_from) + ' перевел ' +
                                     people_info(our_from) + ' ' + str(money) + ' монет')
                    else:
                        send_msg_new(my_peer, people_info(my_from) + ', у вас недостаточно монет!')
            else:
                send_msg_new(my_peer, 'Мне кажется, или ты что-то напутал?!')
        except ValueError:
            send_msg_new(args[0], 'Мне кажется, или ты что-то напутал?!')


    # Зачисление ежедневного вознаграждения
    def add_balans_every_day(*args):
        my_peer = args[0]
        my_from = args[1]
        balans_time = int(db_module.sql_fetch_from_money(db_module.con, 'm_time', my_from)[0][0])
        if balans_time < (time.time() - 8 * 60 * 60):
            idphoto = str(random.randint(457242790, 457242801))
            vk.messages.send(peer_id=my_peer, random_id=0,
                             attachment='photo-' + group_id + '_' + idphoto,
                             message='Вам было зачисленно 1000 бро-коинов!\nПриходи снова через 8 часов🤗')
            db_module.sql_update_from_money_int(db_module.con, 'm_time', str(time.time()), str(my_from))
            add_balans(my_from, 1000)
        else:
            balans_hour = ''
            balans_minut = ''
            balans_second = ''
            balans_time = 28800 - (time.time() - balans_time)
            if balans_time > 3600:
                balans_hour += str(int(balans_time // 3600)) + ' часов '
            if balans_time > 60:
                balans_minut += str(int(balans_time % 3600 // 60)) + ' минут '
            balans_second += str(int(balans_time % 3600 % 60)) + ' секунд'

            top_headlines = newsapi.get_top_headlines(language='ru')
            news_current = (top_headlines['articles'][random.randint(0, len(top_headlines['articles']) - 1)])
            title = news_current['title']
            description = news_current['description']
            url = news_current['url']
            image = news_current['urlToImage']

            # Загрузка фото на комп
            p = requests.get(image)
            out = open("temp.jpg", "wb")
            out.write(p.content)
            out.close()

            # Отправка фото в ВК:
            upload = vk_api.VkUpload(vk)
            photo = upload.photo_messages('temp.jpg')
            owner_id = photo[0]['owner_id']
            photo_id = photo[0]['id']
            access_key = photo[0]['access_key']
            attachment = f'photo{owner_id}_{photo_id}_{access_key}'

            vk.messages.send(peer_id=my_peer, random_id=0,
                             attachment=attachment,
                             message='Бро-коины можно получить не чаще, чем 1 раз в 8 часов! Осталось времени: '
                                     + balans_hour + balans_minut + balans_second + '\n\nНовость дня:\n' + title +
                                     '\n' + description + '\nссылка на источник: ' + url)


    # Добавление n-ой суммы на баланс
    def add_balans(my_from, zp_balans):
        db_module.sql_update_from_money_int(
            db_module.con, 'money', str(int(db_module.sql_fetch_from_money(
                db_module.con, 'money', my_from)[0][0]) + int(zp_balans)), str(my_from))


    def bye_bye(*args):
        first = Dict.func_bye_bye_first[random.randint(0, (len(Dict.func_bye_bye_first)) - 1)]
        second = Dict.func_bye_bye_second[random.randint(0, (len(Dict.func_bye_bye_second)) - 1)]
        send_msg_new(args[0], first + ', ' + second)


    # Проверка на запрет запуска другой игры в данной беседе
    def prov_zap_game(my_peer):
        if str(db_module.sql_fetch(db_module.con, 'zapusk_game', my_peer)[0][0]) == '1':
            return True
        return False


    # Запрет запуска другой игры в данной беседе
    def zapret_zap_game(my_peer):
        if str(db_module.sql_fetch(db_module.con, 'zapusk_game', my_peer)[0][0]) == '1':
            db_module.sql_update(db_module.con, 'zapusk_game', 0, my_peer)
            return True
        else:
            db_module.sql_update(db_module.con, 'zapusk_game', 1, my_peer)
            return False


    # Запрет команды для определенной беседы -------------------------------------------- НУЖНА ОПТИМИЗАЦИЯ
    def zapret(my_peer, chto):
        if (chto in Dict.content_ft) or (chto in Dict.content_vd):
            zap_command = (str(db_module.sql_fetch(db_module.con, 'zap_word', my_peer)[0][0])).split()
            asq = 0
            zap_command_new = ''
            for word in zap_command:
                if str(chto) == word:
                    send_msg_new(my_peer, "Команда снова разрешена")
                    for un_word in zap_command:
                        if un_word != str(chto):
                            zap_command_new += un_word + ' '
                    db_module.sql_update(db_module.con, 'zap_word', zap_command_new, my_peer)
                    asq = 1
                    break
            if asq == 0:
                for word in zap_command:
                    zap_command_new += word + ' '
                zap_command_new += str(chto) + ' '
                db_module.sql_update(db_module.con, 'zap_word', zap_command_new, my_peer)
                send_msg_new(my_peer, "Теперь команда будет недоступна для данной беседы")


    # Проверка команды на наличие в списке запрещенных команд
    def provzapret_ft(my_peer, chto, id_photo):
        zap_command = (str(db_module.sql_fetch(db_module.con, 'zap_word', my_peer)[0][0])).split()
        asq = 0
        for word in zap_command:
            if str(chto) == word:
                send_msg_new(my_peer, "Команда запрещена для данной беседы")
                asq = 1
                break
        if asq == 0:
            send_ft(my_peer, id_photo)


    # Проверка команды на наличие в списке запрещенных команд
    def provzapret_vd(my_peer, chto, id_video):
        zap_command = (str(db_module.sql_fetch(db_module.con, 'zap_word', my_peer)[0][0])).split()
        asq = 0
        for word in zap_command:
            if str(chto) == word:
                send_msg_new(my_peer, "Команда запрещена для данной беседы")
                asq = 1
                break
        if asq == 0:
            send_vd(my_peer, id_video)


    def admin_hentai(my_peer):
        f = open('hent.txt', 'r', encoding="utf-8")
        mess = ''
        for line in f:
            mess += line
        send_msg_new(my_peer, mess)
        f.close()
        f = open('hent2.txt', 'r', encoding="utf-8")
        mess = ''
        for line in f:
            mess += line
        send_msg_new(my_peer, mess)
        f.close()
        f = open('hent3.txt', 'r', encoding="utf-8")
        mess = ''
        for line in f:
            mess += line
        send_msg_new(my_peer, mess)


    # Отправка текстового сообщения -------------------------------------------------ВЫШЕ НУЖНА ОПТИМИЗАЦИЯ

    def birzha(my_peer):
        money_people = db_module.sql_fetch_from_all(db_module.con, 'money', my_peer)
        money_clan = db_module.sql_fetch_clan_all(db_module.con, 'clan_money')
        mon_peop = 0
        mon_clan = 0
        for i in range(len(money_people)):
            mon_peop += int(money_people[i][0])
        for i in range(len(money_clan)):
            mon_clan += int(money_clan[i][0])
        send_msg_new(my_peer,
                     '&#128177;Валюта в обороте:&#128177;\n&#128182;Валюты в обороте у людей: ' + str(mon_peop) +
                     '\n&#128182;Валюты в обороте у кланов: ' + str(mon_clan) +
                     '\n\n&#128179;Курс покупки бро-коинов: 1 рубль = 2000 бро-коинов')


    def send_msg_new(peerid, ms_g):
        vk.messages.send(peer_id=peerid, random_id=0, message=ms_g)


    '''def video_save(*args):
        album_id = {'+tt': '4',
                    '+тт': '4',
                    '+coub': '3'}
        vk_polzovat.video.addToAlbum(target_id='-196288744', album_id=album_id[args[2][0]],
                                     video_id=args[4].message['attachments'][0]['video']['id'], owner_id=args[1])'''


    # Показ онлайна беседы
    def who_online(*args):
        my_peer = args[0]
        try:
            responseonl = vk.messages.getConversationMembers(peer_id=my_peer)
            liss = 'Пользователи онлайн: \n\n'
            count = 1
            for n in range(len(responseonl["profiles"])):
                if responseonl["profiles"][n].get('online'):  # ['vk.com/id'+id|first_name last name]
                    liss += (str(count) + '💚' + str(responseonl["profiles"][n].get('first_name')) + ' ' +
                             str(responseonl["profiles"][n].get('last_name')) + '\n')
                    count += 1
            send_msg_new(my_peer, liss)
        except vk_api.exceptions.ApiError:
            send_msg_new(my_peer, 'Для выполнения данной команды боту необходимы права администратора')


    # Отправка фото с сервера ВК
    def send_ft(my_peer, idphoto):
        vk.messages.send(peer_id=my_peer, random_id=0,
                         attachment='photo-' + group_id + '_' + idphoto)


    # Отправка видео с сервера ВК
    def send_vd(my_peer, idvideo):
        vk.messages.send(peer_id=my_peer, random_id=0,
                         attachment='video-' + group_id + '_' + idvideo)


    # Проверка админки и последующий запрет при ее наличии
    def adm_prov_and_zapret(my_peer, my_from, chto):
        if adm_prov(my_peer, my_from):
            zapret(my_peer, chto)
        else:
            send_msg_new(my_peer, 'Недостаточно прав')


    # Проверка пользователя на наличие прав администратора беседы
    def adm_prov(my_peer, my_from):
        try:
            he_admin = False
            responseapr = vk.messages.getConversationMembers(peer_id=my_peer)
            for m in responseapr["items"]:
                if m["member_id"] == my_from:
                    he_admin = m.get('is_admin')
            if not he_admin:
                he_admin = False
            return he_admin
        except vk_api.exceptions.ApiError:
            send_msg_new(my_peer, 'Для доступа к данной команде боту необходимы права администратора беседы')


    # Личная диалог или беседа
    def lich_or_beseda(my_peer):
        try:
            response = vk.messages.getConversationMembers(peer_id=my_peer)
            if response['count'] <= 2:
                return 1  # Личка
            else:
                return 0  # Беседа
        except vk_api.exceptions.ApiError:
            return 0  # Беседа, но нет прав у бота


    # Новая основная клавиатура
    def main_keyboard_1(my_peer):
        if lich_or_beseda(my_peer):
            keyboard = VkKeyboard(one_time=False)
            # keyboard.add_button('аниме(в разработке)', color=VkKeyboardColor.NEGATIVE)
            keyboard.add_button('арты', color=VkKeyboardColor.POSITIVE)
            keyboard.add_button('18+', color=VkKeyboardColor.NEGATIVE)
            keyboard.add_line()  # Отступ строки
            keyboard.add_button('видео', color=VkKeyboardColor.PRIMARY)
            keyboard.add_line()
            keyboard.add_button('посоветуй аниме', color=VkKeyboardColor.POSITIVE)
            vk.messages.send(peer_id=my_peer, random_id=get_random_id(),
                             keyboard=keyboard.get_keyboard(), message='Воть:')


    def main_keyboard_video(my_peer):
        if lich_or_beseda(my_peer):
            keyboard = VkKeyboard(one_time=False)
            keyboard.add_button('Coub', color=VkKeyboardColor.POSITIVE)
            keyboard.add_button('TikTok', color=VkKeyboardColor.POSITIVE)
            keyboard.add_line()
            keyboard.add_button('обои телефон', color=VkKeyboardColor.POSITIVE)
            keyboard.add_line()
            keyboard.add_button('хентай видео', color=VkKeyboardColor.NEGATIVE)
            keyboard.add_line()  # Отступ строки
            keyboard.add_button('главная', color=VkKeyboardColor.PRIMARY)
            vk.messages.send(peer_id=my_peer, random_id=get_random_id(),
                             keyboard=keyboard.get_keyboard(), message='Выбрана команда видео, выберите видео:')


    def main_keyboard_arts(my_peer):
        if lich_or_beseda(my_peer):
            keyboard = VkKeyboard(one_time=False)
            keyboard.add_button('арт', color=VkKeyboardColor.POSITIVE)
            keyboard.add_button('лоли', color=VkKeyboardColor.NEGATIVE)
            keyboard.add_button('неко', color=VkKeyboardColor.POSITIVE)
            keyboard.add_line()  # Отступ строки
            keyboard.add_button('главная', color=VkKeyboardColor.PRIMARY)
            vk.messages.send(peer_id=my_peer, random_id=get_random_id(),
                             keyboard=keyboard.get_keyboard(), message='Выбрана команда арты, выберите команду:')


    def main_keyboard_hent(my_peer):
        if lich_or_beseda(my_peer):
            keyboard = VkKeyboard(one_time=False)
            keyboard.add_button('ахегао', color=VkKeyboardColor.POSITIVE)
            keyboard.add_button('бдсм', color=VkKeyboardColor.NEGATIVE)
            keyboard.add_button('манга арт', color=VkKeyboardColor.POSITIVE)
            keyboard.add_line()  # Отступ строки
            keyboard.add_button('юри+', color=VkKeyboardColor.NEGATIVE)
            keyboard.add_button('этти', color=VkKeyboardColor.POSITIVE)
            keyboard.add_button('хентай', color=VkKeyboardColor.NEGATIVE)
            keyboard.add_line()  # Отступ строки
            keyboard.add_button('админ хентай', color=VkKeyboardColor.NEGATIVE)
            keyboard.add_line()
            keyboard.add_button('главная', color=VkKeyboardColor.PRIMARY)
            vk.messages.send(peer_id=my_peer, random_id=get_random_id(),
                             keyboard=keyboard.get_keyboard(), message='Выбрана команда хентай, выберите команду:')


    # Запуск потока с одним аргрументом
    def thread_start(Func, *args):
        global kolpot
        x = threading.Thread(target=Func, args=args)
        threads.append(x)
        kolpot += 1
        eventhr.append(kolpot)
        x.start()


    # Игра угадай число
    def game_ugadai_chislo(*args):
        my_peer = args[0]
        my_from = args[1]
        zapret_zap_game(my_peer)
        chel = '&#127918;' + people_info(my_from) + ', '
        send_msg_new(my_peer, chel + 'игра началась для тебя:\n' + ' угадай число от 1 до 3')
        timing = time.time()
        keyboard = VkKeyboard(inline=True)
        keyboard.add_button('1', color=VkKeyboardColor.NEGATIVE)
        keyboard.add_button('2', color=VkKeyboardColor.PRIMARY)
        keyboard.add_button('3', color=VkKeyboardColor.POSITIVE)
        vk.messages.send(peer_id=my_peer, random_id=get_random_id(),
                         keyboard=keyboard.get_keyboard(), message='Ваш ответ:')
        game_chislo = random.randint(1, 3)
        time.sleep(0.1)
        for eventhr[kolpot] in longpoll.listen():
            if time.time() - timing > 10.0:
                send_msg_new(my_peer, chel + 'время ожидания истекло...')
                zapret_zap_game(my_peer)
                break
            if eventhr[kolpot].type == VkBotEventType.MESSAGE_NEW:
                if eventhr[kolpot].message.peer_id == my_peer \
                        and eventhr[kolpot].message.from_id == my_from:
                    slova_g1 = eventhr[kolpot].message.text.split()
                    if len(slova_g1) >= 2:
                        if slova_g1[1] == "1" or slova_g1[1] == "2" or slova_g1[1] == "3":
                            if str(game_chislo) == str(slova_g1[1]):
                                send_msg_new(my_peer, chel + 'правильно!' + ' - загаданное число: ' +
                                             str(game_chislo))
                                zapret_zap_game(my_peer)
                                break
                            else:
                                send_msg_new(my_peer, chel + 'не правильно!' +
                                             ' - загаданное число: ' + str(game_chislo))
                                zapret_zap_game(my_peer)
                                break
                        else:
                            send_msg_new(my_peer, chel + 'кажется, ты написал что-то не то')


    # Выбор ставки
    def stavka_igra(my_peer):
        timing = time.time()
        keyboard = VkKeyboard(inline=True)
        keyboard.add_button('0', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('100', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('250', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('500', color=VkKeyboardColor.POSITIVE)
        vk.messages.send(peer_id=my_peer, random_id=get_random_id(),
                         keyboard=keyboard.get_keyboard(), message='Выберите ставку:')
        for event_stavka in longpoll.listen():
            if time.time() - timing < 60.0:
                if event_stavka.type == VkBotEventType.MESSAGE_NEW:
                    slovo = event_stavka.message.text.split()
                    if len(slovo) > 1:
                        if '0' <= slovo[1] <= '9':
                            send_msg_new(my_peer, 'Ставка: ' + str(slovo[1]))
                            return slovo[1]
            else:
                return 0


    # Деньги победителю
    def money_win(win_from, stavka, uchastniki):
        add_balans(str(win_from), str(int(stavka) * len(uchastniki)))


    # ТЕСТОВОЕ ИЗМЕНЕНИЕ СООБЩЕНИЯ
    def test_edit_message(*args):
        my_peer = args[0]
        f_toggle = False
        send_msg_new(my_peer, 'ТЕСТО')
        for i in range(10):
            vk.messages.edit(
                peer_id=int(args[4].message.peer_id),
                message='Рома' if f_toggle else 'гей',
                conversation_message_id=int(args[4].message.conversation_message_id + 1))
            f_toggle = not f_toggle
            time.sleep(2)

    # ТЕСТОВОЕ ИЗМЕНЕНИЕ СООБЩЕНИЯ
    def ahegao_edit_message(*args):
        my_peer = args[0]
        f_toggle = False
        send_msg_new(my_peer, 'Все для вас, мои любимые!')
        for i in range(10):
            randid = (random.randint(0, photo_aheg['count'] - 1))
            idphoto = (photo_aheg['items'][randid]['id'])
            vk.messages.edit(
                peer_id=int(args[4].message.peer_id),
                attachment='photo' + str(idphoto),
                conversation_message_id=int(args[4].message.conversation_message_id + 1))
            f_toggle = not f_toggle
            time.sleep(2)


    # Игра в мафию??? В РАЗРАБОТКЕ
    def MAFIA_GAME(*args):
        event_func = args[4]
        my_peer = event_func.message.peer_id
        settings = dict(one_time=False, inline=False)

        uchastniki = []
        keyboard_nabor = VkKeyboard(**settings)
        # pop-up кнопка заявки на участие
        keyboard_nabor.add_callback_button(label='Участвовать', color=VkKeyboardColor.SECONDARY,
                                           payload={"type": "show_snackbar", "text": "Заявка на участие принята!"})
        keyboard_nabor.add_line()
        # кнопка смены клавиатуры и начала игры
        keyboard_nabor.add_callback_button(label='Начать принудительно', color=VkKeyboardColor.PRIMARY,
                                           payload={"type": "prinuditelno_nachat"})
        vk.messages.send(
            random_id=get_random_id(),
            peer_id=my_peer,
            keyboard=keyboard_nabor.get_keyboard(),
            message='Принимаются заявки на участие')
        for event_nabor in longpoll.listen():
            # Обрабатываем клики по callback кнопкам
            if event_nabor.type == VkBotEventType.MESSAGE_EVENT:
                if event_nabor.object['peer_id'] == my_peer:
                    if event_nabor.object.payload.get('type') == 'show_snackbar':
                        if event_nabor.object['user_id'] not in uchastniki:
                            uchastniki.append(event_nabor.object.user_id)
                            vk.messages.sendMessageEventAnswer(
                                event_id=event_nabor.object['event_id'],
                                user_id=event_nabor.object['user_id'],
                                peer_id=event_nabor.object['peer_id'],
                                event_data=json.dumps(event_nabor.object['payload']))
                            send_msg_new(my_peer, 'Участников: ' + str(len(uchastniki)))
                        elif event_nabor.object['user_id'] in uchastniki:
                            event_data = {"type": "show_snackbar", "text": "Заявка на участие уже была принята!"}
                            vk.messages.sendMessageEventAnswer(
                                event_id=event_nabor.object['event_id'],
                                user_id=event_nabor.object['user_id'],
                                peer_id=event_nabor.object['peer_id'],
                                event_data=json.dumps(event_data))
                    elif event_nabor.object.payload.get('type') == 'prinuditelno_nachat':
                        # keyboard=keyboard_game.get_keyboard())
                        break


    # ТЕСТОВАЯ КЛАВИАТУРА
    def test_keyboard(*args):
        my_peer = args[0]
        settings = dict(one_time=False, inline=True)
        keyboard_1 = VkKeyboard(**settings)
        # pop-up кнопка
        keyboard_1.add_callback_button(label='Покажи pop-up сообщение', color=VkKeyboardColor.SECONDARY,
                                       payload={"type": "show_snackbar", "text": "Это исчезающее сообщение"})
        keyboard_1.add_line()
        # кнопка переключения на 2ое меню
        keyboard_1.add_callback_button(label='Добавить красного ', color=VkKeyboardColor.PRIMARY,
                                       payload={"type": "my_own_100500_type_edit"})

        # №2. Клавиатура с одной красной callback-кнопкой. Нажатие изменяет меню на предыдущее.
        keyboard_2 = VkKeyboard(**settings)
        # кнопка переключения назад, на 1ое меню.
        keyboard_2.add_callback_button('Назад', color=VkKeyboardColor.NEGATIVE,
                                       payload={"type": "my_own_100500_type_edit"})
        f_toggle: bool = False
        for event in longpoll.listen():
            # Обработка входящего сообщение (НЕ CALLBACK)
            if event.type == VkBotEventType.MESSAGE_NEW:
                if event.obj.message['text'] != '':
                    if event.from_user:
                        if 'callback' not in event.obj.client_info['button_actions']:
                            print(f'Клиент {event.obj.message["from_id"]} не поддерж. callback')
                            send_msg_new(my_peer, f'Клиент {event.obj.message["from_id"]} не поддерж. callback')
                        vk.messages.send(
                            user_id=event.obj.message['from_id'],
                            random_id=get_random_id(),
                            peer_id=my_peer,
                            keyboard=keyboard_1.get_keyboard(),
                            message=event.obj.message['text'])
            # обрабатываем клики по callback кнопкам
            elif event.type == VkBotEventType.MESSAGE_EVENT:
                if event.object.payload.get('type') == 'show_snackbar':
                    vk.messages.sendMessageEventAnswer(
                        event_id=event.object.event_id,
                        user_id=event.object.user_id,
                        peer_id=event.object.peer_id,
                        event_data=json.dumps(event.object.payload))
                elif event.object.payload.get('type') == 'my_own_100500_type_edit':
                    vk.messages.edit(
                        peer_id=event.obj.peer_id,
                        message='ola',
                        conversation_message_id=event.obj.conversation_message_id,
                        keyboard=(keyboard_1 if f_toggle else keyboard_2).get_keyboard())
                    f_toggle = not f_toggle


    # Набор игроков на игру
    def nabor_igrokov(my_peer, stavka):
        uchastniki = []
        timing = time.time()
        keyboard = VkKeyboard(one_time=False, inline=True)
        keyboard.add_callback_button(label='участвую', color=VkKeyboardColor.POSITIVE,
                                     payload={"type": "show_snackbar", "text": "Заявка на участие принята!"})
        keyboard.add_callback_button(label='начать', color=VkKeyboardColor.POSITIVE,
                                     payload={"type": "start_game"})
        vk.messages.send(peer_id=my_peer, random_id=get_random_id(),
                         keyboard=keyboard.get_keyboard(), message='Набор участников:')
        for event in longpoll.listen():
            if time.time() - timing < 60.0:
                if event.type == VkBotEventType.MESSAGE_NEW:
                    words = event.message.text.lower().split()
                    if "участвую" in words:
                        if event.message.from_id > 0:
                            if event.message.from_id not in uchastniki:
                                if int(str(db_module.sql_fetch_from_money(
                                        db_module.con, 'money', str(event.message.from_id))[0][0])) >= \
                                        int(stavka):
                                    uchastniki.append(event.message.from_id)
                                    send_msg_new(my_peer, '&#127918;Участник ' + str(len(uchastniki)) + ' - '
                                                 + people_info(event.message.from_id))
                                else:
                                    send_msg_new(my_peer, people_info(event.message.from_id) +
                                                 ', у вас недостаточно средств на счете! Получите '
                                                 'бро-коины написав "бро награда"')
                        else:
                            send_msg_new(my_peer, 'Боты не могут участвовать в игре!')
                    elif "начать" in words:
                        timing -= timing - 60

                elif event.type == VkBotEventType.MESSAGE_EVENT:
                    if event.object.payload.get('type') == 'start_game':
                        timing -= timing - 60
                    if event.object.payload.get('type') == 'show_snackbar':
                        if event.object.user_id > 0:
                            if event.object.user_id in uchastniki:
                                vk.messages.sendMessageEventAnswer(
                                    event_id=event.object.event_id,
                                    user_id=event.object.user_id,
                                    peer_id=event.object.peer_id,
                                    event_data=json.dumps({"type": "show_snackbar",
                                                           "text": "Ты уже в списке участников!"}))
                            if event.object.user_id not in uchastniki:
                                vk.messages.sendMessageEventAnswer(
                                    event_id=event.object.event_id,
                                    user_id=event.object.user_id,
                                    peer_id=event.object.peer_id,
                                    event_data=json.dumps(event.object.payload))
                                if int(str(db_module.sql_fetch_from_money(
                                        db_module.con, 'money', str(event.object.user_id))[0][0])) >= \
                                        int(stavka):
                                    uchastniki.append(event.object.user_id)
                                    send_msg_new(my_peer, '&#127918;Участник ' + str(len(uchastniki)) + ' - '
                                                 + people_info(event.object.user_id))
                                else:
                                    send_msg_new(my_peer, people_info(event.object.user_id) +
                                                 ', у вас недостаточно средств на счете! Получите '
                                                 'бро-коины написав "бро награда"')
                        else:
                            send_msg_new(my_peer, 'Боты не могут участвовать в игре!')
            if time.time() - timing > 60.0:
                vk.messages.send(peer_id=my_peer, random_id=get_random_id(),
                                 message='&#127918;Участники укомплектованы, игра начинается')
                for i in uchastniki:
                    add_balans(str(i), (str('-') + str(stavka)))
                return uchastniki


    # Игра кто круче
    def game_kto_kruche(my_peer, my_from):
        zapret_zap_game(my_peer)
        send_msg_new(my_peer, '&#127918;Запущена игра "Кто круче?". Чтобы принять участие, '
                              'напишите "участвую". '
                              '\nМинимальное количество участников для запуска: 2')
        stavka = stavka_igra(my_peer)
        uchastniki = nabor_igrokov(my_peer, stavka)
        if len(uchastniki) < 2:
            send_msg_new(my_peer, '&#127918;Слишком мало участников, игра отменена')
            for i in uchastniki:
                add_balans(str(i), str(stavka))
            zapret_zap_game(my_peer)
        else:
            send_msg_new(my_peer, '&#127918;Участники укомплектованы, игра начинается')
            priz = random.randint(0, len(uchastniki) - 1)
            chel = '&#127918;' + people_info(str(uchastniki[priz])) + ', '
            send_msg_new(my_peer, chel + 'ты круче')
            money_win(uchastniki[priz], stavka, uchastniki)
            zapret_zap_game(my_peer)


    # Игра казино
    def game_casino(my_peer, my_from):
        dengi_game = 0
        zapret_zap_game(my_peer)
        send_msg_new(my_peer,
                     '&#127918;' + people_info(my_from) + ', для вас запущена игра "Казино"')
        keyboard = VkKeyboard(inline=True)
        keyboard.add_button('100', color=VkKeyboardColor.PRIMARY)
        keyboard.add_button('500', color=VkKeyboardColor.PRIMARY)
        keyboard.add_button('1000', color=VkKeyboardColor.PRIMARY)
        keyboard.add_button('5000', color=VkKeyboardColor.PRIMARY)
        vk.messages.send(peer_id=my_peer, random_id=get_random_id(),
                         keyboard=keyboard.get_keyboard(), message='Выберите ставку - чем выше ставка, '
                                                                   'тем меньше шанс победить!\n'
                                                                   'Шанс победы = (100 / Ставка * 1.1)%\n'
                                                                   'И помните, бесплатный сыр только в мышеловке!')
        timing = time.time()
        stop = 0
        for event_casino_game in longpoll.listen():
            if time.time() - timing < 15.0:
                if event_casino_game.type == VkBotEventType.MESSAGE_NEW:
                    if event_casino_game.message.from_id == my_from:
                        slovo = event_casino_game.message.text.split()
                        if len(slovo) > 1:
                            if chislo_li_eto(slovo[1]):
                                if float(slovo[1]) > 0:
                                    dengi_game = float(slovo[1])
                                    if int(db_module.sql_fetch_from_money(db_module.con, 'money', my_from)[0][0]) >= \
                                            dengi_game:
                                        break
                                    else:
                                        send_msg_new(my_peer, people_info(my_from) + ', у вас недостаточно монет!\n'
                                                                                     'Игра отменена!')
                                        stop = 1
                                        break
                                else:
                                    send_msg_new(my_peer, people_info(my_from) + ', ставка не может быть '
                                                                                 'отрицательна!\n'
                                                                                 'Введите правильное число!')
                            else:
                                send_msg_new(my_peer, people_info(my_from) + ', введите правильное число!')
            if time.time() - timing >= 15:
                stop = 1
                send_msg_new(my_peer, people_info(my_from) + ', время истекло!\n'
                                                             'Игра отменена!')
                break
        if stop != 1:
            keyboard = VkKeyboard(inline=True)
            keyboard.add_button('2.0', color=VkKeyboardColor.PRIMARY)
            keyboard.add_button('3.0', color=VkKeyboardColor.PRIMARY)
            keyboard.add_button('4.0', color=VkKeyboardColor.PRIMARY)
            keyboard.add_button('5.0', color=VkKeyboardColor.PRIMARY)
            vk.messages.send(peer_id=my_peer, random_id=get_random_id(),
                             keyboard=keyboard.get_keyboard(), message='Выберите множитель - чем выше множитель, '
                                                                       'тем меньше шанс победить!\n'
                                                                       'Шанс победы = (100 / множитель * 1.1)%')
            timing = time.time()
            for event_casino_game in longpoll.listen():
                if time.time() - timing < 15.0:
                    if event_casino_game.type == VkBotEventType.MESSAGE_NEW:
                        if event_casino_game.message.from_id == my_from:
                            slovo = event_casino_game.message.text.split()
                            if len(slovo) > 1:
                                if chislo_li_eto(slovo[1]):
                                    if float(slovo[1]) > 0:
                                        add_balans(my_from, '-' + str(int(dengi_game)))
                                        s = random.random()
                                        send_msg_new(my_peer, 'Колесо фортуны запущено!\n'
                                                              'Ваша ставка: ' + str(int(dengi_game)) +
                                                     '\nВаш множитель: ' + str(slovo[1]) +
                                                     '\nШанс победить: ' + str(100 / (float(slovo[1]) * 1.1)) + '%')
                                        time.sleep(3)
                                        if (s * 100) < (100 / (float(slovo[1]) * 1.1)):
                                            add_balans(my_from, (float(int(dengi_game)) * float(slovo[1])))
                                            send_msg_new(my_peer, people_info(my_from) + ', вы выйграли '
                                                         + str(float(dengi_game) * float(slovo[1])) + ' монет!')
                                        else:
                                            send_msg_new(my_peer, people_info(my_from) + ', к сожалению, вы проиграли!')
                                        break
                                    else:
                                        send_msg_new(my_peer, people_info(my_from) + ', ставка не может быть '
                                                                                     'отрицательна!\n'
                                                                                     'Введите правильное число!')
                                else:
                                    send_msg_new(my_peer, people_info(my_from) + ', введите правильное число!')
                else:
                    send_msg_new(my_peer, 'вы так и не сделали ставку\n'
                                          'Игра отменена!')
                    break
            zapret_zap_game(my_peer)
        else:
            zapret_zap_game(my_peer)


    # Игра бросок кубика
    def game_brosok_kubika(my_peer, my_from):
        zapret_zap_game(my_peer)
        send_msg_new(my_peer,
                     '&#127918;Запущена игра "Бросок кубика". Чтобы принять участие, напишите '
                     '"участвую". \nМинимальное количество участников для запуска: 2')
        stavka = stavka_igra(my_peer)
        uchastniki = nabor_igrokov(my_peer, stavka)
        if len(uchastniki) < 2:
            send_msg_new(my_peer, '&#127918;Слишком мало участников, игра отменена')
            for i in uchastniki:
                add_balans(str(i), str(stavka))
            zapret_zap_game(my_peer)
        else:
            chet = []
            for i in uchastniki:
                send_msg_new(my_peer, '&#9745;Кубики бросает ' + people_info(str(i)) + '...')
                time.sleep(2)
                kubiki = random.randint(2, 12)
                chet.append(kubiki)
                send_msg_new(my_peer, '&#9989;на кубиках ' + str(kubiki))
                time.sleep(1)
            min_chet = 1
            pobeditel = 0
            nich = 0
            for i in range(len(uchastniki)):
                if chet[i] >= min_chet:
                    if chet[i] == min_chet:
                        nich = 1
                    else:
                        nich = 0
                    min_chet = chet[i]
                    pobeditel = uchastniki[i]
            if nich == 1:
                send_msg_new(my_peer, '&#127918;Ничья!')
                for i in uchastniki:
                    add_balans(str(i), str(stavka))
                zapret_zap_game(my_peer)
            else:
                send_msg_new(my_peer, '&#127918;' + people_info(pobeditel) + '&#127881; ' + 'победил!&#127882;')
                money_win(pobeditel, stavka, uchastniki)
                zapret_zap_game(my_peer)


    # Игра математическая викторина
    def game_mat_victorina(my_peer, my_from):
        if int(str(db_module.sql_fetch_from_money(db_module.con, 'money', str(my_from))[0][0])) >= int(300):
            zapret_zap_game(my_peer)
            send_msg_new(my_peer, 'С вашего счета списано 300 монеток\nВремя на каждый ответ - 15 секунд')
            time.sleep(2)
            send_msg_new(my_peer, 'Начинаем!')
            time.sleep(1)
            add_balans(str(my_from), '-300')
            dengi = 50
            for i in range(5):
                stop = 0
                nuli = ''.join(['0' for i in range(i)])
                a = random.randint(1, int('1' + str(nuli)))
                b = random.randint(1, int('1' + str(nuli)))
                timing = time.time()
                znak = '+'
                send_msg_new(my_peer, 'Сколько будет ' + str(a) + ' ' + znak + ' ' + str(b) + ' ?')
                uravnenie = a + b
                for event_victorina_game in longpoll.listen():
                    if time.time() - timing < 15.0:
                        if event_victorina_game.type == VkBotEventType.MESSAGE_NEW:
                            if event_victorina_game.message.from_id == my_from:
                                if event_victorina_game.message.text == str(uravnenie):
                                    send_msg_new(my_peer, 'Верно!')
                                else:
                                    send_msg_new(my_peer, 'Увы, но нет, вы проиграли!')
                                    stop = 1
                                break
                    elif time.time() - timing > 15.0:
                        stop = 1
                        send_msg_new(my_peer, 'Увы, но ваше время истекло, вы проиграли!')
                        break
                if stop == 1:
                    zapret_zap_game(my_peer)
                    break
                else:
                    if i < 4:
                        if i == 3:
                            send_msg_new(my_peer, 'Если вы сейчас нажмете продолжить, то ваш выйгрыш '
                                                  'увеличится в 8 раз!')
                            time.sleep(2)
                        keyboard = VkKeyboard(inline=True)
                        keyboard.add_button('забрать деньги', color=VkKeyboardColor.PRIMARY)
                        keyboard.add_button('продолжить', color=VkKeyboardColor.PRIMARY)
                        vk.messages.send(peer_id=my_peer, random_id=get_random_id(),
                                         keyboard=keyboard.get_keyboard(), message='Что вы предпочтете, забрать '
                                                                                   'выйгрыш, '
                                                                                   'или удвоить его? Ваш выйгрыш: ' +
                                                                                   str(dengi) + ' монет')
                        for event_victorina_game in longpoll.listen():
                            if time.time() - timing < 60.0:
                                if event_victorina_game.type == VkBotEventType.MESSAGE_NEW:
                                    if event_victorina_game.message.from_id == my_from:
                                        if event_victorina_game.message.text == ('[' + 'club' + str(group_id) + '|' +
                                                                                 group_name + ']' + " забрать деньги") \
                                                or (
                                                event_victorina_game.message.text == '[' + 'club' + str(group_id) + '|'
                                                + group_sob + ']' + " забрать деньги"):
                                            add_balans(my_from, dengi)
                                            stop = 1
                                            send_msg_new(my_peer, 'Вы выйграли ' + str(dengi) + ' монет')
                                            break
                                        elif event_victorina_game.message.text == ('[' + 'club' + str(group_id) + '|' +
                                                                                   group_name + ']' + " продолжить") \
                                                or (
                                                event_victorina_game.message.text == '[' + 'club' + str(group_id) + '|'
                                                + group_sob + ']' + " продолжить"):
                                            dengi *= 2
                                            time.sleep(1)
                                            if i == 3:
                                                dengi *= 4
                                            break
                            else:
                                add_balans(my_from, dengi)
                                stop = 1
                                send_msg_new(my_peer, 'Вы выйграли ' + str(dengi) + ' монет')
                                break
                        if stop == 1:
                            zapret_zap_game(my_peer)
                            break
                    else:
                        zapret_zap_game(my_peer)
                        send_msg_new(my_peer, 'Вы выйграли ' + str(dengi) + ' монет')
                        add_balans(my_from, dengi)
        else:
            send_msg_new(my_peer, people_info(my_from) + ', у вас недостаточно средств на счете! Получите '
                                                         'бро-коины написав "бро награда"')


    # Рандомное число от и до
    def random_ot_do_int_chislo(my_peer, ot, do):
        if chislo_li_eto(ot) and chislo_li_eto(do):
            if do > ot:
                send_msg_new(my_peer, 'Ваше случайное число: ' + str(random.randint(int(ot), int(do))))
            else:
                send_msg_new(my_peer, 'Первое число не может быть меньше второго!')
        else:
            send_msg_new(my_peer, 'Вы ввели неправильные числа!')


    # Клавиатура со списком игр
    def klava_game(*args):
        my_peer = args[0]
        send_msg_new(my_peer, '&#8505;Для запуска напишите: игра "номер" Например: игра 1\n'
                              '&#8505;Список игр:\n'
                              '1&#8419;Угадай число\n'
                              '2&#8419;Кто круче\n'
                              '3&#8419;Бросок кубика\n'
                              '4&#8419;Математическая викторина\n'
                              '5&#8419;Казино')


    def send_content(my_peer, what_content, command, ft_or_vd):
        randid = (random.randint(0, what_content['count'] - 1))
        idphoto = (what_content['items'][randid]['id'])
        if ft_or_vd:
            provzapret_ft(my_peer, command, str(idphoto))
        else:
            provzapret_vd(my_peer, command, str(idphoto))

except (urllib3.exceptions.MaxRetryError, socket.gaierror):
    print(" - ошибка подключения к вк")
