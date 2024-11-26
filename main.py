import requests

API_KEY = "ac2e9683866ec54f39f1b50d1634f4e5"

BASE_URL = "https://api.themoviedb.org/3"

def get_popular_movies():
    endpoint = f"{BASE_URL}/movie/popular?language=en-US&page=1"
    params = {
        "api_key": API_KEY
    }
    response = requests.get(endpoint, params)
    if response.status_code == 200:
        return response.json()
    else:
        print("ERROR")
        return None


movies = get_popular_movies()
for movie in movies['results'][:5]:
    print(movie['title'])
