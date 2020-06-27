import json
import socket
import threading
import requests
import urllib3
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
import time
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


def error(Error):
    global oshibka
    oshibka = oshibka + 1
    print("Произошла ошибка" + '№' + str(oshibka) + Error)
    if Error == " - ошибка подключения к вк":
        time.sleep(5.0)
    main()


def main():
    global oshibka, kolpot  # Счетчик ошибок
    try:
        vk_session = vk_api.VkApi(token=APIKEYSS)  # Авторизация под именем сообщества
        longpoll = VkBotLongPoll(vk_session, group_id)
        vk = vk_session.get_api()
        try:

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

            # Проверка матерных слов в сообщении
            def provbadwordth(slovaf):
                for i in slovaf:
                    zap_wordf = open('zap_word.txt', 'r')
                    asq = False
                    for line in zap_wordf:
                        if (str(i)).lower() + '\n' == line:
                            asq = True
                    zap_wordf.close()
                    if asq:
                        if str(i) != '':
                            send_msg('[' + 'id' + str(event.object.from_id) + '|' + 'Осуждаю' + ']')
                            break

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
                                 keyboard=keyboard.get_keyboard(), message='Ващ ответ:')
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
                            if str(eventhr[kolpot].obj.text) == "1" or slova_g1[1] == "1" \
                                    or str(eventhr[kolpot].obj.text) == "2" or slova_g1[1] == "2" \
                                    or str(eventhr[kolpot].obj.text) == "3" or slova_g1[1] == "3":
                                if str(game_chislo) == str(eventhr[kolpot].obj.text) \
                                        or str(game_chislo) == str(slova_g1[1]):
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

            # Игра кто круче
            def game_kto_kruche(my_peer_game2):
                zapret_zap_game(my_peer_game2)
                send_msg_new(my_peer_game2, '&#127918;Запущена игра "Кто круче?". Чтобы принять участие, '
                                            'напишите "участвую". '
                                            '\nМинимальное количество участников для запуска: 2')
                keyboard = VkKeyboard(inline=True)
                keyboard.add_button('участвую', color=VkKeyboardColor.NEGATIVE)
                keyboard.add_button('начать', color=VkKeyboardColor.POSITIVE)
                vk.messages.send(peer_id=my_peer_game2, random_id=get_random_id(),
                                 keyboard=keyboard.get_keyboard(), message='Набор участников:')
                uchastniki = []
                timing = time.time()
                for eventhr[kolpot] in longpoll.listen():
                    if time.time() - timing < 15.0:
                        try:
                            if eventhr[kolpot].type == VkBotEventType.MESSAGE_NEW:
                                if eventhr[kolpot].obj.text == ('[' + 'club' + str(group_id) + '|' +
                                                                group_name + ']' + " начать") \
                                        or (eventhr[kolpot].obj.text == '[' + 'club' + str(group_id) + '|' +
                                            group_sob + ']' + " начать"):
                                    send_msg_new(my_peer_game2, 'Подождите еще немного')
                                elif (eventhr[kolpot].obj.text == "участвую"
                                      or eventhr[kolpot].obj.text == "Участвую"
                                      or eventhr[kolpot].obj.text == '[' + 'club' + str(group_id) + '|' +
                                      group_name + ']' + " участвую"
                                      or eventhr[kolpot].obj.text == '[' + 'club' + str(group_id) + '|' +
                                      group_sob + ']' + " участвую"
                                      or eventhr[kolpot].obj.text == "учавствую"
                                      or eventhr[kolpot].obj.text == "Учавствую") \
                                        and eventhr[kolpot].object.peer_id == my_peer_game2:
                                    if eventhr[kolpot].object.from_id in uchastniki:
                                        send_msg_new(my_peer_game2, '&#127918;Ты уже в списке участников')
                                    else:
                                        uchastniki.append(eventhr[kolpot].object.from_id)
                                        send_msg_new(my_peer_game2, '&#127918;Заявка на участие принята')
                        except AttributeError:
                            send_msg_new(my_peer_game2, '&#127918;Ты уже в списке участников')
                            continue
                    if time.time() - timing > 15.0:
                        if len(uchastniki) < 2:
                            send_msg_new(my_peer_game2, '&#127918;Слишком мало участников, игра отменена')
                            zapret_zap_game(my_peer_game2)
                            break
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
                            break

            # Проверка на запрет запуска другой игры в данной беседе
            def prov_zap_game(my_peer):
                zapusk_gamef = open('zapusk_game.txt', 'r')
                for line in zapusk_gamef:
                    if (str(my_peer)) + '\n' == line:
                        zapusk_gamef.close()
                        send_msg_new(my_peer, '&#128377;Другая игра уже запущена!')
                        return True
                zapusk_gamef.close()
                return False

            # Запрет запуска другой игры в данной беседе
            def zapret_zap_game(my_peer):
                zapusk_gamef = open('zapusk_game.txt', 'r')
                lines = zapusk_gamef.readlines()
                zapusk_gamef.close()
                for line in lines:
                    if line == str(my_peer) + '\n':
                        zapusk_gamef = open("zapusk_game.txt", 'w')
                        for linec in lines:
                            if linec != str(my_peer) + '\n':
                                zapusk_gamef.write(linec)
                        zapusk_gamef.close()
                        return True
                zapusk_gamef = open('zapusk_game.txt', 'a')
                zapusk_gamef.write(str(my_peer) + '\n')
                zapusk_gamef.close()
                return False

            # Игра бросок кубика
            def game_brosok_kubika(my_peer_game3):
                zapret_zap_game(my_peer_game3)
                send_msg_new(my_peer_game3, '&#127918;Запущена игра "Бросок кубика". Чтобы принять участие, напишите '
                                            '"участвую". \nМинимальное количество участников для запуска: 2')
                uchastniki = []
                timing = time.time()
                keyboard = VkKeyboard(inline=True)
                keyboard.add_button('участвую', color=VkKeyboardColor.POSITIVE)
                keyboard.add_button('начать', color=VkKeyboardColor.NEGATIVE)
                vk.messages.send(peer_id=my_peer_game3, random_id=get_random_id(),
                                 keyboard=keyboard.get_keyboard(), message='Набор участников:')
                for eventhr[kolpot] in longpoll.listen():
                    if time.time() - timing < 15.0:
                        if eventhr[kolpot].type == VkBotEventType.MESSAGE_NEW:
                            try:
                                if eventhr[kolpot].obj.text == ('[' + 'club' + str(group_id) + '|' +
                                                                group_name + ']' + " начать") \
                                        or (eventhr[kolpot].obj.text == '[' + 'club' + str(group_id) + '|' +
                                            group_sob + ']' + " начать"):
                                    send_msg_new(my_peer_game3, 'Подождите еще немного')
                                elif (eventhr[kolpot].obj.text == "участвую"
                                      or eventhr[kolpot].obj.text == "Участвую"
                                      or eventhr[kolpot].obj.text == '[' + 'club' + str(group_id) + '|' +
                                      group_name + ']' + " участвую"
                                      or eventhr[kolpot].obj.text == '[' + 'club' + str(group_id) + '|' +
                                      group_sob + ']' + " участвую"
                                      or eventhr[kolpot].obj.text == "учавствую"
                                      or eventhr[kolpot].obj.text == "Учавствую") \
                                        and eventhr[kolpot].object.peer_id == my_peer_game3:
                                    if eventhr[kolpot].object.from_id in uchastniki:
                                        send_msg_new(my_peer_game3, '&#127918;Ты уже в списке участников')
                                    else:
                                        uchastniki.append(eventhr[kolpot].object.from_id)
                                        send_msg_new(my_peer_game3, '&#127918;Заявка на участие принята')
                            except AttributeError:
                                send_msg_new(my_peer_game3, '&#127918;Ты уже в списке участников')
                                continue
                    if time.time() - timing > 15.0:
                        if len(uchastniki) < 2:
                            send_msg_new(my_peer_game3, '&#127918;Слишком мало участников, игра отменена')
                            zapret_zap_game(my_peer_game3)
                            break
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
                            else:
                                responseg3 = vk.users.get(user_ids=pobeditel)
                                he_name = responseg3[0]['first_name']
                                he_family = responseg3[0]['last_name']
                                chel = '&#127918;[' + 'id' + str(pobeditel) + '|' + str(he_name) + ' ' + str(
                                    he_family) + ']' + '&#127881; '
                                send_msg_new(my_peer_game3, chel + 'победил!&#127882;')
                                zapret_zap_game(my_peer_game3)
                                break

            def klava_game(my_peer_klava):
                keyboard = VkKeyboard(inline=True)
                keyboard.add_button('угадай число', color=VkKeyboardColor.PRIMARY)
                keyboard.add_button('бросок кубика', color=VkKeyboardColor.PRIMARY)
                keyboard.add_button('кто круче', color=VkKeyboardColor.PRIMARY)
                vk.messages.send(peer_id=my_peer_klava, random_id=get_random_id(),
                                 keyboard=keyboard.get_keyboard(), message='Список игр:')

            for event in longpoll.listen():  # Постоянный листинг сообщений
                if event.type == VkBotEventType.MESSAGE_NEW:  # Проверка на приход сообщения
                    slova = event.obj.text.split()  # Разделение сообщения на слова
                    thread_start(provbadwordth, slova)  # Проверка чата на матерные слова
                    # Логика ответов
                    # Игры -----------------------------------------------------------------------------------------
                    if event.obj.text == '[' + 'club' + str(group_id) + '|' + \
                            group_sob + ']' + ' угадай число' \
                            or event.obj.text == '[' + 'club' + str(group_id) + '|' + \
                            group_name + ']' + ' угадай число':
                        if not prov_zap_game(event.object.peer_id):
                            thread_start2(game_ugadai_chislo, event.object.peer_id, event.object.from_id)
                    elif event.obj.text == '[' + 'club' + str(group_id) + '|' + \
                            group_sob + ']' + ' кто круче' \
                            or event.obj.text == '[' + 'club' + str(group_id) + '|' + \
                            group_name + ']' + ' кто круче':
                        if not prov_zap_game(event.object.peer_id):
                            thread_start(game_kto_kruche, event.object.peer_id)
                    elif event.obj.text == '[' + 'club' + str(group_id) + '|' + \
                            group_sob + ']' + ' бросок кубика' \
                            or event.obj.text == '[' + 'club' + str(group_id) + '|' + \
                            group_name + ']' + ' бросок кубика':
                        if not prov_zap_game(event.object.peer_id):
                            thread_start(game_brosok_kubika, event.object.peer_id)
                    # Текстовые ответы -----------------------------------------------------------------------------
                    elif event.obj.text == "братик привет":
                        send_msg("&#128075; Приветик")
                        main_keyboard()
                    elif event.obj.text == "пока" or event.obj.text == "спокойной ночи" or event.obj.text == "споки" \
                            or event.obj.text == "bb":
                        send_msg("&#128546; Прощай")
                    elif event.obj.text == "время":
                        send_msg(str(time.ctime()))
                    elif event.obj.text == "команды" or event.obj.text == "братик" or event.obj.text == "Братик" or \
                            event.obj.text == "Команды":
                        thread_start2(send_msg_new, event.object.peer_id,
                                      ' ⚙️ Полный список команд доступен по ссылке vk.com/@bratikbot-commands')
                        main_keyboard()
                    elif event.obj.text == "начать" or event.obj.text == "Начать":
                        main_keyboard()
                    elif event.obj.text == "игры" or event.obj.text == "Игры":
                        klava_game(event.object.peer_id)
                    elif event.obj.text == "онлайн" or event.obj.text == "кто тут":
                        send_msg(who_online())
                    elif event.obj.text == "инфо":
                        send_msg("Мой разработчик - Оганесян Артем.\nВсе вопросы по реализации к нему: vk.com/aom13")
                    elif event.obj.text == "-я админ":
                        if adm_prov():
                            send_msg('Да, ты админ')
                        else:
                            send_msg('Увы но нет')
                    # Ответы со вложениями --------------------------------------------------------------------------
                    elif event.obj.text == "Арт" or event.obj.text == "арт":
                        provzapret('арт', 457241615, 457241726)  # изменять только здесь!
                    elif event.obj.text == "Стикер" or event.obj.text == "стикер":
                        provzapret('стикер', 457241746, 457241786)  # изменять только здесь!
                    elif event.obj.text == "видео" or event.obj.text == "Видео":
                        send_vd(456239025, 456239134)  # изменять только здесь!
                    elif event.obj.text == "хентай" or event.obj.text == "Хентай":
                        provzapret('хент', 457239410, 457239961)  # изменять только здесь!
                    elif event.obj.text == "ахегао" or event.obj.text == "Ахегао":
                        provzapret('ахегао', 457241147, 457241266)  # изменять только здесь!
                    elif event.obj.text == "лоли" or event.obj.text == "Лоли":
                        provzapret('лоли', 457239962, 457241144)  # изменять только здесь!
                    elif event.obj.text == "неко" or event.obj.text == "Неко":
                        if random.randint(0, 1) == 1:
                            provzapret('неко', 457241325, 457241424)  # изменять только здесь!
                        else:
                            provzapret('неко', 457241502, 457241601)  # изменять только здесь!
                    # Команды для запрета других команд (нужно подумать над оптимизацией) ---------------------------
                    elif event.obj.text == "запрет лоли":
                        adm_prov_and_zapret('лоли')
                    elif event.obj.text == "запрет ахегао":
                        adm_prov_and_zapret('ахегао')
                    elif event.obj.text == "запрет хентай":
                        adm_prov_and_zapret('хент')
                    elif event.obj.text == "запрет арт":
                        adm_prov_and_zapret('арт')
                    elif event.obj.text == "запрет неко":
                        adm_prov_and_zapret('неко')
                    # Отладка ---------------------------------------------------------------------------------------
                    if event.obj.text == 'dump':
                        with open('dump.json', 'w') as dump:
                            response = vk.messages.search(date='26062020', peer_id=event.object.peer_id, count=5,
                                                          extended=1)
                            json.dump(response, dump)
                            send_msg('dumped')
        except (requests.exceptions.ConnectionError, urllib3.exceptions.MaxRetryError,
                urllib3.exceptions.NewConnectionError, socket.gaierror):
            error(" - ошибка подключения к вк")

        finally:
            error(' - а хрен его знает')
    except (requests.exceptions.ConnectionError, urllib3.exceptions.MaxRetryError,
            urllib3.exceptions.NewConnectionError, socket.gaierror):
        error(" - ошибка подключения к вк")


#     elif event.obj.text == "-dump":
#         with open('dump.json', 'w') as dump:
#             response = vk.messages.getConversationMembers(peer_id=event.object.peer_id)
#             json.dump(response, dump)
#             send_msg('dumped')
#             print(response['profiles'][0]['first_name'])

if __name__ == '__main__':
    main()
