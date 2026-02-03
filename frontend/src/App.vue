<script setup>
import Navbar from '@/components/Navbar.vue'
import Footer from '@/components/Footer.vue'
import { RouterView } from 'vue-router';
</script>



<!---COMMENTING GITHUGÖLKJERÖLHJKT-->




<template>
  <Navbar :isLoggedIn="false"/>
  <RouterView />
  <div class="fix" style="clear: both; width: 100%;"></div>
  <Footer />

</template>

<style scoped>



</style>
