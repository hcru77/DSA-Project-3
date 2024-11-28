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

# We will get the id for the movie that we want to search up
def get_user_movie(name):
    endpoint = f"{BASE_URL}/search/movie?include_adult=false&language=en-US&page=1"
    params = {
        "api_key": API_KEY,
        "query": name
    }
    response = requests.get(endpoint, params)
    if response.status_code == 200:
        j_res = response.json()
        return find_details(j_res['results'][0]['id'])
    else:
        print("ERROR")
        return None

def find_details(id):
    endpoint = f"{BASE_URL}/movie/{id}?language=en-US"
    params = {
        "api_key": API_KEY
    }
    response = requests.get(endpoint, params)
    if response.status_code == 200:
        return response.json()
    else:
        print("ERROR")
        return None

if __name__ == '__main__':
    #Get the user input
    user_inp = input("Pick a random movie: ")
    mov_response = get_user_movie(user_inp)
    print(mov_response)