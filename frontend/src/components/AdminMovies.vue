<script setup>
    import MoviesList from '@/components/MoviesList.vue';
import { Fieldset } from 'primevue';
import { ref } from 'vue';

    const search_field = defineModel('Bing');
    const fetchComplete = ref(false);
    const movieResults = ref([]);

async function fetchMovieResults(numbers_tried = 1) {
    const num = numbers_tried;
    console.log(search_field.value);

    try {
        const movieResultsPromise = await fetch(`http://localhost:8000/movies/search/${search_field.value}`)
        const movieResultsObject = await movieResultsPromise.json();
        movieResults.value = movieResultsObject.results;
        console.log(movieResults.value)
        fetchComplete.value = true;
        //console.log("successful - ", num);
//        const today = Date.now();
//        const movie_one = Date.parse(upcomingMovies.value[3].release_date);
//        if (today > movie_one) {
//            console.log("movie already out");
//        } else {
//            console.log("movie not out");
//        }
//        
//        console.log(upcomingMovies.value.filter((movie) => Date.parse(movie.release_date) > today))

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
    <h1>Admin - Movie database</h1>
    <form @submit.prevent="fetchMovieResults">
        <label for="movie-search">Sök efter film på TMDB:</label>
        <input type="search" v-model="search_field" id="movie-search">
        <input type="submit" value="Sök">
    </form>

    </div>
    
    <MoviesList v-if="fetchComplete" :movies="movieResults"></MoviesList>
    
    <!--
    <MoviesList title="Already added movies:"/>
    -->

</template>


<style scoped>

h1 {
    display: block;
}

label {
    display: block;
}

form {
    margin-top: 20px;
}

input {
    border: 1px solid black;
    padding: 10px;
    background: white;
    color: black;
    border-bottom: 1px solid #404040;

}



input[type="search"] {
    width: 50%;
    border-top-left-radius: 50px;
    border-bottom-left-radius: 50px;
}
    
</style>