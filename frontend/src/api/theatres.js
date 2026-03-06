
import { authenticatedFetch, normalFetch } from "./general";

export async function getTheatres() {
    return await normalFetch("/api/theatres");
}

