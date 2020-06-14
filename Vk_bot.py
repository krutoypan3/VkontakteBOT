# -*- coding: utf-8 -*-
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id
import random
# Импорт API ключа из отдельного файла
f = open('D://VK_BOT/APIKEY.txt', 'r')
APIKEYSS = f.read()


def main():
    # Авторизация под именем сообщества
    vk_session = vk_api.VkApi(
        token=APIKEYSS)
    # Указываем id сообщества
    longpoll = VkBotLongPoll(vk_session, '196288744')
    vk = vk_session.get_api()

    # Постоянный листинг сообщений
    for event in longpoll.listen():
        # Проверка на приход сообщения
        if event.type == VkBotEventType.MESSAGE_NEW:
            # Логика ответов
            if event.obj.text == "Братик привет" or event.obj.text == "братик привет":
                vk.messages.send(
                    peer_id=event.object.peer_id,
                    random_id=get_random_id(),
                    message=("Приветик")
                )
            elif event.obj.text == "Братик пока" or event.obj.text == "братик пока":
                vk.messages.send(
                    peer_id=event.object.peer_id,
                    random_id=get_random_id(),
                    message=("Прощай")
                )
            elif event.obj.text == "-инфо" or event.obj.text == "-инфо":
                vk.messages.send(
                    peer_id=event.object.peer_id,
                    random_id=get_random_id(),
                    message=("Мой разработчик - студет АГПУ Оганесян Артем.\nВсе вопросы по реализации к нему: "
                             "vk.com/aom13")
                )
            elif event.obj.text == "-команды" or event.obj.text == "-команды" or event.obj.text == "братик" or event.obj.text == "Братик":
                vk.messages.send(
                    peer_id=event.object.peer_id,
                    random_id=get_random_id(),
                    message=("Команды: просто напишите няша и нужную вам команду\n-лоли "
                             "\n-команды\n-инфо\n-хентай\n-арты\n-стикер\n-игры")
                )
            elif event.obj.text == "-лоли" or event.obj.text == "-лоли":
                upload = vk_api.VkUpload(vk)
                photo = upload.photo_messages(
                    'D://VK_BOT/Lolis/ (' + str(random.randint(1, 46219)) + ').jpg')  # Отправляет с пк файлы в беседы
                owner_id = photo[0]['owner_id']
                photo_id = photo[0]['id']
                access_key = photo[0]['access_key']
                attachment = f'photo{owner_id}_{photo_id}_{access_key}'
                vk.messages.send(
                    peer_id=event.object.peer_id,
                    random_id=0,
                    attachment=attachment
                )
            elif event.obj.text == "-арты" or event.obj.text == "-арты":
                upload = vk_api.VkUpload(vk)
                photo = upload.photo_messages(
                    'D://VK_BOT/Artos/ (' + str(random.randint(1, 23)) + ').jpg')  # Отправляет с пк файлы в беседы
                owner_id = photo[0]['owner_id']
                photo_id = photo[0]['id']
                access_key = photo[0]['access_key']
                attachment = f'photo{owner_id}_{photo_id}_{access_key}'
                vk.messages.send(
                    peer_id=event.object.peer_id,
                    random_id=0,
                    attachment=attachment
                )
            elif event.obj.text == "-хент" or event.obj.text == "-хентай":
                upload = vk_api.VkUpload(vk)
                photo = upload.photo_messages(
                    'D://VK_BOT/Hentai/ (' + str(random.randint(1, 419)) + ').jpg')  # Отправляет с пк файлы в беседы
                owner_id = photo[0]['owner_id']
                photo_id = photo[0]['id']
                access_key = photo[0]['access_key']
                attachment = f'photo{owner_id}_{photo_id}_{access_key}'
                vk.messages.send(
                    peer_id=event.object.peer_id,
                    random_id=0,
                    attachment=attachment
                )
            elif event.obj.text == "-стикер" or event.obj.text == "-стик":
                upload = vk_api.VkUpload(vk)
                photo = upload.photo_messages(
                    'D://VK_BOT/Stick/ (' + str(random.randint(1, 101)) + ').png')  # Отправляет с пк файлы в беседы
                owner_id = photo[0]['owner_id']
                photo_id = photo[0]['id']
                access_key = photo[0]['access_key']
                attachment = f'photo{owner_id}_{photo_id}_{access_key}'
                vk.messages.send(
                    peer_id=event.object.peer_id,
                    random_id=0,
                    attachment=attachment
                )
            elif event.obj.text == "-список игр" or event.obj.text == "-игры":
                vk.messages.send(
                    peer_id=event.object.peer_id,
                    random_id=get_random_id(),
                    message=(
                        "Выберите игру ниже из списка: \n-угадай число\n")
                )
            elif event.obj.text == "-угадай число":
                vk.messages.send(
                    peer_id=event.object.peer_id,
                    random_id=get_random_id(),
                    message=("Какое число я загадал? От 1 до 5\nНаграда: экслюзивный хентай"))
                chislos = random.randint(1, 5)
                for event in longpoll.listen():
                    # Проверка на приход сообщения
                    if event.type == VkBotEventType.MESSAGE_NEW:
                        if event.type == VkBotEventType.MESSAGE_NEW:
                            if event.obj.text == str(chislos):
                                vk.messages.send(
                                    peer_id=event.object.peer_id,
                                    random_id=get_random_id(),
                                    message=("Правильно! Вот твоя награда:"))
                                upload = vk_api.VkUpload(vk)
                                photo = upload.photo_messages('D://VK_BOT/Hentai/ (' + str(
                                    random.randint(1, 101)) + ').jpg')  # Отправляет с пк файлы в беседы
                                owner_id = photo[0]['owner_id']
                                photo_id = photo[0]['id']
                                access_key = photo[0]['access_key']
                                attachment = f'photo{owner_id}_{photo_id}_{access_key}'
                                vk.messages.send(peer_id=event.object.peer_id, random_id=0, attachment=attachment)
                            else:
                                vk.messages.send(
                                    peer_id=event.object.peer_id,
                                    random_id=get_random_id(),
                                    message=("Неправильно\n правильный ответ:" + str(chislos)))
                    break
        # Вывод в консоли информации о происходящем
        if event.type == VkBotEventType.MESSAGE_NEW:
            print('Новое сообщение:')
            print('Для меня от: ', end='')
            print(event.obj.from_id)
            print('Текст:', event.obj.text)
            print()
            print('ok')
        elif event.type == VkBotEventType.MESSAGE_REPLY:
            print('Новое сообщение:')
            print('От меня для: ', end='')
            print(event.obj.peer_id)
            print('Текст:', event.obj.text)
            print()
        elif event.type == VkBotEventType.MESSAGE_TYPING_STATE:
            print('Печатает ', end='')
            print(event.obj.from_id, end=' ')
            print('для ', end='')
            print(event.obj.to_id)
            print()
        elif event.type == VkBotEventType.GROUP_JOIN:
            print(event.obj.user_id, end=' ')
            print('Вступил в группу!')
            print()
        elif event.type == VkBotEventType.GROUP_LEAVE:
            print(event.obj.user_id, end=' ')
            print('Покинул группу!')
            print()
        else:
            print(event.type)
            print()


if __name__ == '__main__':
    main()
