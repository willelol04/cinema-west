<script setup>
  import Hero from '@/components/Hero.vue';
  import MoviesList from '@/components/MoviesList.vue';
  import Booking from '@/components/Booking.vue';

</script>
<template>

  <Hero/>
  
  <h1>På bio idag:</h1>
  <MoviesList />

</template>
<style scoped>
    h1 {
        text-align: center;
    }
</style>