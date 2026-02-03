<script setup>
import MoviesList from '@/components/MoviesList.vue';
import { onMounted, ref } from 'vue';

const movieResults = ref([]);
const fetchComplete = ref(false);

async function fetchMovies() {
    const promise = await fetch('http://localhost:8000/movies/all');
    movieResults.value = await promise.json();
    console.log(movieResults.value);
}

onMounted(fetchMovies);
</script>
<template>

  <MoviesList :movies=" movieResults" />

</template>
<style scoped>
  h1 {
    text-align: center;
  }
</style>