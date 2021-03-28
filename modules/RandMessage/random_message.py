from modules import func_module


def add_mess(peer_id, text):
    try:
        f = open('modules/RandMessage/messages/' + str(peer_id) + '.txt', 'a')
    except:
        f = open('modules/RandMessage/messages/' + str(peer_id) + '.txt', 'w')
        f.close()
        f = open('modules/RandMessage/messages/' + str(peer_id) + '.txt', 'a')
    try:
        f.write('\n' + text)
        f.close()
    except:
        f.close()


def get_mess(*args):
    peer_id = args[0]
    f = open('modules/RandMessage/messages/' + str(peer_id) + '.txt', 'r')
    x = f.readlines()
    f.close()
    func_module.send_msg_new(peer_id, x[func_module.random.randint(0, len(x) - 1)])
