import socket
import json
import requests
import vk_api
import sqlite3
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random

# Импорт API ключа(токена) из отдельного файла
f = open('D://VK_BOT/APIKEY.txt', 'r')
APIKEYSS = f.read()
print("Бот работает...")


def main():
    vk_session = vk_api.VkApi(token=APIKEYSS)  # Авторизация под именем сообщества
    longpoll = VkBotLongPoll(vk_session, '196288744')  # Указываем id сообщества
    vk = vk_session.get_api()
    try:
        def zapret(chto):
            zap_command = open('zap_command.txt', 'r')
            asq = 0
            for line in zap_command:
                if str(event.object.peer_id) + str(chto) + '\n' == str(line):
                    send_msg("Команда снова разрешена")
                    lines = zap_command.readlines()
                    zap_command.close()
                    zap_command = open("zap_command.txt", 'w')
                    for linec in lines:
                        if linec != str(event.object.peer_id) + str(chto) + '\n':
                            zap_command.write(linec)
                    asq = 1
                    break
            zap_command.close()
            if asq == 0:
                zap_command = open('zap_command.txt', 'a')
                zap_command.write(str(event.object.peer_id) + str(chto) + '\n')
                zap_command.close()
                send_msg("Команда запрещена для данной беседы")

        def provzapret(chto, a, b):
            zap_command = open('zap_command.txt', 'r')
            asq = 0
            for line in zap_command:
                if str(event.object.peer_id) + str(chto) + '\n' == str(line):
                    send_msg("Команда запрещена для данной беседы")
                    asq = 1
                    break
            zap_command.close()
            if asq == 0:
                send_ft(a, b)

        def send_msg(ms_g):  # Отправка текстового сообщения
            vk.messages.send(peer_id=event.object.peer_id, random_id=0, message=ms_g)

        def send_ft(first_el, end_el):  # Отправка фото с сервера ВК
            vivord = str(random.randint(first_el, end_el))
            vk.messages.send(peer_id=event.object.peer_id, random_id=0, attachment='photo-196288744_' + vivord)

        def send_vd(first_el, end_el):  # Отправка видео с сервера ВК
            vivord = str(random.randint(first_el, end_el))
            vk.messages.send(peer_id=event.object.peer_id, random_id=0, attachment='video-196288744_' + vivord)

        for event in longpoll.listen():  # Постоянный листинг сообщений
            if event.type == VkBotEventType.MESSAGE_NEW:  # Проверка на приход сообщения
                # Логика ответов
                # Текстовые ответы
                if event.obj.text == "братик привет":
                    send_msg("&#128075; Приветик")
                elif event.obj.text == "братик пока":
                    send_msg("&#128546; Прощай")
                elif event.obj.text == "-инфо":
                    send_msg("Мой разработчик - Оганесян Артем.\nВсе вопросы по реализации к нему: vk.com/aom13")
                elif event.obj.text == "-команды" or event.obj.text == "братик" or event.obj.text == "Братик":
                    send_msg('&#129302; Команды: просто напишите "-" и нужную вам команду\n&#128540; -лоли'
                             '\n&#129302; -команды\n&#8505; -инфо\n&#9832; -хентай\n&#127924; -арты\n&#128076; '
                             '\n-видео\n-ахегао\n-неко')
                # Ответы со вложениями
                elif event.obj.text == "-арты" or event.obj.text == "-арт":
                    provzapret('-арт', 457241615, 457241726)
                elif event.obj.text == "-видос" or event.obj.text == "-видео":
                    send_vd(456239025, 456239134)
                elif event.obj.text == "-хентай" or event.obj.text == "-хент":
                    provzapret('-хент', 457239410, 457239961)
                elif event.obj.text == "-ахегао":
                    provzapret('-ахегао', 457241147, 457241266)
                elif event.obj.text == "-запрет -лоли":
                    zapret('-лоли')
                elif event.obj.text == "-запрет -ахегао":
                    zapret('-ахегао')
                elif event.obj.text == "-запрет -хентай":
                    zapret('-хент')
                elif event.obj.text == "-запрет -арт":
                    zapret('-арт')
                elif event.obj.text == "-лоли" or event.obj.text == "-лоля":
                    provzapret('-лоли', 457239962, 457241144)
                elif event.obj.text == "-неко":
                    if random.randint(0, 1) == 1:
                        provzapret('-неко', 457241325, 457241424)
                    else:
                        provzapret('-неко', 457241502, 457241601)
                """elif event.obj.text == "-тест":
                                    send_msg(event.object.from_id)
                                    response = vk.messages.getConversationMembers(peer_id=event.object.from_id,
                                                                                  group_id=event.object.peer_id)
                                    with open('fact.json', 'w') as fact:
                                        json.dump(response, fact)
                                    send_msg(response['items']['is_admin'])"""
    except (requests.exceptions.ReadTimeout, socket.timeout):
        print("SHTEFAN NINE!!!")
        if __name__ == '__main__':
            main()


if __name__ == '__main__':
    main()
