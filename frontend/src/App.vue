<script setup>
import Navbar from '@/components/Navbar.vue'
import Footer from '@/components/Footer.vue'
import { onMounted, watch, ref } from 'vue';
import { RouterView } from 'vue-router';
import { Auth0Plugin, useAuth0, User } from '@auth0/auth0-vue';

const { user, isAuthenticated, isLoading, error } = useAuth0();

const checkedUser = ref(false);

const userExists = async (userAuthId) => {
    try {
        const response = await fetch("http://localhost:8000/auth0/users/"+userAuthId);
        const userResponse = await response.json();
        console.log("user exists: ", userResponse.length > 0 ? true : false);
        console.log(userResponse);
        if(userResponse.length > 0) {
          return true;
        } else {
          return false;
        }
    } catch(e) {
        console.log(e);
        console.log("error fetching user");
    }

}

const addUser = async (usr) => {
    try {
    console.log("received obj", usr)
    const response = await fetch("http://localhost:8000/users", {
        method: "POST",
        body: JSON.stringify(usr),
        headers: {
            "Content-Type": "application/json"
        }

    });
    
    console.log(await response.json());
      
    } catch(e) {
      console.log("e");
      console.log("error adding user");
    }

};


console.log("authenticated:", isAuthenticated.value)

watch(
  () => (user.value),
  async (value) => {
    if(value && !checkedUser.value) {
        checkedUser.value = true;
        if(! await userExists(value.sub)) {
          await addUser({sub: value.sub, email: value.email});
        } else {
          console.log("user exists, woo!")
        }
    } 
  }
)

</script>



<!---COMMENTING GITHUGÖLKJERÖLHJKT-->



<template>
  <div v-if="!isLoading">
  <Navbar />
  <RouterView />
  <Footer />
  </div>

</template>


<style scoped>



</style>
