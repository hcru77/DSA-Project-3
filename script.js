// script.js

// TMDb API Key
const API_KEY = "ac2e9683866ec54f39f1b50d1634f4e5";

// Function to fetch movie recommendations
async function fetchRecommendations(movieName) {
    try {
        // Search for the movie by name
        const searchResponse = await fetch(
            `https://api.themoviedb.org/3/search/movie?api_key=${API_KEY}&query=${encodeURIComponent(movieName)}`
        );
        const searchData = await searchResponse.json();

        // Get the first movie's ID from the search results
        if (searchData.results && searchData.results.length > 0) {
            const movieId = searchData.results[0].id;

            // Fetch recommendations for the movie ID
            const recommendationsResponse = await fetch(
                `https://api.themoviedb.org/3/movie/${movieId}/recommendations?api_key=${API_KEY}`
            );
            const recommendationsData = await recommendationsResponse.json();

            // Return the top 4 recommended movies
            if (recommendationsData.results && recommendationsData.results.length > 0) {
                return recommendationsData.results.slice(0, 4).map(movie => movie.title);
            } else {
                return [];
            }
        } else {
            throw new Error("Movie not found");
        }
    } catch (error) {
        console.error("Error fetching recommendations:", error);
        return null;
    }
}

// Handle movie recommendations
document.getElementById('getRecommendationsButton').addEventListener('click', async () => {
    const movieName = document.getElementById('movieName').value.trim();
    const selectedMovieResult = document.getElementById('selectedMovieResult');
    const recommendations = document.getElementById('recommendations');
    const recommendationsList = document.getElementById('recommendationsList');

    // Clear previous results
    recommendationsList.innerHTML = '';
    recommendations.classList.add('hidden');
    selectedMovieResult.textContent = `Searching for recommendations for "${movieName}"...`;

    // Fetch recommendations
    const recommendedMovies = await fetchRecommendations(movieName);

    if (recommendedMovies) {
        if (recommendedMovies.length > 0) {
            selectedMovieResult.textContent = `You selected: "${movieName}"`;
            recommendations.classList.remove('hidden');
            recommendedMovies.forEach(movie => {
                const li = document.createElement('li');
                li.textContent = movie;
                recommendationsList.appendChild(li);
            });
        } else {
            selectedMovieResult.textContent = `No recommendations found for "${movieName}".`;
        }
    } else {
        selectedMovieResult.textContent = `Error fetching recommendations for "${movieName}".`;
    }
});