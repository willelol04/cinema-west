import { authenticatedFetch, normalFetch } from "./general";

export async function getUser(userAuth0Id, token) {
    return await authenticatedFetch(`/api/auth0/users/${userAuth0Id}`, token);
}


export async function addUser(user, token) {
    return await authenticatedFetch("/api/users", {
        method: "POST",
        body: JSON.stringify(user)
    }, token);
}

export async function deleteUser(user) {
    try {
        const res = await authenticatedFetch("/api/auth0/users", {
            method: "DELETE",
            body: JSON.stringify(user)
        });

        if(!res.ok) {
            err = await res.json();
            console.log(`[${err.error_type}: ${err.detail}]`);
        }
        
        return res.json();
    } catch(e) {
        console.log(e);
    }
}


export async function searchUsers(query, token) {
    return await authenticatedFetch(`/api/users/search/${query}`, token);
}