import json
import requests

def get_movies_from_tastedive(title):
    params = {
        'q': title,
        'type': 'movies',
        'limit': 5
    }
    res = requests.get('https://tastedive.com/api/similar', params=params)
    return json.loads(res.text)


def extract_movie_titles(data):
    return [x['Name'] for x in data['Similar']['Results']]


def get_related_titles(lst):
    result = []
    for m in lst:
        data = get_movies_from_tastedive(m)
        titles = extract_movie_titles(data)
        for t in titles:
            if t not in result:
                result.append(t)
    return result


def get_movie_data(title):
    params = {
        't': title,
        'r': 'json',
    }
    res = requests.get('http://www.omdbapi.com/', params=params)
    return json.loads(res.text)


def get_movie_rating(data):
    rt = 0
    for i in data['Ratings']:
        if i['Source'] == 'Rotten Tomatoes':
            rt = int(i['Value'].replace('%', ''))
    return rt


def get_sorted_recommendations(lst):
    related = get_related_titles(lst)
    ratings = [(get_movie_rating(get_movie_data(m)), m) for m in related]
    return [i2 for (i1, i2) in list(sorted(ratings, reverse=True))]


get_sorted_recommendations(['Tron','Blade Runner'])
