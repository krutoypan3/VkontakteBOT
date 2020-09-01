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
        oshibka = 0  # обнуление счетчика ошибок | не трогать
        print("Бот работает...")
        games = {'1': func_module.game_ugadai_chislo,
                 '2': func_module.game_kto_kruche,
                 '3': func_module.game_brosok_kubika,
                 '4': func_module.game_mat_victorina,
                 '5': func_module.game_casino}
        clan = {'создать': func_module.clan_create,  # GOOD
                'распад': func_module.clan_disvorse,
                'кик': func_module.clan_kick,  # #
                'покинуть': func_module.clan_leave,
                'пригласить': func_module.clan_invite,  # #
                'баланс': func_module.clan_balance,  # #
                'повысить': func_module.clan_up_down,  # #
                'понизить': func_module.clan_up_down,  # #
                'инфо': func_module.clan_info,
                'топ': func_module.clan_balance_top,
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
                      'манга арт': func_module.photo_mart,
                      'этти': func_module.photo_etti,
                      'эччи': func_module.photo_etti}
        content_vd = {'coub': func_module.video_coub,
                      'хентай видео': func_module.video_hent,
                      'тикток': func_module.video_tikt,
                      'tiktok': func_module.video_tikt,
                      'тт': func_module.video_tikt,
                      'tt': func_module.video_tikt}
        keyboard = {'главная': func_module.main_keyboard_1,
                    'арты': func_module.main_keyboard_arts,
                    '18+': func_module.main_keyboard_hent,
                    'видео': func_module.main_keyboard_video}
        func_answer = {'бро награда': func_module.add_balans_every_day,
                       'бро баланс': func_module.balans_status,
                       'бро баланс топ': func_module.balans_top,
                       'развод': func_module.marry_disvorse,
                       'брак статус': func_module.marry_status,
                       'посоветуй аниме': func_module.anime_sovet,
                       'игры': func_module.klava_game,
                       'кто онлайн': func_module.who_online}
        func_answer_more_word = {'перевести': func_module.money_send,
                                 'брак': func_module.marry_create}
        text_answer = {'db help': "Для вставки новой строки в таблицу напишите:\nDB insert 'Название' 'жанр1' 'жанр2' "
                                  "'жанр3' 'кол-во серий'\n\nНапример:\nDB insert Этот замечательный мир Комедия "
                                  "Исекай Приключения 24",
                       'клан': 'Клановые команды:\n\n'
                               '⭐⭐⭐⭐⭐\n&#9209;Клан распад\n'
                               '⭐⭐⭐⭐\n&#128183;Клан вывести "сумма"\n '
                               '⭐⭐⭐\n🔼Клан повысить "кого"\n'
                               '🔽Клан понизить "кого"\n'
                               '⭐⭐\n&#9654;Клан пригласить "кого"\n'
                               '⭐\n&#8505;Клан инфо\n'
                               '&#9664;Клан покинуть\n'
                               '&#9664;Клан кик "кого"\n'
                               '&#127975;Клан баланс\n'
                               '&#128200;Клан топ\n'
                               '&#128182;Клан пополнить "сумма"\n\n'
                               '&#127381;Клан создать "название_слитно" | &#128184;5000 монет',
                       'братик привет': "&#128075; Приветик",
                       'донат': 'Для покупки бро коинов перейдите по ссылке и оплатите нужное количество\n1 рубль = '
                                '2000 бро-коинов\n Ваш баланс будет пополнет в течении суток\nВ комментарии обязательно'
                                ' укажите ссылку на вашу страницу\nhttps://yasobe.ru/na/br_koins',
                       'пока': "&#128546; Прощай",
                       'bb': "&#128546; Прощай",
                       'до завтра': "&#128546; Прощай",
                       'команды': '⚙️ Полный список команд доступен по ссылке ' + 'vk.com/@bratikbot-commands',
                       'братик': '⚙️ Полный список команд доступен по ссылке ' + 'vk.com/@bratikbot-commands',
                       'братик команды': '⚙️ Полный список команд доступен по ссылке ' + 'vk.com/@bratikbot-commands',
                       'инфо': "Мой разработчик - Оганесян Артем.\nВсе вопросы по реализации к нему: vk.com/aom13",
                       'время': str(time.ctime())}
        def main():
            try:
                for event in longpoll.listen():  # Постоянный листинг сообщений
                    if event.type == VkBotEventType.MESSAGE_NEW:  # Проверка на приход сообщения
                        if event.message.from_id > 0:
                            def message_chek(event_func):
                                # Занесение в переменные значений с события
                                from_id = event_func.message.from_id  # Кто написал
                                peer_id = event_func.message.peer_id  # Где написал
                                text = event_func.message.text.lower()  # Что написал
                                words = text.split()  # Разделение сообщения на слова
                                if 'reply_message' in event_func.message:  # Кому то писал?
                                    our_from = event_func.object.message["reply_message"]["from_id"]  # Кому написал
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
                                    if text in text_answer:
                                        func_module.thread_start(func_module.send_msg_new, peer_id, text_answer[text])
                                    if text in func_answer:
                                        func_module.thread_start(func_answer[text], peer_id, from_id, words, our_from,
                                                                 event_func)
                                    if words[0] in func_answer_more_word:
                                        func_module.thread_start(func_answer_more_word[words[0]], peer_id, from_id, words,
                                                                 our_from, event_func)
                                    elif text in content_ft:
                                        func_module.thread_start(func_module.send_content, peer_id, content_ft[text],
                                                                 text, True)
                                    elif text in content_vd:
                                        func_module.thread_start(func_module.send_content, peer_id, content_vd[text],
                                                                 text, False)
                                    if text == "Admin-reboot":
                                        func_module.send_msg_new(peer_id,
                                                                 "Бот уходит на перезагрузку и будет доступен "
                                                                 "через 10-15 секунд")
                                        func_module.zapros_ft_vd()
                                    elif text == "я админ":
                                        if func_module.adm_prov(peer_id, from_id):
                                            func_module.send_msg_new(peer_id, 'Да, ты админ')
                                        else:
                                            func_module.send_msg_new(peer_id, 'Увы но нет')
                                    elif text == "админ хентай":
                                        func_module.thread_start(func_module.admin_hentai, peer_id)
                                    elif text == "nain":
                                        id_photo = 457242784
                                        func_module.provzapret_ft(peer_id, 'nain', str(id_photo))
                                        func_module.main_keyboard_arts(peer_id)
                                    elif len(words) > 1:
                                        if words[0] == 'запрет':
                                            func_module.adm_prov_and_zapret(peer_id, from_id, words[1])
                                    if text in keyboard:
                                        func_module.thread_start(keyboard[text], peer_id)
                                    elif (text in content_ft) or (text in content_vd):
                                        pass
                                    else:
                                        func_module.thread_start(func_module.main_keyboard_1, peer_id)
                            func_module.thread_start(message_chek, event)
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
