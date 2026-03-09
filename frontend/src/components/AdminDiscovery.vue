<script setup>
import MoviesListAdmin from '@/components/MoviesListAdminDiscovery.vue';
import { ref, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import BeatLoader from 'vue-spinner/src/BeatLoader.vue';
import { searchMovies, getMovie } from '../api/movies';
import {useAuth0} from "@auth0/auth0-vue";
const { user, isAuthenticated, isLoading, error, getAccessTokenSilently } = useAuth0();


const search_field = defineModel('Bing');
const fetchComplete = ref(true);
const movieResults = ref([]);

const route = useRoute();
const router = useRouter();

async function movieIsAdded(id) {
    return (await getMovie(id) !== null ? true : false);
}

async function fetchMovieResults() { 
    try {
        fetchComplete.value = false;
        const token = await getAccessTokenSilently();
        movieResults.value = (await searchMovies(route.query.q, token)).results;
        for (const movie of movieResults.value) {
            movie.isAdded = await movieIsAdded(movie.id)
        }
        fetchComplete.value = true;
        search_field.value = '';

    } catch(e) {
        console.log(e);
    } 
}
watch(
() => route.query.q,    
async () => {if(route.query.q) await fetchMovieResults()},
{immediate: true},

)

const onSubmit = () => {
  router.push({query: {q: search_field.value}});
};

const updateMovie = (movie) => {
    movie.isAdded = !movie.isAdded;
}

</script>


<template>
    
    <div class="search-movies">
    <form method="GET" @submit.prevent="onSubmit">
    <label for="movie-search"><h1>Discover movies</h1></label>
        <input type="search" v-model="search_field" id="movie-search">
        <input type="submit" value="Sök">
    </form>
    <MoviesListAdmin v-if="fetchComplete && route.query.q" :title="`Resultat för: `+ (route.query.q ? route.query.q : '')" :movies="movieResults"  @update="updateMovie"/>
    <BeatLoader v-if="!fetchComplete" class="fetch-loading" :color="'#bdc7bf'"/>
    <div v-if="fetchComplete && movieResults?.length === 0 && route.query.q" class="empty">No results were found</div>
    </div>
    

    
    <!--
    <MoviesList title="Already added movies:"/>
    -->

</template>


<style scoped>



.fetch-loading {
    margin-top: 200px;
    text-align: center;
}

h1 {
    display: block;
}

input {
    padding: 10px;
    background: white;
    color: black;
    height: 50px;
    vertical-align: middle;
    border-radius: 7px;
    margin: 0;

}


form {
    margin-bottom: 50px;
}


input[type="search"] {
    width: 30%;
    font-size: 16px;
    font-family:sans-serif;
    border-radius: 7px;
    font-weight: 100;

}
    
@media screen and (max-width: 1200px) {
    input[type="search"] { 
        width: 90%;
    }
    
    input[type="submit"] {
        width: 10%;
    }
}
</style>