<script setup>
import MoviesListAdmin from '@/components/MoviesListAdminDiscovery.vue';
import { ref, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import BeatLoader from 'vue-spinner/src/BeatLoader.vue';
import {useAuth0} from "@auth0/auth0-vue";
import MoviesList from './MoviesList.vue';
const { user, isAuthenticated, isLoading, error, getAccessTokenSilently } = useAuth0();


const search_field = defineModel('Bing');
const fetchComplete = ref(true);
const movieResults = ref([]);

const route = useRoute();
const router = useRouter();


async function fetchMovieResults(numbers_tried = 1) { 
    const num = numbers_tried;
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
    
    <div class="movie-database">
    <h1>Movie Database</h1>
    <MoviesListAdmin/>

    </div>
    

    
    <!--
    <MoviesList title="Already added movies:"/>
    -->

</template>


<style scoped>
  .movie-database {
    width: 100%;
    padding: 20px 10vw;
    text-align: center;
  }
</style>
