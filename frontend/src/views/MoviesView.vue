<script setup>
import { normalFetch } from '@/api/general';
import { getMoviesAll } from '@/api/movies';
import MoviesList from '@/components/MoviesList.vue';
import Sort from '@/components/Sort.vue';
import { onMounted, ref } from 'vue';
import BeatLoader from "vue-spinner/src/BeatLoader.vue";

const movieResults = ref(null);
const fetchComplete = ref(true);

import {useAppToast} from "@/use/useToast.js";
const {successToast, errorToast} = useAppToast();


async function fetchMovies(sortData) {
  const searchParams = new URLSearchParams();

  if(sortData.title !== null) {
    searchParams.append('title', sortData.title)
  }
  if(sortData.genre !== null) {
    searchParams.append('genre', sortData.genre)
  }
  if(sortData.rating !== null) {
    searchParams.append('rating', sortData.rating)
  }
  try {
    fetchComplete.value = false
    movieResults.value = await normalFetch(`/api/movies?${searchParams}`);
    console.log(movieResults.value);
    console.log(searchParams)

  } catch(e) {
    errorToast("Error fetching movies from database. Try refreshing the page.")
  } finally {
    fetchComplete.value = true
  }
}

onMounted( async () => {await fetchMovies({title: null, genre: null, rating: null})});
</script>
<template>
  <main>
    <Sort @update="fetchMovies" />
    <MoviesList v-if="movieResults" title="Movies" :movies="movieResults" />
    <BeatLoader
        class="fetch-loading"
        :color="'#bdc7bf'"
        v-if="!fetchComplete"
    />
  </main>
</template>
<style scoped>
h1 {
  text-align: left;
  margin-bottom: 10px;
}

main {
  background-color: var(--main-bg);
  text-align: center;
  padding: 20px 200px;
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

@media screen and (max-width: 1200px) {
  main {
    padding: 10px;
  }
}
</style>
