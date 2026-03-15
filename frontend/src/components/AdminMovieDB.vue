<script setup>
import MoviesListAdmin from '@/components/MoviesListAdminDB.vue';
import { onMounted, ref, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import BeatLoader from 'vue-spinner/src/BeatLoader.vue';
import MoviesList from './MoviesList.vue';
import { getMovie, getMoviesAllAdmin } from '@/api/movies';
import {useAuth0} from "@auth0/auth0-vue";
const { user, isAuthenticated, isLoading, error, getAccessTokenSilently } = useAuth0();


const movieResults = ref([]);

async function fetchMovies() {
    try {
      movieResults.value = await getMoviesAllAdmin();

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

})

</script>


<template>
    
    <div class="movie-database">
    <h1>Movie Database</h1>
    <MoviesListAdmin v-if="movieResults" :movies="movieResults"  @update="fetchMovies"/>
    </div>

</template>


<style scoped>
  .movie-database {
    width: 100%;
    text-align: center;
  }
</style>