<script setup>
import Navbar from '@/components/Navbar.vue'
import Footer from '@/components/Footer.vue'
import { onMounted, watch, ref, reactive } from 'vue';
import { RouterView } from 'vue-router';
import { Auth0Plugin, useAuth0, User } from '@auth0/auth0-vue';
const { user, isAuthenticated, isLoading, error, getAccessTokenSilently, checkSession } = useAuth0();
import { getCurrentUser, addUser, patchCurrentUserRole } from './api/users';

const checkedUser = ref(false);


watch(
  () => (user.value),
  async (Auth0User) => {
    if(Auth0User && Auth0User.sub && !checkedUser.value) {
        console.log("asdfasdfasdfasfd")
        checkedUser.value = true;
        const token = await getAccessTokenSilently();
        const Auth0UserIsAdmin = Auth0User['http://localhost:8000/roles'].includes('admin')
        const dbUser = await getCurrentUser(token);

        console.log("user is", Auth0User.sub)
        console.log("user is ", dbUser)
        console.log("user is admin: ", Auth0UserIsAdmin)



        if(!dbUser) {
          await addUser({sub: Auth0User.sub, email:Auth0User.email, nickname: Auth0User.nickname, is_admin: Auth0UserIsAdmin}, token);
        } else {
          console.log("user exists, woo!");
          if(Auth0UserIsAdmin !== dbUser.is_admin) {
            await patchCurrentUserRole({is_admin: Auth0UserIsAdmin}, token);
          }
        }
    }
  }
)

onMounted(checkSession);

import Toast from 'primevue/toast';
import { useToast } from 'primevue/usetoast';

const toast = useToast();


</script>

<template>
  <Navbar id="routerView"  />
  <RouterView />
  <Footer  />
  <Toast position="bottom-right" appendTo="router-container"/>

</template>


<style scoped>




</style>
