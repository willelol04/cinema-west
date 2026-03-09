<script setup>
import Navbar from '@/components/Navbar.vue'
import Footer from '@/components/Footer.vue'
import { onMounted, watch, ref, reactive } from 'vue';
import { RouterView } from 'vue-router';
import { Auth0Plugin, useAuth0, User } from '@auth0/auth0-vue';
const { user, isAuthenticated, isLoading, error, getAccessTokenSilently, checkSession } = useAuth0();

import { getUser, addUser } from './api/users';

const checkedUser = ref(false);

const userExists = async (userAuthId) => {
    try {
        const token = await getAccessTokenSilently();
        const user = await getUser(userAuthId, token);
        console.log("user:", user);

        if(user) {
          return true;
        } else {
          return false;
        }
    } catch(e) {
        console.log("error fetching user");
    }

}

watch(
  () => (user.value),
  async (currUser) => {
    if(currUser && currUser.sub && !checkedUser.value) {
        checkedUser.value = true;
        if(! await userExists(currUser.sub)) {
          const token = await getAccessTokenSilently();
          await addUser({sub: currUser.sub, email:currUser.email, nickname: currUser.nickname, is_admin: currUser['http://localhost:8000/roles'].includes('admin')}, token);
        } else {
          console.log("user exists, woo!");

        }
    } 
  }
)

onMounted(checkSession);

</script>

<template>
  <Navbar />
  <RouterView />
  <Footer />

</template>


<style scoped>



</style>
