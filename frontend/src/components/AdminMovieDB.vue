<script setup>
import MoviesListAdmin from '@/components/MoviesListAdmin.vue';
import { onMounted, ref, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import BeatLoader from 'vue-spinner/src/BeatLoader.vue';
import MoviesList from './MoviesList.vue';
import { getMovie, getMoviesAllAdmin } from '@/api/movies';
import {useAuth0} from "@auth0/auth0-vue";
const { user, isAuthenticated, isLoading, error, getAccessTokenSilently } = useAuth0();

import {useAppToast} from "@/use/useToast.js";
const {errorToast} = useAppToast();

const movieResults = ref([]);
const fetchComplete = ref(true)

async function fetchMovies() {
  try {
    fetchComplete.value = false;
    movieResults.value = await getMoviesAllAdmin();

  } catch(e) {
    errorToast("Error fetching movies. Try refreshing the page.")
  }
  finally {
    fetchComplete.value = true;
  }
}

onMounted(async () => {
  await fetchMovies();

})
</script>

<template>
  <div class="movie-database">
    <h1>Movie Database</h1>
    <MoviesListAdmin
        v-if="movieResults && fetchComplete"
        :movies="movieResults"
        action="delete"
        @update="fetchMovies"
    />
    <BeatLoader class="fetch-loading" :color="'#bdc7bf'" v-else />
  </div>
</template>

<style scoped>
.movie-database {
  text-align: center;
}
</style>
