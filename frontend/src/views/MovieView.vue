<script setup>
import MovieDetails from '@/components/MovieDetails.vue';
import Booking from '@/components/Booking.vue';
import { useRoute } from 'vue-router';
import { onMounted, ref } from 'vue';

const movieResults = ref({});

const route = useRoute();

async function fetchMovie() {
    const promise = await fetch('http://localhost:8000/movie/'+route.params.id);
    movieResults.value = await promise.json();
    console.log(movieResults.value);
}

onMounted(fetchMovie);


</script>

<template>
    <MovieDetails :movie="movieResults" />
    <Booking />


</template>

<style scoped>
</style>