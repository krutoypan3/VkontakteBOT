import json
import socket
import time
import requests
import urllib3
from vk_api.bot_longpoll import VkBotEventType

# Функция обработки ошибок
from db_module import con, sql_insert_anime_base
import functions_bot
from functions_bot import longpoll


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
        print("Бот работает...")
        def main():
            global oshibka, kolpot  # Счетчик ошибок и счетчик количества потоков
            try:
                for event in longpoll.listen():  # Постоянный листинг сообщений
                    if event.type == VkBotEventType.MESSAGE_NEW:  # Проверка на приход сообщения
                        if event.object.from_id > 0:
                            def messege_chek(peer_id, from_id, text):
                                slova = event.obj.text.lower().split()  # Разделение сообщения на слова
                                functions_bot.thread_start2(functions_bot.add_balans, from_id, '2')
                                # Логика ответов
                                # Игры --------------------------------------------------------------------------------
                                if len(slova) > 5:
                                    if slova[0] + ' ' + slova[1] + ' ' + slova[2] == 'случайное число от' and \
                                            slova[4] == 'до':
                                        functions_bot.thread_start3(functions_bot.random_ot_do_int_chislo, peer_id,
                                                                    slova[3], slova[5])
                                if len(slova) > 2:
                                    if slova[0] == 'DB' and slova[1] == 'insert':
                                        anime_name = ''
                                        for i in range(len(slova) - 4):
                                            if i > 1:
                                                anime_name += slova[i] + ' '
                                        entities = str(anime_name), str(slova[-4]), str(slova[-3]), \
                                                   str(slova[-2]), str(slova[-1])
                                        sql_insert_anime_base(con, entities)
                                        functions_bot.send_msg_new(peer_id, "Операция выполнена")
                                if len(slova) > 1:
                                    if slova[0] == 'DB' and slova[1] == 'help':
                                        functions_bot.send_msg_new(peer_id,
                                                                   "Для вставки новой строки в таблицу напишите:"
                                                                   "\nDB insert 'Название' 'жанр1' 'жанр2' 'жанр3' "
                                                                   "'кол-во серий'\n\nНапример:\nDB insert Этот "
                                                                   "замечательный мир Комедия Исекай Приключения 24")
                                    elif slova[0] + ' ' + slova[1] == 'игра 1':
                                        if not functions_bot.prov_zap_game(peer_id):
                                            functions_bot.thread_start2(functions_bot.game_ugadai_chislo, peer_id,
                                                                        from_id)
                                        else:
                                            functions_bot.send_msg_new(peer_id, '&#128377;Другая игра уже запущена!')
                                    elif slova[0] + ' ' + slova[1] == 'игра 2':
                                        if not functions_bot.prov_zap_game(peer_id):
                                            functions_bot.thread_start1(functions_bot.game_kto_kruche, peer_id)
                                        else:
                                            functions_bot.send_msg_new(peer_id, '&#128377;Другая игра уже запущена!')
                                    elif slova[0] + ' ' + slova[1] == 'игра 3':
                                        if not functions_bot.prov_zap_game(peer_id):
                                            functions_bot.thread_start1(functions_bot.game_brosok_kubika, peer_id)
                                        else:
                                            functions_bot.send_msg_new(peer_id, '&#128377;Другая игра уже запущена!')
                                    elif slova[0] + ' ' + slova[1] == 'игра 4':
                                        if not functions_bot.prov_zap_game(peer_id):
                                            functions_bot.thread_start2(functions_bot.game_mat_victorina, peer_id,
                                                                        from_id)
                                        else:
                                            functions_bot.send_msg_new(peer_id, '&#128377;Другая игра уже запущена!')
                                    elif slova[0] + ' ' + slova[1] == 'игра 5':
                                        if not functions_bot.prov_zap_game(peer_id):
                                            functions_bot.thread_start2(functions_bot.game_casino, peer_id, from_id)
                                        else:
                                            functions_bot.send_msg_new(peer_id, '&#128377;Другая игра уже запущена!')
                                    elif slova[0] + ' ' + slova[1] == 'клан создать':
                                        functions_bot.thread_start3(functions_bot.clan_create, peer_id, from_id, slova)
                                    elif slova[0] + ' ' + slova[1] == 'клан распад':
                                        functions_bot.thread_start2(functions_bot.clan_disvorse, peer_id, from_id)
                                    elif slova[0] + ' ' + slova[1] == 'клан кик':
                                        functions_bot.thread_start3(functions_bot.clan_kick, peer_id, from_id, slova[2])
                                    elif slova[0] + ' ' + slova[1] == 'клан покинуть':
                                        functions_bot.thread_start2(functions_bot.clan_leave, peer_id, from_id)
                                    elif slova[0] + ' ' + slova[1] == 'клан пригласить':
                                        functions_bot.thread_start3(functions_bot.clan_invite, peer_id, from_id,
                                                                    slova[2])
                                    elif len(slova) > 2:
                                        if slova[0] + ' ' + slova[1] + ' ' + slova[2] == 'клан баланс топ':
                                            functions_bot.thread_start1(functions_bot.clan_balance_top, peer_id)
                                    if slova[0] + ' ' + slova[1] == 'клан баланс':
                                        functions_bot.thread_start2(functions_bot.clan_balance, peer_id, from_id)
                                    elif slova[0] + ' ' + slova[1] == 'клан повысить':
                                        functions_bot.thread_start4(functions_bot.clan_up_down, peer_id, from_id,
                                                                    slova[2], True)
                                    elif slova[0] + ' ' + slova[1] == 'клан понизить':
                                        functions_bot.thread_start4(functions_bot.clan_up_down, peer_id, from_id,
                                                                    slova[2], False)
                                    elif slova[0] + ' ' + slova[1] == 'клан инфо':
                                        functions_bot.thread_start2(functions_bot.clan_info, peer_id, from_id)
                                    elif len(slova) > 3:
                                        if slova[0] + ' ' + slova[1] + ' ' + slova[2] == 'клан казна пополнить':
                                            functions_bot.thread_start3(functions_bot.clan_add_balance, peer_id,
                                                                        from_id, slova[3])
                                        elif slova[0] + ' ' + slova[1] + ' ' + slova[2] == 'клан казна вывести':
                                            functions_bot.thread_start3(functions_bot.clan_rem_balance, peer_id,
                                                                        from_id, slova[3])

                                # Текстовые ответы --------------------------------------------------------------------
                                if len(slova) > 0:
                                    if text == "клан" or text == "кланы" or text == "клан помощь" or \
                                            text == "кланы помощь":
                                        functions_bot.send_msg_new(peer_id, 'Клановые команды:\n'
                                                                            '\n'
                                                                            '⭐⭐⭐⭐⭐\n'
                                                                            '&#9209;Клан распад\n'
                                                                            '⭐⭐⭐⭐\n'
                                                                            '&#128183;Клан казна вывести "сумма"\n'
                                                                            '⭐⭐⭐\n'
                                                                            '🔼Клан повысить "кого"\n'
                                                                            '🔽Клан понизить "кого"\n'
                                                                            '⭐⭐\n'
                                                                            '&#9654;Клан пригласить "кого"\n'
                                                                            '⭐\n'
                                                                            '&#8505;Клан инфо\n'
                                                                            '&#9664;Клан покинуть\n'
                                                                            '&#127975;Клан баланс\n'
                                                                            '&#128200;Клан баланс топ\n'
                                                                            '&#128182;Клан казна пополнить "сумма"\n\n'
                                                                            '&#127381;Клан создать "название_слитно" |'
                                                                            '&#128184;15000 монет\n')

                                    if text == "братик привет":
                                        functions_bot.send_msg_new(peer_id, "&#128075; Приветик")
                                    elif text == "Донат" or text == "Купить бро коины" or \
                                            text == "донат" or text == "купить бро коины":
                                        functions_bot.send_msg_new(peer_id,
                                                                   'Для покупки бро коинов перейдите по ссылке и '
                                                                   'оплатите '
                                                                   'нужное'
                                                                   ' количество\n1 рубль = 2000 бро-коинов\n'
                                                                   'Ваш баланс будет пополнет в течении суток\n'
                                                                   'В комментарии обязательно укажите ссылку на вашу '
                                                                   'страницу\n'
                                                                   'https://yasobe.ru/na/br_koins')
                                    elif text == "Admin-reboot":
                                        functions_bot.send_msg_new(peer_id,
                                                                   "Бот уходит на перезагрузку и будет доступен "
                                                                   "через 10-15 секунд")
                                        functions_bot.zapros_ft_vd()
                                    elif text == "посоветуй аниме":
                                        functions_bot.thread_start1(functions_bot.anime_sovet, peer_id)
                                    elif text == "пока" or text == "спокойной ночи" or \
                                            text == "споки" or text == "bb":
                                        functions_bot.send_msg_new(peer_id, "&#128546; Прощай")
                                    elif text == "время":
                                        functions_bot.send_msg_new(peer_id, str(time.ctime()))
                                    elif text == "времятест":
                                        functions_bot.send_msg_new(peer_id, str(time.time()))
                                    elif text == "команды" or text == "братик":
                                        functions_bot.send_msg_new(peer_id,
                                                                   '⚙️ Полный список команд доступен по ссылке ' +
                                                                   'vk.com/@bratikbot-commands')
                                    elif text == "игры":
                                        functions_bot.klava_game(peer_id)
                                    elif text == "бро награда" or \
                                            text == "бро шекель":
                                        functions_bot.thread_start2(functions_bot.add_balans_every_day, peer_id,
                                                                    from_id)  # DB
                                    elif text == "бро баланс":
                                        functions_bot.thread_start2(functions_bot.balans_status, peer_id, from_id)
                                    elif text == "бро баланс топ":
                                        functions_bot.thread_start1(functions_bot.balans_top, peer_id)  # DB
                                    elif text == "онлайн" or text == "кто тут":
                                        functions_bot.send_msg_new(peer_id, functions_bot.who_online(peer_id))
                                    elif text == "инфо":
                                        functions_bot.send_msg_new(peer_id,
                                                                   "Мой разработчик - Оганесян Артем.\nВсе вопросы по "
                                                                   "реализации к нему: vk.com/aom13")
                                    elif text == "я админ":
                                        if functions_bot.adm_prov(peer_id, from_id):
                                            functions_bot.send_msg_new(peer_id, 'Да, ты админ')
                                        else:
                                            functions_bot.send_msg_new(peer_id, 'Увы но нет')
                                    # Ответы со вложениями ------------------------------------------------------------

                                    elif text == "арт":
                                        functions_bot.send_content(peer_id, functions_bot.photo_arts, 'арт', True)
                                    elif text == "nain":
                                        idphoto = 457242784
                                        functions_bot.provzapret_ft(peer_id, 'nain', str(idphoto))
                                        functions_bot.main_keyboard_arts(peer_id)
                                    elif text == "юри+":
                                        functions_bot.thread_start4(functions_bot.send_content, peer_id,
                                                                    functions_bot.photo_ur18, 'юри+', True)
                                    elif text == "стикер":
                                        functions_bot.thread_start4(functions_bot.send_content, peer_id,
                                                                    functions_bot.photo_stik, 'стикер', True)
                                    elif text == "coub":
                                        functions_bot.thread_start4(functions_bot.send_content, peer_id,
                                                                    functions_bot.video_coub, 'coub', False)
                                    elif text == "хентай":
                                        functions_bot.thread_start4(functions_bot.send_content, peer_id,
                                                                    functions_bot.photo_hent, 'хентай', True)
                                    elif text == "бдсм":
                                        functions_bot.thread_start4(functions_bot.send_content, peer_id,
                                                                    functions_bot.photo_bdsm, 'бдсм', True)
                                    elif text == "ахегао":
                                        functions_bot.thread_start4(functions_bot.send_content, peer_id,
                                                                    functions_bot.photo_aheg, 'ахегао', True)
                                    elif text == "лоли":
                                        functions_bot.thread_start4(functions_bot.send_content, peer_id,
                                                                    functions_bot.photo_loli, 'лоли', True)
                                    elif text == "неко":
                                        functions_bot.thread_start4(functions_bot.send_content, peer_id,
                                                                    functions_bot.photo_neko, 'неко', True)
                                    elif text == "манга арт":
                                        functions_bot.thread_start4(functions_bot.send_content, peer_id,
                                                                    functions_bot.photo_mart, 'манга арт', True)
                                    elif len(slova) > 1:
                                        if slova[0] == 'запрет':
                                            functions_bot.adm_prov_and_zapret(peer_id, from_id, slova[1])
                                        elif slova[1] == 'участвую':
                                            if not functions_bot.prov_zap_game(peer_id):
                                                functions_bot.send_msg_new(peer_id, 'Игра уже закончилась')
                                        elif slova[0] + ' ' + slova[1] == 'брак статус':
                                            functions_bot.thread_start2(functions_bot.marry_status, peer_id, from_id)
                                        elif slova[0] == "брак":
                                            functions_bot.thread_start3(functions_bot.marry_create, peer_id, from_id,
                                                                        slova[1])
                                        elif slova[0] == "перевести":
                                            functions_bot.thread_start4(functions_bot.money_send, peer_id, from_id,
                                                                        slova[1], slova[2])
                                    elif text == "развод":
                                        functions_bot.thread_start2(functions_bot.marry_disvorse, peer_id, from_id)
                                    # Отладка -------------------------------------------------------------------------
                                    elif text == 'dump':
                                        with open('dump.json', 'w') as dump:
                                            functions_bot.send_msg_new(peer_id, peer_id)
                                            auth = requests.get('https://oauth.vk.com/authorize',
                                                                params={
                                                                    'client_id': '7522555',
                                                                    'redirect_uri': 'https://oauth.vk.com/blank.html',
                                                                    'response_type': 'token'

                                                                }
                                                                )
                                            print(auth.text)
                                            json.dump(auth.text, dump)
                                            functions_bot.send_msg_new(peer_id, 'dumped')
                                    elif text == "начать" or text == "главная":
                                        if functions_bot.lich_or_beseda:
                                            functions_bot.main_keyboard_1(peer_id)
                                    elif text == "арты":
                                        if functions_bot.lich_or_beseda:
                                            functions_bot.main_keyboard_arts(peer_id)
                                    elif text == "18+":
                                        if functions_bot.lich_or_beseda:
                                            functions_bot.main_keyboard_hent(peer_id)
                                    elif text == "видео":
                                        if functions_bot.lich_or_beseda:
                                            functions_bot.main_keyboard_video(peer_id)
                                    elif text == "аниме(в разработке)" or text == "amv(в разработке)":
                                        functions_bot.send_msg_new(peer_id, "Написано же в разработке))")
                                        functions_bot.main_keyboard_1(peer_id)
                                    else:
                                        functions_bot.main_keyboard_1(peer_id)

                            functions_bot.thread_start3(messege_chek, event.object.peer_id, event.object.from_id,
                                                        event.obj.text.lower())
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
