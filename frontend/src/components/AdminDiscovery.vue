<script setup>
import MoviesListAdmin from '@/components/MoviesListAdmin.vue';
import { ref, watch, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import BeatLoader from 'vue-spinner/src/BeatLoader.vue';
import { searchMovies, getMovie, getMoviesAll } from '../api/movies';
import {useAuth0} from "@auth0/auth0-vue";
const { user, isAuthenticated, isLoading, error, getAccessTokenSilently } = useAuth0();
import {debounce} from 'lodash';
import Search from '@/components/Search.vue';


import {useAppToast} from "@/use/useToast.js";
const {errorToast} = useAppToast();

const fetchComplete = ref(true);
const movieResults = ref([]);
const addedMovies = ref([]);

const route = useRoute();
const router = useRouter();

async function movieIsAdded(id) {
  return (await getMovie(id) !== null ? true : false);
}

async function fetchMovieResults() {
  if(route.query.q) {
    fetchComplete.value = false;
    const token = await getAccessTokenSilently();
    try {
      movieResults.value = (await searchMovies(route.query.q, token)).results;
    } catch(e) {
      errorToast("Error fetching results from TMDB. Try refreshing the page.")
    }
    try {
      addedMovies.value = await getMoviesAll();
    } catch(e) {
      errorToast("Error fetching movies from database. Try refreshing the page.")
    }
    fetchComplete.value = true;

  }

}

const handleAdd = (movie) => {
  addedMovies.value.push(movie)
};

const movieDisplay = computed(() => {
  if (movieResults.value && addedMovies) {
    return movieResults.value.filter(item_one => ! addedMovies.value.some(item_two => item_one.id === item_two.id))

  }
  else {
    return []
  }
})
</script>

<template>
  <div class="search-movies">
    <h1>Discover Movies on TMDB:</h1>
    <Search
        :header="`Search Movies on TMDB:`"
        :searchFunction="fetchMovieResults"
    />
    <MoviesListAdmin
        v-if="fetchComplete && route.query.q"
        :title="`Resultat för: `+ (route.query.q ? route.query.q : '')"
        :movies="movieDisplay"
        action="add"
        @add="handleAdd"
    />
    <BeatLoader
        v-if="!fetchComplete"
        class="fetch-loading"
        :color="'#bdc7bf'"
    />
    <div
        v-if="fetchComplete && movieResults?.length === 0 && route.query.q"
        class="empty"
    >
      No results were found
    </div>
  </div>
</template>

<style scoped>


.fetch-loading {
  margin-top: 200px;
  text-align: center;
}

h1 {
  display: block;
  margin-top: 24px;
  margin-bottom: 24px;
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
  font-family: sans-serif;
  border-radius: 7px;
  font-weight: 100;
}

@media screen and (max-width: 1200px) {
  input[type="search"] {
    width: 90%;
  }
}
</style>
