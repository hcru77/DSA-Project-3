import requests
from myhashmap import HashTable, MemberDetails
from redblacktree import RedBlackTree, RBNode
import time

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
def search_movie(name):
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


# Involved with finding the actual details of the movie
def find_movie_details(id):
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


# Get the details for each of the people
def find_member_details(id):
    endpoint = f"{BASE_URL}/person/{id}?language=en-US"
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


def fetch_movie_credits(id):
    endpoint = f"{BASE_URL}/person/{id}/movie_credits?"
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

    """
    *
    *
    Using the API calls we will get the necessary data for the movie
    *
    *
    """
    # initialize red-black tree and hash table
    tree = RedBlackTree()
    hash_map = HashTable(100)

    # bool to choose whether to use hash table/tree
    isTree = True

    # Get the user input
    user_inp = input("Pick a random movie: ")
    user_mov = search_movie(user_inp)  # Searches the movie from its name to get the id
    mov_id = user_mov['results'][0]['id']

    mov_details = find_movie_details(mov_id)  # Gets the details once we are given the movie id
    mov_cast = get_credits(mov_id)  # Gets the credits details once we are given the movie id

    # Get a list of the names of the top 10 actors that are involved in each movie
    crew_list = []
    for i, credit_dets in enumerate(mov_cast['cast']):
        if i == 10:
            break
        crew_list.append(credit_dets['name'])

    # Appending the directors and screenwriters to the crew list
    for crew_dets in mov_cast['crew']:
        if crew_dets['job'] == "Director" or crew_dets['job'] == "Screenplay":
            crew_list.append(crew_dets['name'])

    # Create the list that includes all instances of the MemberDetails class
    people_list = []

    # start the timer for insertion into tree
    start_time = time.time()
    # Crew list includes the names of the actors and crew involved

    for person in crew_list:
        # Initialize the list that will store all the movies that a particular person has been in
        movie_list = []
        # Grabbing the id information and then fetching the movies that a particular person has worked in
        id_info = search_by_name(person)
        person_id = id_info['results'][0]['id']
        person_movies = fetch_movie_credits(person_id)
        # Loop through the movie titles and store them into the movie_list
        #
        #
        # NOTE FOR LATER: WE CAN DIRECTLY STORE THEM INTO THE DATA STRUCTURES HERE RATHER THAN IN A LATER STEP
        #
        #
        for movie in person_movies['cast']:
            movie_list.append(movie['title'])
        people_list.append(MemberDetails(person, movie_list))

        # inserts into either tree or hash map
        if isTree:
            tree.insert(MemberDetails(person, movie_list))
        else:
            hash_map.set_val(MemberDetails(person, movie_list))

    # end timer and print result
    end_time = time.time()
    print(f"Inserting into tree/map took {end_time - start_time:.2f} seconds")

    tree.inorder_traversal(tree.root)

    """
    *
    *
    Begin initializing the data structures and storing the people objects
    *
    *
    """
