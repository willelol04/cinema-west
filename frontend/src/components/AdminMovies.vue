<script setup>
import MoviesListAdmin from '@/components/MoviesListAdmin.vue';
import { ref, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import BeatLoader from 'vue-spinner/src/BeatLoader.vue';


const search_field = defineModel('Bing');
const fetchComplete = ref(true);
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
    fetchComplete.value = false;
    try {
    const movieResultsPromise = await fetch(`http://localhost:8000/tmdb/movies/search/${route.query.q}`)
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
        <input type="search" v-model="search_field" id="movie-search">
        <input type="submit" value="Sök">
    </form>
    <MoviesListAdmin v-if="fetchComplete && route.query.q" :title="`Resultat för: `+ (route.query.q ? route.query.q : '')" :movies="movieResults">
    </MoviesListAdmin>
    <BeatLoader v-if="!fetchComplete" class="fetch-loading" :color="'#bdc7bf'"/>
    <div v-if="fetchComplete && movieResults.length === 0 && route.query.q" class="empty">No results were found</div>
    </div>
    

    
    <!--
    <MoviesList title="Already added movies:"/>
    -->

</template>


<style scoped>

.fetch-loading {
    margin-top: 200px;
}

h1 {
    display: block;
    text-align: center;
}

label {
    display: block;
}

form {
    margin-top: 20px;
    text-align: center;
}

input {
    border: 1px solid black;
    padding: 10px;
    background: white;
    color: black;
    border-bottom: 1px solid #404040;
    height: 50px;
    vertical-align: middle;

}



input[type="search"] {
    width: 30%;
    font-size: 16px;
    border-top-left-radius: 50px;
    border-bottom-left-radius: 50px;
    font-family:sans-serif; 
    font-weight: 100;
}
    
</style>