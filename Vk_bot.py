import socket
import requests
import urllib3
from vk_api.bot_longpoll import VkBotEventType
from modules.Dict import *
from modules import func_module
from modules.func_module import longpoll
from modules import autowall


# Функция обработки ошибок
def error(ErrorF):
    global oshibka
    oshibka += 1
    print("Произошла ошибка " + '№' + str(oshibka) + ' ' + ErrorF)
    if ErrorF == " - ошибка подключения к вк":
        time.sleep(1.0)
    main()


if __name__ == '__main__':
    # Основной цикл программы
    try:
        # Первичный запуск
        func_module.thread_start(func_module.listing_new_anime_series)
        func_module.thread_start(autowall.create_post)
        oshibka = 0  # обнуление счетчика ошибок | не трогать
        print("Бот работает...")
        def main():
            try:
                for event in longpoll.listen():  # Постоянный листинг сообщений
                    def message_chek(event_func):
                        if event_func.type == VkBotEventType.MESSAGE_NEW:  # Проверка на приход сообщения
                            if event_func.message.from_id > 0:
                                if "action" in event_func.message:
                                    if 'member_id' in event_func.message['action']:
                                        if str(event_func.message["action"]["member_id"]) == '-' + str(func_module.group_id):
                                            func_module.send_msg_new(event_func.message.peer_id, 'Ку. Это типа приветствие;)')

                                # Занесение в переменные значений с события
                                from_id = event_func.message.from_id  # Кто написал
                                peer_id = event_func.message.peer_id  # Где написал
                                text = event_func.message.text.lower()  # Что написал
                                words = text.split()  # Разделение сообщения на слова
                                if 'reply_message' in event_func.message:  # Кому то писал?
                                    our_from = event_func.object.message["reply_message"]["from_id"]  # Кому написал
                                else:
                                    our_from = ''
                                # Логика ответов
                                func_module.thread_start(func_module.add_exp, peer_id, from_id)

                                if 'payload' in event_func.message:
                                    if peer_id > 2000000000:
                                        if event_func.message['payload'] in payload_button_group:
                                            func_module.thread_start(payload_button_group[event_func.message['payload']], peer_id, from_id, words, our_from,
                                                                     event_func)
                                if 'payload' in event_func.message:
                                    if 'payload_button_anime_follow_' in event_func.message['payload']:
                                        pass
                                if len(words) > 5:
                                    if words[0] + ' ' + words[1] + ' ' + words[2] == 'случайное число от' and \
                                            words[4] == 'до':
                                        func_module.thread_start(func_module.random_ot_do_int_chislo, peer_id,
                                                                 words[3], words[5])
                                if len(words) > 1:
                                    if words[0] == 'игра':
                                        if words[1] in games:
                                            if not func_module.prov_zap_game(peer_id):
                                                func_module.thread_start(games[words[1]], peer_id, from_id)
                                            else:
                                                func_module.send_msg_new(peer_id, '&#128377;Другая игра уже запущена!')
                                    if words[0] == 'клан':
                                        if words[1] in clan:
                                            func_module.thread_start(clan[words[1]], peer_id, from_id, words, our_from,
                                                                     event_func)
                                if len(words) > 0:
                                    '''if text == '+tt':
                                        func_module.video_save(peer_id, from_id, words, our_from, event_func)'''
                                    if text == 'биржа':
                                        func_module.thread_start(func_module.birzha, peer_id)
                                    '''if text == 'test':
                                        func_module.test_keyboard(peer_id)'''
                                    if text == 'test':
                                        func_module.thread_start(func_module.test_edit_message, peer_id, from_id, words,
                                                                 our_from, event_func)
                                    if text in text_answer:
                                        func_module.thread_start(func_module.send_msg_new, peer_id, text_answer[text])
                                    if text in func_answer:
                                        func_module.thread_start(func_answer[text], peer_id, from_id, words, our_from,
                                                                 event_func)
                                    if words[0] in func_answer_more_word:
                                        func_module.thread_start(func_answer_more_word[words[0]], peer_id, from_id,
                                                                 words, our_from, event_func)
                                    elif text in content_ft:
                                        func_module.thread_start(func_module.send_content, peer_id, content_ft[text],
                                                                 text, True)
                                    elif text in content_vd:
                                        func_module.thread_start(func_module.send_content, peer_id, content_vd[text],
                                                                 text, False)
                                    if text == "admin-reboot":
                                        func_module.send_msg_new(peer_id,
                                                                 "Бот уходит на перезагрузку и будет доступен "
                                                                 "через 10-15 секунд")
                                        func_module.zapros_ft_vd()
                                    elif text == "я админ":
                                        if func_module.adm_prov(peer_id, from_id):
                                            func_module.send_msg_new(peer_id, 'Да, ты админ')
                                        else:
                                            func_module.send_msg_new(peer_id, 'Увы но нет')
                                    elif len(words) > 1:
                                        if words[0] == 'запрет':
                                            func_module.adm_prov_and_zapret(peer_id, from_id, words[1])
                                    if text in keyboard:
                                        func_module.thread_start(keyboard[text], peer_id)
                                    elif (text in content_ft) or (text in content_vd):
                                        pass
                                    else:
                                        func_module.thread_start(func_module.main_keyboard_1, peer_id)

                        if event_func.type == VkBotEventType.MESSAGE_EVENT:
                            from_id = event_func.object.user_id  # Кто написал
                            peer_id = event_func.object.peer_id  # Где написал
                            if 'payload_button_anime_follow_' in event_func.object.payload.get('type'):
                                words = ('смотрю ' + event_func.object.payload.get('type')[28:]).split()
                                func_module.thread_start(func_module.add_anime_ongoing_listing, peer_id, from_id,
                                                         words, '', event_func)

                    func_module.thread_start(message_chek, event)


            except (requests.exceptions.ConnectionError, urllib3.exceptions.MaxRetryError,
                    urllib3.exceptions.NewConnectionError, socket.gaierror):
                error(" - ошибка подключения к вк")
            except Exception as ERROR:
                error(str(ERROR))

            finally:
                error('Неизвестная мне ошибка, но не критично, наверное')


        main()
    except (requests.exceptions.ConnectionError, urllib3.exceptions.MaxRetryError,
            urllib3.exceptions.NewConnectionError, socket.gaierror):
        error(" - ошибка подключения к вк")

    finally:
        error('Неизвестная мне ошибка, но не критично, наверное')
