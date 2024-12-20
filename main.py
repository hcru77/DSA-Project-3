import os
import requests
from myhashmap import HashTable, MemberDetails
from redblacktree import RedBlackTree, RBNode
import time


API_KEY = os.getenv('API_KEY')

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

# Find the movies that a director has directed
def fetch_movie_director(id):
    endpoint = f"{BASE_URL}/person/{id}/movie_credits?"
    params = {
        "api_key": API_KEY
    }
    response = requests.get(endpoint, params)
    if response.status_code == 200:
        full_response = response.json()
        return [movie['title'] for movie in full_response.get('crew',[])
                if movie.get('job') == "Director"]
    else:
        print("ERROR")
        return None

# Find the movies that a writer has written
def fetch_movie_screenwriter(id):
    endpoint = f"{BASE_URL}/person/{id}/movie_credits?"
    params = {
        "api_key": API_KEY
    }
    response = requests.get(endpoint, params)
    if response.status_code == 200:
        full_response = response.json()
        return [movie['title'] for movie in full_response.get('crew', [])
                if movie.get('job') == "Screenplay"]
    else:
        print("ERROR")
        return None

def fetch_collection_details(id):
    endpoint = f"{BASE_URL}/collection/{id}?"
    params = {
        "api_key": API_KEY
    }
    response = requests.get(endpoint, params)
    if response.status_code == 200:
        return response.json()
    else:
        print("ERROR")
        return None

"""
*
*
*
The recommendation algorithms
*
*
*
"""

# We will make the recommendation but the search will be performed on the hash map
def actor_recommend_map(hash_m, obj_list, related_movs):
    # Initiating the dictionary that will keep count of the people involved in a particular movie
    common_movies = {}
    seen = []
    # Loop through the list of actor objects and then observe the movies each is in
    for actor_obj in obj_list:
        for i, movie_name in enumerate(actor_obj.movies):
            if i == 20:
                break
            curr_mov = search_movie(movie_name)  # Searches the movie from its name to get the id
            mov_id = curr_mov['results'][0]['id']
            if curr_mov['results'][0]['title'] in related_movs or curr_mov['results'][0]['title'] in seen:
                continue
            seen.append(curr_mov['results'][0]['title'])
            # Get list of the people that are involved
            mov_credits = get_credits(mov_id)

            # We will loop through the people that are in the cast and the people that are in the crew
            # We will perform a search in the hash map
            for cast_details in mov_credits['cast']:
                if hash_m.in_map(cast_details['name']) and cast_details['name'] != actor_obj.name:
                    if movie_name not in common_movies:
                        common_movies[movie_name] = 1
                    else:
                        common_movies[movie_name] += 1

            for crew_details in mov_cast['crew']:
                if hash_m.in_map(crew_details['name']):
                    if movie_name not in common_movies:
                        common_movies[movie_name] = 1
                    else:
                        common_movies[movie_name] += 1

    return common_movies



# We will make the recommendations searching the tree
def actor_recommend_tree(my_tree, obj_list, related_movs):
    # Initiating the dictionary that will keep count of the people involved in a particular movie
    common_movies = {}
    seen = []
    # Loop through the list of actor objects and then observe the movies each is in
    for actor_obj in obj_list:
        for i, movie_name in enumerate(actor_obj.movies):
            if i == 20:
                break
            curr_mov = search_movie(movie_name)  # Searches the movie from its name to get the id
            mov_id = curr_mov['results'][0]['id']
            if curr_mov['results'][0]['title'] in related_movs or curr_mov['results'][0]['title'] in seen:
                continue
            seen.append(curr_mov['results'][0]['title'])
            # Get list of the people that are involved
            mov_credits = get_credits(mov_id)

            # We will loop through the people that are in the cast and the people that are in the crew
            # We will perform a search in the hash map
            for cast_details in mov_credits['cast']:
                if my_tree.search(cast_details['name']) and cast_details['name'] != actor_obj.name:
                    if movie_name not in common_movies:
                        common_movies[movie_name] = 1
                    else:
                        common_movies[movie_name] += 1

            for crew_details in mov_cast['crew']:
                if my_tree.search(crew_details['name']):
                    if movie_name not in common_movies:
                        common_movies[movie_name] = 1
                    else:
                        common_movies[movie_name] += 1

    return common_movies


# Responsible for getting the movie collection aka prequels and sequels for filtering and other recommendations
def get_movie_collection(mov_id):
    mov_details = find_movie_details(mov_id)
    if not mov_details['belongs_to_collection']:
        return [mov_details['title']]

    collection_id = mov_details['belongs_to_collection']['id']
    collection_details = fetch_collection_details(collection_id)
    movie_collection = [movie['title'] for movie in collection_details.get('parts', [])]
    return movie_collection


# Simpler recommendation based on the directors movies and similarities to the current movie
def director_recommend(director, movie_name, movie_collection_name, seen_movies):
    # takes in director(string) and gives list of 10 most popular movies

    search_results = search_by_name(director)
    if not search_results or not search_results.get("results"):
        return f"No director found with the name '{director}'."

    director_id = search_results["results"][0]["id"]

    movies_url = f"{BASE_URL}/person/{director_id}/movie_credits"
    movies_params = {"api_key": API_KEY}
    movies_response = requests.get(movies_url, params=movies_params)
    movies_response.raise_for_status()
    movies_data = movies_response.json()

    # adds movie that the user inputted and its collection to a set and makes sure to exclude it in recommendation
    excluded_movies = set(movie_collection_name)
    excluded_movies.add(movie_name)
    excluded_movies.update(seen_movies)
    directed_movies = [
        {"title": movie["title"], "popularity": movie["popularity"]}
        for movie in movies_data.get("crew", [])
        if movie["job"] == "Director" and movie["title"] not in excluded_movies
    ]

    recommended_movies = sorted(directed_movies, key=lambda x: x["popularity"], reverse=True)
    return recommended_movies[:3]


# Will give recommendation based on the screenwriter and the genres of the current movie
def screenwriter_recommend(screenwriter, movie_name, movie_collection_name, seen_movies):
    search_results = search_by_name(screenwriter)
    if not search_results or not search_results.get("results"):
        return f"No director found with the name '{screenwriter}'."

    screenwriter_id = search_results["results"][0]["id"]

    movies_url = f"{BASE_URL}/person/{screenwriter_id}/movie_credits"
    movies_params = {"api_key": API_KEY}
    movies_response = requests.get(movies_url, params=movies_params)
    movies_response.raise_for_status()
    movies_data = movies_response.json()

    excluded_movies = set(movie_collection_name)
    excluded_movies.add(movie_name)
    excluded_movies.update(seen_movies)
    directed_movies = [
        {"title": movie["title"], "popularity": movie["popularity"]}
        for movie in movies_data.get("crew", [])
        if movie["job"] == "Screenplay" and movie["title"] not in excluded_movies
    ]

    recommended_movies = sorted(directed_movies, key=lambda x: x["popularity"], reverse=True)
    return recommended_movies[:3]


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

    # Get the user input
    user_inp = input("Pick a random movie: ")
    user_mov = search_movie(user_inp)  # Searches the movie from its name to get the id
    mov_id = user_mov['results'][0]['id']

    # Get the collection of movies that are related to the user movie
    movie_collection = get_movie_collection(mov_id)


    mov_details = find_movie_details(mov_id)  # Gets the details once we are given the movie id
    mov_cast = get_credits(mov_id)  # Gets the credits details once we are given the movie id

    # Get a list of the names of the top 10 actors that are involved in each movie
    cast_list = []
    crew_list = {}
    for i, credit_dets in enumerate(mov_cast['cast']):
        if i == 10:
            break
        cast_list.append(credit_dets['name'])

    # Appending the directors and screenwriters to the crew list

    for crew_dets in mov_cast['crew']:
        if crew_dets['job'] == "Director":
            crew_list[crew_dets['name']] = "Director"
        elif crew_dets['job'] == "Screenplay":
            crew_list[crew_dets['name']] = "Screenplay"

    """
    *
    *
    Begin initializing the data structures and storing the movies that people are involved in
    *
    *
    """

    cast_obj_list = []

    for key in crew_list:
        # Initialize the list that will store all the movies that a particular person has been in
        movie_list = []

        # Grabbing the id information and then fetching the movies that a particular person has worked in
        id_info = search_by_name(key)
        person_id = id_info['results'][0]['id']

        # Store the movie titles based on if they are directed by this person
        if crew_list[key] == "Director":
            movie_list = fetch_movie_director(person_id)
        else:
            movie_list = fetch_movie_screenwriter(person_id)

        # Insert the item into the data structures and into the list of objects
        cast_obj_list.append(MemberDetails(key, movie_list))
        tree.insert(MemberDetails(key, movie_list))
        hash_map.set_val(MemberDetails(key, movie_list))

    for person in cast_list:
        # Initialize the list that will store all the movies that a particular person has been in
        movie_list = []

        # Grabbing the id information and then fetching the movies that a particular person has worked in
        id_info = search_by_name(person)
        person_id = id_info['results'][0]['id']
        person_movies = fetch_movie_credits(person_id)

        # Loop through the movie titles and store them into the movie_list
        for movie in person_movies['cast']:
            movie_list.append(movie)

        # Sort the list based on the popularity only to get the most popular
        movie_list.sort(key=lambda x: x['popularity'], reverse=True)
        movie_names_list = []
        for i in movie_list:
            movie_names_list.append(i['title'])

        # Insert the item into the data structures and into the list of objects
        cast_obj_list.append(MemberDetails(person, movie_names_list))
        tree.insert(MemberDetails(person, movie_names_list))
        hash_map.set_val(MemberDetails(person, movie_names_list))

    """
    *
    *
    Testing out the run
    *
    *
    """

    # end timer and print result
    start_time = time.time()
    common_movies_tree = actor_recommend_tree(tree, cast_obj_list, movie_collection)
    end_time = time.time()
    print(f"Searching tree took {end_time - start_time:.2f} seconds")

    start_time = time.time()
    common_movies_map = actor_recommend_map(hash_map, cast_obj_list, movie_collection)
    end_time = time.time()
    print(f"Searching map took {end_time - start_time:.2f} seconds")

    print()
    """
    *
    *
    Grab the movie with the highest frequency of common actors / crew members
    *
    *
    """

    # Result lists for the actor , director, screenwriter, and collection recommendations
    recom_actors = []

    # Sort the map so that it is going in descending order
    common_movies_map = dict(sorted(common_movies_map.items(), key=lambda x:x[1], reverse=True))
    # Looping through the common movies and going to extract the movie with most common actors
    for i, key in enumerate(common_movies_map):
        if i == 3:
            break
        recom_actors.append(key)

    print(f"Recommendation from cast and crew: {recom_actors}")

    director_seen = False
    screenw_seen = False
    director_list = []
    sw_list = []

    for key in crew_list:
        if crew_list[key] == "Director" and director_seen == False:
            movie_pairs = director_recommend(key, mov_details['title'], movie_collection, recom_actors)
            for movie in movie_pairs:
                director_list.append(movie["title"])
                if movie["title"] not in recom_actors:
                    recom_actors.append(movie["title"])
            director_seen = True
        elif not screenw_seen:
            movie_pairs = screenwriter_recommend(key, mov_details['title'], movie_collection, recom_actors)
            for movie in movie_pairs:
                sw_list.append(movie["title"])
                if movie["title"] not in recom_actors:
                    recom_actors.append(movie["title"])
            screenw_seen = True
    if len(sw_list) != 0:
        print(f"This is the sw list: {sw_list}")
    else:
        print("No screenwriter recommendations")

    if len(director_list) != 0:
        print(f"This is the director list: {director_list}")
    else:
        print("No director recommendations")

    if len(movie_collection) != 1:
        print(f"This is the whole movie collection: {movie_collection}")
    else:
        print("This is not part of a collection")




