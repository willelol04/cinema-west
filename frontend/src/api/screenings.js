import { authenticatedFetch, normalFetch } from "./general";

export function deleteScreening(screening, token) {
    return authenticatedFetch("/api/screenings", token, {
        method: "DELETE",
        body: JSON.stringify({id: screening.id}),
    });
}