import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
import time

# Импорт API ключа(токена) из отдельного файла
f = open('D://VK_BOT/APIKEY.txt', 'r')
APIKEYSS = f.read()
print("Бот работает...")


def main():
    vk_session = vk_api.VkApi(token=APIKEYSS)  # Авторизация под именем сообщества
    longpoll = VkBotLongPoll(vk_session, '196288744')  # Указываем id сообщества
    vk = vk_session.get_api()
    try:
        # Запрет команды для определенной беседы
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
                send_msg("Теперь команда будет недоступна для данной беседы")

        # Проверка команды на наличие в списке запрещенных команд
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

        # Добавление нецензурного слова в словарь
        def addbadword(chto):
            global zap_word
            zap_wordf = open('zap_word.txt', 'r')
            zap_word = zap_wordf.read()
            zap_wordf.close()
            zap_wordf = open('zap_word.txt', 'w')
            zap_word += str(chto) + '\n'
            zap_wordf.write(zap_word)

        # Проверка чата на нецензурную брань
        def provbadword(mat):
            zap_wordf = open('zap_word.txt', 'r')
            zap_word = zap_wordf.read()
            zap_wordf.close()
            asq = 0
            if mat + '\n' in zap_word:
                asq = 1
            return asq

        # Отправка текстового сообщения
        def send_msg(ms_g):
            vk.messages.send(peer_id=event.object.peer_id, random_id=0, message=ms_g)

        # Показ онлайна беседы
        def who_online():
            try:
                response = vk.messages.getConversationMembers(peer_id=event.object.peer_id)
                liss = 'Пользователи онлайн: \n\n'
                for i in response["profiles"]:
                    if i.get('online'):  # ['vk.com/id'+id|first_name last name]
                        liss += ('[' + 'id' + str(i.get('id')) + '|' + str(i.get('first_name')) + ' ' + str(
                            i.get('last_name')) + ']' + '\n')
                return liss
            except:
                send_msg('Для выполнения данной команды боту неоюходимы права администратора')
                main()

        # Отправка фото с сервера ВК
        def send_ft(first_el, end_el):
            vivord = str(random.randint(first_el, end_el))
            vk.messages.send(peer_id=event.object.peer_id, random_id=0, attachment='photo-196288744_' + vivord)

        # Отправка видео с сервера ВК
        def send_vd(first_el, end_el):
            vivord = str(random.randint(first_el, end_el))
            vk.messages.send(peer_id=event.object.peer_id, random_id=0, attachment='video-196288744_' + vivord)

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
                for i in response["items"]:
                    if i["member_id"] == event.object.from_id:
                        he_admin = i.get('is_admin')
                if not he_admin:
                    he_admin = False
                return he_admin
            except:
                send_msg('Для доступа к данной команде боту необходимы права администратора беседы')
                main()

        for event in longpoll.listen():  # Постоянный листинг сообщений
            if event.type == VkBotEventType.MESSAGE_NEW:  # Проверка на приход сообщения
                # Логика ответов
                # Текстовые ответы -----------------------------------------------------------------------------
                if provbadword(str(event.obj.text)):
                    if str(event.obj.text) != '':
                        send_msg('Ты шо материшься')
                if event.obj.text == "братик привет":
                    send_msg("&#128075; Приветик")
                elif event.obj.text == "пока" or event.obj.text == "спокойной ночи" or event.obj.text == "споки" \
                        or event.obj.text == "bb":
                    send_msg("&#128546; Прощай")
                elif event.obj.text == "-время":
                    send_msg(str(time.ctime()))
                elif event.obj.text == "-онлайн" or event.obj.text == "-кто тут":
                    send_msg(who_online())
                elif event.obj.text == "-инфо":
                    send_msg("Мой разработчик - Оганесян Артем.\nВсе вопросы по реализации к нему: vk.com/aom13")
                elif event.obj.text == "-команды" or event.obj.text == "братик" or event.obj.text == "Братик":
                    send_msg('&#129302; Команды: просто напишите "-" и нужную вам команду\n&#128540; -лоли'
                             '\n&#129302; -команды\n&#8505; -инфо\n&#9832; -хентай\n&#127924; -арты\n&#128076; '
                             '\n-видео\n-ахегао\n-неко\n-запрет "команда" | например: (-запрет -лоли)')
                elif event.obj.text == "-я админ":
                    if adm_prov():
                        send_msg('Да, ты админ')
                    else:
                        send_msg('Увы но нет')
                # Ответы со вложениями --------------------------------------------------------------------------
                elif event.obj.text == "-арты" or event.obj.text == "-арт":
                    provzapret('-арт', 457241615, 457241726)
                elif event.obj.text == "-видос" or event.obj.text == "-видео":
                    send_vd(456239025, 456239134)
                elif event.obj.text == "-хентай" or event.obj.text == "-хент":
                    provzapret('-хент', 457239410, 457239961)
                elif event.obj.text == "-ахегао":
                    provzapret('-ахегао', 457241147, 457241266)
                elif event.obj.text == "-лоли" or event.obj.text == "-лоля":
                    provzapret('-лоли', 457239962, 457241144)
                elif event.obj.text == "-неко":
                    if random.randint(0, 1) == 1:
                        provzapret('-неко', 457241325, 457241424)
                    else:
                        provzapret('-неко', 457241502, 457241601)
                # Команды для запрета других команд (нужно подумать над оптимизацией) ---------------------------
                elif event.obj.text == "-запрет -лоли":
                    adm_prov_and_zapret('-лоли')
                elif event.obj.text == "-добавить мат":  # нужно подумать над аргументами фунции !!!!!!!!!!!!!!!!!!!!!!
                    if not provbadword('лох'):
                        addbadword('лох')
                    else:
                        send_msg('Мат уже был добавлен ранее')
                elif event.obj.text == "-запрет -ахегао":
                    adm_prov_and_zapret('-ахегао')
                elif event.obj.text == "-запрет -хентай":
                    adm_prov_and_zapret('-хент')
                elif event.obj.text == "-запрет -арт":
                    adm_prov_and_zapret('-арт')
                elif event.obj.text == "-запрет -неко":
                    adm_prov_and_zapret('-неко')
    except:
        print("SHTEFAN NINE!!!")
        main()


if __name__ == '__main__':
    main()
