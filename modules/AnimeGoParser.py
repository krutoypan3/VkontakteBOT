import requests
from bs4 import BeautifulSoup
import sqlite3

headers = {'authoriti': 'animego.org',
           'method': 'GET',
           'path': '/',
           'scheme': 'https',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
           'Accept-Language': 'ru,ru-ru;q=0.5',
           'Accept-Encoding': 'gzip, deflate, br',
           'cookie': 'device_view=full; REMEMBERME=VU5cVXNlckJ1bmRsZVxFbnRpdHlcVXNlcjpZVzl0TVRNPToxNjMzNzQ0NzUzOmZmM'
                     'ThhNGU3Mjk4OTgyZDcwNWU4OWYxNzdmMzRlYzViYzNmZWE2MjY5ZWM2MjY5YmUyYzgzYzU5YWQzOGZlNDk%3D',
           # ВАЖНО Я ХЗ НАСЧЕТ СТАБИЛЬНОЙ РАБОТЫ
           'DNT': '1',  # ЭТОГО КЛЮЧА PHPSESSID
           'Upgrade-Insecure-Requests': '1',
           'sec-fetch-user': '?1',
           'sec-fetch-dest': 'document',
           'sec-fetch-mode': 'navigate',
           'sec-fetch-site': 'none',
           'Cache-Control': 'max-age=0'}


def series(Anime_urls):  # Определяет кол-во серий в аниме
    try:
        response2 = requests.request("GET", Anime_urls, headers=headers)
        soup2 = BeautifulSoup(response2.text, "lxml")
        anima2 = soup2.find_all('div', {'class': 'anime-info'})  # Получаем все таблицы с вопросами
        Anime_seri = ''
        for i in range(len(anima2[0].contents[0].contents)):
            Anime_seri = anima2[0].contents[0].contents[i].next
            if Anime_seri == 'Эпизоды':
                Anime_seri = anima2[0].contents[0].contents[i+1].next
                return Anime_seri
        return 'неизвестно'
    except Exception:
        return 'неизвестно'


def search(Anime_name):  # Поиск аниме по названию
    Anime_name_q = ''
    Anime_name = Anime_name.split()
    for i in range(len(Anime_name)):
        Anime_name_q += Anime_name[i]
        if Anime_name[-1] != Anime_name[i]:
            Anime_name_q += '+'
    response = requests.request("get", 'https://animego.org/search/all?q=' + Anime_name_q, headers=headers)
    try:
        soup = BeautifulSoup(response.text, "lxml")
        anima = soup.find_all('div', {'class': 'animes-grid-item col-6 col-sm-6 col-md-4 col-lg-3 col-xl-2 col-ul-2'})  # Получаем все таблицы с вопросами
        for animeshka in anima:
            try:
                Anime_name = animeshka.contents[0].contents[1].contents[1].contents[0].attrs['title']  # Название+
                Anime_type = animeshka.contents[0].contents[1].contents[2].contents[0].contents[0].next  # Тип аниме+
                Anime_year = animeshka.contents[0].contents[1].contents[2].contents[2].contents[0].next  # год+
                Anime_urls = animeshka.contents[0].contents[1].contents[1].contents[0].attrs['href']  # Ссылка+
                try:
                    Anime_rait = animeshka.contents[0].contents[0].contents[2].contents[0].contents[1].next  # рейтинг+
                except IndexError:
                    Anime_rait = 'без рейтинга'
                try:
                    Anime_pict = animeshka.contents[0].contents[0].contents[1].contents[0].attrs['data-original']  # Картинка+
                except KeyError:
                    Anime_pict = 'https://upload.wikimedia.org/wikipedia/ru/0/04/%D0%9D%D0%95%D0%A2_%D0%94%D0%9E%D0%A1%D0%A2%D0%A3%D0%9F%D0%9D%D0%9E%D0%93%D0%9E_%D0%98%D0%97%D0%9E%D0%91%D0%A0%D0%90%D0%96%D0%95%D0%9D%D0%98%D0%AF.jpg'

                return Anime_name, Anime_pict, Anime_urls, Anime_type, Anime_year, Anime_rait
            except IndexError as ERROR:
                print(ERROR)
    except UnicodeEncodeError as ERROR:
        print(ERROR)


search('Akame ga kill')


class AnimeGo:
    print('Создан экземпляр класса AnimeGo')
    def __init__(self, Anime_type):
        if Anime_type == 'ongoing':
            self.url = 'https://animego.org/anime/filter/type-is-tv-or-movie/status-is-ongoing-or-released/apply?&page='
            self.col = 3
            print('Инициализация класса AnimeGo ongoing')
        elif Anime_type == 'finish':
            self.url = 'https://animego.org/anime/filter/type-is-tv-or-movie/status-is-released/apply?&direction=desc&page='
            self.col = 100
            print('Инициализация класса AnimeGo finish')

    def random_anime(self):
        Anime = []
        url = self.url
        print('Инициализация функции AnimeGo.random_anime')
        for i in range(self.col):
            print('Сканирование тайтлов - ' + str(i) + '%')
            ani = url + str(i+1)
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.90 Safari/537.36,',
                'Origin': 'http://example.com',
                'Referer': 'http://example.com/some_page'}
            response = requests.request("get", ani, headers=headers)
            try:
                soup = BeautifulSoup(response.text, "lxml")
                anima = soup.find_all('div', {'id': 'anime-list-container'})  # Получаем все таблицы с вопросами
                for animeshka in anima:
                    for g in range(len(animeshka.contents)):
                        try:
                            Anime_janr = []
                            Anime_name = animeshka.contents[g].next.contents[1].contents[0].next.next  # Название
                            Anime_type = animeshka.contents[g].next.contents[1].contents[2].next.next.next  # Тип аниме
                            Anime_year = animeshka.contents[g].next.contents[1].contents[2].contents[2].next.next  # год
                            Anime_urls = animeshka.contents[g].next.contents[1].contents[0].next.attrs['href']  # Ссылка

                            try:
                                Anime_rait = animeshka.contents[g].next.contents[0].contents[2].contents[0].contents[1].next  # рейтинг
                            except IndexError:
                                Anime_rait = 'без рейтинга'


                            '''def series():
                                response2 = requests.request("GET", Anime_urls)
                                soup2 = BeautifulSoup(response2.text, "lxml")
                                anima2 = soup2.find_all('div', {'class': 'anime-info'})  # Получаем все таблицы с вопросами
                                Anime_ser = anima2[0].contents[0].contents[3].next
                                return Anime_ser
                            Anime_seri = series()'''

                            try:
                                for k in range(len(animeshka.contents[g].next.contents[1].contents[2].contents[4].contents)):
                                    if k % 2 == 0:
                                        Anime_janr.append(animeshka.contents[g].next.contents[1].contents[2].contents[4].contents[k].next)
                            except IndexError:
                                Anime_janr.append('Информация о жанрах отсутствует')

                            try:
                                Anime_pict = animeshka.contents[g].next.contents[0].contents[0].next.next['data-original']  # Картинка
                            except KeyError:
                                Anime_pict = 'https://upload.wikimedia.org/wikipedia/ru/0/04/%D0%9D%D0%95%D0%A2_%D0%94%D0%9E%D0%A1%D0%A2%D0%A3%D0%9F%D0%9D%D0%9E%D0%93%D0%9E_%D0%98%D0%97%D0%9E%D0%91%D0%A0%D0%90%D0%96%D0%95%D0%9D%D0%98%D0%AF.jpg'

                            if len(animeshka.contents[g].next.contents[1].contents[3].contents) > 0:
                                Anime_dict = animeshka.contents[g].next.contents[1].contents[3].contents[0]
                            else:
                                Anime_dict = 'Описание отсутствует'
                            while '\n' in Anime_dict or '  ' in Anime_dict:
                                Anime_dict = Anime_dict.replace("\n", "")
                                Anime_dict = Anime_dict.replace("  ", " ")

                            Anime.append([Anime_name, Anime_pict, Anime_urls, Anime_dict, Anime_type, Anime_year, Anime_janr, Anime_rait])
                        except IndexError as ERROR:
                            print(ERROR)
            except UnicodeEncodeError as ERROR:
                print(ERROR)
        print('Количество аниме в базе - ' + str(len(Anime)))
        return Anime

# rec = AnimeGo('finish')
# print(len(rec.random_anime()))
# ric = AnimeGo('ongoing')
# print(len(ric.random_anime()))
# 0 0 - Название
# 0 1 - Картинка
# 0 2 - Ссылка
# 0 3 - Описание
# 0 4 - Тип аниме
# 0 4 - Год выхода
# 0 5 - Жанр аниме
# 0 6 - Рейтинг аниме
# 0 7 - Кол-во серий