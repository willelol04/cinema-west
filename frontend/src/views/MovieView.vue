<script setup>
import MovieDetails from '@/components/MovieDetails.vue';
import { useRoute } from 'vue-router';
import { onMounted, ref } from 'vue';
import { getMovie } from '@/api/movies';

const movieResults = ref({});

const route = useRoute();

async function fetchMovie() {
    movieResults.value = await getMovie(route.params.id);
    console.log(movieResults.value);
}

onMounted(fetchMovie);


</script>

<template>
    <MovieDetails :movie="movieResults" />
</template>

<style scoped>
</style>