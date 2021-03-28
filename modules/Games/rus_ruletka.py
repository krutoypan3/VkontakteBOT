from modules import func_module as fm


# Выбор ставки
def stavka_f(my_peer):
    timing = fm.time.time()
    keyboard = fm.VkKeyboard(inline=True)
    keyboard.add_button('Жизнь', color=fm.VkKeyboardColor.POSITIVE)
    keyboard.add_button('Развлечение', color=fm.VkKeyboardColor.POSITIVE)
    fm.vk.messages.send(peer_id=my_peer, random_id=fm.get_random_id(),
                     keyboard=keyboard.get_keyboard(), message='Выберите ставку:')
    for event_stavka in fm.longpoll.listen():
        if fm.time.time() - timing < 60.0:
            if event_stavka.type == fm.VkBotEventType.MESSAGE_NEW:
                slovo = event_stavka.message.text.split()
                if len(slovo) > 1:
                    if '0' <= slovo[1] <= '9':
                        fm.send_msg_new(my_peer, 'Ставка: ' + str(slovo[1]))
                        return slovo[1]
        else:
            return 'Развлечение'


# Игра кто круче
def game_rus_ruletka(*args):
    my_peer = args[0]
    fm.zapret_zap_game(my_peer)
    fm.send_msg_new(my_peer, '&#127918;Запущена русская рулетка". Чтобы принять участие, '
                          'напишите "участвую". '
                          '\nМинимальное количество участников для запуска: 2')
    stavka = stavka_f(my_peer)  # Ставка на игру
    kik = False
    if stavka == 'Развлечение':
        kik = True
    uchastniki = fm.nabor_igrokov(my_peer, stavka)  # Массив с id участников
    if len(uchastniki) < 2:
        fm.send_msg_new(my_peer, '&#127918;Слишком мало участников, игра отменена')
        fm.zapret_zap_game(my_peer)
    else:
        fm.send_msg_new(my_peer, '&#127918;Участники укомплектованы, да начнется игра на выживание!')
        vistrel = False
        while not vistrel:
            for i in uchastniki:
                fm.send_msg_new(my_peer, 'Барабан на револьвере крутит ' + fm.people_info(uchastniki[i]))
                if fm.random.randint(0, 5) == 1:
                    fm.send_msg_new(my_peer, 'ВЫСТРЕЛ!\n' + fm.people_info(uchastniki[i]) + ' засадил себе пулю в задницу!')
                    if kik:
                        fm.send_msg_new(my_peer, fm.people_info(uchastniki[i]) + ' пожертвовал своей задницей для адских утех')
                        fm.remove_chat_user(my_peer, '', '', uchastniki[i])
                    vistrel = True
                    break
                else:
                    fm.send_msg_new(my_peer, 'ВЫСТРЕЛ! Пусто...')
        fm.zapret_zap_game(my_peer)
