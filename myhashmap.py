def hash_key(key):
    new_num = 0
    for i, letter in enumerate(key):
        new_num += ord(letter) * (31**i)
    return new_num

class MemberDetails:
    def __init__(self, name, movies):
        # Name is a basic string and the movies is going to be an array of strings
        self.name = name
        self.movies = movies

# I read how to create hash map from geeks for geeks article, so the create_buckets, get, and set functions are all
# inspired by the article: https://www.geeksforgeeks.org/hash-map-in-python/
class HashTable:
    def __init__(self, size):
        # Initializing hash map by getting size and making proper amount of buckets
        self.size = size
        self.hash_table = self.create_buckets()

    def create_buckets(self):
        # We are creating the empty hash map with all the buckets starting as empty arrays
        return [[] for _ in range(self.size)]

    def set_val(self, key, value):
        # Using the hashing function from before that we learned in class, I will get the hashed index for the key
        hashed_key = hash_key(key) % self.size

        # Find the bucket based on the hashed key
        bucket = self.hash_table[hashed_key]

        # Loop through the items in the bucket to check if the key is already in bucket
        for i, item in enumerate(bucket):
            if item.name == key:
                # We will replace the value of the key
                bucket[i].movies = value
                return
        # Since it wasn't found we will add it to the hash map
        bucket.append(MemberDetails(key, value))

    def get_val(self, key):
        # This will be the same as the set_val regarding searching
        hashed_key = hash_key(key) % self.size

        bucket = self.hash_table[hashed_key]
        for i, item in enumerate(bucket):
            # If we found item then just return else we will print that it wasn't found
            if item.name == key:
                return item.movies
        return f"{key} not in the hash map\n"

