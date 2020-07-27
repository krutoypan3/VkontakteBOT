import json
import socket
import threading
import requests
import urllib3
import sqlite3
from sqlite3 import Error
import random
import time
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id


# Функция обработки ошибок
def error(ErrorF):
    global oshibka
    oshibka += 1
    print("Произошла ошибка " + '№' + str(oshibka) + ' ' + ErrorF)
    if ErrorF == " - ошибка подключения к вк":
        time.sleep(5.0)
    main()


# Первичный запуск программы и внесение изменений для старта программы
try:
    API_GROUP_KEY = '956c94c497adaa135a29605943d6ab551d74a6071757da8e4aa516a2fd4c980e96cfbe101b06a9d57e2b6'
    API_USER_KEY = '34469a24e88620d4ee0961cc31e2c1c96d5cb01edd3ee50ed1f08fac299571630f4f602564c89419cbc58'
    print("Бот работает...")
    group_id = '196288744'  # Указываем id сообщества, изменять только здесь!
    oshibka = 0  # обнуление счетчика ошибок
    threads = list()
    eventhr = []
    kolpot = -1
    group_sob = "@bratikbot"  # Указываем короткое имя бота (если нет то id)
    group_name = "Братик"  # Указываем название сообщества

    vk_session = vk_api.VkApi(token=API_GROUP_KEY)  # Авторизация под именем сообщества
    longpoll = VkBotLongPoll(vk_session, group_id)
    vk = vk_session.get_api()

    vk_session_user = vk_api.VkApi(token=API_USER_KEY)  # Авторизация под именем пользователя
    vk_polzovat = vk_session_user.get_api()

    # Авторизация сервисным токеном
    ser_token = 'c14c6918c14c6918c14c691807c13e8ffacc14cc14c69189e4cb11298fa3a5dff633603'
    client_secret = '3GBA2mEv669lqnF8WZyA'
    vk_session_SERVISE = vk_api.VkApi(app_id=7530210, token=ser_token, client_secret=client_secret)
    vk_session_SERVISE.server_auth()
    vk_SERVISE = vk_session_SERVISE.get_api()
    vk_session_SERVISE.token = {'access_token': ser_token, 'expires_in': 0}

    global photo_loli, photo_neko, photo_arts, photo_hent, photo_aheg, photo_stik, photo_mart, video_coub, photo_bdsm
    # Отправка запросов на информацию об фотографиях и видео в группе
    def zapros_ft_vd():
        global photo_loli, photo_neko, photo_arts, photo_hent, photo_aheg, photo_stik, photo_mart, video_coub, \
            photo_bdsm
        photo_loli = vk_SERVISE.photos.get(owner_id='-' + group_id, album_id=271418270, count=1000)  # Тут находятся
        photo_neko = vk_SERVISE.photos.get(owner_id='-' + group_id, album_id=271449419, count=1000)  # альбомы группы
        photo_arts = vk_SERVISE.photos.get(owner_id='-' + group_id, album_id=271418213, count=1000)  # и их id
        photo_hent = vk_SERVISE.photos.get(owner_id='-' + group_id, album_id=271418234, count=1000)  # по которым внизу
        photo_aheg = vk_SERVISE.photos.get(owner_id='-' + group_id, album_id=271421874, count=1000)  # будут отбираться
        photo_stik = vk_SERVISE.photos.get(owner_id='-' + group_id, album_id=271599613, count=1000)  # фото + 10 сек
        photo_mart = vk_SERVISE.photos.get(owner_id='-' + group_id, album_id=271761499, count=1000)  # к запуску
        photo_bdsm = vk_SERVISE.photos.get(owner_id='-' + group_id, album_id=272201504, count=1000)  #
        video_coub = vk_polzovat.video.get(owner_id='-' + group_id, count=200)                       # album_id=1,

    zapros_ft_vd()

    '''
    with open('dump_video.json', 'w') as dump:
        rndid = (random.randint(0, video_coub['count'] - 1))
        print(video_coub['items'][rndid]['id'])
        json.dump(video_coub, dump)
    '''





except (requests.exceptions.ConnectionError, urllib3.exceptions.MaxRetryError,
        urllib3.exceptions.NewConnectionError, socket.gaierror):
    error(" - ошибка подключения к вк")

# Работа с базой данных
try:
    # Соединение с БД
    def sql_connection():
        try:
            conc1 = sqlite3.connect('mydatabase.db', check_same_thread=False)  # Подключение к БД
            return conc1
        except Error:
            print(Error)


    # Создание таблицы в БД
    def sql_table(conc3):
        cursorObj4 = conc3.cursor()  # Курсор БД
        cursorObj4.execute("CREATE TABLE anime_base(name string PRIMARY KEY, genre string, series string)")
        conc3.commit()


    con = sql_connection()  # Соединение с БД


    # Вставка СТРОКИ в ТАБЛИЦУ peer_params в БД
    def sql_insert(conc2, entities):
        cursorObj3 = conc2.cursor()
        cursorObj3.execute('INSERT INTO peer_params(peer_id, zapusk_game, filter_mata) VALUES(?, ?, ?)', entities)
        conc2.commit()


    # Вставка СТРОКИ в ТАБЛИЦУ from_params в БД
    def sql_insert_from(conc2, entities):
        cursorObj3 = conc2.cursor()
        cursorObj3.execute(
            'INSERT INTO from_params(peer_id, from_id, money, m_time, warn, marry_id) VALUES(?, ?, ?, ?, ?, ?)',
            entities)
        conc2.commit()


    # Обновление параметра в таблице peer_params
    def sql_update(con5, what_fetch, what_fetch_new, peer_id_val):
        cursorObj1 = con5.cursor()
        cursorObj1.execute('UPDATE peer_params SET ' + str(what_fetch) + ' = ' + str(what_fetch_new) +
                           ' where peer_id = ' + str(peer_id_val))
        con5.commit()


    # Обновление параметра в таблице from_params
    def sql_update_from(con5, what_fetch, what_fetch_new, peer_id_val, from_id_val):
        cursorObj1 = con5.cursor()
        cursorObj1.execute('UPDATE from_params SET ' + str(what_fetch) + ' = ' + str(what_fetch_new) +
                           ' where peer_id = ' + str(peer_id_val) + ' AND from_id = ' + str(from_id_val))
        con5.commit()


    # Получение параметров из таблицы peer_params
    def sql_fetch(conc, what_return, peer_id_val):
        cursorObj2 = conc.cursor()
        cursorObj2.execute('SELECT ' + str(what_return) + ' FROM peer_params WHERE peer_id = ' + str(peer_id_val))
        rows = cursorObj2.fetchall()
        if len(rows) == 0:  # Проверка на наличие записи в таблице и при ее отсутствии, создание новой
            entities = peer_id_val, '0', '1'
            sql_insert(conc, entities)
            rows = sql_fetch(conc, what_return, peer_id_val)
            return rows
        else:
            return rows


    # Получение параметров из таблицы from_params
    def sql_fetch_from(conc, what_return, peer_id_val, from_id_val):
        cursorObj2 = conc.cursor()
        cursorObj2.execute('SELECT ' + str(what_return) + ' FROM from_params WHERE peer_id = ' + str(
            peer_id_val) + ' AND from_id = ' + str(from_id_val))
        rows = cursorObj2.fetchall()
        if len(rows) == 0:  # Проверка на наличие записи в таблице и при ее отсутствии, создание новой
            entities = str(peer_id_val), str(from_id_val), '0', '0', '0', '0'
            sql_insert_from(conc, entities)
            rows = sql_fetch_from(conc, what_return, peer_id_val, from_id_val)
            return rows
        return rows


    # Получение параметров из таблицы from_params
    def sql_fetch_from_all(conc, what_return, peer_id_val):
        cursorObj2 = conc.cursor()
        cursorObj2.execute('SELECT ' + str(what_return) + ' FROM from_params WHERE peer_id = ' + str(
            peer_id_val))
        rows = cursorObj2.fetchall()
        return rows


    # Посоветуй аниме
    def anime_sovet(peer_id):
        time.sleep(1)
        timing = time.time()
        if lich_or_beseda(peer_id):
            keyboard = VkKeyboard(one_time=True)
        else:
            keyboard = VkKeyboard(inline=True)
        keyboard.add_button('Исекай', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('Романтика', color=VkKeyboardColor.PRIMARY)
        keyboard.add_button('Приключения', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('Гарем', color=VkKeyboardColor.PRIMARY)
        keyboard.add_line()  # Отступ строки
        keyboard.add_button('Фэнтези', color=VkKeyboardColor.PRIMARY)
        keyboard.add_button('Этти', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('Повседневность', color=VkKeyboardColor.PRIMARY)
        keyboard.add_button('Детектив', color=VkKeyboardColor.POSITIVE)
        vk.messages.send(peer_id=peer_id, random_id=get_random_id(),
                         keyboard=keyboard.get_keyboard(), message='Выберите жанр:')
        for event_stavka in longpoll.listen():
            if time.time() - timing < 60.0:
                if event_stavka.type == VkBotEventType.MESSAGE_NEW:
                    slovo = event_stavka.obj.text.split()
                    if len(slovo) > 1:
                        if (slovo[0] == ('[' + 'club' + str(group_id) + '|' + group_name + ']')) or \
                                (slovo[0] == ('[' + 'club' + str(group_id) + '|' + group_sob + ']')):
                            thread_start3(sql_fetch_anime_base, con, slovo[1], peer_id)
                    elif len(slovo) == 1:
                        thread_start3(sql_fetch_anime_base, con, slovo[0], peer_id)
                    break


    # Получение параметров из таблицы anime_base
    def sql_fetch_anime_base(conc, janr, peer_id):
        cursorObj2 = conc.cursor()
        cursorObj2.execute('SELECT ' + str('name') + ' FROM anime_base WHERE janr = "' + str(janr) + '" OR janr2 = "'
                           + str(janr) + '" OR janr3 = "' + str(janr) + '"')
        rows = cursorObj2.fetchall()
        message = 'Аниме в жанре ' + janr + ':\n'
        for i in rows:
            message += i[0] + '\n'
        send_msg_new(peer_id, message)


    # Вставка строки в таблицу anime_base
    def sql_insert_anime_base(conc2, entities):
        cursorObj3 = conc2.cursor()
        cursorObj3.execute(
            'INSERT INTO anime_base(name, janr, janr2, janr3, series) VALUES(?, ?, ?, ?, ?)', entities)
        conc2.commit()


    # Обнуление игр во всех беседах
    cursorObj = con.cursor()
    cursorObj.execute('UPDATE peer_params SET zapusk_game = 0')
    con.commit()
except (requests.exceptions.ConnectionError, urllib3.exceptions.MaxRetryError,
        urllib3.exceptions.NewConnectionError, socket.gaierror):
    error(" - ошибка подключения к вк")

# ОСНОВНЫЕ ФУНКЦИИ
try:
    # Статус брака
    def marry_status(my_peer, my_from):
        marry_id = str(sql_fetch_from(con, 'marry_id', my_peer, my_from)[0][0])
        if marry_id == 'None' or marry_id == '0':
            send_msg_new(my_peer, 'Вы не состоите в браке')
        else:
            marry_user2 = vk.users.get(user_ids=marry_id, name_case='ins')
            he_name2 = marry_user2[0]['first_name']
            he_family2 = marry_user2[0]['last_name']
            chel2 = '[' + 'id' + str(marry_id) + '|' + str(he_name2) + ' ' + str(he_family2) + ']'
            send_msg_new(my_peer, 'Вы состоите в браке с ' + chel2)


    # Развод
    def marry_disvorse(my_peer, my_from):
        marry_id = str(sql_fetch_from(con, 'marry_id', my_peer, my_from)[0][0])
        if str(marry_id) == 'None' or str(marry_id) == '0':
            send_msg_new(my_peer, 'Вы не состоите в браке!')
        else:
            marry_user = vk.users.get(user_ids=my_from)
            marry_user2 = vk.users.get(user_ids=marry_id, name_case='ins')
            he_name = marry_user[0]['first_name']
            he_family = marry_user[0]['last_name']
            he_name2 = marry_user2[0]['first_name']
            he_family2 = marry_user2[0]['last_name']
            chel = '[' + 'id' + str(my_from) + '|' + str(he_name) + ' ' + str(he_family) + ']'
            chel2 = '[' + 'id' + str(marry_id) + '|' + str(he_name2) + ' ' + str(he_family2) + ']'
            sql_update_from(con, 'marry_id', str('0'), str(my_peer), str(my_from))
            sql_update_from(con, 'marry_id', str('0'), str(my_peer), str(marry_id))
            send_msg_new(my_peer, chel + ' разводится с ' + chel2)


    # Создание брака
    def marry_create(my_peer, my_from, id2):
        our_from = ''
        for i in id2:
            if '0' <= i <= '9':
                our_from += i
            if i == '|':
                break
        if str(my_from) == str(our_from):
            send_msg_new(my_peer, 'Ты чо? Дебил?')
        else:
            marry_id = str(sql_fetch_from(con, 'marry_id', my_peer, my_from)[0][0])
            marry_id2 = str(sql_fetch_from(con, 'marry_id', my_peer, our_from)[0][0])
            if (marry_id == 'None' or marry_id == '0') and (marry_id2 == 'None' or marry_id2 == '0'):
                marry_user = vk.users.get(user_ids=my_from, name_case='gen')
                marry_user2 = vk.users.get(user_ids=our_from)
                he_name = marry_user[0]['first_name']
                he_family = marry_user[0]['last_name']
                he_name2 = marry_user2[0]['first_name']
                he_family2 = marry_user2[0]['last_name']
                chel = '[' + 'id' + str(my_from) + '|' + str(he_name) + ' ' + str(he_family) + ']'
                chel2 = '[' + 'id' + str(our_from) + '|' + str(he_name2) + ' ' + str(he_family2) + ']'
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
                        if str(eventhr[kolpot].object.peer_id) == str(my_peer) and str(
                                eventhr[kolpot].object.from_id) == str(our_from):
                            slova_m = eventhr[kolpot].obj.text.split()
                            if len(slova_m) == 2:
                                if slova_m[1] == "💝да":
                                    sql_update_from(con, 'marry_id', str(our_from), str(my_peer), str(my_from))
                                    sql_update_from(con, 'marry_id', str(my_from), str(my_peer), str(our_from))
                                    send_msg_new(my_peer, 'Брак успешно заключен!')
                                    break
                                elif slova_m[1] == "💔нет":
                                    send_msg_new(my_peer, 'Увы, но брак не будет заключен')
                                    break
            else:
                send_msg_new(my_peer, 'Один из вас уже находится в браке!')


    # Проверка баланса
    def balans_status(my_peer, my_from):
        balans = str(sql_fetch_from(con, 'money', my_peer, my_from)[0][0])
        send_msg_new(my_peer, 'Ваш баланс : ' + str(balans) + ' бро-коинов')


    # Баланс топ
    def balans_top(my_peer):
        send_msg_new(my_peer, 'Считаем деньги...')
        kol_vo = str(sql_fetch_from_all(con, 'money', my_peer))
        mesta = str(sql_fetch_from_all(con, 'from_id', my_peer))
        idall = mesta.split()
        monall = kol_vo.split()
        mess = ''
        for i in range(len(idall) - 1):
            a = ''
            b = ''
            for j in (idall[i]):
                if '0' <= str(j) <= '9':
                    a += str(j)
            for k in (monall[i]):
                if '0' <= str(k) <= '9':
                    b += str(k)
            user = vk.users.get(user_ids=a)
            a = str(user[0]['first_name']) + ' ' + str(user[0]['last_name'])
            mess += '💰' + str(a) + ' - ' + str(b) + ' бро-коинов\n'
        send_msg_new(my_peer, mess)


    # Зачисление ежедневного вознаграждения
    def add_balans_every_day(my_peer, my_from):
        if int(sql_fetch_from(con, 'm_time', my_peer, my_from)[0][0]) < (time.time() - 8 * 60 * 60):
            add_balans(my_peer, my_from, 1000)
            send_msg_new(my_peer, 'Вам было зачисленно 1000 бро-коинов!')
        else:
            send_msg_new(my_peer, 'Бро-коины можно получить не чаще, чем 1 раз в 8 часов!')


    # Добавление n-ой суммы на баланс
    def add_balans(my_peer, my_from, zp_balans):
        balans = int(sql_fetch_from(con, 'money', my_peer, my_from)[0][0])
        balans += int(zp_balans)
        sql_update_from(con, 'money', str(balans), str(my_peer), str(my_from))
        sql_update_from(con, 'm_time', str(time.time()), str(my_peer), str(my_from))


    # Проверка на запрет запуска другой игры в данной беседе
    def prov_zap_game(my_peer):
        if str(sql_fetch(con, 'zapusk_game', my_peer)[0][0]) == '1':
            return True
        return False


    # Запрет запуска другой игры в данной беседе
    def zapret_zap_game(my_peer):
        if str(sql_fetch(con, 'zapusk_game', my_peer)[0][0]) == '1':
            sql_update(con, 'zapusk_game', 0, my_peer)
            return True
        else:
            sql_update(con, 'zapusk_game', 1, my_peer)
            return False


    # Запрет команды для определенной беседы -------------------------------------------- НУЖНА ОПТИМИЗАЦИЯ
    def zapret(my_peer, chto):
        zap_command = open('zap_command.txt', 'r')
        asq = 0
        for line in zap_command:
            if str(my_peer) + ' ' + str(chto) + '\n' == str(line):
                send_msg_new(my_peer, "Команда снова разрешена")
                lines = zap_command.readlines()
                zap_command.close()
                zap_command = open("zap_command.txt", 'w')
                for linec in lines:
                    if linec != str(my_peer) + ' ' + str(chto) + '\n':
                        zap_command.write(linec)
                asq = 1
                break
        zap_command.close()
        if asq == 0:
            zap_command = open('zap_command.txt', 'a')
            zap_command.write(str(my_peer) + ' ' + str(chto) + '\n')
            zap_command.close()
            send_msg_new(my_peer, "Теперь команда будет недоступна для данной беседы")


    # Проверка команды на наличие в списке запрещенных команд
    def provzapret_ft(my_peer, chto, idphoto):
        zap_command = open('zap_command.txt', 'r')
        asq = 0
        for line in zap_command:
            if str(my_peer) + ' ' + str(chto) + '\n' == str(line):
                send_msg_new(my_peer, "Команда запрещена для данной беседы")
                asq = 1
                break
        zap_command.close()
        if asq == 0:
            send_ft(my_peer, idphoto)


    # Проверка команды на наличие в списке запрещенных команд
    def provzapret_vd(my_peer, chto, idvideo):
        zap_command = open('zap_command.txt', 'r')
        asq = 0
        for line in zap_command:
            if str(my_peer) + ' ' + str(chto) + '\n' == str(line):
                send_msg_new(my_peer, "Команда запрещена для данной беседы")
                asq = 1
                break
        zap_command.close()
        if asq == 0:
            send_vd(my_peer, idvideo)


    # Отправка текстового сообщения -------------------------------------------------ВЫШЕ НУЖНА ОПТИМИЗАЦИЯ
    def send_msg_new(peerid, ms_g):
        vk.messages.send(peer_id=peerid, random_id=0, message=ms_g)


    # Показ онлайна беседы
    def who_online(my_peer):
        try:
            responseonl = vk.messages.getConversationMembers(peer_id=my_peer)
            liss = 'Пользователи онлайн: \n\n'
            for n in responseonl["profiles"]:
                if n.get('online'):  # ['vk.com/id'+id|first_name last name]
                    liss += ('💚' + str(n.get('first_name')) + ' ' + str(n.get('last_name')) + '\n')
            return liss
        except vk_api.exceptions.ApiError:
            send_msg_new(my_peer, 'Для выполнения данной команды боту необходимы права администратора')
            main()


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
            main()


    # Личная диалог или беседа
    def lich_or_beseda(my_peer):
        try:
            responselic = vk.messages.getConversationMembers(peer_id=my_peer)
            if responselic['count'] <= 2:
                return 1  # Личка
            else:
                return 0  # Беседа
        except vk_api.exceptions.ApiError:
            return 0

    # Новая основная клавиатура
    def main_keyboard_1(my_peer):
        if lich_or_beseda(my_peer):
            keyboard = VkKeyboard(one_time=True)
            keyboard.add_button('аниме(в разработке)', color=VkKeyboardColor.NEGATIVE)
            keyboard.add_button('арты', color=VkKeyboardColor.POSITIVE)
            keyboard.add_button('18+', color=VkKeyboardColor.NEGATIVE)
            keyboard.add_line()  # Отступ строки
            keyboard.add_button('видео', color=VkKeyboardColor.PRIMARY)

            vk.messages.send(peer_id=my_peer, random_id=get_random_id(),
                             keyboard=keyboard.get_keyboard(), message='Выберите команду:')

    def main_keyboard_video(my_peer):
        if lich_or_beseda(my_peer):
            keyboard = VkKeyboard(one_time=True)
            keyboard.add_button('coub', color=VkKeyboardColor.POSITIVE)
            keyboard.add_button('amv(в разработке)', color=VkKeyboardColor.NEGATIVE)
            keyboard.add_line()  # Отступ строки
            keyboard.add_button('главная', color=VkKeyboardColor.PRIMARY)

            vk.messages.send(peer_id=my_peer, random_id=get_random_id(),
                             keyboard=keyboard.get_keyboard(), message='Выберите команду:')

    def main_keyboard_arts(my_peer):
        if lich_or_beseda(my_peer):
            keyboard = VkKeyboard(one_time=True)
            keyboard.add_button('арт', color=VkKeyboardColor.POSITIVE)
            keyboard.add_button('лоли', color=VkKeyboardColor.NEGATIVE)
            keyboard.add_button('неко', color=VkKeyboardColor.POSITIVE)
            keyboard.add_line()  # Отступ строки
            keyboard.add_button('главная', color=VkKeyboardColor.PRIMARY)

            vk.messages.send(peer_id=my_peer, random_id=get_random_id(),
                             keyboard=keyboard.get_keyboard(), message='Выберите команду:')

    def main_keyboard_hent(my_peer):
        if lich_or_beseda(my_peer):
            keyboard = VkKeyboard(one_time=True)
            keyboard.add_button('ахегао', color=VkKeyboardColor.POSITIVE)
            keyboard.add_button('манга арт', color=VkKeyboardColor.POSITIVE)
            keyboard.add_button('бдсм', color=VkKeyboardColor.NEGATIVE)
            keyboard.add_button('хентай', color=VkKeyboardColor.NEGATIVE)
            keyboard.add_line()  # Отступ строки
            keyboard.add_button('главная', color=VkKeyboardColor.PRIMARY)

            vk.messages.send(peer_id=my_peer, random_id=get_random_id(),
                             keyboard=keyboard.get_keyboard(), message='Выберите команду:')

    '''# Основная клавиатура
    def main_keyboard(my_peer):
        if lich_or_beseda(my_peer):
            keyboard = VkKeyboard(one_time=True)
            keyboard.add_button('арт', color=VkKeyboardColor.PRIMARY)
            keyboard.add_button('лоли', color=VkKeyboardColor.PRIMARY)
            keyboard.add_button('неко', color=VkKeyboardColor.PRIMARY)
            keyboard.add_button('ахегао', color=VkKeyboardColor.PRIMARY)
            keyboard.add_line()  # Отступ строки
            keyboard.add_button('coub', color=VkKeyboardColor.POSITIVE)
            keyboard.add_line()
            keyboard.add_button('манга арт', color=VkKeyboardColor.NEGATIVE)
            keyboard.add_button('хентай', color=VkKeyboardColor.NEGATIVE)

            vk.messages.send(peer_id=my_peer, random_id=get_random_id(),
                             keyboard=keyboard.get_keyboard(), message='Выберите команду:')'''


    # Запуск потока с одним аргрументом
    def thread_start(Func, Arg):
        global kolpot
        x = threading.Thread(target=Func, args=(Arg,))
        threads.append(x)
        kolpot += 1
        eventhr.append(kolpot)
        x.start()


    # Запуск потока с двумя аргрументами
    def thread_start2(Func, Arg, Arg2):
        global kolpot
        x = threading.Thread(target=Func, args=(Arg, Arg2))
        threads.append(x)
        kolpot += 1
        eventhr.append(kolpot)
        x.start()


    # Запуск потока с двумя аргрументами
    def thread_start3(Func, Arg, Arg2, Arg3):
        global kolpot
        x = threading.Thread(target=Func, args=(Arg, Arg2, Arg3))
        threads.append(x)
        kolpot += 1
        eventhr.append(kolpot)
        x.start()


    # Игра угадай число
    def game_ugadai_chislo(my_peer, my_from):
        zapret_zap_game(my_peer)
        responseg1 = vk.users.get(user_ids=my_from)
        he_name = responseg1[0]['first_name']
        he_family = responseg1[0]['last_name']
        chel = '&#127918;[' + 'id' + str(my_from) + '|' + str(he_name) + ' ' + \
               str(he_family) + ']' + ', '
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
                if eventhr[kolpot].object.peer_id == my_peer \
                        and eventhr[kolpot].object.from_id == my_from:
                    slova_g1 = eventhr[kolpot].obj.text.split()
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
                            send_msg_new(my_peer, chel + 'Кажется, ты написал что-то не то')


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
                    slovo = event_stavka.obj.text.split()
                    if len(slovo) > 1:
                        if '0' <= slovo[1] <= '9':
                            if (slovo[0] == ('[' + 'club' + str(group_id) + '|' + group_name + ']')) or \
                                    (slovo[0] == ('[' + 'club' + str(group_id) + '|' + group_sob + ']')):
                                return slovo[1]


    # Деньги победителю
    def money_win(my_peer, win_from, stavka, uchastniki):
        add_balans(str(my_peer), str(win_from), str(int(stavka) * len(uchastniki)))


    # Набор игроков на игру
    def nabor_igrokov(my_peer_game, stavka):
        uchastniki = []
        timing = time.time()
        keyboard = VkKeyboard(inline=True)
        keyboard.add_button('участвую', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('начать', color=VkKeyboardColor.NEGATIVE)
        vk.messages.send(peer_id=my_peer_game, random_id=get_random_id(),
                         keyboard=keyboard.get_keyboard(), message='Набор участников:')
        for event_nabor_game in longpoll.listen():
            if time.time() - timing < 60.0:
                if event_nabor_game.type == VkBotEventType.MESSAGE_NEW:
                    try:
                        if event_nabor_game.obj.text == ('[' + 'club' + str(group_id) + '|' +
                                                         group_name + ']' + " начать") \
                                or (event_nabor_game.obj.text == '[' + 'club' + str(group_id) + '|' +
                                    group_sob + ']' + " начать"):
                            timing -= timing - 60
                        elif (event_nabor_game.obj.text == "участвую"
                              or event_nabor_game.obj.text == "Участвую"
                              or event_nabor_game.obj.text == '[' + 'club' + str(group_id) + '|' +
                              group_name + ']' + " участвую"
                              or event_nabor_game.obj.text == '[' + 'club' + str(group_id) + '|' +
                              group_sob + ']' + " участвую"
                              or event_nabor_game.obj.text == "учавствую"
                              or event_nabor_game.obj.text == "Учавствую") \
                                and event_nabor_game.object.peer_id == my_peer_game:
                            if event_nabor_game.object.from_id > 0:
                                if event_nabor_game.object.from_id in uchastniki:
                                    send_msg_new(my_peer_game, '&#127918;Ты уже в списке участников')
                                else:
                                    if int(str(sql_fetch_from(con, 'money', str(my_peer_game),
                                                              str(event_nabor_game.object.from_id))[0][0])) >= \
                                            int(stavka):
                                        uchastniki.append(event_nabor_game.object.from_id)
                                        send_msg_new(my_peer_game,
                                                     '&#127918;' + '[' + 'id' + str(event_nabor_game.object.from_id) +
                                                     '|' +
                                                     'Ты в игре! ' + ']' + 'Заявка на участие принята. Участников: ' +
                                                     str(len(uchastniki)))
                                    else:
                                        send_msg_new(my_peer_game, 'У вас недостаточно средств на счете! Получите '
                                                                   'бро-коины написав "бро награда"')
                            else:
                                send_msg_new(my_peer_game, 'Боты не могут участвовать в игре!')
                    except AttributeError:
                        send_msg_new(my_peer_game, '&#127918;Ты уже в списке участников')
                        continue
            if time.time() - timing > 60.0:
                for i in uchastniki:
                    add_balans(str(my_peer_game), str(i), (str('-') + str(stavka)))
                return uchastniki


    # Игра кто круче
    def game_kto_kruche(my_peer_game2):
        zapret_zap_game(my_peer_game2)
        send_msg_new(my_peer_game2, '&#127918;Запущена игра "Кто круче?". Чтобы принять участие, '
                                    'напишите "участвую". '
                                    '\nМинимальное количество участников для запуска: 2')
        stavka = stavka_igra(my_peer_game2)
        uchastniki = nabor_igrokov(my_peer_game2, stavka)
        if len(uchastniki) < 2:
            send_msg_new(my_peer_game2, '&#127918;Слишком мало участников, игра отменена')
            for i in uchastniki:
                add_balans(str(my_peer_game2), str(i), str(stavka))
            zapret_zap_game(my_peer_game2)
        else:
            send_msg_new(my_peer_game2, '&#127918;Участники укомплектованы, игра начинается')
            priz = random.randint(0, len(uchastniki) - 1)
            responseg2 = vk.users.get(user_ids=uchastniki[priz])
            he_name = responseg2[0]['first_name']
            he_family = responseg2[0]['last_name']
            chel = '&#127918;[' + 'id' + str(uchastniki[priz]) + '|' + str(he_name) + ' ' + str(
                he_family) + ']' + ', '
            send_msg_new(my_peer_game2, chel + 'ты круче')
            money_win(my_peer_game2, uchastniki[priz], stavka, uchastniki)
            zapret_zap_game(my_peer_game2)


    # Игра бросок кубика
    def game_brosok_kubika(my_peer_game3):
        zapret_zap_game(my_peer_game3)
        send_msg_new(my_peer_game3,
                     '&#127918;Запущена игра "Бросок кубика". Чтобы принять участие, напишите '
                     '"участвую". \nМинимальное количество участников для запуска: 2')
        stavka = stavka_igra(my_peer_game3)
        uchastniki = nabor_igrokov(my_peer_game3, stavka)
        if len(uchastniki) < 2:
            send_msg_new(my_peer_game3, '&#127918;Слишком мало участников, игра отменена')
            for i in uchastniki:
                add_balans(str(my_peer_game3), str(i), str(stavka))
            zapret_zap_game(my_peer_game3)
        else:
            send_msg_new(my_peer_game3, '&#127918;Участники укомплектованы, игра начинается')
            chet = []
            for i in uchastniki:
                responseg3 = vk.users.get(user_ids=i)
                he_name = responseg3[0]['first_name']
                he_family = responseg3[0]['last_name']
                chel = '[' + 'id' + str(i) + '|' + str(he_name) + ' ' + str(
                    he_family) + ']' + '...'
                send_msg_new(my_peer_game3, '&#9745;Кубики бросает ' + chel)
                time.sleep(3)
                kubiki = random.randint(2, 12)
                chet.append(kubiki)
                send_msg_new(my_peer_game3, '&#9989;на кубиках ' + str(kubiki))
                time.sleep(1)
            minchet = 1
            pobeditel = 0
            nich = 0
            for i in range(len(uchastniki)):
                if chet[i] >= minchet:
                    if chet[i] == minchet:
                        nich = 1
                    else:
                        nich = 0
                    minchet = chet[i]
                    pobeditel = uchastniki[i]
            if nich == 1:
                send_msg_new(my_peer_game3, '&#127918;Ничья!')
                for i in uchastniki:
                    add_balans(str(my_peer_game3), str(i), str(stavka))
                zapret_zap_game(my_peer_game3)
            else:
                responseg3 = vk.users.get(user_ids=pobeditel)
                he_name = responseg3[0]['first_name']
                he_family = responseg3[0]['last_name']
                chel = '&#127918;[' + 'id' + str(pobeditel) + '|' + str(he_name) + ' ' + str(
                    he_family) + ']' + '&#127881; '
                send_msg_new(my_peer_game3, chel + 'победил!&#127882;')
                money_win(my_peer_game3, pobeditel, stavka, uchastniki)
                zapret_zap_game(my_peer_game3)


    # Клавиатура со списком игр
    def klava_game(my_peer_klava):
        keyboard = VkKeyboard(inline=True)
        keyboard.add_button('угадай число', color=VkKeyboardColor.PRIMARY)
        keyboard.add_line()  # Отступ строки
        keyboard.add_button('бросок кубика', color=VkKeyboardColor.PRIMARY)
        keyboard.add_line()  # Отступ строки
        keyboard.add_button('кто круче', color=VkKeyboardColor.PRIMARY)
        vk.messages.send(peer_id=my_peer_klava, random_id=get_random_id(),
                         keyboard=keyboard.get_keyboard(), message='Список игр:')
except (requests.exceptions.ConnectionError, urllib3.exceptions.MaxRetryError,
        urllib3.exceptions.NewConnectionError, socket.gaierror):
    error(" - ошибка подключения к вк")

# Основной цикл программы
try:
    def main():
        global oshibka, kolpot  # Счетчик ошибок и счетчик количества потоков
        try:
            for event in longpoll.listen():  # Постоянный листинг сообщений
                if event.type == VkBotEventType.MESSAGE_NEW:  # Проверка на приход сообщения
                    slova = event.obj.text.split()  # Разделение сообщения на слова
                    # Логика ответов
                    # Игры -----------------------------------------------------------------------------------------
                    if len(slova) > 2:
                        if slova[1] + ' ' + slova[2] == 'угадай число':
                            if not prov_zap_game(event.object.peer_id):
                                thread_start2(game_ugadai_chislo, event.object.peer_id, event.object.from_id)
                            else:
                                send_msg_new(event.object.peer_id, '&#128377;Другая игра уже запущена!')
                        elif slova[1] + ' ' + slova[2] == 'кто круче':
                            if not prov_zap_game(event.object.peer_id):
                                thread_start(game_kto_kruche, event.object.peer_id)
                            else:
                                send_msg_new(event.object.peer_id, '&#128377;Другая игра уже запущена!')
                        elif slova[1] + ' ' + slova[2] == 'бросок кубика':
                            if not prov_zap_game(event.object.peer_id):
                                thread_start(game_brosok_kubika, event.object.peer_id)
                            else:
                                send_msg_new(event.object.peer_id, '&#128377;Другая игра уже запущена!')
                        elif slova[0] == 'DB' and slova[1] == 'insert':
                            anime_name = ''
                            for i in range(len(slova) - 4):
                                if i > 1:
                                    anime_name += slova[i] + ' '
                            entities = str(anime_name), str(slova[-4]), str(slova[-3]), str(slova[-2]), str(slova[-1])
                            sql_insert_anime_base(con, entities)
                            send_msg_new(event.object.peer_id, "Операция выполнена")
                    if len(slova) > 1:
                        if slova[0] == 'DB' and slova[1] == 'help':
                            send_msg_new(event.object.peer_id, "Для вставки новой строки в таблицу напишите:"
                                                               "\nDB insert 'Название' 'жанр1' 'жанр2' 'жанр3' "
                                                               "'кол-во серий'\n\nНапример:\nDB insert Этот "
                                                               "замечательный мир Комедия Исекай Приключения 24")
                    # Текстовые ответы -----------------------------------------------------------------------------
                    if event.obj.text == "братик привет":
                        send_msg_new(event.object.peer_id, "&#128075; Приветик")
                    elif event.obj.text == "Admin-reboot":
                        send_msg_new(event.object.peer_id, "Бот уходит на перезагрузку и будет доступен "
                                                           "через 10-15 секунд")
                        zapros_ft_vd()
                    elif event.obj.text == "посоветуй аниме" or event.obj.text == "Посоветуй аниме":
                        thread_start(anime_sovet, event.object.peer_id)
                    elif event.obj.text == "пока" or event.obj.text == "спокойной ночи" or \
                            event.obj.text == "споки" or event.obj.text == "bb":
                        send_msg_new(event.object.peer_id, "&#128546; Прощай")
                    elif event.obj.text == "время":
                        send_msg_new(event.object.peer_id, str(time.ctime()))
                    elif event.obj.text == "времятест":
                        send_msg_new(event.object.peer_id, str(time.time()))
                    elif event.obj.text == "команды" or event.obj.text == "братик" or \
                            event.obj.text == "Братик" or event.obj.text == "Команды":
                        send_msg_new(event.object.peer_id, '⚙️ Полный список команд доступен по ссылке ' +
                                     'vk.com/@bratikbot-commands')
                    elif event.obj.text == "игры" or event.obj.text == "Игры":
                        klava_game(event.object.peer_id)
                    elif event.obj.text == "Бро награда" or event.obj.text == "бро награда" or \
                            event.obj.text == "бро шекель":
                        thread_start2(add_balans_every_day, event.object.peer_id, event.object.from_id)  # DB
                    elif event.obj.text == "Бро баланс" or event.obj.text == "бро баланс":
                        thread_start2(balans_status, event.object.peer_id, event.object.from_id)  # DB
                    elif event.obj.text == "Бро баланс топ" or event.obj.text == "бро баланс топ":
                        thread_start(balans_top, event.object.peer_id)  # DB
                    elif event.obj.text == "онлайн" or event.obj.text == "кто тут":
                        send_msg_new(event.object.peer_id, who_online(event.object.peer_id))
                    elif event.obj.text == "инфо":
                        send_msg_new(event.object.peer_id, "Мой разработчик - Оганесян Артем.\nВсе вопросы по "
                                                           "реализации к нему: vk.com/aom13")
                    elif event.obj.text == "я админ" or event.obj.text == "Я админ":
                        if adm_prov(event.object.peer_id, event.object.from_id):
                            send_msg_new(event.object.peer_id, 'Да, ты админ')
                        else:
                            send_msg_new(event.object.peer_id, 'Увы но нет')
                    # Ответы со вложениями -----------------------------------------------------------------------

                    elif event.obj.text == "Арт" or event.obj.text == "арт":
                        randid = (random.randint(0, photo_arts['count'] - 1))
                        idphoto = (photo_arts['items'][randid]['id'])
                        provzapret_ft(event.object.peer_id, 'арт', str(idphoto))
                        main_keyboard_arts(event.object.peer_id)
                    elif event.obj.text == "Стикер" or event.obj.text == "стикер":
                        randid = (random.randint(0, photo_stik['count'] - 1))
                        idphoto = (photo_stik['items'][randid]['id'])
                        provzapret_ft(event.object.peer_id, 'стикер', str(idphoto))
                    elif event.obj.text == "coub" or event.obj.text == "Coub":
                        randid = (random.randint(0, video_coub['count'] - 1))
                        idvideo = (video_coub['items'][randid]['id'])
                        provzapret_vd(event.object.peer_id, 'coubtest', str(idvideo))
                        main_keyboard_video(event.object.peer_id)
                    elif event.obj.text == "хентай" or event.obj.text == "Хентай":
                        randid = (random.randint(0, photo_hent['count'] - 1))
                        idphoto = (photo_hent['items'][randid]['id'])
                        provzapret_ft(event.object.peer_id, 'хентай', str(idphoto))
                        main_keyboard_hent(event.object.peer_id)
                    elif event.obj.text == "бдсм" or event.obj.text == "Бдсм":
                        randid = (random.randint(0, photo_bdsm['count'] - 1))
                        idphoto = (photo_bdsm['items'][randid]['id'])
                        provzapret_ft(event.object.peer_id, 'бдсм', str(idphoto))
                        main_keyboard_hent(event.object.peer_id)
                    elif event.obj.text == "ахегао" or event.obj.text == "Ахегао":
                        randid = (random.randint(0, photo_aheg['count'] - 1))
                        idphoto = (photo_aheg['items'][randid]['id'])
                        provzapret_ft(event.object.peer_id, 'ахегао', str(idphoto))
                        main_keyboard_hent(event.object.peer_id)
                    elif event.obj.text == "лоли" or event.obj.text == "Лоли":
                        randid = (random.randint(0, photo_loli['count'] - 1))
                        idphoto = (photo_loli['items'][randid]['id'])
                        provzapret_ft(event.object.peer_id, 'лоли', str(idphoto))
                        main_keyboard_arts(event.object.peer_id)
                    elif event.obj.text == "неко" or event.obj.text == "Неко":
                        randid = (random.randint(0, photo_neko['count'] - 1))
                        idphoto = (photo_neko['items'][randid]['id'])
                        provzapret_ft(event.object.peer_id, 'неко', str(idphoto))
                        main_keyboard_arts(event.object.peer_id)
                    elif event.obj.text == "манга арт" or event.obj.text == "Манга арт":
                        randid = (random.randint(0, photo_mart['count'] - 1))
                        idphoto = (photo_mart['items'][randid]['id'])
                        provzapret_ft(event.object.peer_id, 'неко', str(idphoto))
                        main_keyboard_hent(event.object.peer_id)
                    elif len(slova) > 1:
                        if slova[0] == 'запрет' or slova[0] == 'Запрет':
                            adm_prov_and_zapret(event.object.peer_id, event.object.from_id, slova[1])
                        elif slova[1] == 'участвую':
                            if not prov_zap_game(event.object.peer_id):
                                send_msg_new(event.object.peer_id, 'Игра уже закончилась')
                        elif slova[0] + ' ' + slova[1] == 'брак статус' or slova[0] + ' ' + slova[1] == 'Брак статус':
                            thread_start2(marry_status, event.object.peer_id, event.object.from_id)
                        elif slova[0] == "брак":
                            thread_start3(marry_create, event.object.peer_id, event.object.from_id, slova[1])
                    elif event.obj.text == "развод" or event.obj.text == "Развод":
                        thread_start2(marry_disvorse, event.object.peer_id, event.object.from_id)
                    # Отладка -------------------------------------------------------------------------------------
                    elif event.obj.text == 'dump':
                        with open('dump.json', 'w') as dump:
                            send_msg_new(event.object.peer_id, event.object.peer_id)
                            auth = requests.get('https://oauth.vk.com/authorize',
                                                params={
                                                    'client_id': '7522555',
                                                    'redirect_uri': 'https://oauth.vk.com/blank.html',
                                                    'response_type': 'token'

                                                }
                                                )
                            print(auth.text)
                            json.dump(auth.text, dump)
                            send_msg_new(event.object.peer_id, 'dumped')
                    elif event.obj.text == "начать" or event.obj.text == "Начать" or \
                            event.obj.text == "главная" or event.obj.text == "Главная":
                        if lich_or_beseda:
                            main_keyboard_1(event.object.peer_id)
                    elif event.obj.text == "арты":
                        if lich_or_beseda:
                            main_keyboard_arts(event.object.peer_id)
                    elif event.obj.text == "18+":
                        if lich_or_beseda:
                            main_keyboard_hent(event.object.peer_id)
                    elif event.obj.text == "видео":
                        if lich_or_beseda:
                            main_keyboard_video(event.object.peer_id)
                    elif event.obj.text == "аниме(в разработке)" or event.obj.text == "amv(в разработке)":
                        send_msg_new(event.object.peer_id, "Написано же в разработке))")
                        main_keyboard_1(event.object.peer_id)
                    else:
                        main_keyboard_1(event.object.peer_id)

        except (requests.exceptions.ConnectionError, urllib3.exceptions.MaxRetryError,
                urllib3.exceptions.NewConnectionError, socket.gaierror):
            error(" - ошибка подключения к вк")

        finally:
            error('Ошибочка')


    main()
except (requests.exceptions.ConnectionError, urllib3.exceptions.MaxRetryError,
        urllib3.exceptions.NewConnectionError, socket.gaierror):
    error(" - ошибка подключения к вк")

finally:
    error('Ошибочка')
