# import json
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

# Импорт API ключа(токена) из отдельного файла
f = open('D://VK_BOT/APIKEY.txt', 'r')
APIKEYSS = f.read()  # токен нужно поместить в файл выше(путь можно изменить)), изменять только здесь!
f.close()
print("Бот работает...")
group_id = '196288744'  # Указываем id сообщества, изменять только здесь!
oshibka = 0  # обнуление счетчика ошибок
threads = list()
eventhr = []
kolpot = -1
z = open('zapusk_game.txt', 'w')
z.close()
group_sob = "@bratikbot"  # Указываем короткое имя бота (если нет то id)
group_name = "Братик"  # Указываем название сообщества


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
    cursorObj4.execute("CREATE TABLE peer_params(peer_id integer PRIMARY KEY, zapusk_game text, filter_mata integer)")
    conc3.commit()


con = sql_connection()  # Соединение с БД
'''sql_table(con)'''  # Создание таблицы в БД


# Вставка СТРОКИ в ТАБЛИЦУ в БД
def sql_insert(conc2, entities):
    cursorObj3 = conc2.cursor()
    cursorObj3.execute('INSERT INTO peer_params(peer_id, zapusk_game, filter_mata) VALUES(?, ?, ?)', entities)
    conc2.commit()


'''entities = (2000000019, 0, 0) # Строка которую нужно вставить
   sql_insert(con, entities)'''  # Вставка СТРОКИ в ТАБЛИЦУ в БД


# Обновление параметра в таблице
def sql_update(conc5, what_fetch, what_fetch_new, peer_id_val):
    cursorObj1 = conc5.cursor()
    cursorObj1.execute('UPDATE peer_params SET ' + str(what_fetch) + ' = ' + str(what_fetch_new) + ' where peer_id = '
                       + str(peer_id_val))
    conc5.commit()


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


# Обнуление игр во всех беседах
cursorObj = con.cursor()
cursorObj.execute('UPDATE peer_params SET zapusk_game = 0')
con.commit()


def error(ErrorF):
    global oshibka
    oshibka = oshibka + 1
    print("Произошла ошибка " + '№' + str(oshibka) + ' ' + ErrorF)
    if ErrorF == " - ошибка подключения к вк":
        time.sleep(5.0)
    main()


try:
    def main():
        global oshibka, kolpot  # Счетчик ошибок
        try:
            vk_session = vk_api.VkApi(token=APIKEYSS)  # Авторизация под именем сообщества
            longpoll = VkBotLongPoll(vk_session, group_id)
            vk = vk_session.get_api()
            try:

                def filter_mata_status(my_peer):
                    if str(sql_fetch(con, 'filter_mata', my_peer)[0][0]) == '1':
                        return True
                    return False

                # Проверка на запрет запуска другой игры в данной беседе
                def prov_zap_game(my_peer):
                    if str(sql_fetch(con, 'zapusk_game', my_peer)[0][0]) == '1':
                        send_msg_new(my_peer, '&#128377;Другая игра уже запущена!')
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

                # Запрет команды для определенной беседы
                def zapret(chto):
                    zap_command = open('zap_command.txt', 'r')
                    asq = 0
                    for line in zap_command:
                        if str(event.object.peer_id) + ' ' + str(chto) + '\n' == str(line):
                            send_msg("Команда снова разрешена")
                            lines = zap_command.readlines()
                            zap_command.close()
                            zap_command = open("zap_command.txt", 'w')
                            for linec in lines:
                                if linec != str(event.object.peer_id) + ' ' + str(chto) + '\n':
                                    zap_command.write(linec)
                            asq = 1
                            break
                    zap_command.close()
                    if asq == 0:
                        zap_command = open('zap_command.txt', 'a')
                        zap_command.write(str(event.object.peer_id) + ' ' + str(chto) + '\n')
                        zap_command.close()
                        send_msg("Теперь команда будет недоступна для данной беседы")

                # Проверка команды на наличие в списке запрещенных команд
                def provzapret(chto, a, b):
                    zap_command = open('zap_command.txt', 'r')
                    asq = 0
                    for line in zap_command:
                        if str(event.object.peer_id) + ' ' + str(chto) + '\n' == str(line):
                            send_msg("Команда запрещена для данной беседы")
                            asq = 1
                            break
                    zap_command.close()
                    if asq == 0:
                        send_ft(a, b)

                # Включение \ Отключение фильтра мата
                def proverka_slov(peer_id_mat):
                    if len(slova) > 1:
                        if slova[0] + ' ' + slova[1] == 'фильтр мата' or slova[0] + ' ' + slova[1] == 'Фильтр мата':
                            if adm_prov():
                                if str(sql_fetch(con, 'filter_mata', peer_id_mat)[0][0]) == '1':
                                    sql_update(con, 'filter_mata', '0', peer_id_mat)
                                    send_msg_new(peer_id_mat, 'Фильтр мата отключен')
                                else:
                                    sql_update(con, 'filter_mata', '1', peer_id_mat)
                                    send_msg_new(peer_id_mat, 'Фильтр мата включен')
                            else:
                                send_msg_new(peer_id_mat, 'Как станешь админом, так сразу')

                # Проверка матерных слов в сообщении
                def provbadwordth(slovaf):
                    for i in slovaf:
                        zap_wordf = open('zap_word.txt', 'r')
                        asq = False
                        for line in zap_wordf:
                            if (str(i)).lower() + '\n' == line:
                                asq = True
                        zap_wordf.close()
                        if event.object.from_id > 0:
                            if asq:
                                if str(i) != '':
                                    send_msg('[' + 'id' + str(event.object.from_id) + '|' + 'За мат осуждаю' + ']')
                                    break
                        else:
                            if asq:
                                send_msg('[' + 'club' + str(
                                    -event.object.from_id) + '|' + 'Ты, как бот, подаешь плохой пример' + ']')

                # Отправка текстового сообщения
                def send_msg(ms_g):
                    vk.messages.send(peer_id=event.object.peer_id, random_id=0, message=ms_g)

                # Отправка текстового сообщения
                def send_msg_new(peerid, ms_g):
                    vk.messages.send(peer_id=peerid, random_id=0, message=ms_g)

                # Показ онлайна беседы
                def who_online():
                    try:
                        responseonl = vk.messages.getConversationMembers(peer_id=event.object.peer_id)
                        liss = 'Пользователи онлайн: \n\n'
                        for n in responseonl["profiles"]:
                            if n.get('online'):  # ['vk.com/id'+id|first_name last name]
                                liss += ('💚' + str(n.get('first_name')) + ' ' + str(n.get('last_name')) + '\n')
                        return liss
                    except vk_api.exceptions.ApiError:
                        send_msg('Для выполнения данной команды боту неоюходимы права администратора')
                        main()

                # Отправка фото с сервера ВК
                def send_ft(first_el, end_el):
                    vivord = str(random.randint(first_el, end_el))
                    vk.messages.send(peer_id=event.object.peer_id, random_id=0,
                                     attachment='photo-' + group_id + '_' + vivord)
                    time.sleep(1)
                    main_keyboard()

                # Отправка видео с сервера ВК
                def send_vd(first_el, end_el):
                    vivord = str(random.randint(first_el, end_el))
                    vk.messages.send(peer_id=event.object.peer_id, random_id=0,
                                     attachment='video-' + group_id + '_' + vivord)
                    time.sleep(1)
                    main_keyboard()

                # Проверка админки и последующий запрет при ее наличии
                def adm_prov_and_zapret(chto):
                    if adm_prov():
                        zapret(chto)
                    else:
                        send_msg('Недостаточно прав')

                # Проверка пользователя на наличие прав администратора беседы
                def adm_prov():
                    try:
                        he_admin = False
                        responseapr = vk.messages.getConversationMembers(peer_id=event.object.peer_id)
                        for m in responseapr["items"]:
                            if m["member_id"] == event.object.from_id:
                                he_admin = m.get('is_admin')
                        if not he_admin:
                            he_admin = False
                        return he_admin
                    except vk_api.exceptions.ApiError:
                        send_msg('Для доступа к данной команде боту необходимы права администратора беседы')
                        main()

                # Личная диалог или беседа
                def lich_or_beseda():
                    try:
                        responselic = vk.messages.getConversationMembers(peer_id=event.object.peer_id)
                        if responselic['count'] <= 2:
                            return 1
                        else:
                            return 0
                    except vk_api.exceptions.ApiError:
                        return 0

                # Основная клавиатура
                def main_keyboard():
                    if lich_or_beseda():
                        keyboard = VkKeyboard(one_time=True)
                        keyboard.add_button('арт', color=VkKeyboardColor.PRIMARY)
                        keyboard.add_button('лоли', color=VkKeyboardColor.PRIMARY)
                        keyboard.add_button('неко', color=VkKeyboardColor.PRIMARY)
                        keyboard.add_button('ахегао', color=VkKeyboardColor.PRIMARY)
                        keyboard.add_line()  # Отступ строки
                        keyboard.add_button('хентай', color=VkKeyboardColor.NEGATIVE)
                        keyboard.add_line()
                        keyboard.add_button('видео', color=VkKeyboardColor.POSITIVE)

                        vk.messages.send(peer_id=event.object.peer_id, random_id=get_random_id(),
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
                    x = threading.Thread(target=Func, args=(Arg, Arg2))
                    threads.append(x)
                    x.start()

                # Игра угадай число
                def game_ugadai_chislo(my_peer_game1, my_from):
                    zapret_zap_game(my_peer_game1)
                    responseg1 = vk.users.get(user_ids=my_from)
                    he_name = responseg1[0]['first_name']
                    he_family = responseg1[0]['last_name']
                    chel = '&#127918;[' + 'id' + str(event.object.from_id) + '|' + str(he_name) + ' ' + \
                           str(he_family) + ']' + ', '
                    send_msg(chel + 'игра началась для тебя:\n' + ' угадай число от 1 до 3')
                    timing = time.time()
                    keyboard = VkKeyboard(inline=True)
                    keyboard.add_button('1', color=VkKeyboardColor.NEGATIVE)
                    keyboard.add_button('2', color=VkKeyboardColor.PRIMARY)
                    keyboard.add_button('3', color=VkKeyboardColor.POSITIVE)
                    vk.messages.send(peer_id=my_peer_game1, random_id=get_random_id(),
                                     keyboard=keyboard.get_keyboard(), message='Ваш ответ:')
                    game_chislo = random.randint(1, 3)
                    time.sleep(0.1)
                    for eventhr[kolpot] in longpoll.listen():
                        if time.time() - timing > 10.0:
                            send_msg_new(my_peer_game1, chel + 'время ожидания истекло...')
                            zapret_zap_game(my_peer_game1)
                            break
                        if eventhr[kolpot].type == VkBotEventType.MESSAGE_NEW:
                            if eventhr[kolpot].object.peer_id == my_peer_game1 \
                                    and eventhr[kolpot].object.from_id == my_from:
                                slova_g1 = eventhr[kolpot].obj.text.split()
                                if len(slova_g1) >= 2:
                                    if slova_g1[1] == "1" or slova_g1[1] == "2" or slova_g1[1] == "3":
                                        if str(game_chislo) == str(slova_g1[1]):
                                            send_msg_new(my_peer_game1, chel + 'правильно!' + ' - загаданное число: ' +
                                                         str(game_chislo))
                                            zapret_zap_game(my_peer_game1)
                                            break
                                        else:
                                            send_msg_new(my_peer_game1, chel + 'не правильно!' +
                                                         ' - загаданное число: ' + str(game_chislo))
                                            zapret_zap_game(my_peer_game1)
                                            break
                                    else:
                                        send_msg_new(my_peer_game1, chel + 'Кажется, ты написал что-то не то')

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
                        send_msg('&#127918;Участники укомплектованы, игра начинается')
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

                def money_reward(my_peer_money, my_from_money):
                    money_playerf = open('money_reward.txt', 'r')
                    responsemr = vk.users.get(user_ids=my_from_money)
                    he_name = responsemr[0]['first_name']
                    he_family = responsemr[0]['last_name']
                    chel = '[' + 'id' + str(my_from_money) + '|' + str(he_name) + ' ' + str(
                        he_family) + ']'
                    asqmoney = False
                    moneyall = money_playerf.readlines()
                    for line in moneyall:
                        line_slovo = line.split()
                        if len(line_slovo) >= 4:
                            if str(my_peer_money) + ' ' + str(my_from_money) == str(line_slovo[0]) + ' ' + str(
                                    line_slovo[1]):
                                asqmoney = True
                                if (float(line_slovo[3]) + 10 * 60) < time.time():
                                    money_playerf.close()
                                    money_playerf = open('money_reward.txt', 'w')
                                    for linec in moneyall:
                                        linec_slovo = linec.split()
                                        if (str(linec_slovo[0]) + ' ' + str(linec_slovo[1])) != (
                                                (str(my_peer_money)) + ' ' + str(my_from_money)):
                                            money_playerf.write(linec)
                                        else:
                                            newlinec = linec_slovo
                                            newlinec[2] = str(int(line_slovo[2]) + 500)
                                            newlinec[3] = str(time.time())
                                            whatwrite = ''
                                            for i in range(len(newlinec)):
                                                whatwrite += (newlinec[i] + ' ')
                                            whatwrite += '\n'
                                            money_playerf.write(whatwrite)
                                            send_msg_new(my_peer_money, 'Получено 500 бро-коинов!')
                                    money_playerf.close()
                                    send_msg_new(my_peer_money,
                                                 chel + ', теперь у тебя ' + str(
                                                     int(line_slovo[2]) + 500) + ' бро-коинов')
                                    break
                                else:
                                    money_playerf.close()
                                    send_msg_new(my_peer_money,
                                                 chel + ', ты уже получил свои деньги за последние 10 минут!')
                                    break
                    if not asqmoney:
                        money_playerf.close()
                        money_playerf = open('money_reward.txt', 'a')
                        send_msg_new(my_peer_money, chel + ', вот тебе 1000 бро-коинов на начальные расходы')
                        money_playerf.write(
                            str(my_peer_money) + ' ' + str(my_from_money) + ' ' + '1000' + ' ' + str(
                                time.time()) + ' \n')
                        money_playerf.close()

                def balans(my_peer_balans, my_from_balans):
                    money_playerfb = open('money_reward.txt', 'r')
                    responsemr = vk.users.get(user_ids=my_from_balans)
                    he_name = responsemr[0]['first_name']
                    he_family = responsemr[0]['last_name']
                    chel = '[' + 'id' + str(my_from_balans) + '|' + str(he_name) + ' ' + str(
                        he_family) + ']'
                    moneyallb = money_playerfb.readlines()
                    asqb = False
                    for line in moneyallb:
                        line_slovo = line.split()
                        if len(line_slovo) >= 4:
                            if str(my_peer_balans) + ' ' + str(my_from_balans) == str(line_slovo[0]) + ' ' + str(
                                    line_slovo[1]):
                                send_msg_new(my_peer_balans, chel + ', у тебя ' + line_slovo[2] + ' бро-коинов')
                                asqb = True
                                money_playerfb.close()
                                break
                    money_playerfb.close()
                    if not asqb:
                        send_msg_new(my_peer_balans,
                                     'Ой, похоже у тебя еще нет бро-коинов...\nДля получения первых 1000 бро-коинов '
                                     'напиши "бро награда"')

                for event in longpoll.listen():  # Постоянный листинг сообщений
                    if event.type == VkBotEventType.MESSAGE_NEW:  # Проверка на приход сообщения
                        slova = event.obj.text.split()  # Разделение сообщения на слова
                        if filter_mata_status(event.object.peer_id):
                            thread_start(provbadwordth, slova)  # Проверка чата на матерные слова
                        thread_start(proverka_slov, event.object.peer_id)
                        # Логика ответов
                        # Игры -----------------------------------------------------------------------------------------
                        if len(slova) > 2:
                            if slova[1] + ' ' + slova[2] == 'угадай число':
                                if not prov_zap_game(event.object.peer_id):
                                    thread_start2(game_ugadai_chislo, event.object.peer_id, event.object.from_id)
                            elif slova[1] + ' ' + slova[2] == 'кто круче':
                                if not prov_zap_game(event.object.peer_id):
                                    thread_start(game_kto_kruche, event.object.peer_id)
                            elif slova[1] + ' ' + slova[2] == 'бросок кубика':
                                if not prov_zap_game(event.object.peer_id):
                                    thread_start(game_brosok_kubika, event.object.peer_id)
                            elif slova[1] == 'участвую':
                                if not prov_zap_game(event.object.peer_id):
                                    send_msg_new(event.object.peer_id, 'Игра уже закончилась')
                        # Текстовые ответы -----------------------------------------------------------------------------
                        if event.obj.text == "братик привет":
                            send_msg("&#128075; Приветик")
                            main_keyboard()
                        elif event.obj.text == "пока" or event.obj.text == "спокойной ночи" or \
                                event.obj.text == "споки" or event.obj.text == "bb":
                            send_msg("&#128546; Прощай")
                        elif event.obj.text == "время":
                            send_msg(str(time.ctime()))
                        elif event.obj.text == "времятест":
                            send_msg(str(time.time()))
                        elif event.obj.text == "команды" or event.obj.text == "братик" or \
                                event.obj.text == "Братик" or event.obj.text == "Команды":
                            send_msg_new(event.object.peer_id, '⚙️ Полный список команд доступен по ссылке ' +
                                         'vk.com/@bratikbot-commands')
                            main_keyboard()
                        elif event.obj.text == "начать" or event.obj.text == "Начать":
                            main_keyboard()
                        elif event.obj.text == "игры" or event.obj.text == "Игры":
                            klava_game(event.object.peer_id)
                        elif event.obj.text == "Бро награда" or event.obj.text == "бро награда" or \
                                event.obj.text == "бро шекель":
                            thread_start2(money_reward, event.object.peer_id, event.object.from_id)
                        elif event.obj.text == "Бро баланс" or event.obj.text == "бро баланс":
                            thread_start2(balans, event.object.peer_id, event.object.from_id)
                        elif event.obj.text == "онлайн" or event.obj.text == "кто тут":
                            send_msg_new(event.object.peer_id, who_online())
                        elif event.obj.text == "инфо":
                            send_msg_new(event.object.peer_id, "Мой разработчик - Оганесян Артем.\nВсе вопросы по "
                                                               "реализации к нему: vk.com/aom13")
                        elif event.obj.text == "я админ" or event.obj.text == "Я админ":
                            if adm_prov():
                                send_msg('Да, ты админ')
                            else:
                                send_msg('Увы но нет')

                        # Ответы со вложениями -----------------------------------------------------------------------

                        elif event.obj.text == "Арт" or event.obj.text == "арт":
                            provzapret('арт', 457241615, 457241726)  # изменять только здесь!
                        elif event.obj.text == "Стикер" or event.obj.text == "стикер":
                            provzapret('стикер', 457241746, 457241786)  # изменять только здесь!
                        elif event.obj.text == "видео" or event.obj.text == "Видео":
                            send_vd(456239025, 456239134)  # изменять только здесь!
                        elif event.obj.text == "хентай" or event.obj.text == "Хентай":
                            provzapret('хентай', 457239410, 457239961)  # изменять только здесь!
                        elif event.obj.text == "ахегао" or event.obj.text == "Ахегао":
                            provzapret('ахегао', 457241147, 457241266)  # изменять только здесь!
                        elif event.obj.text == "лоли" or event.obj.text == "Лоли":
                            provzapret('лоли', 457239962, 457241144)  # изменять только здесь!
                        elif event.obj.text == "неко" or event.obj.text == "Неко":
                            if random.randint(0, 1) == 1:
                                provzapret('неко', 457241325, 457241424)  # изменять только здесь!
                            else:
                                provzapret('неко', 457241502, 457241601)  # изменять только здесь!
                        elif len(slova) > 1:
                            if slova[0] == 'запрет' or slova[0] == 'Запрет':
                                adm_prov_and_zapret(slova[1])
                        # Отладка -------------------------------------------------------------------------------------
                        """if event.obj.text == 'dump':
                            with open('dump.json', 'w') as dump:
                                send_msg(event.object.peer_id)
                                response = vk.messages.getHistory(offset='0', count='50', peer_id=event.object.peer_id,
                                                                  start_message_id='-1')
                                json.dump(response, dump)
                                send_msg('dumped')"""
            except (requests.exceptions.ConnectionError, urllib3.exceptions.MaxRetryError,
                    urllib3.exceptions.NewConnectionError, socket.gaierror):
                error(" - ошибка подключения к вк")

            finally:
                error('- а хрен его знает')

        except (requests.exceptions.ConnectionError, urllib3.exceptions.MaxRetryError,
                urllib3.exceptions.NewConnectionError, socket.gaierror):
            error(" - ошибка подключения к вк")

    main()

except (requests.exceptions.ConnectionError, urllib3.exceptions.MaxRetryError,
        urllib3.exceptions.NewConnectionError, socket.gaierror):
    error(" - ошибка подключения к вк")

finally:
    error('- а хрен его знает')
#     elif event.obj.text == "-dump":
#         with open('dump.json', 'w') as dump:
#             response = vk.messages.getConversationMembers(peer_id=event.object.peer_id)
#             json.dump(response, dump)
#             send_msg('dumped')
#             print(response['profiles'][0]['first_name'])
