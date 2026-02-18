<script setup>
import MoviesListAdmin from '@/components/MoviesListAdminDiscovery.vue';
import { onMounted, ref, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import BeatLoader from 'vue-spinner/src/BeatLoader.vue';
import MoviesList from './MoviesList.vue';


const movieResults = ref([]);



async function fetchMovies() { 
    try {
    const movieResultsPromise = await fetch("http://localhost:8000/movies", {
      headers: {
        "Content-type": "application/json",
      }
    })
    const movieResultsObject = await movieResultsPromise.json();
    movieResults.value = movieResultsObject;
    for(const movie of movieResults.value) {
      movie.isAdded = true;
    }

    console.log(movieResults.value);

    } catch(e) {
    console.log(e);
    console.log("failed");
    } finally {
    console.log("quit");
    }
}

onMounted(fetchMovies)

</script>


<template>
    
    <div class="movie-database">
    <h1>Movie Database</h1>
    <MoviesListAdmin v-if="movieResults" :movies="movieResults" @update="fetchMovies" title="Added:"/>
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
