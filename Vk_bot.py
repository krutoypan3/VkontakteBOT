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
    # Импорт API ключа(токена) из отдельного файла
    f = open('C://APIKEY.txt', 'r')
    APIKEYSS = f.read()  # токен нужно поместить в файл выше(путь можно изменить)), изменять только здесь!
    f.close()
    print("Бот работает...")
    group_id = '196288744'  # Указываем id сообщества, изменять только здесь!
    oshibka = 0  # обнуление счетчика ошибок
    threads = list()
    eventhr = []
    kolpot = -1
    group_sob = "@bratikbot"  # Указываем короткое имя бота (если нет то id)
    group_name = "Братик"  # Указываем название сообщества

    vk_session = vk_api.VkApi(token=APIKEYSS)  # Авторизация под именем сообщества
    longpoll = VkBotLongPoll(vk_session, group_id)
    vk = vk_session.get_api()

    # Авторизация сервисным токеном
    f1 = open('C://ser_token.txt', 'r')
    ser_token = f1.read()
    f1.close()
    f1 = open('C://client_secret.txt', 'r')
    client_secret = f1.read()
    f1.close()
    vk_session_SERVISE = vk_api.VkApi(app_id=7530210,
                                      token=ser_token,
                                      client_secret=client_secret)
    vk_session_SERVISE.server_auth()
    vk_SERVISE = vk_session_SERVISE.get_api()
    vk_session_SERVISE.token = {'access_token': ser_token, 'expires_in': 0}
    photo_loli = vk_SERVISE.photos.get(owner_id='-' + group_id, album_id=271418270, count=1000)  # Тут находятся
    photo_neko = vk_SERVISE.photos.get(owner_id='-' + group_id, album_id=271449419, count=1000)  # альбомы группы
    photo_arts = vk_SERVISE.photos.get(owner_id='-' + group_id, album_id=271418213, count=1000)  # и их id
    photo_hent = vk_SERVISE.photos.get(owner_id='-' + group_id, album_id=271418234, count=1000)  # по которым внизу
    photo_aheg = vk_SERVISE.photos.get(owner_id='-' + group_id, album_id=271421874, count=1000)  # будут отбираться фото
    photo_stik = vk_SERVISE.photos.get(owner_id='-' + group_id, album_id=271599613,
                                       count=1000)  # и скинутся пользователю

    '''
    with open('dump.json', 'w') as dump:
        rndid = (random.randint(0, photo_stik['count']))
        print(photo_stik['items'][rndid]['id'])
        json.dump(photo_loli, dump)
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
        cursorObj4.execute("CREATE TABLE from_params(from_id integer PRIMARY KEY, money integer, warn integer)")
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


    # Статус фильтра мата
    def filter_mata_status(my_peer):
        if str(sql_fetch(con, 'filter_mata', my_peer)[0][0]) == '1':
            return True
        return False


    # Проверка баланса
    def balans_status(my_peer, my_from):
        balans = str(sql_fetch_from(con, 'money', my_peer, my_from)[0][0])
        send_msg_new(my_peer, 'Ваш баланс : ' + str(balans) + ' бро-коинов')


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
    def provzapret(my_peer, chto, idphoto):
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


    # Включение \ Отключение фильтра мата
    def proverka_slov(peer_id_mat, my_from, slova):
        if len(slova) > 1:
            if slova[0] + ' ' + slova[1] == 'фильтр мата' or slova[0] + ' ' + slova[1] == 'Фильтр мата':
                if adm_prov(peer_id_mat, my_from):
                    if str(sql_fetch(con, 'filter_mata', peer_id_mat)[0][0]) == '1':
                        sql_update(con, 'filter_mata', '0', peer_id_mat)
                        send_msg_new(peer_id_mat, 'Фильтр мата отключен')
                    else:
                        sql_update(con, 'filter_mata', '1', peer_id_mat)
                        send_msg_new(peer_id_mat, 'Фильтр мата включен')
                else:
                    send_msg_new(peer_id_mat, 'Как станешь админом, так сразу')


    # Проверка матерных слов в сообщении
    def provbadwordth(my_peer, my_from, slovaf):
        for i in slovaf:
            zap_wordf = open('zap_word.txt', 'r')
            asq = False
            for line in zap_wordf:
                if (str(i)).lower() + '\n' == line:
                    asq = True
            zap_wordf.close()
            if my_from > 0:
                if asq:
                    if str(i) != '':
                        send_msg_new(my_peer, '[' + 'id' + str(my_from) + '|' + 'За мат осуждаю' + ']')
                        break
            else:
                if asq:
                    send_msg_new(my_peer, '[' + 'club' + str(
                        -my_from) + '|' + 'Ты, как бот, подаешь плохой пример' + ']')


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
        main_keyboard(my_peer)


    # Отправка видео с сервера ВК
    def send_vd(my_peer, first_el, end_el):
        vivord = str(random.randint(first_el, end_el))
        vk.messages.send(peer_id=my_peer, random_id=0,
                         attachment='video-' + group_id + '_' + vivord)
        time.sleep(1)
        main_keyboard(my_peer)


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
                return 1
            else:
                return 0
        except vk_api.exceptions.ApiError:
            return 0


    # Основная клавиатура
    def main_keyboard(my_peer):
        if lich_or_beseda(my_peer):
            keyboard = VkKeyboard(one_time=True)
            keyboard.add_button('арт', color=VkKeyboardColor.PRIMARY)
            keyboard.add_button('лоли', color=VkKeyboardColor.PRIMARY)
            keyboard.add_button('неко', color=VkKeyboardColor.PRIMARY)
            keyboard.add_button('ахегао', color=VkKeyboardColor.PRIMARY)
            keyboard.add_line()  # Отступ строки
            keyboard.add_button('хентай', color=VkKeyboardColor.NEGATIVE)
            keyboard.add_line()
            keyboard.add_button('видео', color=VkKeyboardColor.POSITIVE)

            vk.messages.send(peer_id=my_peer, random_id=get_random_id(),
                             keyboard=keyboard.get_keyboard(), message='Выберите команду:')


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


    # Набор игроков на игру
    def nabor_igrokov(my_peer_game):
        uchastniki = []
        timing = time.time()
        keyboard = VkKeyboard(inline=True)
        keyboard.add_button('участвую', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button('начать', color=VkKeyboardColor.NEGATIVE)
        vk.messages.send(peer_id=my_peer_game, random_id=get_random_id(),
                         keyboard=keyboard.get_keyboard(), message='Набор участников:')
        for eventhr[kolpot] in longpoll.listen():
            if time.time() - timing < 60.0:
                if eventhr[kolpot].type == VkBotEventType.MESSAGE_NEW:
                    try:
                        if eventhr[kolpot].obj.text == ('[' + 'club' + str(group_id) + '|' +
                                                        group_name + ']' + " начать") \
                                or (eventhr[kolpot].obj.text == '[' + 'club' + str(group_id) + '|' +
                                    group_sob + ']' + " начать"):
                            timing -= timing - 60
                        elif (eventhr[kolpot].obj.text == "участвую"
                              or eventhr[kolpot].obj.text == "Участвую"
                              or eventhr[kolpot].obj.text == '[' + 'club' + str(group_id) + '|' +
                              group_name + ']' + " участвую"
                              or eventhr[kolpot].obj.text == '[' + 'club' + str(group_id) + '|' +
                              group_sob + ']' + " участвую"
                              or eventhr[kolpot].obj.text == "учавствую"
                              or eventhr[kolpot].obj.text == "Учавствую") \
                                and eventhr[kolpot].object.peer_id == my_peer_game:
                            if eventhr[kolpot].object.from_id > 0:
                                if eventhr[kolpot].object.from_id in uchastniki:
                                    send_msg_new(my_peer_game, '&#127918;Ты уже в списке участников')
                                else:
                                    uchastniki.append(eventhr[kolpot].object.from_id)
                                    send_msg_new(my_peer_game,
                                                 '&#127918;Заявка на участие принята. Участников: ' +
                                                 str(len(uchastniki)))
                            else:
                                send_msg_new(my_peer_game, 'Боты не могут участвовать в игре!')
                    except AttributeError:
                        send_msg_new(my_peer_game, '&#127918;Ты уже в списке участников')
                        continue
            if time.time() - timing > 60.0:
                return uchastniki


    # Игра кто круче
    def game_kto_kruche(my_peer_game2):
        zapret_zap_game(my_peer_game2)
        send_msg_new(my_peer_game2, '&#127918;Запущена игра "Кто круче?". Чтобы принять участие, '
                                    'напишите "участвую". '
                                    '\nМинимальное количество участников для запуска: 2')
        uchastniki = nabor_igrokov(my_peer_game2)
        if len(uchastniki) < 2:
            send_msg_new(my_peer_game2, '&#127918;Слишком мало участников, игра отменена')
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
            zapret_zap_game(my_peer_game2)


    # Игра бросок кубика
    def game_brosok_kubika(my_peer_game3):
        zapret_zap_game(my_peer_game3)
        send_msg_new(my_peer_game3,
                     '&#127918;Запущена игра "Бросок кубика". Чтобы принять участие, напишите '
                     '"участвую". \nМинимальное количество участников для запуска: 2')
        uchastniki = nabor_igrokov(my_peer_game3)
        if len(uchastniki) < 2:
            send_msg_new(my_peer_game3, '&#127918;Слишком мало участников, игра отменена')
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
                zapret_zap_game(my_peer_game3)
            else:
                responseg3 = vk.users.get(user_ids=pobeditel)
                he_name = responseg3[0]['first_name']
                he_family = responseg3[0]['last_name']
                chel = '&#127918;[' + 'id' + str(pobeditel) + '|' + str(he_name) + ' ' + str(
                    he_family) + ']' + '&#127881; '
                send_msg_new(my_peer_game3, chel + 'победил!&#127882;')
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
                    if filter_mata_status(event.object.peer_id):  # Проверка чата на матерные слова
                        thread_start3(provbadwordth, event.object.peer_id, event.object.from_id, slova)
                    thread_start3(proverka_slov, event.object.peer_id, event.object.from_id, slova)
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
                    # Текстовые ответы -----------------------------------------------------------------------------
                    if event.obj.text == "братик привет":
                        send_msg_new(event.object.peer_id, "&#128075; Приветик")
                        main_keyboard(event.object.peer_id)
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
                        main_keyboard(event.object.peer_id)
                    elif event.obj.text == "начать" or event.obj.text == "Начать":
                        main_keyboard(event.object.peer_id)
                    elif event.obj.text == "игры" or event.obj.text == "Игры":
                        klava_game(event.object.peer_id)
                    elif event.obj.text == "Бро награда" or event.obj.text == "бро награда" or \
                            event.obj.text == "бро шекель":
                        thread_start2(add_balans_every_day, event.object.peer_id, event.object.from_id)  # DB
                    elif event.obj.text == "Бро баланс" or event.obj.text == "бро баланс":
                        thread_start2(balans_status, event.object.peer_id, event.object.from_id)  # DB
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

                    if event.obj.text == "Арт" or event.obj.text == "арт":
                        randid = (random.randint(0, photo_arts['count'] - 1))
                        idphoto = (photo_arts['items'][randid]['id'])
                        provzapret(event.object.peer_id, 'арт', str(idphoto))
                    elif event.obj.text == "Стикер" or event.obj.text == "стикер":
                        randid = (random.randint(0, photo_stik['count'] - 1))
                        idphoto = (photo_stik['items'][randid]['id'])
                        provzapret(event.object.peer_id, 'стикер', str(idphoto))
                    elif event.obj.text == "видео" or event.obj.text == "Видео":
                        send_vd(event.object.peer_id, 456239025, 456239134)  # изменять только здесь!
                    elif event.obj.text == "хентай" or event.obj.text == "Хентай":
                        randid = (random.randint(0, photo_hent['count'] - 1))
                        idphoto = (photo_hent['items'][randid]['id'])
                        provzapret(event.object.peer_id, 'хентай', str(idphoto))  # изменять только здесь!
                    elif event.obj.text == "ахегао" or event.obj.text == "Ахегао":
                        randid = (random.randint(0, photo_aheg['count'] - 1))
                        idphoto = (photo_aheg['items'][randid]['id'])
                        provzapret(event.object.peer_id, 'ахегао', str(idphoto))  # изменять только здесь!
                    elif event.obj.text == "лоли" or event.obj.text == "Лоли":
                        randid = (random.randint(0, 999))  # Нельзя чтобы в альбоме было более 1000 фотографий
                        idphoto = (photo_loli['items'][randid]['id'])
                        provzapret(event.object.peer_id, 'лоли', str(idphoto))  # изменять только здесь!
                    elif event.obj.text == "неко" or event.obj.text == "Неко":
                        randid = (random.randint(0, photo_neko['count'] - 1))
                        idphoto = (photo_neko['items'][randid]['id'])
                        provzapret(event.object.peer_id, 'неко', str(idphoto))  # изменять только здесь!
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

        except (requests.exceptions.ConnectionError, urllib3.exceptions.MaxRetryError,
                urllib3.exceptions.NewConnectionError, socket.gaierror):
            error(" - ошибка подключения к вк")


    main()
except (requests.exceptions.ConnectionError, urllib3.exceptions.MaxRetryError,
        urllib3.exceptions.NewConnectionError, socket.gaierror):
    error(" - ошибка подключения к вк")
