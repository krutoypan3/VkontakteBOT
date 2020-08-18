import json
import socket
import time
import requests
import urllib3
from vk_api.bot_longpoll import VkBotEventType

# Функция обработки ошибок
from db_module import con, sql_insert_anime_base
import func_module
from func_module import longpoll


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
        print("Бот работает...")
        games = {'1': func_module.game_ugadai_chislo,
                 '2': func_module.game_kto_kruche,
                 '3': func_module.game_brosok_kubika,
                 '4': func_module.game_mat_victorina,
                 '5': func_module.game_casino}
        clan = {'создать': func_module.clan_create,     # GOOD
                'распад': func_module.clan_disvorse,
                'кик': func_module.clan_kick,           # #
                'покинуть': func_module.clan_leave,
                'пригласить': func_module.clan_invite,  # #
                'баланс': func_module.clan_balance,     # #
                'повысить': func_module.clan_up_down,   # #
                'понизить': func_module.clan_up_down,   # #
                'инфо': func_module.clan_info}          # #
        clan2 = {'топ': func_module.clan_balance_top,
                 'пополнить': func_module.clan_add_balance,
                 'вывести': func_module.clan_rem_balance}
        content_ft = {'арт': func_module.photo_arts,
                      'юри+': func_module.photo_ur18,
                      'стикер': func_module.photo_stik,
                      'хентай': func_module.photo_hent,
                      'бдсм': func_module.photo_bdsm,
                      'ахегао': func_module.photo_aheg,
                      'лоли': func_module.photo_loli,
                      'неко': func_module.photo_neko,
                      'манга арт': func_module.photo_mart}
        content_vd = {'coub': func_module.video_coub}

        def main():
            try:
                for event in longpoll.listen():  # Постоянный листинг сообщений
                    if event.type == VkBotEventType.MESSAGE_NEW:  # Проверка на приход сообщения
                        if event.message.from_id > 0:
                            def messege_chek(event_func):

                                # Занесение в переменные значений с события
                                from_id = event_func.message.from_id  # Кто написал
                                peer_id = event_func.message.peer_id  # Где написал
                                text = event_func.message.text.lower()  # Что написал
                                words = text.split()  # Разделение сообщения на слова
                                if 'reply_message' in event_func.message:  # Кому то писал?
                                    our_from = event_func.object.message["reply_message"]["from_id"]   # Кому написал
                                else:
                                    our_from = ''
                                func_module.thread_start(func_module.add_balans, from_id, '2')  # Добавляем 2 монетки

                                # Логика ответов
                                # Игры --------------------------------------------------------------------------------
                                if len(words) > 5:
                                    if words[0] + ' ' + words[1] + ' ' + words[2] == 'случайное число от' and \
                                            words[4] == 'до':
                                        func_module.thread_start(func_module.random_ot_do_int_chislo, peer_id,
                                                                 words[3], words[5])
                                if len(words) > 2:
                                    if words[0] == 'DB' and words[1] == 'insert':
                                        anime_name = ''
                                        for i in range(len(words) - 4):
                                            if i > 1:
                                                anime_name += words[i] + ' '
                                        entities = str(anime_name), str(words[-4]), str(words[-3]), \
                                                   str(words[-2]), str(words[-1])
                                        sql_insert_anime_base(con, entities)
                                        func_module.send_msg_new(peer_id, "Операция выполнена")
                                if len(words) > 1:
                                    if words[0] == 'DB' and words[1] == 'help':
                                        func_module.send_msg_new(peer_id,
                                                                 "Для вставки новой строки в таблицу напишите:"
                                                                 "\nDB insert 'Название' 'жанр1' 'жанр2' 'жанр3' "
                                                                 "'кол-во серий'\n\nНапример:\nDB insert Этот "
                                                                 "замечательный мир Комедия Исекай Приключения 24")
                                    # good \/
                                    if words[0] == 'игра':
                                        if words[1] in games:
                                            if not func_module.prov_zap_game(peer_id):
                                                func_module.thread_start(games[words[1]], peer_id, from_id)
                                            else:
                                                func_module.send_msg_new(peer_id, '&#128377;Другая игра уже запущена!')
                                    if words[0] == 'клан':
                                        if words[1] in clan:
                                            func_module.thread_start(clan[words[1]], peer_id, from_id, words, our_from)
                                        if len(words) > 2:
                                            if words[2] in clan2:
                                                if len(words) > 2:
                                                    if words[0] + ' ' + words[1] == 'клан баланс':
                                                        func_module.thread_start(clan2[words[2]], peer_id,
                                                                                 from_id, words)

                                    # good /\
                                # Текстовые ответы --------------------------------------------------------------------
                                if len(words) > 0:
                                    if text == "клан" or text == "кланы" or text == "клан помощь" or \
                                            text == "кланы помощь":
                                        func_module.send_msg_new(peer_id, 'Клановые команды:\n'
                                                                          '\n'
                                                                          '⭐⭐⭐⭐⭐\n'
                                                                          '&#9209;Клан распад\n'
                                                                          '⭐⭐⭐⭐\n'
                                                                          '&#128183;Клан баланс вывести "сумма"\n'
                                                                          '⭐⭐⭐\n'
                                                                          '🔼Клан повысить "кого"\n'
                                                                          '🔽Клан понизить "кого"\n'
                                                                          '⭐⭐\n'
                                                                          '&#9654;Клан пригласить "кого"\n'
                                                                          '⭐\n'
                                                                          '&#8505;Клан инфо\n'
                                                                          '&#9664;Клан покинуть\n'
                                                                          '&#9664;Клан кик "кого"\n'
                                                                          '&#127975;Клан баланс\n'
                                                                          '&#128200;Клан баланс топ\n'
                                                                          '&#128182;Клан баланс пополнить "сумма"\n\n'
                                                                          '&#127381;Клан создать "название_слитно" |'
                                                                          '&#128184;5000 монет\n')

                                    elif text == "братик привет":
                                        func_module.send_msg_new(peer_id, "&#128075; Приветик")
                                    elif text == "Донат" or text == "Купить бро коины" or \
                                            text == "донат" or text == "купить бро коины":
                                        func_module.send_msg_new(peer_id,
                                                                 'Для покупки бро коинов перейдите по ссылке и '
                                                                 'оплатите '
                                                                 'нужное'
                                                                 ' количество\n1 рубль = 2000 бро-коинов\n'
                                                                 'Ваш баланс будет пополнет в течении суток\n'
                                                                 'В комментарии обязательно укажите ссылку на вашу '
                                                                 'страницу\n'
                                                                 'https://yasobe.ru/na/br_koins')
                                    elif text == "Admin-reboot":
                                        func_module.send_msg_new(peer_id,
                                                                 "Бот уходит на перезагрузку и будет доступен "
                                                                 "через 10-15 секунд")
                                        func_module.zapros_ft_vd()
                                    elif text == "посоветуй аниме":
                                        func_module.thread_start(func_module.anime_sovet, peer_id)
                                    elif text == "пока" or text == "спокойной ночи" or \
                                            text == "споки" or text == "bb":
                                        func_module.send_msg_new(peer_id, "&#128546; Прощай")
                                    elif text == "время":
                                        func_module.send_msg_new(peer_id, str(time.ctime()))
                                    elif text == "команды" or text == "братик":
                                        func_module.send_msg_new(peer_id,
                                                                 '⚙️ Полный список команд доступен по ссылке ' +
                                                                 'vk.com/@bratikbot-commands')
                                    elif text == "игры":
                                        func_module.klava_game(peer_id)
                                    elif text == "бро награда" or \
                                            text == "бро шекель":
                                        func_module.thread_start(func_module.add_balans_every_day, peer_id,
                                                                 from_id)  # DB
                                    elif text == "бро баланс":
                                        func_module.thread_start(func_module.balans_status, peer_id, from_id)
                                    elif text == "бро баланс топ":
                                        func_module.thread_start(func_module.balans_top, peer_id)  # DB
                                    elif text == "онлайн" or text == "кто тут":
                                        func_module.send_msg_new(peer_id, func_module.who_online(peer_id))
                                    elif text == "инфо":
                                        func_module.send_msg_new(peer_id,
                                                                 "Мой разработчик - Оганесян Артем.\nВсе вопросы по "
                                                                 "реализации к нему: vk.com/aom13")
                                    elif text == "я админ":
                                        if func_module.adm_prov(peer_id, from_id):
                                            func_module.send_msg_new(peer_id, 'Да, ты админ')
                                        else:
                                            func_module.send_msg_new(peer_id, 'Увы но нет')
                                    # Ответы со вложениями ------------------------------------------------------------
                                    elif text in content_ft:
                                        func_module.thread_start(func_module.send_content, peer_id, content_ft[text],
                                                                 text, True)
                                    elif text in content_vd:
                                        func_module.thread_start(func_module.send_content, peer_id, content_vd[text],
                                                                 text, False)

                                    elif text == "nain":
                                        idphoto = 457242784
                                        func_module.provzapret_ft(peer_id, 'nain', str(idphoto))
                                        func_module.main_keyboard_arts(peer_id)
                                    elif len(words) > 1:
                                        if words[0] == 'запрет':
                                            func_module.adm_prov_and_zapret(peer_id, from_id, words[1])
                                        elif words[1] == 'участвую':
                                            if not func_module.prov_zap_game(peer_id):
                                                func_module.send_msg_new(peer_id, 'Игра уже закончилась')
                                        elif words[0] + ' ' + words[1] == 'брак статус':                            #
                                            func_module.thread_start(func_module.marry_status, peer_id, from_id,
                                                                     words, our_from)
                                    elif words[0] == "брак":                                                        #
                                        func_module.thread_start(func_module.marry_create, peer_id, from_id,
                                                                 words, our_from)
                                    elif words[0] == "перевести":                                                   #
                                        func_module.thread_start(func_module.money_send, peer_id, from_id,
                                                                 words, our_from)
                                    elif text == "развод":
                                        func_module.thread_start(func_module.marry_disvorse, peer_id, from_id)
                                    # Отладка -------------------------------------------------------------------------
                                    elif text == 'dump':
                                        with open('dump.json', 'w') as dump:
                                            func_module.send_msg_new(peer_id, peer_id)
                                            auth = requests.get('https://oauth.vk.com/authorize',
                                                                params={
                                                                    'client_id': '7522555',
                                                                    'redirect_uri': 'https://oauth.vk.com/blank.html',
                                                                    'response_type': 'token'

                                                                }
                                                                )
                                            print(auth.text)
                                            json.dump(auth.text, dump)
                                            func_module.send_msg_new(peer_id, 'dumped')
                                    elif text == "начать" or text == "главная":
                                        if func_module.lich_or_beseda:
                                            func_module.main_keyboard_1(peer_id)
                                    elif text == "арты":
                                        if func_module.lich_or_beseda:
                                            func_module.main_keyboard_arts(peer_id)
                                    elif text == "18+":
                                        if func_module.lich_or_beseda:
                                            func_module.main_keyboard_hent(peer_id)
                                    elif text == "видео":
                                        if func_module.lich_or_beseda:
                                            func_module.main_keyboard_video(peer_id)
                                    elif text == "аниме(в разработке)" or text == "amv(в разработке)":
                                        func_module.send_msg_new(peer_id, "Написано же в разработке))")
                                        func_module.main_keyboard_1(peer_id)
                                    else:
                                        func_module.main_keyboard_1(peer_id)

                            func_module.thread_start(messege_chek, event)
            except (requests.exceptions.ConnectionError, urllib3.exceptions.MaxRetryError,
                    urllib3.exceptions.NewConnectionError, socket.gaierror):
                error(" - ошибка подключения к вк")

            finally:
                error('Неизвестная мне ошибка, но не критично, наверное')


        main()
    except (requests.exceptions.ConnectionError, urllib3.exceptions.MaxRetryError,
            urllib3.exceptions.NewConnectionError, socket.gaierror):
        error(" - ошибка подключения к вк")

    finally:
        error('Неизвестная мне ошибка, но не критично, наверное')
