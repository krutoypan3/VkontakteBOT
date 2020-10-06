import requests
import random


def get_random_popular():
    film = []
    url = "https://api.themoviedb.org/3/movie/popular?api_key=5fc88fd5afbf802885cb03ed5ec0e35a&language=ru-RU&page=" + \
          str(random.randint(1, 5)) + str()
    response = requests.request("GET", url)
    data = response.json()
    film_number = random.randint(0, 19)
    film_title = data['results'][film_number]['title']  # Название
    film_overview = data['results'][film_number]['overview']  # Описание
    film_release_date = data['results'][film_number]['release_date']  # Дата релиза
    film_id = data['results'][film_number]['id']  # id фильма
    photo_url = 'https://image.tmdb.org/t/p/w600_and_h900_bestv2'
    film_poster_path = photo_url + data['results'][film_number]['poster_path']  # Ссылка на картинку
    film_vote_average = data['results'][film_number]['vote_average']  # Рейтинг фильма
    url = 'https://api.themoviedb.org/3/movie/' + str(film_id) + \
          '?api_key=5fc88fd5afbf802885cb03ed5ec0e35a&language=ru-RU'
    response = requests.request("GET", url)
    data = response.json()
    film_url = data['homepage']  # Ссылка на фильм
    if film_url == '':
        film_url = 'нет доступной ссылки'
    film_janr = []
    for i in data['genres']:
        film_janr.append(i['name'])
    film.append([film_title, film_overview, film_release_date, film_id, film_poster_path, film_vote_average, film_janr,
                 film_url])
    return film[0]
    # film[0] - название
    # film[1] - описание
    # film[2] - дата релиза
    # film[3] - id фильма
    # film[4] - картинка
    # film[5] - рейтинг
    # film[6] - жанры (массив)
    # film[7] - ссылка на фильм
