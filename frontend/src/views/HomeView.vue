<script setup>
import Hero from '@/components/Hero.vue';
import MoviesList from '@/components/MoviesList.vue';
import { ref, onMounted } from 'vue';
import { getMovieSchedule } from '@/api/movies';
import BeatLoader from 'vue-spinner/src/BeatLoader.vue';
import {useAppToast} from "@/use/useToast.js";

const {successToast, errorToast} = useAppToast();

const schedule = ref(null)
const fetchComplete = ref(true)

 const fetchMovies = async () => {
    try {
      fetchComplete.value = false;
      schedule.value = await getMovieSchedule();
    } catch(e) {
      errorToast("Error fetching movie schedule Try refreshing the page.");
    } finally {
      fetchComplete.value = true;
    }
}


 onMounted(fetchMovies)

</script>
<template>
  <main>
  <Hero v-if="schedule?.upcoming.length > 0" :upcomingMovies="schedule.upcoming"/>
    <div v-if="schedule?.today.length > 0 " class="hr"></div>
  <MoviesList class="movies-list" v-if="schedule?.today.length > 0 " :scroll="true" :movies="schedule.today" title="Playing Today:" />
    <div v-if="schedule?.tomorrow.length > 0 " class="hr"></div>
  <MoviesList class="movies-list" v-if="schedule?.tomorrow.length > 0 " :scroll="true" :movies="schedule.tomorrow" title="Playing Tomorrow:"/>
    <BeatLoader class="fetch-loading" :color="'#bdc7bf'" v-if="!fetchComplete"/>
  </main>

</template>
<style scoped>

.hr {
  width: 100%;
  margin: 0 auto;
  border: 1px solid #2b2b2b
}



main {
  background-color: var(--main-bg);
  width: 100%;
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.movies-list {
  padding: 20px 200px;
}

@media screen and (max-width: 1200px) {
  .movies-list {
    padding: 10px;
  }
}


</style>