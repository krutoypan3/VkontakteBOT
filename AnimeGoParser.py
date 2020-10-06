import requests
from bs4 import BeautifulSoup


class AnimeGo:
    print('Создан экземпляр класса AnimeGo')
    def __init__(self, Anime_type):
        if Anime_type == 'ongoing':
            self.url = 'https://animego.org/anime/filter/status-is-ongoing-or-released/apply?&page='
            self.col = 3
            print('Инициализация класса AnimeGo ongoing')
        elif Anime_type == 'finish':
            self.url = 'https://animego.org/anime/filter/status-is-released/apply?&direction=desc&page='
            self.col = 100
            print('Инициализация класса AnimeGo finish')

    def random_anime(self):
        Anime = []
        url = self.url
        print('Инициализация функции AnimeGo.random_anime')
        for i in range(self.col):
            ani = url + str(i+1)
            print(ani)
            response = requests.request("GET", ani)
            print(response)
            print(response.text)
            try:
                soup = BeautifulSoup(response.text, "lxml")
                print(soup)
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
        print(len(Anime))
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
