<script setup>
import { normalFetch } from '@/api/general';
import { getMoviesAll } from '@/api/movies';
import MoviesList from '@/components/MoviesList.vue';
import Sort from '@/components/Sort.vue';
import { onMounted, ref } from 'vue';

const movieResults = ref([]);
const fetchComplete = ref(false);

async function fetchMovies() {
    try {
      movieResults.value = await getMoviesAll();
      console.log(movieResults.value);

    } catch(e) {
      console.log(e)
    }
}

async function updateMovies(sortData) {
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
      movieResults.value = await normalFetch(`/api/movies?${searchParams}`);
      console.log(movieResults.value);
      console.log(searchParams)

    } catch(e) {
      console.log(e)
    }
}

onMounted(fetchMovies);
</script>
<template>
  <main>
    <MoviesList :filter="true" @update="updateMovies" :movies="movieResults" />
  </main>

</template>
<style scoped>
  h1 {
    text-align: center;
  }

  main {
    background-color: var(--main-bg);
  }
</style>