<script setup>
import Navbar from '@/components/Navbar.vue'
import Footer from '@/components/Footer.vue'
import { RouterView } from 'vue-router';
import { useAuth0, User } from '@auth0/auth0-vue';

const { user, isAuthenticated, isLoading, error } = useAuth0();


const checkUserExists = async () => {
  const response = fetch("/")
}


</script>



<!---COMMENTING GITHUGÖLKJERÖLHJKT-->



<template>


  <div v-if="isLoading === false">
  <Navbar />
  <RouterView />
  <Footer />
  </div>

</template>


<style scoped>



</style>
