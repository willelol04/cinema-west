
export async function authenticatedFetch(url, token, options = {}) {
    
    const promise = await fetch(url, {
        ...options,
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`,
        }
    });

    if(!promise.ok) {
        throw await promise.json();
    }
    
    return await promise.json();
}

export async function normalFetch(url, options = {}) {
    const promise = await fetch(url, {
        ...options,
        headers: {
            "Content-Type": "application/json",
        }
    })
    
    if(!promise.ok) {
        throw await promise.json()
    }
    
    return await promise.json()
}