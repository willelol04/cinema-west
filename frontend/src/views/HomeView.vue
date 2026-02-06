<script setup>
import Hero from '@/components/Hero.vue';
import MoviesList from '@/components/MoviesList.vue';
import Booking from '@/components/Booking.vue';
import { ref, onMounted } from 'vue';
import { ConfirmPopupStyle } from 'primevue';
  
const ourMovies = ref([]) 

async function testFetch() {
    const promise = await fetch('http://localhost:8000/movies/all', {
    });
    const data = await promise.json();
    const getData = data;
    console.log(getData);
    ourMovies.value = getData;
  
} 
 
onMounted(testFetch)
 
</script>
<template>
  <Hero/>
  <div class="hr"  style="width: 100%; margin: 0 auto; border: 1px solid #2b2b2b"></div>
  <MoviesList :display="5" title="Playing Today:"/>
  <div class="hr" style="width: 100%; margin: 0 auto; border: 1px solid #2b2b2b" ></div>
  <MoviesList :display="5" title="Playing Tomorrow:" :showTimes="false" />

</template>
<style scoped>
</style>