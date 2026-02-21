<script setup>
import Hero from '@/components/Hero.vue';
import MoviesList from '@/components/MoviesList.vue';
import Booking from '@/components/Booking.vue';
import { ref, onMounted } from 'vue';
import { ConfirmPopupStyle } from 'primevue';
  
const ourMovies = ref([]) 
const fetchComplete = ref(false)

 const testFetch = async () => {
    try {
      const promise = await fetch('http://localhost:8000/movies');
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
  <div class="hr"  style="width: 100%; margin: 0 auto; border: 1px solid #2b2b2b"></div>
  <MoviesList v-if="fetchComplete" :display="1" :movies="ourMovies" title="Playing Today:" :showTimes="false" />
  <div class="hr" style="width: 100%; margin: 0 auto; border: 1px solid #2b2b2b" ></div>
  <MoviesList v-if="fetchComplete" :display="1" :movies="ourMovies" title="Playing Tomorrow:" :showTimes="false" />

</template>
<style scoped>
</style>