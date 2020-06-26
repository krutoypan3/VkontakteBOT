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
# import json

# Импорт API ключа(токена) из отдельного файла
f = open('D://VK_BOT/APIKEY.txt', 'r')
APIKEYSS = f.read()  # токен нужно поместить в файл выше(путь можно изменить)), изменять только здесь!
print("Бот работает...")
group_id = '196288744'  # Указываем id сообщества, изменять только здесь!
oshibka = 0  # обнуление счетчика ошибок
threads = list()
eventhr = []
kolpot = -1


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
                    response = vk.messages.getConversationMembers(peer_id=event.object.peer_id)
                    liss = 'Пользователи онлайн: \n\n'
                    for n in response["profiles"]:
                        if n.get('online'):  # ['vk.com/id'+id|first_name last name]
                            liss += ('[' + 'id' + str(n.get('id')) + '|' + str(n.get('first_name')) + ' ' + str(
                                n.get('last_name')) + ']' + '\n')
                    return liss
                except vk_api.exceptions.ApiError:
                    send_msg('Для выполнения данной команды боту неоюходимы права администратора')
                    main()

            # Отправка фото с сервера ВК
            def send_ft(first_el, end_el):
                vivord = str(random.randint(first_el, end_el))
                vk.messages.send(peer_id=event.object.peer_id, random_id=0,
                                 attachment='photo-' + group_id + '_' + vivord)
                main_keyboard()

            # Отправка видео с сервера ВК
            def send_vd(first_el, end_el):
                vivord = str(random.randint(first_el, end_el))
                vk.messages.send(peer_id=event.object.peer_id, random_id=0,
                                 attachment='video-' + group_id + '_' + vivord)
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
                    response = vk.messages.getConversationMembers(peer_id=event.object.peer_id)
                    for m in response["items"]:
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
                    response = vk.messages.getConversationMembers(peer_id=event.object.peer_id)
                    if response['count'] <= 2:
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

            def thread_start(Func, Arg):
                global kolpot
                x = threading.Thread(target=Func, args=(Arg,))
                threads.append(x)
                kolpot += 1
                eventhr.append(kolpot)
                x.start()

            def thread_start2(Func, Arg, Arg2):
                x = threading.Thread(target=Func, args=(Arg, Arg2))
                threads.append(x)
                x.start()

            def testmultipot(my_peer, my_from):
                send_msg(str(time.ctime()))
                timing = time.time()
                for eventhr[kolpot] in longpoll.listen():
                    if time.time() - timing > 10.0:
                        send_msg_new(my_peer, 'Время ожидания истекло')
                        break
                    if eventhr[kolpot].type == VkBotEventType.MESSAGE_NEW:
                        if eventhr[kolpot].object.peer_id == my_peer and eventhr[kolpot].object.from_id == my_from:
                            send_msg_new(my_peer, 'Тест прошел удачно')
                            break

            def game_ugadai_chislo(my_peer, my_from):
                global he_name
                response = vk.users.get(user_ids=my_from)
                he_name = response[0]['first_name']
                he_family = response[0]['last_name']
                chel = '[' + 'id' + str(event.object.from_id) + '|' + str(he_name) + ' ' + str(he_family) + ']' + ', '
                send_msg(chel + 'игра началась для тебя:\n' + ' угадай число от 1 до 3')
                timing = time.time()
                game_chislo = random.randint(1, 3)
                for eventhr[kolpot] in longpoll.listen():
                    if time.time() - timing > 10.0:
                        send_msg_new(my_peer, chel + 'время ожидания истекло...')
                        break
                    if eventhr[kolpot].type == VkBotEventType.MESSAGE_NEW:
                        if eventhr[kolpot].object.peer_id == my_peer and eventhr[kolpot].object.from_id == my_from:
                            if str(game_chislo) == str(event.obj.text):
                                send_msg_new(my_peer, chel + 'правильно!')
                                break
                            else:
                                send_msg_new(my_peer, chel + 'не правильно!' +
                                             ' - загаданное число: ' + str(game_chislo))
                                break

            for event in longpoll.listen():  # Постоянный листинг сообщений
                if event.type == VkBotEventType.MESSAGE_NEW:  # Проверка на приход сообщения
                    # Логика ответов
                    # Текстовые ответы -----------------------------------------------------------------------------
                    slova = event.obj.text.split()
                    thread_start(provbadwordth, slova)
                    if event.obj.text == "братик привет":
                        send_msg("&#128075; Приветик")
                        main_keyboard()
                    elif event.obj.text == 'угадай число' or event.obj.text == 'Угадай число':
                        thread_start2(game_ugadai_chislo, event.object.peer_id, event.object.from_id)
                    elif event.obj.text == "пока" or event.obj.text == "спокойной ночи" or event.obj.text == "споки" \
                            or event.obj.text == "bb":
                        send_msg("&#128546; Прощай")
                    elif event.obj.text == "время":
                        send_msg(str(time.ctime()))
                    elif event.obj.text == "тест мультипоточности":
                        thread_start2(testmultipot, event.object.peer_id, event.object.from_id)
                    elif event.obj.text == "-команды" or event.obj.text == "братик" or event.obj.text == "Братик":
                        send_msg('&#129302; Команды: просто напишите "-" и нужную вам команду\n&#128540; -лоли'
                                 '\n&#129302; -команды\n&#8505; -инфо\n&#9832; -хентай\n&#127924; -арты\n&#128076; '
                                 '\n-видео\n-ахегао\n-неко\n\nКоманды администрирования беседы:'
                                 '\n-запрет "команда" | например: (-запрет -лоли)')
                        main_keyboard()
                    elif event.obj.text == "начать" or event.obj.text == "Начать":
                        main_keyboard()
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

        except (requests.exceptions.ConnectionError, urllib3.exceptions.MaxRetryError,
                urllib3.exceptions.NewConnectionError, socket.gaierror):
            error(" - ошибка подключения к вк")

        finally:
            error('')
    except (requests.exceptions.ConnectionError, urllib3.exceptions.MaxRetryError,
            urllib3.exceptions.NewConnectionError, socket.gaierror):
        error(" - ошибка подключения к вк")


#     elif event.obj.text == "-dump":
#         with open('dump.json', 'w') as dump:
#             response = vk.messages.getConversationMembers(peer_id=event.object.peer_id)
#             json.dump(response, dump)
#             send_msg('dumped')

if __name__ == '__main__':
    main()
