/*
const userExists = async (userAuthId) => {
    try {
        const response = await fetch("/api/auth0/users/"+userAuthId);
        const userResponse = await response.json();
        console.log("user exists: ", userResponse ? true : false);
        console.log(userResponse);
        if(userResponse) {
          return true;
        } else {
          return false;
        }
    } catch(e) {
        console.log(e);
        console.log("error fetching user");
    }

}

const addUser = async (user) => {
    try {
    console.log("received obj", user)
    const token = await getAccessTokenSilently();
    const response = await fetch("/api/users", {
        method: "POST",
        body: JSON.stringify(user),
        headers: {
            "Content-Type": "application/json",
            "authorization": `Bearer ${token}`,
        }

    });
    
    console.log(await response.json());
      
    } catch(e) {
      console.log(e);
      console.log("error adding user");
    }

};


const cancelBooking = async (booking) => {
    try {
        const token = await getAccessTokenSilently();
        const res = await fetch("/api/bookings", {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({
                id: booking.id, 
                screening_id: booking.screening.id
            }),
        });

        if (!res.ok) {
            const err = await res.json();
            alert("Booking cancellation failed: ", err);
            return;
        }

        const result = await res.json();
        console.log(result);
        fetchBookings();
    } catch (e) {
        console.log(e);
        alert("Something went wrong: " + e.message);
    }
};

const fetchBookings = async () => { 
    try {
    const token = await getAccessTokenSilently();
    const bookingsPromise = await fetch("/api/my-bookings/", {
      headers: {
        "Content-type": "application/json",
        "Authorization": `Bearer ${token}`
      }
    })

    bookings.value = await bookingsPromise.json();

    console.log(bookings.value);

    } catch(e) {
        alert(e);
    }    
}


async function fetchMovie() {
    const promise = await fetch("/api/movies/id/"+route.params.id);
    movieResults.value = await promise.json();
    console.log(movieResults.value);
}

async function fetchMovies() {
    const promise = await fetch("/api/movies");
    movieResults.value = await promise.json();
    console.log(movieResults.value);
}

async function updateMovies(sortData) {
    const searchParams = new URLSearchParams();
    if(sortData.title !== null) {
      searchParams.append('title', sortData.title)
    }
    if(sortData.genre !== null) {
      searchParams.append('genre', sortData.genre)
    }
    if(sortData.rating !== null) {
      searchParams.append('rating', sortData.rating)
    }
    const promise = await fetch(`/api/movies?${searchParams}`);
    movieResults.value = await promise.json();
    console.log(movieResults.value);
    console.log(searchParams)
}

 const testFetch = async () => {
    try {
      const params = new URLSearchParams({start_date: format(Date.now(), 'yyyy-MM-dd'), end_date: format(Date.now(), 'yyyy-MM-dd')});
      const promise = await fetch(`/api/movies/schedule`);
      ourMovies.value = await promise.json();
      fetchComplete.value = true;
    } catch(e) {
      console.log(e);
    }
  
} 

async function fetchBooking() {
    try {
        const token = await getAccessTokenSilently();
        const promise = await fetch(`/api/bookings/${route.params.id}`, {
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
        }
        );
        
        if(!promise.ok ) {
            router.push('/');
            return;
        }
        

        bookingResult.value = await promise.json();
        


        formData.amount = bookingResult.value.total_price
        console.log(bookingResult.value);
        if(bookingResult.value.status == 'complete') {
            paymentComplete.value = true;
            router.push("/");
        } else {
            fetchComplete.value = true;

        }

    } catch(e) {
        console.log(e);
        alert("Something went wrong: " + e.message);
    }
}


const cancelBooking = async (booking_id) => {
    try {
        const token = await getAccessTokenSilently();
        const res = await fetch("/api/bookings", {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({
                id: bookingResult.value.id, 
                screening_id: bookingResult.value.screening_id
            }),
        });

        if (!res.ok) {
            const err = await res.json();
            alert("Booking cancellation failed: ", err);
            return;
        }

        const result = await res.json();
        console.log(result);
    } catch (e) {
        console.log(e);
        alert("Something went wrong: " + e.message);
    }
};

const payBooking = async () => {
    try {
        fetchComplete.value = false;
        const token = await getAccessTokenSilently();
        const res = await fetch("/api/pay-booking", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({
                booking_id: route.params.id, 
                username: formData.ssn,
                password: formData.password,
                from_account: formData.account,
                amount: formData.amount,
            }),
        });

        if (!res.ok) {
            const err = await res.json();
            alert(`[${err.error_type}: ${err.detail}]`);
            return;
        }

        const result = await res.json();
        console.log(result);
        fetchComplete.value = true;
        alert("Payment successful!");
        paymentComplete.value = true;
        router.push("/profile");
    } catch (e) {
        console.log(e);
        alert("Something went wrong: " + e.message);
    }
};

async function fetchFilters() {
    try {
    fetchComplete.value = false;
    const promise = await fetch("/api/filters");
    filters.value = await promise.json();
    fetchComplete.value = true;
    console.log(filters.value);
    } catch(e){
       alert(e) 
       fetchComplete.value = false;
    }
}

const deleteUser = async () => {
        try {
        const token = await getAccessTokenSilently()
        const response = await fetch("/api/auth0/users/", {
            method: "DELETE",
            body: JSON.stringify(props.user),
            headers: {
                "Content-Type": "application/json",
                "authorization": `Bearer ${token}`,
            }

        });
        
        
        if (!response.ok) {
            const error = await response.json();
            alert(`Error: ${error.detail}`)
            console.log(error)
            return null
        }
        
        if(props.isMyProfile === true) {
            logout();
        }

            
        } catch(e) {
            alert(`Error: ${e}`)
            console.log(e)
        } finally {
            
        }

}

const addMovie = async (movie) => {
    const token = await getAccessTokenSilently();
    const response = await fetch("/api/movies/", {
        method: "POST",
        body: JSON.stringify({id: movie.id}),
        headers: {
            "Content-Type": "application/json",
            "authorization": `Bearer ${token}`,
        }

    });

    console.log(response);
    emit('update')

};

const deleteMovie = async (movie) => {
    try {
    const token = await getAccessTokenSilently();
    const response = await fetch("/api/movies/", {
        method: "DELETE",
        body: JSON.stringify(movie),
        headers: {
          "Content-Type": "application/json",
          "authorization": `Bearer ${token}`,
        }

    });
    
    if (!response.ok) {
        const error = await response.json();
        alert(`Error: ${error.detail}`)
        console.log(error)
        return null
    }
    
    emit('update');
    alert("Movie removed");

    } catch(e) {
        console.log(e)
    }

};

const addMovie = async (movie) => {
    const token = await getAccessTokenSilently();
    const response = await fetch("/api/movies/", {
        method: "POST",
        body: JSON.stringify(movie),
        headers: {
            "Content-Type": "application/json",
            "authorization": `Bearer ${token}`,
        }

    });

    console.log(response);
    emit('update')

};

const deleteMovie = async (movie) => {
    try {
    const token = await getAccessTokenSilently();
    const response = await fetch("/api/movies/", {
        method: "DELETE",
        body: JSON.stringify(movie),
        headers: {
          "Content-Type": "application/json",
          "authorization": `Bearer ${token}`,
        }

    });
    
    if (!response.ok) {
        const error = await response.json();
        alert(`Error: ${error.detail}`)
        console.log(error)
        return null
    }
    
    emit('update');
    alert("Movie removed");

    } catch(e) {
        console.log(e)
    }

};


const updateScreening = async (screening) => {
    try {
    const token = await getAccessTokenSilently();
    const response = await fetch("/api/screenings", {
        method: "PATCH",
        body: JSON.stringify({id: screening.id, start_time: screening.start_time}),
        headers: {
          "Content-Type": "application/json",
          "authorization": `Bearer ${token}`,
        }

    });
    
    if (!response.ok) {
        const error = await response.json();
        alert(`Error: ${error.detail}`)
        console.log(error)
        return null
    }
    
    emit('update');
    alert("Screening updated");

    } catch(e) {
        console.log(e)
    }

};


const deleteScreening = async (screening_id) => {
    if(confirm("Are you sure you want to delete this screening?")) {
    try {
    const token = await getAccessTokenSilently();
    const response = await fetch("/api/screenings", {
        method: "DELETE",
        body: JSON.stringify({id: screening_id}),
        headers: {
          "Content-Type": "application/json",
          "authorization": `Bearer ${token}`,
        }

    });
    
    if (!response.ok) {
        const error = await response.json();
        alert(`Error: ${error.detail}`)
        console.log(error)
        return null
    }
    
    emit('update');
    alert("Screening removed");

    } catch(e) {
        console.log(e)
    }


    }
};

async function fetchUpcoming(numbers_tried = 1) {
    const num = numbers_tried;
    try {
        const upcomingMoviePromise = await fetch("/api/movies/upcoming")
        const upcomingMovieObject = await upcomingMoviePromise.json();
        upcomingMovies.value = upcomingMovieObject;
        console.log(upcomingMovies.value);
        fetchComplete.value = true;
        console.log("successful - ", num);
    } catch(e) {
        console.log(e);
        setTimeout(() => {fetchUpcoming(1+num)}, 20000);
        console.log("failed - ", num);
    } finally {
        console.log("quit");
    }
}

async function fetchScreening() {
    const promise = await fetch("/api/screenings/"+route.params.id);
    screeningResult.value = await promise.json();
    booked_seat_ids.value = screeningResult.value.booked_seat_ids;
    console.log(screeningResult.value);

}

const bookTickets = async () => {
    if(checkedSeats.value.length > 0) {
        try {
        const token = await getAccessTokenSilently();
        const response = await fetch("/api/bookings", {
            method: "POST",
            body: JSON.stringify({seats: checkedSeats.value, screening_id: screeningResult.value.id}),
            headers: {
                "Content-Type": "application/json",
                "authorization": `Bearer ${token}`,
            }

        });
        
        if (!response.ok) {
            const error = await response.json();
            alert(`Error: ${error.detail}`)
            console.log(error)
            return null
        }
        
        const bookingId = await response.json()

        console.log(bookingId);
        ws.send(JSON.stringify({msg: "user", timestamp: timestamp}))
        console.log("Sent")

        router.push(`/payment/${bookingId}`)
            
        } catch(e) {
            alert(`Error: ${e}`)
            console.log(e)
        } finally {
        checkedSeats.value = [];
        await fetchScreening();
            
        }

    }

}

const fetchMovies = async () => {
    const promise = await fetch("/api/movies");
    movieResults.value = await promise.json();
    console.log(movieResults.value);
}

const fetchTheatres = async () => {
    const promise = await fetch("/api/theatres");
    theatreResults.value = await promise.json();
    console.log(theatreResults.value);
}

const addScreening = async () => {
    if (screening.start_times.length > 0) {
    const token = await getAccessTokenSilently();
    const response = await fetch("/api/screenings", {
        method: "POST",
        body: JSON.stringify(screening),
        headers: {
            "Content-Type": "application/json",
            "authorization": `Bearer ${token}`,
        }

    });
    
    alert("Screening(s) added.")
    console.log(await response.text());
    }

}

const fetchTheatres = async () => {
    const promise = await fetch("/api/theatres");
    theatresResults.value = await promise.json();
}

async function fetchMovies() { 
    try {
    const movieResultsPromise = await fetch("/api/movies", {
      headers: {
        "Content-type": "application/json",
      }
    })
    const movieResultsObject = await movieResultsPromise.json();
    movieResults.value = movieResultsObject;
    for(const movie of movieResults.value) {
      movie.isAdded = true;
      movie.showScreenings = false;
      for(const screening of movie.screenings) {
        screening.showEdit = false;
      }
    }

    console.log(movieResults.value);

    } catch(e) {
    console.log(e);
    console.log("failed");
    } finally {
    console.log("quit");
    }
}

async function movieIsAdded(id) {
    const token = await getAccessTokenSilently();
    const promise = await fetch("/api/movie/isadded/"+id, {
      headers: {
        "Content-type": "application/json",
        "authorization": `Bearer ${token}`,
      }
    });
    const result = await promise.json();
    console.log(result.message);
    return result.message;
}

async function fetchMovieResults(numbers_tried = 1) { 
    const num = numbers_tried;
    fetchComplete.value = false;
    try {
    const token = await getAccessTokenSilently();
    const movieResultsPromise = await fetch(`/api/tmdb/movies/search/${route.query.q}`, {
      headers: {
        "Content-type": "application/json",
        "authorization": `Bearer ${token}`,
      }
    })
    const movieResultsObject = await movieResultsPromise.json();
    for (const movie of movieResultsObject.results) {
        if (await movieIsAdded(movie.id) == true) {
            movie.isAdded = true;
            console.log(movie.id, "is added")
        }
    }
    
    movieResults.value = movieResultsObject.results;

    console.log(movieResults.value);
    fetchComplete.value = true;
    search_field.value = '';

    } catch(e) {
    console.log(e);
    setTimeout(() => {fetchMovieResults(1+num)}, 20000);
    console.log("failed - ", num);
    } finally {
    console.log("quit");
    }
}

async function fetchCustomerResults(numbers_tried = 1) { 
    const num = numbers_tried;
    fetchComplete.value = false;
    try {
    const token = await getAccessTokenSilently();
    const customerResultsPromise = await fetch(`/api/users/search/${route.query.q}`, {
      headers: {
        "Content-type": "application/json",
        "authorization": `Bearer ${token}`,
      }
    })
    const customerResultsObject = await customerResultsPromise.json();

    customerResults.value = customerResultsObject;

    console.log(customerResults.value);
    fetchComplete.value = true;
    console.log(fetchComplete.value)
    search_field.value = '';

    } catch(e) {
    console.log(e);
    setTimeout(() => {fetchCustomerResults(1+num)}, 20000);
    console.log("failed - ", num);
    } finally {
    console.log("quit");
    }
}

const cancelBooking = async (booking) => {
    try {
        const token = await getAccessTokenSilently();
        const res = await fetch("/api/bookings", {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({
                id: booking.id, 
                screening_id: booking.screening.id
            }),
        });

        if (!res.ok) {
            const err = await res.json();
            alert("Booking cancellation failed: ", err);
            return;
        }

        const result = await res.json();
        console.log(result);
        fetchCustomerResults();
    } catch (e) {
        console.log(e);
        alert("Something went wrong: " + e.message);
    }
};
*/