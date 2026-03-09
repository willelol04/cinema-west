
import { authenticatedFetch, normalFetch } from "./general";

export async function getTheatres(token) {
    return await authenticatedFetch("/api/theatres", token);
}

