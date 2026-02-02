<script setup>
    import MoviesListAdmin from '@/components/MoviesListAdmin.vue';
import { roundToNearestMinutes } from 'date-fns';
import { Fieldset } from 'primevue';
import { onMounted, ref, watch } from 'vue';
import { useRouter, routeLocationKey, useRoute } from 'vue-router';

    const search_field = defineModel('Bing');
    const fetchComplete = ref(false);
    const movieResults = ref([]);
    
    const route = useRoute();
    const router = useRouter();

async function movieIsAdded(id) {
    const promise = await fetch('http://localhost:8000/movie/isadded/'+id);
    const result = await promise.json();
    console.log(result.message);
    return result.message;
}

async function fetchMovieResults(numbers_tried = 1) { 
    const num = numbers_tried;

    try {
    const movieResultsPromise = await fetch(`http://localhost:8000/movies/search/${route.query.q}`)
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
watch(
() => route.query.q,    
() => {if(route.query.q) fetchMovieResults()},
{immediate: true},

)

const onSubmit = () => {
  router.push({query: {q: search_field.value}});
};





</script>


<template>
    
    <div class="search-movies">
    <h1>Discover movies</h1>
    <form method="GET" @submit.prevent="onSubmit">
        <label for="movie-search">Sök efter film på TMDB:</label>
        <input type="search" v-model="search_field" id="movie-search">
        <input type="submit" value="Sök">
    </form>

    </div>
    
    <MoviesListAdmin v-if="fetchComplete && route.query.q" :title="`Resultat för: `+ (route.query.q ? route.query.q : '')" :movies="movieResults">
    </MoviesListAdmin>
    <div v-if="movieResults.length === 0 && route.query.q" class="empty">No results were found</div>
    
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