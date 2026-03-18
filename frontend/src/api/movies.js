import { authenticatedFetch, normalFetch } from "./general";

export function getMovieSchedule() {

    const error_message = "Failed fetching movie schedule";
    const success_message = "Successfully fetching movie schedule";

    return normalFetch("/api/movies/schedule", error_message, success_message);
}

export function getMovie(id) {
    return normalFetch(`/api/movies/id/${id}`);
}

export function getMoviesAll() {
    return normalFetch("/api/movies");
}

export function getMoviesAllAdmin() {
  return normalFetch("/api/admin/movies");
}


export function deleteMovie(movie, token) {
    return authenticatedFetch("/api/movies", token, {
        method: "DELETE",
        body: JSON.stringify(movie),
    });
}

export function addMovie(movie, token) {
    return authenticatedFetch("/api/movies", token, {
        method: "POST",
        body: JSON.stringify(movie),
    });
}

export function searchMovies(query, token) {
    return authenticatedFetch(`/api/tmdb/movies/search/${query}`, token);
}
