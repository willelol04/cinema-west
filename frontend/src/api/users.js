import { authenticatedFetch, normalFetch } from "./general";

export async function getUser(userAuth0Id, token) {
    return await authenticatedFetch(`/api/auth0/users/${userAuth0Id}`, token);
}


export async function addUser(user, token) {
    return await authenticatedFetch("/api/users", token, {
        method: "POST",
        body: JSON.stringify(user)
    });
}

export async function deleteUser(user,  token) {
        return await authenticatedFetch("/api/auth0/users", token, {
            method: "DELETE",
            body: JSON.stringify(user)
        });
}


export async function searchUsers(query, token) {
    return await authenticatedFetch(`/api/users/search/${query}`, token);
}