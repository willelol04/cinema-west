<script setup>
import { onMounted } from 'vue';
import {useAuth0} from "@auth0/auth0-vue";

const { loginWithRedirect, isLoading } = useAuth0()


onMounted(async () => {
    loginWithRedirect();
})

</script>
<template>

</template>

<style scoped>

</style>