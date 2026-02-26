<script setup>
import MoviesList from '@/components/MoviesList.vue';
import { ref } from 'vue';

const fetchComplete = ref(true);
    

async function fetchCustomers() { 
    fetchComplete.value = false;
    try {
    const token = await getAccessTokenSilently();
    const movieResultsPromise = await fetch(`http://localhost:8000/tmdb/movies/search/${route.query.q}`, {
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
</script>


<template>
    <div class="search-movies">
    <h1>Admin - Tickets</h1>
    <form method="POST" @submit.prevent="onSubmit">
        <label for="movie-search">Sök efter kund:</label>
        <input type="search" id="movie-search">
        <input type="submit" value="Sök">
    </form>
    </div>
    <div class="added-movies">
    <MoviesList v-if="false" title="Anna Andersson - Biljetter"/>
    </div>
    
</template>


<style scoped>

label {
    display: block;
}

form {
    margin-top: 20px;
}

input {
    border: 1px solid black;
    padding: 10px;

}


input[type="search"] {
    width: 50%;
}
    
</style>