<script setup>
import MoviesListAdmin from '@/components/MoviesListAdmin.vue';
import { onMounted, ref } from 'vue';
import BeatLoader from 'vue-spinner/src/BeatLoader.vue';
import { getMoviesAllAdmin } from '@/api/movies';
import {useAuth0} from "@auth0/auth0-vue";
const { user, isAuthenticated, isLoading, error } = useAuth0();

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

const handleDelete = (movie) => {
  if(movieResults.value) {
    movieResults.value = movieResults.value.filter(m => m.id !== movie.id )
  }
};

onMounted(async () => {
  await fetchMovies();

})
</script>

<template>
  <div class="movie-database">
    <MoviesListAdmin
        v-if="movieResults && fetchComplete"
        :movies="movieResults"
        title="Movie Database"
        action="delete"
        @delete="handleDelete"
    />
    <BeatLoader class="fetch-loading" :color="'#bdc7bf'" v-else />
  </div>
</template>

<style scoped>

</style>
