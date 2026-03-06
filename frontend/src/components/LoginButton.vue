<script setup lang="ts">
import { useAuth0 } from '@auth0/auth0-vue'
import {useRoute, useRouter} from 'vue-router';

const route = useRoute();
const router = useRouter();

const { loginWithRedirect, isLoading } = useAuth0()

const handleLogin = () => {
  sessionStorage.setItem('redirect_url', window.location.pathname);
  loginWithRedirect();
}
</script>

<template>
  <button 
    @click="handleLogin" 
    class="button login"
    :disabled="isLoading"
    >
    {{ isLoading ? 'Loading...' : 'Log In/Sign up' }}
  </button>
</template>

<style scoped>

button {
    width: 175px;
    background-color: rgba(43, 43, 43, 0.753);
    color: white;
    padding: 8px 5px;
    border-radius: 5px;
    font-size: 18px;
    border: 1px solid #404040;
    margin: 0;
}
</style>