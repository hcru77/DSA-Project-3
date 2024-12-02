class MemberDetails:
    def __init__(self, name, movies):
        # Name is a basic string and the movies is going to be an array of strings
        self.name = name
        self.movies = movies

    def __eq__(self, other):
        # checks if names are equal
        return self.name == other

    def __lt__(self, other):
        # checks if name is less than other name lexicographically
        return self.name < other


