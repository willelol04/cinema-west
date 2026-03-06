import { authenticatedFetch, normalFetch } from "./general";

export function getScreening(id) {
    return normalFetch(`/api/screenings/${id}`);
}

export function deleteScreening(screening, token) {
    return authenticatedFetch("/api/screenings", token, {
        method: "DELETE",
        body: JSON.stringify({id: screening.id}),
    });
}

export function updateScreening(screening, token) {
    return authenticatedFetch("/api/screenings", token, {
        method: "PATCH",
        body: JSON.stringify({id: screening.id, start_time: screening.start_time}),
    });
}

export function addScreening(screening, token) {
    return authenticatedFetch("/api/screenings", token, {
        method: "POST",
        body: JSON.stringify({
                movie_id: screening.movie_id,
                theatre_id: screening.theatre_id,
                start_times: screening.start_times,
        }),
    });
}