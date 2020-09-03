# Работа с базой данных
import os
import socket
import psycopg2
import requests
import urllib3
from dotenv import load_dotenv
load_dotenv()


database_key = os.environ.get("database_key")
user_key = os.environ.get("user_key")
password_key = os.environ.get("password_key")
host_key = os.environ.get("host_key")
port_key = os.environ.get("port_key")


# Соединение с БД
def sql_connection():
    conc1 = psycopg2.connect(
        database=database_key,  # Название базы данных
        user=user_key,  # Имя пользователя
        password=password_key,  # Пароль пользователя
        host=host_key,  # Хост
        port=port_key  # Порт
    )
    return conc1


try:

    # Создание таблицы в БД
    def sql_table(conc3):
        cursorObj4 = conc3.cursor()  # Курсор БД
        cursorObj4.execute("CREATE TABLE clan_info(clan_name text, clan_money text, clan_admin text)")
        conc3.commit()


    con = sql_connection()  # Создание соединения с БД


    # Вставка СТРОКИ в ТАБЛИЦУ peer_params в БД
    def sql_insert(conc2, entities):
        cursorObj3 = conc2.cursor()
        cursorObj3.execute('INSERT INTO peer_params(peer_id, zapusk_game, filter_mata, zap_word) VALUES(%s, %s, %s, %s)', entities)
        conc2.commit()


    # Вставка СТРОКИ в ТАБЛИЦУ from_params в БД
    def sql_insert_from(conc2, entities):
        cursorObj3 = conc2.cursor()
        cursorObj3.execute(
            'INSERT INTO from_params(peer_id, from_id, money, m_time, warn, marry_id) VALUES(%s, %s, %s, %s, %s, %s)',
            entities)
        conc2.commit()


    # Вставка СТРОКИ в ТАБЛИЦУ from_money в БД
    def sql_insert_clan_info(conc2, entities):
        cursorObj3 = conc2.cursor()
        cursorObj3.execute(
            'INSERT INTO clan_info(clan_name, clan_money, clan_admin) VALUES(%s, %s, %s)',
            entities)
        conc2.commit()


    # Вставка СТРОКИ в ТАБЛИЦУ from_money в БД
    def sql_insert_from_money(conc2, entities):
        cursorObj3 = conc2.cursor()
        cursorObj3.execute(
            'INSERT INTO from_money(from_id, money, m_time, clan_name, first_name, last_name, clan_rank) '
            'VALUES(%s, %s, %s, %s, %s, %s, %s)',
            entities)
        conc2.commit()


    # Обновление параметра в таблице peer_params
    def sql_update(con5, what_fetch, what_fetch_new, peer_id_val):
        cursorObj1 = con5.cursor()
        cursorObj1.execute('UPDATE peer_params SET ' + str(what_fetch) + ' = ' + str(what_fetch_new) +
                           ' where peer_id = ' + str(peer_id_val))
        con5.commit()


    # Обновление параметра в таблице from_params
    def sql_update_from(con5, what_fetch, what_fetch_new, peer_id_val, from_id_val):
        cursorObj1 = con5.cursor()
        cursorObj1.execute('UPDATE from_params SET ' + str(what_fetch) + ' = ' + str(what_fetch_new) +
                           ' where peer_id = ' + str(peer_id_val) + ' AND from_id = ' + str(from_id_val))
        con5.commit()


    # Обновление параметра в таблице from_money INT
    def sql_update_from_money_int(con6, what_fetch, what_fetch_new, from_id_val):
        cursorObj1 = con6.cursor()
        cursorObj1.execute('UPDATE from_money SET ' + str(what_fetch) + ' = ' + str(what_fetch_new) +
                           ' where from_id = ' + str(from_id_val))
        con6.commit()

        # Обновление параметра в таблице from_money INT


    def sql_update_from_money_text(con6, what_fetch, what_fetch_new, from_id_val):
        cursorObj1 = con6.cursor()  # SELECT CAST ('100' AS INTEGER)
        cursorObj1.execute('UPDATE from_money SET ' + str(what_fetch) + ' = CAST(' + "'" + str(what_fetch_new) + "'"
                           + ' AS varchar)' +
                           ' where from_id = ' + str(from_id_val) + '::int')
        con6.commit()


    # Обновление параметра в таблице clan_info
    def sql_update_clan_info(con6, what_fetch, what_fetch_new, clan_id_val):
        cursorObj1 = con6.cursor()
        cursorObj1.execute('UPDATE clan_info SET ' + str(what_fetch) + ' = CAST(' + "'" + str(what_fetch_new) + "'"
                           + ' AS varchar)' +
                           ' where clan_name = CAST(' + "'" + str(clan_id_val) + "'" + ' AS varchar)')
        con6.commit()


    # Получение параметров из таблицы clan_info
    def sql_fetch_clan_info(conc, what_return, clan_name):
        try:
            cursorObj1 = conc.cursor()
            cursorObj1.execute('SELECT ' + str(what_return) + ' FROM clan_info WHERE clan_name = CAST(' + "'" +
                               str(clan_name) + "'" + ' AS varchar)')
            rows = cursorObj1.fetchall()[0]
            return rows
        except:
            cursorObj1 = conc.cursor()
            cursorObj1.execute("ROLLBACK")
            conc.commit()
            return 'NULL'


    def sql_delite_clan_info(conc, clan_name):
        cursorObj1 = conc.cursor()
        cursorObj1.execute('DELETE FROM clan_info WHERE clan_name = CAST(' + "'" + str(clan_name) +
                           "'" + ' AS varchar)')


    # Получение параметров из таблицы peer_params
    def sql_fetch(conc, what_return, peer_id_val):
        cursorObj1 = conc.cursor()
        cursorObj1.execute('SELECT ' + str(what_return) + ' FROM peer_params WHERE peer_id = ' + str(peer_id_val))
        rows = cursorObj1.fetchall()
        if len(rows) == 0:  # Проверка на наличие записи в таблице и при ее отсутствии, создание новой
            entities = peer_id_val, '0', '1', ''
            sql_insert(conc, entities)
            rows = sql_fetch(conc, what_return, peer_id_val)
        return rows


    # Получение параметров из таблицы from_params
    def sql_fetch_from(conc, what_return, peer_id_val, from_id_val):
        cursorObj1 = conc.cursor()
        cursorObj1.execute('SELECT ' + str(what_return) + ' FROM from_params WHERE peer_id = ' + str(
            peer_id_val) + ' AND from_id = ' + str(from_id_val))
        rows = cursorObj1.fetchall()
        if len(rows) == 0:  # Проверка на наличие записи в таблице и при ее отсутствии, создание новой
            entities = str(peer_id_val), str(from_id_val), '0', '0', '0', '0'
            sql_insert_from(conc, entities)
            rows = sql_fetch_from(conc, what_return, peer_id_val, from_id_val)
        return rows


    # Получение параметров из таблицы from_money
    def sql_fetch_from_money(conc, what_return, from_id):
        try:
            cursorObj1 = conc.cursor()
            cursorObj1.execute('SELECT ' + str(what_return) + ' FROM from_money WHERE from_id = ' + str(from_id))
            rows = cursorObj1.fetchall()
            if len(rows) == 0:  # Проверка на наличие записи в таблице и при ее отсутствии, создание новой
                from func_module import vk
                entities = str(from_id), '0', '0', 'NULL', str(vk.users.get(user_ids=from_id)[0]['first_name']), \
                           str(vk.users.get(user_ids=from_id)[0]['last_name']), '0'
                sql_insert_from_money(conc, entities)
                rows = sql_fetch_from_money(conc, what_return, from_id)
            return rows
        except 'psycopg2.errors.InFailedSqlTransaction':
            cursorObj1 = conc.cursor()
            cursorObj1.execute("ROLLBACK")
            conc.commit()
            print('что хотели вернуть - ', + what_return + ' \nкого - ' + from_id)
            return 'NULL'


    # Получение параметров из таблицы from_money
    def sql_fetch_from_money_clan(conc, what_return, clan_name):
        cursorObj1 = conc.cursor()
        cursorObj1.execute('SELECT ' + str(what_return) + ' FROM from_money WHERE clan_name = CAST(' + "'" +
                           str(clan_name) + "'" + ' AS varchar)')
        rows = cursorObj1.fetchall()
        return rows


    # Получение параметров из таблицы from_money
    def sql_fetch_from_all(conc, what_return, peer_id_val):
        cursorObj1 = conc.cursor()
        cursorObj1.execute('SELECT ' + str(what_return) + ' FROM from_money')  # WHERE peer_id = ' + str(peer_id_val)
        rows = cursorObj1.fetchall()
        return rows


    # Получение параметров из таблицы clan_info
    def sql_fetch_clan_all(conc, what_return):
        cursorOb1 = conc.cursor()
        cursorOb1.execute('SELECT ' + str(what_return) + ' FROM clan_info')
        rows = cursorOb1.fetchall()
        return rows


    # Получение параметров из таблицы anime_base
    def sql_fetch_anime_base(conc, janr, peer_id):
        cursorObj1 = conc.cursor()
        cursorObj1.execute('SELECT ' + str('name') + " FROM anime_base WHERE janr = '" + janr + "' OR janr2 = '"
                           + janr + "' OR janr3 = '" + janr + "'")
        rows = cursorObj1.fetchall()
        message = 'Аниме в жанре ' + janr + ':\n'
        for i in rows:
            message += i[0] + '\n'
        from func_module import send_msg_new
        send_msg_new(peer_id, message)


    # Вставка строки в таблицу anime_base
    def sql_insert_anime_base(conc2, entities):
        cursorObj3 = conc2.cursor()
        cursorObj3.execute(
            'INSERT INTO anime_base(name, janr, janr2, janr3, series) VALUES(%s, %s, %s, %s, %s)', entities)
        conc2.commit()


    # Обнуление игр во всех беседах
    cursorObj = con.cursor()
    cursorObj.execute('UPDATE peer_params SET zapusk_game = 0')
    con.commit()
except (requests.exceptions.ConnectionError, urllib3.exceptions.MaxRetryError,
        urllib3.exceptions.NewConnectionError, socket.gaierror):
    print(" - ошибка подключения к вк")

except 'psycopg2.errors.InFailedSqlTransaction':
    con = sql_connection()
    cursorObj2 = con.cursor()
    cursorObj2.execute("ROLLBACK")
    con.commit()
    print('Почему это произошло?')

except Exception:
    con = sql_connection()
    cursorObj2 = con.cursor()
    cursorObj2.execute("ROLLBACK")
    con.commit()
    print('OMG what is it?')