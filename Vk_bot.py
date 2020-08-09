import json
import socket
import threading
import psycopg2
import requests
import urllib3
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
        time.sleep(1.0)
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

    # Авторизация под именем сообщества
    vk_session = vk_api.VkApi(token=API_GROUP_KEY)
    longpoll = VkBotLongPoll(vk_session, group_id)
    vk = vk_session.get_api()

    # Авторизация под именем пользователя
    vk_session_user = vk_api.VkApi(token=API_USER_KEY)
    vk_polzovat = vk_session_user.get_api()

    # Авторизация сервисным токеном
    ser_token = 'c14c6918c14c6918c14c691807c13e8ffacc14cc14c69189e4cb11298fa3a5dff633603'
    client_secret = '3GBA2mEv669lqnF8WZyA'
    vk_session_SERVISE = vk_api.VkApi(app_id=7530210, token=ser_token, client_secret=client_secret)
    vk_session_SERVISE.server_auth()
    vk_SERVISE = vk_session_SERVISE.get_api()
    vk_session_SERVISE.token = {'access_token': ser_token, 'expires_in': 0}

    global photo_loli, photo_neko, photo_arts, photo_hent, photo_aheg, photo_stik, photo_mart, video_coub, photo_bdsm, \
        photo_ur18


    # Отправка запросов на информацию об фотографиях и видео в группе
    def zapros_ft_vd():
        global photo_loli, photo_neko, photo_arts, photo_hent, photo_aheg, photo_stik, photo_mart, video_coub, \
            photo_bdsm, photo_ur18
        photo_loli = vk_SERVISE.photos.get(owner_id='-' + group_id, album_id=271418270, count=1000)  # Тут находятся
        photo_neko = vk_SERVISE.photos.get(owner_id='-' + group_id, album_id=271449419, count=1000)  # альбомы группы
        photo_arts = vk_SERVISE.photos.get(owner_id='-' + group_id, album_id=271418213, count=1000)  # и их id
        photo_hent = vk_SERVISE.photos.get(owner_id='-' + group_id, album_id=271418234, count=1000)  # по которым внизу
        photo_aheg = vk_SERVISE.photos.get(owner_id='-' + group_id, album_id=271421874, count=1000)  # будут отбираться
        photo_stik = vk_SERVISE.photos.get(owner_id='-' + group_id, album_id=271599613, count=1000)  # фото + 10 сек
        photo_mart = vk_SERVISE.photos.get(owner_id='-' + group_id, album_id=271761499, count=1000)  # к запуску
        photo_bdsm = vk_SERVISE.photos.get(owner_id='-' + group_id, album_id=272201504, count=1000)  #
        photo_ur18 = vk_SERVISE.photos.get(owner_id='-' + group_id, album_id=272411793, count=1000)  #
        video_coub = vk_polzovat.video.get(owner_id='-' + group_id, count=200)  # album_id=1,


    zapros_ft_vd()

    '''
    with open('dump_video.json', 'w') as dump:
        rndid = (random.randint(0, video_coub['count'] - 1))
        print(video_coub['items'][rndid]['id'])
        json.dump(video_coub, dump)
    '''


except (requests.exceptions.ConnectionError, urllib3.exceptions.MaxRetryError,
        urllib3.exceptions.NewConnectionError, socket.gaierror):
    print(" - ошибка подключения к вк")

# Работа с базой данных
try:
    # Соединение с БД
    def sql_connection():
        conc1 = psycopg2.connect(
            database="d67k7fgai9grnr",  # Название базы данных
            user="xwifncxeppnpby",  # Имя пользователя
            password="27a756814e5b031d650bf4a747ed727e507e51c17bce57cb53c8f4f949fee2bd",  # Пароль пользователя
            host="ec2-52-201-55-4.compute-1.amazonaws.com",  # Хост
            port="5432"  # Порт
        )
        return conc1


    # Создание таблицы в БД
    def sql_table(conc3):
        cursorObj4 = conc3.cursor()  # Курсор БД
        cursorObj4.execute("CREATE TABLE clan_info(clan_name text, clan_money text, clan_admin text)")
        conc3.commit()


    con = sql_connection()  # Создание соединения с БД


    # Вставка СТРОКИ в ТАБЛИЦУ peer_params в БД
    def sql_insert(conc2, entities):
        cursorObj3 = conc2.cursor()
        cursorObj3.execute('INSERT INTO peer_params(peer_id, zapusk_game, filter_mata) VALUES(%s, %s, %s)', entities)
        conc2.commit()


    # Вставка СТРОКИ в ТАБЛИЦУ from_params в БД
    def sql_insert_from(conc2, entities):
        cursorObj3 = conc2.cursor()
        cursorObj3.execute(
            'INSERT INTO from_params(peer_id, from_id, money, m_time, warn, marry_id) VALUES(%s, %s, %s, %s, %s, %s)',
            entities)
        conc2.commit()


    # Вставка СТРОКИ в ТАБЛИЦУ from_money в БД
    def sql_insert_clan_info(conc2, entities):
        cursorObj3 = conc2.cursor()
        cursorObj3.execute(
            'INSERT INTO clan_info(clan_name, clan_money, clan_admin) VALUES(%s, %s, %s)',
            entities)
        conc2.commit()


    # Вставка СТРОКИ в ТАБЛИЦУ from_money в БД
    def sql_insert_from_money(conc2, entities):
        cursorObj3 = conc2.cursor()
        cursorObj3.execute(
            'INSERT INTO from_money(from_id, money, m_time, clan_name) VALUES(%s, %s, %s, %s)',
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


    # Обновление параметра в таблице from_money INT
    def sql_update_from_money_int(con6, what_fetch, what_fetch_new, from_id_val):
        cursorObj1 = con6.cursor()
        cursorObj1.execute('UPDATE from_money SET ' + str(what_fetch) + ' = ' + str(what_fetch_new) +
                           ' where from_id = ' + str(from_id_val))
        con6.commit()

        # Обновление параметра в таблице from_money INT


    def sql_update_from_money_text(con6, what_fetch, what_fetch_new, from_id_val):
        cursorObj1 = con6.cursor()  # SELECT CAST ('100' AS INTEGER)
        cursorObj1.execute('UPDATE from_money SET ' + str(what_fetch) + ' = CAST(' + "'" + str(what_fetch_new) + "'"
                           + ' AS varchar)' +
                           ' where from_id = ' + str(from_id_val) + '::int')
        con6.commit()


    # Обновление параметра в таблице clan_info
    def sql_update_clan_info(con6, what_fetch, what_fetch_new, clan_id_val):
        cursorObj1 = con6.cursor()
        cursorObj1.execute('UPDATE clan_info SET ' + str(what_fetch) + ' = CAST(' + "'" + str(what_fetch_new) + "'"
                           + ' AS varchar)' +
                           ' where clan_name = CAST(' + "'" + str(clan_id_val) + "'" + ' AS varchar)')
        con6.commit()


    # Получение параметров из таблицы clan_info
    def sql_fetch_clan_info(conc, what_return, clan_name):
        try:
            cursorObj2 = conc.cursor()
            cursorObj2.execute('SELECT ' + str(what_return) + ' FROM clan_info WHERE clan_name = CAST(' + "'" +
                               str(clan_name) + "'" + ' AS varchar)')
            rows = cursorObj2.fetchall()[0]
            return rows
        except:
            cursorObj2 = conc.cursor()
            cursorObj2.execute("ROLLBACK")
            conc.commit()
            return 'NULL'


    def sql_delite_clan_info(conc, clan_name):
        cursorObj2 = conc.cursor()
        cursorObj2.execute('DELETE FROM clan_info WHERE clan_name = CAST(' + "'" + str(clan_name) +
                           "'" + ' AS varchar)')


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


    # Получение параметров из таблицы from_money
    def sql_fetch_from_money(conc, what_return, from_id):
        cursorObj2 = conc.cursor()
        cursorObj2.execute('SELECT ' + str(what_return) + ' FROM from_money WHERE from_id = ' + str(from_id))
        rows = cursorObj2.fetchall()
        if len(rows) == 0:  # Проверка на наличие записи в таблице и при ее отсутствии, создание новой
            entities = str(from_id), '0', '0', 'NULL'
            sql_insert_from_money(conc, entities)
            rows = sql_fetch_from_money(conc, what_return, from_id)
        return rows


    # Получение параметров из таблицы from_money
    def sql_fetch_from_money_clan(conc, what_return, clan_name):
        cursorObj2 = conc.cursor()
        cursorObj2.execute('SELECT ' + str(what_return) + ' FROM from_money WHERE clan_name = CAST(' + "'" +
                           str(clan_name) + "'" + ' AS varchar)')
        rows = cursorObj2.fetchall()
        return rows


    # Получение параметров из таблицы from_params
    def sql_fetch_from_all(conc, what_return, peer_id_val):
        cursorObj2 = conc.cursor()
        cursorObj2.execute('SELECT ' + str(what_return) + ' FROM from_money')  # WHERE peer_id = ' + str(peer_id_val)
        rows = cursorObj2.fetchall()
        return rows


    # Получение параметров из таблицы from_params
    def sql_fetch_clan_all(conc, what_return):
        cursorObj2 = conc.cursor()
        cursorObj2.execute('SELECT ' + str(what_return) + ' FROM clan_info')
        rows = cursorObj2.fetchall()
        return rows


    # Посоветуй аниме
    def anime_sovet(peer_id):
        time.sleep(1)
        timing = time.time()
        keyboard = VkKeyboard(one_time=True)
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
        cursorObj2.execute('SELECT ' + str('name') + " FROM anime_base WHERE janr = '" + janr + "' OR janr2 = '"
                           + janr + "' OR janr3 = '" + janr + "'")
        rows = cursorObj2.fetchall()
        message = 'Аниме в жанре ' + janr + ':\n'
        for i in rows:
            message += i[0] + '\n'
        send_msg_new(peer_id, message)


    # Вставка строки в таблицу anime_base
    def sql_insert_anime_base(conc2, entities):
        cursorObj3 = conc2.cursor()
        cursorObj3.execute(
            'INSERT INTO anime_base(name, janr, janr2, janr3, series) VALUES(%s, %s, %s, %s, %s)', entities)
        conc2.commit()


    # Обнуление игр во всех беседах
    cursorObj = con.cursor()
    cursorObj.execute('UPDATE peer_params SET zapusk_game = 0')
    con.commit()
except (requests.exceptions.ConnectionError, urllib3.exceptions.MaxRetryError,
        urllib3.exceptions.NewConnectionError, socket.gaierror):
    print(" - ошибка подключения к вк")

# ОСНОВНЫЕ ФУНКЦИИ
try:
    # Инфа о человеке
    def people_info(people_id):
        people = vk.users.get(user_ids=people_id)
        people = str(people[0]['first_name']) + ' ' + str(people[0]['last_name'])
        return people


    def clan_create(my_peer, my_from, clan_name):
        if len(clan_name) >= 3:
            cln_name = str(sql_fetch_from_money(con, 'clan_name', my_from)[0][0])
            if (cln_name == 'NULL' or cln_name is None) and \
                    sql_fetch_clan_info(con, 'clan_name', clan_name[2]) == 'NULL':
                if int(sql_fetch_from_money(con, 'money', my_from)[0][0]) >= 15000:
                    sql_update_from_money_text(con, 'clan_name', clan_name[2], str(my_from))
                    add_balans(my_from, '-15000')
                    entities = str(clan_name[2]), '0', str(my_from)
                    sql_insert_clan_info(con, entities)
                    sql_update_clan_info(con, 'clan_admin', my_from, clan_name[2])
                    send_msg_new(my_peer, 'Клан ' + clan_name[2] + ' успешно создан!')
                else:
                    send_msg_new(my_peer, people_info(my_from) + ', у вас недостаточно монет!')
            else:
                send_msg_new(my_peer, people_info(my_from) + ', вы уже состоите в клане!')
        else:
            send_msg_new(my_peer, 'Для создания клана напишите "Клан создать "название_клана""\n'
                                  'Стоимость создания клана - 15000 монет')


    def chislo_li_eto(chto):
        a = ''
        for i in str(chto):
            if '0' <= str(i) <= '9':
                a += str(i)
            elif str(i) == '-':
                a += str(i)
            else:
                return False
        if a == '':
            return False
        else:
            return True


    def clan_rem_balance(my_peer, my_from, money):
        clan_name = sql_fetch_from_money(con, 'clan_name', my_from)[0][0]
        if clan_name != 'NULL' and clan_name is not None:
            if str(sql_fetch_clan_info(con, 'clan_admin', clan_name)[0]) == str(my_from):
                clan_bals = sql_fetch_clan_info(con, 'clan_money', clan_name)[0]
                if chislo_li_eto(money):
                    if int(clan_bals) >= int(money):
                        clan_add_balance(my_peer, my_from, int(-int(money)))
                        send_msg_new(my_peer, people_info(my_from) + ' вывел из казны клана ' + money + ' монет')
                    else:
                        send_msg_new(my_peer, people_info(my_from) + ', в казне недостаточно монет!')
                else:
                    send_msg_new(my_peer, people_info(my_from) + ', введите правильное число!')
            else:
                send_msg_new(my_peer, people_info(my_from) + ', вы не являетесь адмнистратором клана!')
        else:
            send_msg_new(my_peer, people_info(my_from) + ', вы не состоите в клане!')


    def clan_add_balance(my_peer, my_from, money):
        clan_name = sql_fetch_from_money(con, 'clan_name', my_from)[0][0]
        if clan_name != 'NULL' and clan_name is not None:
            if chislo_li_eto(money):
                if int(sql_fetch_from_money(con, 'money', my_from)[0][0]) >= int(money):
                    add_balans(my_from, int(-int(money)))
                    money_clan = int(sql_fetch_clan_info(con, 'clan_money', clan_name)[0]) + int(money)
                    sql_update_clan_info(con, 'clan_money', money_clan, clan_name)
                    if int(money) > 0:
                        send_msg_new(my_peer, 'Казна клана ' + clan_name + ' пополнена на ' + str(money) + ' монет')
                else:
                    send_msg_new(my_peer, people_info(my_from) + ', у вас недостаточно монет!')
            else:
                send_msg_new(my_peer, people_info(my_from) + ', введите правильное число!')
        else:
            send_msg_new(my_peer, people_info(my_from) + ', вы не состоите в клане!')


    # Баланс клана
    def clan_balance(my_peer, my_from):
        clan_name = sql_fetch_from_money(con, 'clan_name', my_from)[0][0]
        if clan_name != 'NULL' and clan_name is not None:
            money = sql_fetch_clan_info(con, 'clan_money', clan_name)[0]
            send_msg_new(my_peer, 'В казне вашего клана ' + str(money) + ' монет')
        else:
            send_msg_new(my_peer, people_info(my_from) + ', вы не состоите в клане!')


    def clan_info(my_peer, my_from):
        clan_name = sql_fetch_from_money(con, 'clan_name', my_from)[0][0]
        if clan_name != 'NULL' and clan_name is not None:
            send_msg_new(my_peer, people_info(my_from) + ', вы состоите в клане ' + clan_name)
        else:
            send_msg_new(my_peer, people_info(my_from) + ', вы не состоите в клане!')


    # Баланс клана топ
    def clan_balance_top(my_peer):
        idall = sql_fetch_clan_all(con, 'clan_name')
        monall = sql_fetch_clan_all(con, 'clan_money')
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


    def clan_kick(my_peer, my_from, id2):
        clan_name = sql_fetch_from_money(con, 'clan_name', my_from)[0][0]
        our_from = ''
        for i in id2:
            if '0' <= i <= '9':
                our_from += i
            if i == '|':
                break
        if clan_name != 'NULL' and clan_name is not None:
            if sql_fetch_from_money(con, 'clan_name', our_from)[0][0] == clan_name:
                if str(sql_fetch_clan_info(con, 'clan_admin', clan_name)[0]) == str(my_from):
                    sql_update_from_money_text(con, 'clan_name', 'NULL', our_from)
                    send_msg_new(my_peer, people_info(our_from) + ' исключен из клана!')
                else:
                    send_msg_new(my_peer, people_info(my_from) + ', вы не являетесь адмнистратором клана!')
            else:
                send_msg_new(my_peer, people_info(my_from) + ', данный человек не состоит в вашем клане!')
        else:
            send_msg_new(my_peer, people_info(my_from) + ', вы не состоите в клане!')


    def clan_disvorse(my_peer, my_from):
        clan_name = sql_fetch_from_money(con, 'clan_name', my_from)[0][0]
        if clan_name != 'NULL' and clan_name is not None:
            clan_adm = sql_fetch_clan_info(con, 'clan_admin', clan_name)
            if str(clan_adm[0]) == str(my_from):
                clan_members = sql_fetch_from_money_clan(con, 'from_id', clan_name)
                sql_delite_clan_info(con, clan_name)
                for i in clan_members:
                    sql_update_from_money_text(con, 'clan_name', 'NULL', i[0])
                send_msg_new(my_peer, 'Клан ' + clan_name + ' распался')
            else:
                send_msg_new(my_peer, people_info(my_from) + ', вы не являетесь администратором клана!')
        else:
            send_msg_new(my_peer, people_info(my_from) + ', вы не состоите в клане!')


    def clan_leave(my_peer, my_from):
        clan_name = sql_fetch_from_money(con, 'clan_name', my_from)[0][0]
        if clan_name != 'NULL' and clan_name is not None:
            clan_adm = sql_fetch_clan_info(con, 'clan_admin', clan_name)
            if str(clan_adm[0]) == str(my_from):
                send_msg_new(my_peer, people_info(my_from) + ', вы не можете покинуть клан, так как являетесь главой')
            else:
                sql_update_from_money_text(con, 'clan_name', 'NULL', my_from)
                send_msg_new(my_peer, people_info(my_from) + ', вы покинули клан ' + clan_name)
        else:
            send_msg_new(my_peer, people_info(my_from) + ', вы не состоите в клане!')


    def clan_invite(my_peer, my_from, id2):
        clan_name_my = sql_fetch_from_money(con, 'clan_name', my_from)[0][0]
        our_from = ''
        for i in id2:
            if '0' <= i <= '9':
                our_from += i
            if i == '|':
                break
        if our_from != '':
            clan_name_our = sql_fetch_from_money(con, 'clan_name', our_from)[0][0]
            if clan_name_my != 'NULL' and clan_name_my != 'None':
                clan_adm = sql_fetch_clan_info(con, 'clan_admin', clan_name_my)[0]
                if str(clan_adm) == str(my_from):
                    if my_from != our_from:
                        if clan_name_our == 'NULL' or clan_name_our is None:
                            timing = time.time()
                            keyboard = VkKeyboard(inline=True)
                            keyboard.add_button('да', color=VkKeyboardColor.PRIMARY)
                            keyboard.add_button('нет', color=VkKeyboardColor.NEGATIVE)
                            vk.messages.send(peer_id=my_peer, random_id=get_random_id(),
                                             keyboard=keyboard.get_keyboard(),
                                             message=people_info(
                                                 our_from) + ', вы были приглашены в клан ' + clan_name_my
                                                     + '\nВступить в клан?\nПриглашение действует в течении 60 секунд')
                            for eventhr[kolpot] in longpoll.listen():
                                if time.time() - timing > 60.0:
                                    send_msg_new(my_peer, 'Срок действия приглашения истек...')
                                    break
                                if eventhr[kolpot].type == VkBotEventType.MESSAGE_NEW:
                                    if str(eventhr[kolpot].object.peer_id) == str(my_peer) and str(
                                            eventhr[kolpot].object.from_id) == str(our_from):
                                        slova_m = eventhr[kolpot].obj.text.split()
                                        if len(slova_m) == 2:
                                            if slova_m[1] == "да":
                                                sql_update_from_money_text(con, 'clan_name', clan_name_my, our_from)
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
                    send_msg_new(my_peer, people_info(my_from) + ', вы не являетесь администратором клана!')
            else:
                send_msg_new(my_peer, people_info(my_from) + ', вы не состоите в клане!')


    # Статус брака
    def marry_status(my_peer, my_from):
        marry_id = str(sql_fetch_from(con, 'marry_id', my_peer, my_from)[0][0])
        if marry_id == 'None' or marry_id == '0':
            send_msg_new(my_peer, 'Вы не состоите в браке')
        else:
            send_msg_new(my_peer, 'Вы состоите в браке с ' + people_info(marry_id))


    # Развод
    def marry_disvorse(my_peer, my_from):
        marry_id = str(sql_fetch_from(con, 'marry_id', my_peer, my_from)[0][0])
        if str(marry_id) == 'None' or str(marry_id) == '0':
            send_msg_new(my_peer, 'Вы не состоите в браке!')
        else:
            sql_update_from(con, 'marry_id', str('0'), str(my_peer), str(my_from))
            sql_update_from(con, 'marry_id', str('0'), str(my_peer), str(marry_id))
            send_msg_new(my_peer, people_info(my_from) + ' разводится с ' + people_info(marry_id))


    # Создание брака
    def marry_create(my_peer, my_from, id2):
        our_from = ''
        for i in id2:
            if '0' <= i <= '9':
                our_from += i
            if i == '|':
                break
        if str(my_from) == str(our_from):
            send_msg_new(my_peer, 'Ты чо? Дебил? Одиночество? Да? Иди лучше подрочи...')
        else:
            marry_id = str(sql_fetch_from(con, 'marry_id', my_peer, my_from)[0][0])
            marry_id2 = str(sql_fetch_from(con, 'marry_id', my_peer, our_from)[0][0])
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


    def balans_status(my_peer, my_from):
        balans = str(sql_fetch_from_money(con, 'money', my_from)[0][0])
        send_msg_new(my_peer, people_info(my_from) + ', ваш баланс : ' + str(balans) + ' бро-коинов')


    # Баланс топ
    def balans_top(my_peer):
        send_msg_new(my_peer, 'Считаем деньги... Подождите 10 секундочек')
        idall = (str(sql_fetch_from_all(con, 'from_id', my_peer))).split()
        monall = (str(sql_fetch_from_all(con, 'money', my_peer))).split()
        mess = ''
        people = []
        for i in range(len(idall)):
            a = ''
            b = ''
            for j in (idall[i]):
                if '0' <= str(j) <= '9':
                    a += str(j)
            for k in (monall[i]):
                if '0' <= str(k) <= '9':
                    b += str(k)
            people.append([str(a), int(b)])
        people = sorted(people, key=lambda peoples: (-peoples[1]))
        for i in range(len(people)):
            if int(people[i][1]) > 0 and i <= 30:
                if i == 0:
                    mess += '&#128142;'
                elif i == 1:
                    mess += '&#128176;'
                elif i == 2:
                    mess += '&#128179;'
                else:
                    mess += '&#128182;'
                mess += str(i + 1) + '. ' + people_info(people[i][0]) + ' - ' + str(people[i][1]) + ' монет\n'
        send_msg_new(my_peer, mess)


    # Отправка денег от одного участника к другому
    def money_send(my_peer, my_from, our, money):
        try:
            our_from = ''
            for i in our:
                if '0' <= i <= '9':
                    our_from += i
                if i == '|':
                    break
            if our_from != '':
                if int(str(sql_fetch_from_money(con, 'money', str(my_from))[0][0])) >= int(money) > 0:
                    add_balans(str(my_from), '-' + str(money))
                    add_balans(str(our_from), str(money))
                    send_msg_new(my_peer, people_info(my_from) + ' перевел ' +
                                 people_info(our_from) + ' ' + str(money) + ' монет')
                else:
                    send_msg_new(my_peer, people_info(my_from) + ', у вас недостаточно монет!')
            else:
                send_msg_new(my_peer, 'Мне кажется, или ты что-то напутал?!')
        except ValueError:
            send_msg_new(my_peer, 'Мне кажется, или ты что-то напутал?!')


    # Зачисление ежедневного вознаграждения
    def add_balans_every_day(my_peer, my_from):
        balans_time = int(sql_fetch_from_money(con, 'm_time', my_from)[0][0])
        if balans_time < (time.time() - 8 * 60 * 60):
            add_balans(my_from, 1000)
            send_msg_new(my_peer, 'Вам было зачисленно 1000 бро-коинов!')
            sql_update_from_money_int(con, 'm_time', str(time.time()), str(my_from))
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
            send_msg_new(my_peer, 'Бро-коины можно получить не чаще, чем 1 раз в 8 часов! Осталось времени: '
                         + balans_hour + balans_minut + balans_second)


    # Добавление n-ой суммы на баланс
    def add_balans(my_from, zp_balans):
        balans = int(sql_fetch_from_money(con, 'money', my_from)[0][0])
        balans += int(zp_balans)
        sql_update_from_money_int(con, 'money', str(balans), str(my_from))


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
            vk.messages.send(peer_id=my_peer, random_id=get_random_id(),
                             keyboard=keyboard.get_keyboard(), message='Выберите команду:')


    def main_keyboard_video(my_peer):
        if lich_or_beseda(my_peer):
            keyboard = VkKeyboard(one_time=False)
            keyboard.add_button('coub', color=VkKeyboardColor.POSITIVE)
            # keyboard.add_button('amv(в разработке)', color=VkKeyboardColor.NEGATIVE)
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
            keyboard.add_button('хентай', color=VkKeyboardColor.NEGATIVE)
            keyboard.add_line()  # Отступ строки
            keyboard.add_button('главная', color=VkKeyboardColor.PRIMARY)
            vk.messages.send(peer_id=my_peer, random_id=get_random_id(),
                             keyboard=keyboard.get_keyboard(), message='Выбрана команда хентай, выберите команду:')


    # Запуск потока без аргрументов
    def thread_start0(Func):
        global kolpot
        x = threading.Thread(target=Func)
        threads.append(x)
        kolpot += 1
        eventhr.append(kolpot)
        x.start()


    # Запуск потока с одним аргрументом
    def thread_start1(Func, Arg):
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


    # Запуск потока с двумя аргрументами
    def thread_start4(Func, Arg, Arg2, Arg3, Arg4):
        global kolpot
        x = threading.Thread(target=Func, args=(Arg, Arg2, Arg3, Arg4))
        threads.append(x)
        kolpot += 1
        eventhr.append(kolpot)
        x.start()


    # Игра угадай число
    def game_ugadai_chislo(my_peer, my_from):
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
                    slovo = event_stavka.obj.text.split()
                    if len(slovo) > 1:
                        if '0' <= slovo[1] <= '9':
                            send_msg_new(my_peer, 'Ставка: ' + str(slovo[1]))
                            return slovo[1]
            else:
                return 0


    # Деньги победителю
    def money_win(win_from, stavka, uchastniki):
        add_balans(str(win_from), str(int(stavka) * len(uchastniki)))


    # Набор игроков на игру
    def nabor_igrokov(my_peer_game, stavka):
        uchastniki = []
        timing = time.time()
        keyboard = VkKeyboard(one_time=False)
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
                                    if int(str(sql_fetch_from_money(con, 'money',
                                                                    str(event_nabor_game.object.from_id))[0][0])) >= \
                                            int(stavka):
                                        uchastniki.append(event_nabor_game.object.from_id)
                                        send_msg_new(my_peer_game,
                                                     '&#127918;' + people_info(event_nabor_game.object.from_id)
                                                     + ', заявка на участие принята. Участников: ' +
                                                     str(len(uchastniki)))
                                    else:
                                        send_msg_new(my_peer_game, people_info(event_nabor_game.object.from_id) +
                                                     ', у вас недостаточно средств на счете! Получите '
                                                     'бро-коины написав "бро награда"')
                            else:
                                send_msg_new(my_peer_game, 'Боты не могут участвовать в игре!')
                    except AttributeError:
                        send_msg_new(my_peer_game, '&#127918;' + people_info(event_nabor_game.object.from_id)
                                     + 'Ты уже в списке участников')
                        continue
            if time.time() - timing > 60.0:
                keyboard = VkKeyboard(one_time=True)
                keyboard.add_button('Не забудьте подписаться на бота', color=VkKeyboardColor.POSITIVE)
                vk.messages.send(peer_id=my_peer_game, random_id=get_random_id(),
                                 keyboard=keyboard.get_keyboard(), message='&#127918;Участники укомплектованы, '
                                                                           'игра начинается')
                for i in uchastniki:
                    add_balans(str(i), (str('-') + str(stavka)))
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
                add_balans(str(i), str(stavka))
            zapret_zap_game(my_peer_game2)
        else:
            send_msg_new(my_peer_game2, '&#127918;Участники укомплектованы, игра начинается')
            priz = random.randint(0, len(uchastniki) - 1)
            chel = '&#127918;' + people_info(str(uchastniki[priz])) + ', '
            send_msg_new(my_peer_game2, chel + 'ты круче')
            money_win(uchastniki[priz], stavka, uchastniki)
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
                add_balans(str(i), str(stavka))
            zapret_zap_game(my_peer_game3)
        else:
            chet = []
            for i in uchastniki:
                send_msg_new(my_peer_game3, '&#9745;Кубики бросает ' + people_info(str(i)) + '...')
                time.sleep(2)
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
                    add_balans(str(i), str(stavka))
                zapret_zap_game(my_peer_game3)
            else:
                send_msg_new(my_peer_game3, '&#127918;' + people_info(pobeditel) + '&#127881; ' + 'победил!&#127882;')
                money_win(pobeditel, stavka, uchastniki)
                zapret_zap_game(my_peer_game3)


    def game_mat_victorina(my_peer, my_from):
        if int(str(sql_fetch_from_money(con, 'money', str(my_from))[0][0])) >= int(300):
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
                send_msg_new(my_peer, 'Сколько будет ' + str(a) + znak + str(b) + ' ?')
                uravnenie = a + b
                for event_victorina_game in longpoll.listen():
                    if time.time() - timing < 15.0:
                        if event_victorina_game.type == VkBotEventType.MESSAGE_NEW:
                            if event_victorina_game.object.from_id == my_from:
                                if event_victorina_game.obj.text == str(uravnenie):
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
                                    if event_victorina_game.object.from_id == my_from:
                                        if event_victorina_game.obj.text == ('[' + 'club' + str(group_id) + '|' +
                                                                             group_name + ']' + " забрать деньги") \
                                                or (event_victorina_game.obj.text == '[' + 'club' + str(group_id) + '|'
                                                    + group_sob + ']' + " забрать деньги"):
                                            add_balans(my_from, dengi)
                                            stop = 1
                                            send_msg_new(my_peer, 'Вы выйграли ' + str(dengi) + ' монет')
                                            break
                                        elif event_victorina_game.obj.text == ('[' + 'club' + str(group_id) + '|' +
                                                                               group_name + ']' + " продолжить") \
                                                or (
                                                event_victorina_game.obj.text == '[' + 'club' + str(group_id) + '|' +
                                                group_sob + ']' + " продолжить"):
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


    # Клавиатура со списком игр
    def klava_game(my_peer_klava):
        keyboard = VkKeyboard(inline=True)
        keyboard.add_button('угадай число', color=VkKeyboardColor.PRIMARY)
        keyboard.add_line()  # Отступ строки
        keyboard.add_button('бросок кубика', color=VkKeyboardColor.PRIMARY)
        keyboard.add_line()  # Отступ строки
        keyboard.add_button('кто круче', color=VkKeyboardColor.PRIMARY)
        keyboard.add_line()  # Отступ строки
        keyboard.add_button('математическая викторина', color=VkKeyboardColor.PRIMARY)
        vk.messages.send(peer_id=my_peer_klava, random_id=get_random_id(),
                         keyboard=keyboard.get_keyboard(), message='Список игр:')
except (requests.exceptions.ConnectionError, urllib3.exceptions.MaxRetryError,
        urllib3.exceptions.NewConnectionError, socket.gaierror):
    print(" - ошибка подключения к вк")

# Основной цикл программы
try:
    def main():
        global oshibka, kolpot  # Счетчик ошибок и счетчик количества потоков
        try:
            for event in longpoll.listen():  # Постоянный листинг сообщений
                if event.type == VkBotEventType.MESSAGE_NEW:  # Проверка на приход сообщения
                    if event.object.from_id > 0:
                        def messege_chek(peer_id, from_id, text):
                            slova = event.obj.text.split()  # Разделение сообщения на слова
                            # Логика ответов
                            # Игры --------------------------------------------------------------------------------------
                            if len(slova) > 2:
                                if slova[1] + ' ' + slova[2] == 'угадай число':
                                    if not prov_zap_game(peer_id):
                                        thread_start2(game_ugadai_chislo, peer_id, from_id)
                                    else:
                                        send_msg_new(peer_id, '&#128377;Другая игра уже запущена!')
                                elif slova[1] + ' ' + slova[2] == 'кто круче':
                                    if not prov_zap_game(peer_id):
                                        thread_start1(game_kto_kruche, peer_id)
                                    else:
                                        send_msg_new(peer_id, '&#128377;Другая игра уже запущена!')
                                elif slova[1] + ' ' + slova[2] == 'бросок кубика':
                                    if not prov_zap_game(peer_id):
                                        thread_start1(game_brosok_kubika, peer_id)
                                    else:
                                        send_msg_new(peer_id, '&#128377;Другая игра уже запущена!')
                                elif slova[1] + ' ' + slova[2] == 'математическая викторина':
                                    if not prov_zap_game(peer_id):
                                        thread_start2(game_mat_victorina, peer_id, from_id)
                                    else:
                                        send_msg_new(peer_id, '&#128377;Другая игра уже запущена!')
                                elif slova[0] == 'DB' and slova[1] == 'insert':
                                    anime_name = ''
                                    for i in range(len(slova) - 4):
                                        if i > 1:
                                            anime_name += slova[i] + ' '
                                    entities = str(anime_name), str(slova[-4]), str(slova[-3]), \
                                               str(slova[-2]), str(slova[-1])
                                    sql_insert_anime_base(con, entities)
                                    send_msg_new(peer_id, "Операция выполнена")

                            if len(slova) > 1:
                                if slova[0] == 'DB' and slova[1] == 'help':
                                    send_msg_new(peer_id, "Для вставки новой строки в таблицу напишите:"
                                                          "\nDB insert 'Название' 'жанр1' 'жанр2' 'жанр3' "
                                                          "'кол-во серий'\n\nНапример:\nDB insert Этот "
                                                          "замечательный мир Комедия Исекай Приключения 24")

                                elif slova[0] + ' ' + slova[1] == 'Клан создать':
                                    thread_start3(clan_create, peer_id, from_id, slova)
                                elif slova[0] + ' ' + slova[1] == 'Клан распад':
                                    thread_start2(clan_disvorse, peer_id, from_id)
                                elif slova[0] + ' ' + slova[1] == 'Клан кик':
                                    thread_start3(clan_kick, peer_id, from_id, slova[2])
                                elif slova[0] + ' ' + slova[1] == 'Клан покинуть':
                                    thread_start2(clan_leave, peer_id, from_id)
                                elif slova[0] + ' ' + slova[1] == 'Клан пригласить':
                                    thread_start3(clan_invite, peer_id, from_id, slova[2])
                                elif len(slova) > 2:
                                    if slova[0] + ' ' + slova[1] + ' ' + slova[2] == 'Клан баланс топ':
                                        thread_start1(clan_balance_top, peer_id)
                                if slova[0] + ' ' + slova[1] == 'Клан баланс':
                                    thread_start2(clan_balance, peer_id, from_id)
                                elif slova[0] + ' ' + slova[1] == 'Клан инфо':
                                    thread_start2(clan_info, peer_id, from_id)
                                elif len(slova) > 3:
                                    if slova[0] + ' ' + slova[1] + ' ' + slova[2] == 'Клан казна пополнить':
                                        thread_start3(clan_add_balance, peer_id, from_id, slova[3])
                                    elif slova[0] + ' ' + slova[1] + ' ' + slova[2] == 'Клан казна вывести':
                                        thread_start3(clan_rem_balance, peer_id, from_id, slova[3])

                            # Текстовые ответы ------------------------------------------------------------------------
                            if len(slova) > 0:
                                if text == "Клан" or text == "Кланы" or text == "Клан помощь" or text == "Кланы помощь":
                                    send_msg_new(peer_id, 'Клановые команды:\n'
                                                          '&#8505;Клан инфо\n'
                                                          '&#127381;Клан создать "название_слитно" |'
                                                          '&#128184;15000 монет\n'
                                                          '&#9209;Клан распад\n'
                                                          '&#9664;Клан покинуть\n'
                                                          '&#9654;Клан пригласить "кого"\n'
                                                          '&#127975;Клан баланс\n'
                                                          '&#128200;Клан баланс топ\n'
                                                          '&#128182;Клан казна пополнить "сумма"\n'
                                                          '&#128183;Клан казна вывести "сумма"')

                                if text == "братик привет":
                                    send_msg_new(peer_id, "&#128075; Приветик")
                                elif text == "Admin-reboot":
                                    send_msg_new(peer_id, "Бот уходит на перезагрузку и будет доступен "
                                                          "через 10-15 секунд")
                                    zapros_ft_vd()
                                elif text == "посоветуй аниме" or text == "Посоветуй аниме":
                                    thread_start1(anime_sovet, peer_id)
                                elif text == "пока" or text == "спокойной ночи" or \
                                        text == "споки" or text == "bb":
                                    send_msg_new(peer_id, "&#128546; Прощай")
                                elif text == "время":
                                    send_msg_new(peer_id, str(time.ctime()))
                                elif text == "времятест":
                                    send_msg_new(peer_id, str(time.time()))
                                elif text == "команды" or text == "братик" or \
                                        text == "Братик" or text == "Команды":
                                    send_msg_new(peer_id, '⚙️ Полный список команд доступен по ссылке ' +
                                                 'vk.com/@bratikbot-commands')
                                elif text == "игры" or text == "Игры":
                                    klava_game(peer_id)
                                elif text == "Бро награда" or text == "бро награда" or \
                                        text == "бро шекель":
                                    thread_start2(add_balans_every_day, peer_id, from_id)  # DB
                                elif text == "Бро баланс" or text == "бро баланс":
                                    thread_start2(balans_status, peer_id, from_id)
                                elif text == "Бро баланс топ" or text == "бро баланс топ":
                                    thread_start1(balans_top, peer_id)  # DB
                                elif text == "онлайн" or text == "кто тут":
                                    send_msg_new(peer_id, who_online(peer_id))
                                elif text == "инфо":
                                    send_msg_new(peer_id, "Мой разработчик - Оганесян Артем.\nВсе вопросы по "
                                                          "реализации к нему: vk.com/aom13")
                                elif text == "я админ" or text == "Я админ":
                                    if adm_prov(peer_id, from_id):
                                        send_msg_new(peer_id, 'Да, ты админ')
                                    else:
                                        send_msg_new(peer_id, 'Увы но нет')
                                # Ответы со вложениями ----------------------------------------------------------------

                                elif text == "Арт" or text == "арт":
                                    randid = (random.randint(0, photo_arts['count'] - 1))
                                    idphoto = (photo_arts['items'][randid]['id'])
                                    provzapret_ft(peer_id, 'арт', str(idphoto))
                                    main_keyboard_arts(peer_id)
                                elif text == "Юри+" or text == "юри+":
                                    randid = (random.randint(0, photo_ur18['count'] - 1))
                                    idphoto = (photo_ur18['items'][randid]['id'])
                                    provzapret_ft(peer_id, 'юри+', str(idphoto))
                                    main_keyboard_hent(peer_id)
                                elif text == "Стикер" or text == "стикер":
                                    randid = (random.randint(0, photo_stik['count'] - 1))
                                    idphoto = (photo_stik['items'][randid]['id'])
                                    provzapret_ft(peer_id, 'стикер', str(idphoto))
                                elif text == "coub" or text == "Coub":
                                    randid = (random.randint(0, video_coub['count'] - 1))
                                    idvideo = (video_coub['items'][randid]['id'])
                                    provzapret_vd(peer_id, 'coubtest', str(idvideo))
                                    main_keyboard_video(peer_id)
                                elif text == "хентай" or text == "Хентай":
                                    randid = (random.randint(0, photo_hent['count'] - 1))
                                    idphoto = (photo_hent['items'][randid]['id'])
                                    provzapret_ft(peer_id, 'хентай', str(idphoto))
                                    main_keyboard_hent(peer_id)
                                elif text == "бдсм" or text == "Бдсм":
                                    randid = (random.randint(0, photo_bdsm['count'] - 1))
                                    idphoto = (photo_bdsm['items'][randid]['id'])
                                    provzapret_ft(peer_id, 'бдсм', str(idphoto))
                                    main_keyboard_hent(peer_id)
                                elif text == "ахегао" or text == "Ахегао":
                                    randid = (random.randint(0, photo_aheg['count'] - 1))
                                    idphoto = (photo_aheg['items'][randid]['id'])
                                    provzapret_ft(peer_id, 'ахегао', str(idphoto))
                                    main_keyboard_hent(peer_id)
                                elif text == "лоли" or text == "Лоли":
                                    randid = (random.randint(0, photo_loli['count'] - 1))
                                    idphoto = (photo_loli['items'][randid]['id'])
                                    provzapret_ft(peer_id, 'лоли', str(idphoto))
                                    main_keyboard_arts(peer_id)
                                elif text == "неко" or text == "Неко":
                                    randid = (random.randint(0, photo_neko['count'] - 1))
                                    idphoto = (photo_neko['items'][randid]['id'])
                                    provzapret_ft(peer_id, 'неко', str(idphoto))
                                    main_keyboard_arts(peer_id)
                                elif text == "манга арт" or text == "Манга арт":
                                    randid = (random.randint(0, photo_mart['count'] - 1))
                                    idphoto = (photo_mart['items'][randid]['id'])
                                    provzapret_ft(peer_id, 'неко', str(idphoto))
                                    main_keyboard_hent(peer_id)
                                elif len(slova) > 1:
                                    if slova[0] == 'запрет' or slova[0] == 'Запрет':
                                        adm_prov_and_zapret(peer_id, from_id, slova[1])
                                    elif slova[1] == 'участвую':
                                        if not prov_zap_game(peer_id):
                                            send_msg_new(peer_id, 'Игра уже закончилась')
                                    elif slova[0] + ' ' + slova[1] == 'брак статус' or slova[0] + ' ' + \
                                            slova[1] == 'Брак статус':
                                        thread_start2(marry_status, peer_id, from_id)
                                    elif slova[0] == "брак":
                                        thread_start3(marry_create, peer_id, from_id, slova[1])
                                    elif slova[0] == "перевести" or slova[0] == "Перевести":
                                        thread_start4(money_send, peer_id, from_id,
                                                      slova[1], slova[2])
                                elif text == "развод" or text == "Развод":
                                    thread_start2(marry_disvorse, peer_id, from_id)
                                # Отладка -----------------------------------------------------------------------------
                                elif text == 'dump':
                                    with open('dump.json', 'w') as dump:
                                        send_msg_new(peer_id, peer_id)
                                        auth = requests.get('https://oauth.vk.com/authorize',
                                                            params={
                                                                'client_id': '7522555',
                                                                'redirect_uri': 'https://oauth.vk.com/blank.html',
                                                                'response_type': 'token'

                                                            }
                                                            )
                                        print(auth.text)
                                        json.dump(auth.text, dump)
                                        send_msg_new(peer_id, 'dumped')
                                elif text == "начать" or text == "Начать" or \
                                        text == "главная" or text == "Главная":
                                    if lich_or_beseda:
                                        main_keyboard_1(peer_id)
                                elif text == "арты":
                                    if lich_or_beseda:
                                        main_keyboard_arts(peer_id)
                                elif text == "18+":
                                    if lich_or_beseda:
                                        main_keyboard_hent(peer_id)
                                elif text == "видео":
                                    if lich_or_beseda:
                                        main_keyboard_video(peer_id)
                                elif text == "аниме(в разработке)" or text == "amv(в разработке)":
                                    send_msg_new(peer_id, "Написано же в разработке))")
                                    main_keyboard_1(peer_id)
                                else:
                                    main_keyboard_1(peer_id)

                        thread_start3(messege_chek, event.object.peer_id, event.object.from_id, event.obj.text)
                    else:
                        send_msg_new(event.object.peer_id, 'Господин бот, охлади свое траханье')
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
