<script setup>
import { onMounted } from 'vue';
import { useAuth0 } from '@auth0/auth0-vue';
import { useRouter, useRoute } from 'vue-router';

const router = useRouter();
const route = useRoute();

onMounted(async () => {
  router.push('https://dev-3ww5cwntj1o7ydv4.eu.auth0.com/authorize?client_id=sZDxzMh7CtpOdufVC7ZV9uzTlqRrZ4kA&scope=openid+profile+email+offline_access&redirect_uri=http%3A%2F%2Flocalhost%3A3000%2Fcallback&audience=http%3A%2F%2Flocalhost%3A8000&response_type=code&response_mode=query')
})

</script>
<template>

</template>

<style scoped>

</style>