<script setup>
  import Hero from '@/components/Hero.vue';
  import MoviesList from '@/components/MoviesList.vue';
  import Booking from '@/components/Booking.vue';
  import { ref, onMounted } from 'vue';
  
 const ourMovies = ref([]) 
  
 async function testFetch() {
  const promise = await fetch('http://localhost:8000/movies/all');
  const data = await promise.json();
  const getData = JSON.parse(data);
  console.log(getData);
  ourMovies.value = getData;
  
 } 
 
 onMounted(testFetch)
 
</script>
<template>
  <Hero/>
  <div class="hr"  style="width: 100%; margin: 0 auto; border: 1px solid #2b2b2b"></div>
  <MoviesList :movies="ourMovies" title="Playing Today:"/>
  <div class="hr" style="width: 100%; margin: 0 auto; border: 1px solid #2b2b2b" ></div>
  <MoviesList title="Playing Tomorrow:" :showTimes="true" />

</template>
<style scoped>
</style>