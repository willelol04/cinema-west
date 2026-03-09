import { authenticatedFetch, normalFetch } from "./general";

export async function getBooking(id, token) {
    return await authenticatedFetch(`/api/bookings/${id}`, token);

}

export async function deleteBooking(booking, token) {
    return await authenticatedFetch("/api/bookings", token, {
        method: "DELETE",
        body: JSON.stringify(booking)
    });

}

export async function getMyBookings(token) {
    return await authenticatedFetch("/api/my-bookings", token);

}

export async function addBooking(booking, token) {
    return await authenticatedFetch("/api/bookings", token, {
        method: "POST",
        body: JSON.stringify(booking)
    });

}