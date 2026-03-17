<script setup>
import { normalFetch } from '@/api/general';
import { getMoviesAll } from '@/api/movies';
import MoviesList from '@/components/MoviesList.vue';
import Sort from '@/components/Sort.vue';
import { onMounted, ref } from 'vue';
import BeatLoader from "vue-spinner/src/BeatLoader.vue";

const movieResults = ref([]);
const fetchComplete = ref(true);



async function fetchMovies(sortData) {
    fetchComplete.value = false
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
    } finally {
      fetchComplete.value = true
    }
}

onMounted( async () => {await fetchMovies({title: null, genre: null, rating: null})});

</script>
<template>
  <main>
    <h1>Movies</h1>
    <Sort @update="fetchMovies"/>
    <MoviesList v-if="fetchComplete" :movies="movieResults" />
    <BeatLoader class="fetch-loading" :color="'#bdc7bf'" v-else />
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
  }

  @media screen and (max-width: 1200px) {
    main {
      padding: 10px;
    }
  }
</style>