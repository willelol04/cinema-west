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
        checkedUser.value = true;
        const token = await getAccessTokenSilently();
        const Auth0UserIsAdmin = Auth0User['http://localhost:8000/roles'].includes('admin')
        let dbUser;
        try {
            dbUser = await getCurrentUser(token);
         } catch {
           dbUser = null
         }




        if(!dbUser) {
          await addUser({sub: Auth0User.sub, email:Auth0User.email, nickname: Auth0User.nickname, is_admin: Auth0UserIsAdmin}, token);
        } else {
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
  <Toast position="top-center" id="toast"/>
  <Footer  />

</template>


<style>

#toast {
  margin-bottom: 150px;
}


@media screen and (max-width: 768px) {
  #toast {
    width: 70vw;
    display: block;
    position: relative;
    margin-left: auto;
    margin-right: auto;
    padding: 0;
    text-align: center;
  }
}


</style>
