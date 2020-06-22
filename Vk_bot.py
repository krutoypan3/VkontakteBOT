from socket import socket
import requests
import vk_api
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
                             '-стикер\n-цитата\n-видео\n-ахегао\n-неко')
                # Ответы со вложениями
                elif event.obj.text == "-арты" or event.obj.text == "-арт":
                    send_ft(457241615, 457241726)
                elif event.obj.text == "-видос" or event.obj.text == "-видео":
                    send_vd(456239025, 456239134)
                elif event.obj.text == "-хентай" or event.obj.text == "-хент":
                    send_ft(457239410, 457239961)
                elif event.obj.text == "-ахегао":
                    send_ft(457241147, 457241266)
                elif event.obj.text == "-лоли" or event.obj.text == "-лоля":
                    send_ft(457239962, 457241144)
                elif event.obj.text == "-неко":
                    if random.randint(0, 1) == 1:
                        send_ft(457241325, 457241424)
                    else:
                        send_ft(457241502, 457241601)
    except (requests.exceptions.ReadTimeout, socket.timeout):
        print("SHTEFAN NINE!!!")


if __name__ == '__main__':
    main()