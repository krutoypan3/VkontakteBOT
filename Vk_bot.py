# -*- coding: utf-8 -*-
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id
import random


f = open('D://VK_BOT/APIKEY.txt', 'r')
APIKEYSS = f.read()

def main():
    """ Пример использования bots longpoll
        https://vk.com/dev/bots_longpoll
    """

    vk_session = vk_api.VkApi(
        token=APIKEYSS)

    longpoll = VkBotLongPoll(vk_session, '196288744')
    vk = vk_session.get_api()
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
            elif event.obj.text == "Братик инфо" or event.obj.text == "братик инфо":
                vk.messages.send(
                    peer_id=event.object.peer_id,

                    random_id=get_random_id(),
                    message=("Мой разработчик - студет АГПУ Оганесян Артем.\nВсе вопросы по реализации к нему: vk.com/aom13")
                )
            elif event.obj.text == "Братик команды" or event.obj.text == "братик команды" or event.obj.text == "братик" or event.obj.text == "Братик":
                vk.messages.send(
                    peer_id=event.object.peer_id,

                    random_id=get_random_id(),
                    message=("Команды: просто напишите няша и нужную вам команду\n-лоли \n-команды\n-инфо\n-хентай\n-арты\n-стикер")
                )
            elif event.obj.text == "Братик лоли" or event.obj.text == "братик лоли":
                upload = vk_api.VkUpload(vk)
                photo = upload.photo_messages('D://VK_BOT/Lolis/(' + str(random.randint(1, 10010)) + ').jpg') # Отправляет с пк файлы в беседы
                owner_id = photo[0]['owner_id']
                photo_id = photo[0]['id']
                access_key = photo[0]['access_key']
                attachment = f'photo{owner_id}_{photo_id}_{access_key}'
                vk.messages.send(peer_id=event.object.peer_id, random_id=0, attachment=attachment)

            elif event.obj.text == "Братик арты" or event.obj.text == "братик арты":
                upload = vk_api.VkUpload(vk)
                photo = upload.photo_messages('D://VK_BOT/Artos/ (' + str(random.randint(1, 23)) + ').jpg') # Отправляет с пк файлы в беседы
                owner_id = photo[0]['owner_id']
                photo_id = photo[0]['id']
                access_key = photo[0]['access_key']
                attachment = f'photo{owner_id}_{photo_id}_{access_key}'
                vk.messages.send(peer_id=event.object.peer_id, random_id=0, attachment=attachment)

            elif event.obj.text == "Братик хентай" or event.obj.text == "братик хентай":
                upload = vk_api.VkUpload(vk)
                photo = upload.photo_messages('D://VK_BOT/Hentai/ (' + str(random.randint(1, 101)) + ').jpg') # Отправляет с пк файлы в беседы
                owner_id = photo[0]['owner_id']
                photo_id = photo[0]['id']
                access_key = photo[0]['access_key']
                attachment = f'photo{owner_id}_{photo_id}_{access_key}'
                vk.messages.send(peer_id=event.object.peer_id, random_id=0, attachment=attachment)

            elif event.obj.text == "Братик стикер" or event.obj.text == "братик стикер":
                upload = vk_api.VkUpload(vk)
                photo = upload.photo_messages('D://VK_BOT/Stick/ (' + str(random.randint(1, 101)) + ').png') # Отправляет с пк файлы в беседы
                owner_id = photo[0]['owner_id']
                photo_id = photo[0]['id']
                access_key = photo[0]['access_key']
                attachment = f'photo{owner_id}_{photo_id}_{access_key}'
                vk.messages.send(peer_id=event.object.peer_id, random_id=0, attachment=attachment)

            elif event.obj.text == "Братик игра" or event.obj.text == "братик игра":
                vk.messages.send(
                    peer_id=event.object.peer_id,

                    random_id=get_random_id(),
                    message=(
                        "Запустился режим игры. Выберите игру ниже из списка: \n-угадай число\n")
                )

            elif event.obj.text == "Братик игра угадай число" or event.obj.text == "братик игра угадай число":
                vk.messages.send(
                    peer_id=event.object.peer_id,
                    random_id=get_random_id(),
                    message=("Какое число я загадал? От 1 до до 10"))
                chislos = random.randint(1,10)
                if event.obj.text == "chislo":
                    vk.messages.send(
                        peer_id=event.object.peer_id,
                        random_id=get_random_id(),
                        message=("Правильно"))
                else:
                    vk.messages.send(
                        peer_id=event.object.peer_id,
                        random_id=get_random_id(),
                        message=("Неправильно"))



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
