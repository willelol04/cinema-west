<script setup>
import MoviesList from '@/components/MoviesList.vue';
import Sort from '@/components/Sort.vue';
import { onMounted, ref } from 'vue';

const movieResults = ref([]);
const fetchComplete = ref(false);

async function fetchMovies() {
    const promise = await fetch("/api/movies");
    movieResults.value = await promise.json();
    console.log(movieResults.value);
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
    const promise = await fetch(`/api/movies?${searchParams}`);
    movieResults.value = await promise.json();
    console.log(movieResults.value);
    console.log(searchParams)
}

onMounted(fetchMovies);
</script>
<template>
  <MoviesList :filter="true" @update="updateMovies" :movies="movieResults" />

</template>
<style scoped>
  h1 {
    text-align: center;
  }
</style>