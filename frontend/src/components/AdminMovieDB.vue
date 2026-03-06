<script setup>
import MoviesListAdmin from '@/components/MoviesListAdminDB.vue';
import { onMounted, ref, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import BeatLoader from 'vue-spinner/src/BeatLoader.vue';
import MoviesList from './MoviesList.vue';
import { getMovie } from '@/api/movies';


const movieResults = ref([]);
const theatresResults = ref(null)


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

onMounted(async () => {
  await fetchMovies();
  await fetchTheatres();

})

const popMovie = (ind) => {
  movieResults.value.splice(ind, 1)
}

const updateMovie = async (movie) => {
  movie.screenings = await getMovie(movie).screenings;
  movie.showEdit = false;
  movie.showScreenings = false;

}

</script>


<template>
    
    <div class="movie-database">
    <h1>Movie Database</h1>
    <MoviesListAdmin v-if="movieResults" :movies="movieResults" :theatres="theatresResults" @popMovie="popMovie" @updateMovie="updateMovie" title="Added:"/>
    </div>
    

    
    <!--
    <MoviesList title="Already added movies:"/>
    -->

</template>


<style scoped>
  .movie-database {
    width: 100%;
    text-align: center;
  }
</style>
