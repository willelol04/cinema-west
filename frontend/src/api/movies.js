import { authenticatedFetch, normalFetch } from "./general";


export function getMovie(id) {
    return normalFetch(`/api/movies/id/${id}`);
}

export function getMoviesAll() {
    return normalFetch("/api/movies");
}

export function deleteMovie(movie, token) {
    return authenticatedFetch("/api/movies", token, {
        method: "DELETE",
        body: JSON.stringify({id: movie.id}),
    });
}

export function addMovie(movie, token) {
    return authenticatedFetch("/api/movies", token, {
        method: "POST",
        body: JSON.stringify({id: movie.id}),
    });
}

export function searchMovies(query, token) {
    return authenticatedFetch(`/api/tmdb/movies/search/${query}`, token);
}
