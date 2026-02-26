<script setup>
import Navbar from '@/components/Navbar.vue'
import Footer from '@/components/Footer.vue'
import { onMounted, watch, ref, reactive } from 'vue';
import { RouterView } from 'vue-router';
import { Auth0Plugin, useAuth0, User } from '@auth0/auth0-vue';

const { user, isAuthenticated, isLoading, error, getAccessTokenSilently, checkSession } = useAuth0();

const checkedUser = ref(false);



const userExists = async (userAuthId) => {
    try {
        const response = await fetch("http://localhost:8000/auth0/users/"+userAuthId);
        const userResponse = await response.json();
        console.log("user exists: ", userResponse ? true : false);
        console.log(userResponse);
        if(userResponse) {
          return true;
        } else {
          return false;
        }
    } catch(e) {
        console.log(e);
        console.log("error fetching user");
    }

}

const privateApiTest = async (token) => {
  try {
    const response = await fetch("http://localhost:8000/api/private", {
      headers: {
        "authorization": `Bearer ${token}`,
      }
    });
    console.log(token)
    const userResponse = await response.json();
    console.log(userResponse);
  } catch(e) {
    console.log(e);
  }

}

const addUser = async (user) => {
    try {
    console.log("received obj", user)
    const token = await getAccessTokenSilently();
    const response = await fetch("http://localhost:8000/users", {
        method: "POST",
        body: JSON.stringify(user),
        headers: {
            "Content-Type": "application/json",
            "authorization": `Bearer ${token}`,
        }

    });
    
    console.log(await response.json());
      
    } catch(e) {
      console.log(e);
      console.log("error adding user");
    }

};


console.log("authenticated:", isAuthenticated.value)

onMounted(async () => { await privateApiTest();})

watch(
  () => ([user, user.value]),
  async ([user, value]) => {
    if(user && value && !checkedUser.value) {
        checkedUser.value = true;
        const token = await getAccessTokenSilently();
        console.log(token);
        console.log("curr user:", user)
        console.log("curr name:", value.name)
        console.log("curr roles:", value["http://localhost:8000/roles"])
        console.log([1,2,2,3,3,])
        if(! await userExists(value.sub)) {
          await addUser({sub: value.sub, nickname: value.nickname, email: value.email});
        } else {
          console.log("user exists, woo!");
          await privateApiTest(token);

        }
    } 
  }
)

onMounted( async () => console.log("hej: ", await checkSession()))

</script>




<!---COMMENTING GITHUGÖLKJERÖLHJKT-->



<template>
  <Navbar />
  <RouterView />
  <Footer />

</template>


<style scoped>



</style>
