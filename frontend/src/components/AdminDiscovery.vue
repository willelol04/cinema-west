<script setup>
import MoviesListAdmin from '@/components/MoviesListAdminDiscovery.vue';
import { ref, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import BeatLoader from 'vue-spinner/src/BeatLoader.vue';
import { searchMovies, getMovie } from '../api/movies';
import {useAuth0} from "@auth0/auth0-vue";
const { user, isAuthenticated, isLoading, error, getAccessTokenSilently } = useAuth0();
import {debounce} from 'lodash';
import Search from '@/components/Search.vue';


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

    } catch(e) {
        console.log(e);
    } 
}

const updateMovie = (movie) => {
    movie.isAdded = !movie.isAdded;
}


</script>


<template>
    
    <div class="search-movies">
      <h1>Discover Movies on TMDB:</h1>
    <Search :header="`Search Movies on TMDB:`" :searchFunction="fetchMovieResults"/>
    <MoviesListAdmin v-if="fetchComplete && route.query.q" :title="`Resultat för: `+ (route.query.q ? route.query.q : '')" :movies="movieResults"  @update="updateMovie"/>
    <BeatLoader v-if="!fetchComplete" class="fetch-loading" :color="'#bdc7bf'"/>
    <div v-if="fetchComplete && movieResults?.length === 0 && route.query.q" class="empty">No results were found</div>
    </div>

</template>

<style scoped>
h1 {
  text-align: center;
  margin-bottom: 20px;
}

.fetch-loading {
    margin-top: 200px;
    text-align: center;
}

h1 {
    display: block;
}

input {
    padding: 10px;
    background: var(--secondary-bg);
    color: white;
    height: 50px;
    vertical-align: middle;
    border: 1px solid var(--default-border-bg);
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
    
}
</style>