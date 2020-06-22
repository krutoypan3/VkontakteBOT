from socket import socket
import requests
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id
import random

# Импорт API ключа(токена) из отдельного файла
f = open('D://VK_BOT/APIKEY.txt', 'r')
APIKEYSS = f.read()


def main():
    # Авторизация под именем сообщества
    vk_session = vk_api.VkApi(
        token=APIKEYSS)
    # Указываем id сообщества
    longpoll = VkBotLongPoll(vk_session, '196288744')
    vk = vk_session.get_api()
    try:
        # Постоянный листинг сообщений
        for event in longpoll.listen():
            # Проверка на приход сообщения
            if event.type == VkBotEventType.MESSAGE_NEW:
                # Логика ответов
                if event.obj.text == "Братик привет" or event.obj.text == "братик привет":
                    vk.messages.send(
                        peer_id=event.object.peer_id,
                        random_id=get_random_id(),
                        message=("&#128075; Приветик")
                    )
                elif event.obj.text == "Братик пока" or event.obj.text == "братик пока":
                    vk.messages.send(
                        peer_id=event.object.peer_id,
                        random_id=get_random_id(),
                        message=("&#128546; Прощай")
                    )
                elif event.obj.text == "-инфо" or event.obj.text == "-инфо":
                    vk.messages.send(
                        peer_id=event.object.peer_id,
                        random_id=get_random_id(),
                        message=("Мой разработчик - Оганесян Артем.\nВсе вопросы по реализации к нему: "
                                 "vk.com/aom13")
                    )
                elif event.obj.text == "-команды" or event.obj.text == "-команды" or event.obj.text == "братик" or event.obj.text == "Братик":
                    vk.messages.send(
                        peer_id=event.object.peer_id,
                        random_id=get_random_id(),
                        message=('&#129302; Команды: просто напишите "-" и нужную вам команду\n&#128540; -лоли'
                                 '\n&#129302; -команды\n&#8505; -инфо\n&#9832; -хентай\n&#127924; -арты\n&#128076; '
                                 '-стикер\n-цитата\n-видео\n-ахегао\n-неко')
                    )
                elif event.obj.text == "-арты" or event.obj.text == "-арт":
                    upload = vk_api.VkUpload(vk)
                    photo = upload.photo_messages(
                        'D://VK_BOT/Artos/ (' + str(random.randint(1, 59)) + ').jpg')  # Отправляет с пк файлы в беседы
                    owner_id = photo[0]['owner_id']
                    photo_id = photo[0]['id']
                    access_key = photo[0]['access_key']
                    attachment = f'photo{owner_id}_{photo_id}_{access_key}'
                    vk.messages.send(
                        peer_id=event.object.peer_id,
                        random_id=0,
                        attachment=attachment
                    )
                elif event.obj.text == "-видос" or event.obj.text == "-видео":
                    vivi = 'video-196288744_'
                    vivord = str(random.randint(456239025, 456239134))
                    vk.messages.send(
                        peer_id=event.object.peer_id,
                        random_id=0,
                        attachment=vivi + vivord
                    )
                elif event.obj.text == "-хентай" or event.obj.text == "-хент":
                    vivi = 'photo-196288744_'
                    vivord = str(random.randint(457239410, 457239961))
                    vk.messages.send(
                        peer_id=event.object.peer_id,
                        random_id=0,
                        attachment=vivi + vivord
                    )
                elif event.obj.text == "-ахегао":
                    vivi = 'photo-196288744_'
                    vivord = str(random.randint(457241147, 457241266))
                    vk.messages.send(
                        peer_id=event.object.peer_id,
                        random_id=0,
                        attachment=vivi + vivord
                    )
                elif event.obj.text == "-неко":
                    vivi = 'photo-196288744_'
                    if random.randint(0, 1) == 1:
                        vivord = str(random.randint(457241325, 457241424))
                    else:
                        vivord = str(random.randint(457241502, 457241601))
                    vk.messages.send(
                        peer_id=event.object.peer_id,
                        random_id=0,
                        attachment=vivi + vivord
                    )
                elif event.obj.text == "-лоли" or event.obj.text == "-лоля":
                    vivi = 'photo-196288744_'
                    vivord = str(random.randint(457239962, 457241144))
                    vk.messages.send(
                        peer_id=event.object.peer_id,
                        random_id=0,
                        attachment=vivi + vivord
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
                elif event.obj.text == "-цитаты" or event.obj.text == "-цитата":
                    upload = vk_api.VkUpload(vk)
                    photo = upload.photo_messages(
                        'D://VK_BOT/Tsitati/ (' + str(random.randint(1, 2)) + ').jpg')  # Отправляет с пк файлы в беседы
                    owner_id = photo[0]['owner_id']
                    photo_id = photo[0]['id']
                    access_key = photo[0]['access_key']
                    attachment = f'photo{owner_id}_{photo_id}_{access_key}'
                    vk.messages.send(
                        peer_id=event.object.peer_id,
                        random_id=0,
                        attachment=attachment
                    )
    except (requests.exceptions.ReadTimeout, socket.timeout):
        print("SHTEFAN NINE!!!")


if __name__ == '__main__':
    main()
