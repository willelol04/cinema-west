<script setup>
  import Hero from '@/components/Hero.vue';
  import MoviesList from '@/components/MoviesList.vue';
  import Booking from '@/components/Booking.vue';
  

</script>
<template>
  <Hero/>
  <div class="hr" style="width: 100%; margin: 0 auto; border: 1px solid #2b2b2b"></div>
  <MoviesList title="Playing Today:"/>
  <div class="hr" style="width: 100%; margin: 0 auto; border: 1px solid #2b2b2b" ></div>
  <MoviesList title="Playing Tomorrow:" />

</template>
<style scoped>
</style>