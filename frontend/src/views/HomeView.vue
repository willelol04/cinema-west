<script setup>
import Hero from '@/components/Hero.vue';
import MoviesList from '@/components/MoviesList.vue';
import Booking from '@/components/Booking.vue';
import { ref, onMounted } from 'vue';
import { ConfirmPopupStyle } from 'primevue';
import { format, formatDistance, formatRelative, subDays } from 'date-fns';
  
const ourMovies = ref([]) 
const fetchComplete = ref(false)

 const testFetch = async () => {
    try {
      const params = new URLSearchParams({start_date: format(Date.now(), 'yyyy-MM-dd'), end_date: format(Date.now(), 'yyyy-MM-dd')});
      const promise = await fetch(`http://localhost:8000/movies/schedule`);
      ourMovies.value = await promise.json();
      fetchComplete.value = true;
    } catch(e) {
      console.log(e);
    }
  
} 
 
 onMounted(testFetch)
 
</script>
<template>
  <Hero/>
  <div class="hr"></div>
  <MoviesList class="movieslist" v-if="fetchComplete" :display="5" :movies="ourMovies.today" title="Playing Today:" :showTimes="false" />
  <div class="hr"></div>
  <MoviesList class="movieslist" v-if="fetchComplete" :display="5" :movies="ourMovies.tomorrow" title="Playing Tomorrow:" :showTimes="false" />

</template>
<style scoped>

.hr {
  width: 100%; 
  margin: 0 auto; 
  border: 1px solid #2b2b2b
}
    
    
    
@media screen and(max-width: 1600px) {
}
</style>