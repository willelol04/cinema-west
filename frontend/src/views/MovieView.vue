<script setup>
import MovieDetails from '@/components/MovieDetails.vue';
import { useRoute } from 'vue-router';
import { onMounted, ref } from 'vue';
import { getMovie } from '@/api/movies';

import BeatLoader from 'vue-spinner/src/BeatLoader.vue';

const movieResults = ref({});
const fetchComplete = ref(true)

const route = useRoute();

async function fetchMovie() {
    fetchComplete.value = false;
    movieResults.value = await getMovie(route.params.id);
    console.log(movieResults.value);
    fetchComplete.value = true;
}

onMounted(fetchMovie);


</script>

<template>
  <main>
    <MovieDetails v-if="fetchComplete" :movie="movieResults" />
    <BeatLoader class="fetch-loading" :color="'#bdc7bf'" v-else />
  </main>
</template>

<style scoped>

main {
  width: 100%;
  flex: 1;
  display: flex;
  flex-direction: column;
}

</style>