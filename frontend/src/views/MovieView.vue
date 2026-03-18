<script setup>
import MovieDetails from '@/components/MovieDetails.vue';
import { useRoute } from 'vue-router';
import { onMounted, ref } from 'vue';
import { getMovie } from '@/api/movies';

import BeatLoader from 'vue-spinner/src/BeatLoader.vue';

const movieResults = ref(null);
const fetchComplete = ref(true)

import {useAppToast} from "@/use/useToast.js";
const {successToast, errorToast} = useAppToast();

const route = useRoute();

async function fetchMovie() {
  try {
    fetchComplete.value = false;
    movieResults.value = await getMovie(route.params.id);
    console.log(movieResults.value);
  } catch (e) {
    errorToast("Erroring fetching movie from database. Try refreshing the page.")
  } finally {
    fetchComplete.value = true;
  }
}

onMounted(fetchMovie);
</script>

<template>
  <main>
    <MovieDetails v-if="movieResults" :movie="movieResults" />
    <BeatLoader
        class="fetch-loading"
        :color="'#bdc7bf'"
        v-if="!fetchComplete"
    />
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
