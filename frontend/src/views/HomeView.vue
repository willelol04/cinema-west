<script setup>
  import Hero from '@/components/Hero.vue';
  import MoviesList from '@/components/MoviesList.vue';
  import Booking from '@/components/Booking.vue';
  

</script>
<template>
  <Hero/>
  
  <h1>På bio idag - 2026-01-27</h1>
  <MoviesList />
  <h1>På bio imorgon - 2026-01-28</h1>
  <MoviesList />

</template>
<style scoped>
    h1 {
      padding: 60px 200px;
    }
</style>