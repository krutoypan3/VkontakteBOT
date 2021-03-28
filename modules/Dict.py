import time
from modules import func_module
from modules.RandMessage import random_message
from modules.Games import rus_ruletka

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
              'эччи': func_module.photo_etti,
              'nain': func_module.photo_gitl}
content_vd = {'coub': func_module.video_coub,
              'хентай видео': func_module.video_hent,
              'тикток': func_module.video_tikt,
              'tiktok': func_module.video_tikt,
              'тт': func_module.video_tikt,
              'tt': func_module.video_tikt,
              'обои телефон': func_module.oboiv_tele}
keyboard = {'главная': func_module.main_keyboard_1,
            'арты': func_module.main_keyboard_arts,
            '18+': func_module.main_keyboard_hent,
            'видео': func_module.main_keyboard_video}
func_answer = {'бро награда': func_module.add_balans_every_day,
               'бро баланс': func_module.balans_status,
               'бро баланс топ': func_module.balans_top,
               'бро': func_module.add_balans_every_day,
               'развод': func_module.marry_disvorse,
               'брак статус': func_module.marry_status,
               'игры': func_module.klava_game,
               'кто онлайн': func_module.who_online,
               'пока': func_module.bye_bye,
               'bb': func_module.bye_bye,
               'бб': func_module.bye_bye,
               'до завтра': func_module.bye_bye,
               'я пошел': func_module.bye_bye,
               'я ушел': func_module.bye_bye,
               'я пшел': func_module.bye_bye,
               'до скорого': func_module.bye_bye,
               'курс': func_module.curs_value,
               'валюта': func_module.curs_value,
               'доллар': func_module.curs_value,
               'евро': func_module.curs_value,
               'id': func_module.dialog_id,
               'онгоинги': func_module.AnimeGo_Ongoings,
               'онгоинг': func_module.AnimeGo_Ongoings,
               'выходит': func_module.AnimeGo_Ongoings,
               'что выходит': func_module.AnimeGo_Ongoings,
               'онг': func_module.AnimeGo_Ongoings,
               'случайное аниме': func_module.AnimeGo_Finish,
               'посоветуй фильм': func_module.Film_popular,
               'фильм': func_module.Film_popular,
               'популярный фильм': func_module.Film_popular,
               'популярные фильмы': func_module.Film_popular,
               'популярное': func_module.Film_popular,
               'info': func_module.info_for_user,
               'инфа': func_module.info_for_user,
               'информация': func_module.info_for_user,
               'обо мне': func_module.info_for_user,
               'я': func_module.info_for_user,
               'кто я': func_module.info_for_user,
               'информация обо мне': func_module.info_for_user,
               'следить за аниме': func_module.anime_ongoings_list,
               'мой календарь': func_module.anime_ongoing_pesonal_list,
               '!ахегао': func_module.ahegao_edit_message,
               'посоветуй аниме': func_module.AnimeGo_Finish,
               'посоветуй онгоинг': func_module.AnimeGo_Ongoings,
               'что за аниме': func_module.anime_search_from_image,
               'что это': func_module.anime_search_from_image,
               'что это за аниме': func_module.anime_search_from_image,
               'кто это': func_module.anime_search_from_image,
               'rand': random_message.get_mess,
               # 'дуэль': rus_ruletka.game_rus_ruletka,
               # 'testkey': func_module.test_keyboard,
               # 'mafiatest': func_module.MAFIA_GAME,
               'mine list': func_module.send_command_to_minecraft_server_lite,
               }

func_bye_bye_first = ['Пока', 'Прощай', 'Удачи', 'До скорого', 'Скоро увидимся',
                      'Тебя тут никто не держит', 'Бывай']
func_bye_bye_second = ['гнилой ананас', 'нелюдь', 'семпай', 'кохай', 'извращенец', 'б-бака!', 'сладенький', 'братишка',
                       'неудачник', 'бро', 'девственник']

func_answer_more_word = {'перевести': func_module.money_send,
                         'брак': func_module.marry_create,
                         'ковид': func_module.covid,
                         'коронавирус': func_module.covid,
                         'погода': func_module.weather,
                         'covid': func_module.covid,
                         'аниме': func_module.AnimeGo_Search,
                         'anime': func_module.AnimeGo_Search,
                         'смотрю': func_module.add_anime_ongoing_listing,
                         'minep': func_module.send_commnad_to_minecraft_server_password,
                         }
text_answer = {'db help': "Для вставки новой строки в таблицу напишите:\nDB insert 'Название' 'жанр1' 'жанр2' "
                          "'жанр3' 'кол-во серий'\n\nНапример:\nDB insert Этот замечательный мир Комедия "
                          "Исекай Приключения 24",
               'идея': '&#127880;Скажите, что вы хотели бы увидеть в боте нового?&#127880;\n'
                       'https://forms.gle/Q5ahBpR8csVAnRMM7',
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
               'время': str(time.ctime()),
               'minecraft': 'Скачать сборку можно по этой ссылке: '
                            '\n'
                            'Полная сборка: https://drive.google.com/drive/folders/1tV0UNeStzMSgUp419xaEafqrgHDfTQ4c?usp=sharing\n'
                            'Или же скачать файлы с расширением .jar и скинуть в папку mods\n'
                            'Новые моды: https://cloud.mail.ru/public/2dxj/RqjcwQreL\n'
                            'Инструкция по подключению: '
                            'https://docs.google.com/document/d/1udSQnv_EJyJ3NSrNxbKWLQYLj7b2tidpfOjsePEcPkQ/edit?usp=sharing \n'
                            '\nСервер работает только когда его включил @aom13(Артем)'}

payload_button_group = {
    '"sovet_anime"': func_module.AnimeGo_Finish,
    '"sovet_ongoing"': func_module.AnimeGo_Ongoings,
}
