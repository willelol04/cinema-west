<script setup>
import { onMounted } from 'vue';
import { useAuth0 } from '@auth0/auth0-vue';
import { useRouter, useRoute } from 'vue-router';

const router = useRouter();
const route = useRoute();

onMounted(async () => {
  try {
    const redirectUrl = sessionStorage.getItem('redirect_url')
    sessionStorage.removeItem('redirect_url');
    if(redirectUrl?.startsWith('/')) {
      await router.push(redirectUrl);
    } else {
      await router.replace('/');
    }
  } catch(e) {
    await router.replace('/');
  }
});
</script>
<template></template>

<style scoped></style>
