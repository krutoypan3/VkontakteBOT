import time
import func_module

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
               'кто онлайн': func_module.who_online,
               'пока': func_module.bye_bye,
               'bb': func_module.bye_bye,
               'до завтра': func_module.bye_bye,
               'я пошел': func_module.bye_bye,
               'я ушел': func_module.bye_bye,
               'я пшел': func_module.bye_bye,
               'до скорого': func_module.bye_bye
               }

func_bye_bye_first = ['Пока', 'Прощай', 'Удачи', 'До скорого', 'Скоро увидимся',
                      'Тебя тут никто не держит', 'Бывай']
func_bye_bye_second = ['гнилой ананас', 'нелюдь', 'семпай', 'кохай', 'извращенец', 'б-бака!', 'сладенький', 'братишка',
                       'неудачник', 'бро', 'девственник']


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
               'бот': 'Я здесь, без паники!',
               'донат': 'Для покупки бро коинов перейдите по ссылке и оплатите нужное количество\n1 рубль = '
                        '2000 бро-коинов\n Ваш баланс будет пополнет в течении суток\nВ комментарии обязательно'
                        ' укажите ссылку на вашу страницу\nЯндексДеньги, Mastercard, Visa\n'
                        'https://yasobe.ru/na/br_koins\nQiwi.\nhttps://qiwi.com/n/AOM13',
               'команды': '⚙️ Полный список команд доступен по ссылке ' + 'vk.com/@bratikbot-commands',
               'братик': '⚙️ Полный список команд доступен по ссылке ' + 'vk.com/@bratikbot-commands',
               'братик команды': '⚙️ Полный список команд доступен по ссылке ' + 'vk.com/@bratikbot-commands',
               'инфо': "Мой разработчик - Оганесян Артем.\nВсе вопросы по реализации к нему: vk.com/aom13",
               'время': str(time.ctime())}