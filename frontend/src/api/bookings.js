import { authenticatedFetch, normalFetch } from "./general";

export async function deleteBooking(booking, token) {
    return await authenticatedFetch("/api/bookings", token, {
        method: "DELETE",
        body: JSON.stringify(booking)
    });

}