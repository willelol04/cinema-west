<script setup>
import MoviesListAdmin from '@/components/MoviesListAdminDB.vue';
import { onMounted, ref, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import BeatLoader from 'vue-spinner/src/BeatLoader.vue';
import MoviesList from './MoviesList.vue';
import { getMovie, getMoviesAll } from '@/api/movies';
import { getTheatres } from '@/api/theatres';


const movieResults = ref([]);
const theatresResults = ref(null)


const fetchTheatres = async () => {
    theatresResults.value = await getTheatres();
}

async function fetchMovies() { 
    try {
      movieResults.value = await getMoviesAll();

      for(const movie of movieResults.value) {
        movie.isAdded = true;
        movie.showScreenings = false;

        for(const screening of movie.screenings) {
          screening.showEdit = false;
        }

      }

    } catch(e) {
    console.log(e);
    } 
}

onMounted(async () => {
  await fetchMovies();
  await fetchTheatres();

})

</script>


<template>
    
    <div class="movie-database">
    <h1>Movie Database</h1>
    <MoviesListAdmin v-if="movieResults" :movies="movieResults" :theatres="theatresResults" @update="fetchMovies"/>
    </div>

</template>


<style scoped>
  .movie-database {
    width: 100%;
    text-align: center;
  }
</style>