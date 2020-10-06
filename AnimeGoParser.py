import requests
from bs4 import BeautifulSoup


class AnimeGoFinish:
    def __init__(self):
        Anime = []
        url = 'https://animego.org/anime/filter/status-is-released/apply?&direction=desc&page='
        for i in range(100):
            ani = url + str(i+1)
            response = requests.request("GET", ani)
            try:
                with open('test.html', 'w', encoding='utf-8') as output_file:
                    output_file.write(response.text)
                soup = BeautifulSoup(response.text, "lxml")
                anima = soup.find_all('div', {'id': 'anime-list-container'})  # Получаем все таблицы с вопросами
                for animeshka in anima:
                    for g in range(len(animeshka.contents)):
                        Anime_name = animeshka.contents[i].next.contents[1].contents[0].next.next  # Название
                        try:
                            Anime_pict = animeshka.contents[i].next.contents[0].contents[0].next.next['data-original']  # Картинка
                        except KeyError:
                            Anime_pict = 'https://upload.wikimedia.org/wikipedia/ru/0/04/%D0%9D%D0%95%D0%A2_%D0%94%D0%9E%D0%A1%D0%A2%D0%A3%D0%9F%D0%9D%D0%9E%D0%93%D0%9E_%D0%98%D0%97%D0%9E%D0%91%D0%A0%D0%90%D0%96%D0%95%D0%9D%D0%98%D0%AF.jpg'
                        Anime_urls = animeshka.contents[i].next.contents[1].contents[0].next.attrs['href']  # Ссылка
                        if len(animeshka.contents[i].next.contents[1].contents[3].contents) > 0:
                            Anime_dict = animeshka.contents[i].next.contents[1].contents[3].contents[0]
                        else:
                            Anime_dict = 'Описание отсутствует'
                        while '\n' in Anime_dict or '  ' in Anime_dict:
                            Anime_dict = Anime_dict.replace("\n", "")
                            Anime_dict = Anime_dict.replace("  ", " ")
                        Anime.append([Anime_name, Anime_pict, Anime_urls, Anime_dict])
            except UnicodeEncodeError as ERROR:
                print(ERROR)


class AnimeGoOngoing:
    def __init__(self):
        Anime = []
        url = ['https://animego.org/anime/filter/status-is-ongoing-or-released/apply?&page=1',
               'https://animego.org/anime/filter/status-is-ongoing-or-released/apply?&page=2',
               'https://animego.org/anime/filter/status-is-ongoing-or-released/apply?&page=3']
        for i in url:
            response = requests.request("GET", i)
            with open('test.html', 'w', encoding='utf-8') as output_file:
                output_file.write(response.text)
            soup = BeautifulSoup(response.text, "lxml")
            anima = soup.find_all('div', {'id': 'anime-list-container'})  # Получаем все таблицы с вопросами
            for animeshka in anima:
                for g in range(len(animeshka.contents)):
                    Anime_name = animeshka.contents[i].next.contents[1].contents[0].next.next  # Название
                    Anime_pict = animeshka.contents[i].next.contents[0].contents[0].next.next['data-original']  # Картинка
                    Anime_urls = animeshka.contents[i].next.contents[1].contents[0].next.attrs['href']  # Ссылка
                    if len(animeshka.contents[i].next.contents[1].contents[3].contents) > 0:
                        Anime_dict = animeshka.contents[i].next.contents[1].contents[3].contents[0]
                    else:
                        Anime_dict = 'Описание отсутствует'
                    while '\n' in Anime_dict or '  ' in Anime_dict:
                        Anime_dict = Anime_dict.replace("\n", "")
                        Anime_dict = Anime_dict.replace("  ", " ")
                    Anime.append([Anime_name, Anime_pict, Anime_urls, Anime_dict])


# rec = AnimeGoFinish
# print(len(rec.Anime))
# ric = AnimeGoOngoing
# print(len(ric.Anime))
# 0 0 - Название
# 0 1 - Картинка
# 0 2 - Ссылка
# 0 3 - Описание
