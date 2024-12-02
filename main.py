import requests
from myhashmap import HashTable, MemberDetails
from redblacktree import RedBlackTree, RBNode

API_KEY = "ac2e9683866ec54f39f1b50d1634f4e5"

BASE_URL = "https://api.themoviedb.org/3"

'''
*
*
*
These are going to be all of the functions necessary to make all of the API calls for the required data
*
*
*
'''

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
        return response.json()
    else:
        print("ERROR")
        return None

# Involved with finding the actual details of the movie
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

# Will find credits for a given movie
def get_credits(id):
    endpoint = f"{BASE_URL}/movie/{id}/credits?language=en-US"
    params = {
        "api_key": API_KEY
    }
    response = requests.get(endpoint, params)
    if response.status_code == 200:
        return response.json()
    else:
        print("ERROR")
        return None

# Get some more details on a particular cast member
def search_by_name(name):
    endpoint = f"{BASE_URL}/search/person?include_adult=false&language=en-US&page=1"
    params = {
        "api_key": API_KEY,
        "query": name
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
    user_mov = get_user_movie(user_inp)
    mov_id = user_mov['results'][0]['id']

    mov_details = find_details(mov_id)
    mov_cast = get_credits(mov_id)

    # Getting all the credits and their respective characters
    for credit_dets in mov_cast['cast']:
        if "(uncredited)" not in credit_dets['character']:
            print(f"Actor Name: {credit_dets['name']}; Character: {credit_dets['character']}")

    print()

    # Obtaining the details of the crew and their jobs
    for crew_dets in mov_cast['crew']:
        if crew_dets['job'] == "Director" or crew_dets['job'] == "Screenplay":
            print(f"Name: {crew_dets['name']}; Known For: {crew_dets['known_for_department']}; "
                  f"Department: {crew_dets['department']}; Job: {crew_dets['job']}")


    # Testing the hash map class along with the cast member class
    myMap = HashTable(50)
    myObj = MemberDetails("Cody Zack", ["suite life", "riverdale"])
    myMap.set_val(myObj)
    currList = myMap.get_val("Cody Zack")
    # for i in currList:
    #     print(i)

    tree = RedBlackTree()
    tree.insert(myObj)

    currArr = tree.search("Cody Zack")
    for i in currArr:
        print(i)







