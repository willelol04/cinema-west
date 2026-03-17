<script setup>
import Hero from '@/components/Hero.vue';
import MoviesList from '@/components/MoviesList.vue';
import { ref, onMounted } from 'vue';
import { ConfirmPopupStyle } from 'primevue';
import { format, formatDistance, formatRelative, subDays } from 'date-fns';
import { getMovieSchedule } from '@/api/movies';
  
import BeatLoader from 'vue-spinner/src/BeatLoader.vue';
const schedule = ref([]) 
const fetchComplete = ref(false)

 const fetchMovies = async () => {
    try {
      schedule.value = await getMovieSchedule();
      fetchComplete.value = true;
    } catch(e) {
      console.log(e);
    }
  
} 

 
 onMounted(fetchMovies)
 
</script>
<template>
  <main v-if="fetchComplete">
  <Hero :upcomingMovies="schedule.upcoming"/>
    <div v-if="schedule.today.length > 0 " class="hr"></div>
  <MoviesList class="movieslist" v-if="schedule.today.length > 0 " :scroll="true" :movies="schedule.today" title="Playing Today:" :showTimes="false" />
    <div v-if="schedule.tomorrow.length > 0 " class="hr"></div>
  <MoviesList class="movieslist" v-if="schedule.tomorrow.length > 0 " :scroll="true" :movies="schedule.tomorrow" title="Playing Tomorrow:" :showTimes="false" />

  </main>
  <BeatLoader class="fetch-loading" :color="'#bdc7bf'" v-else />

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

.movieslist {
  margin-bottom: 50px;
  padding: 20px 200px;
}

@media screen and (max-width: 1200px) {
  .movieslist {
    padding: 10px;
  }
}


</style>