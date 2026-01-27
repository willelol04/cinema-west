<script setup>
    import { RouterLink } from 'vue-router';

</script>

<template>
    <section>
        <h2>404 Page not found</h2>
        <RouterLink to="/">Go back to home</RouterLink>
    </section>

</template>

<style scoped>

section {
    padding: 20px 200px;
    width: 100%;
    margin: 0 auto;
    text-align: center;
}

a {
    padding: 5px 10px;
    display: block;
    width: fit-content;
    margin: 0 auto;
    margin-top: 30px;
    border-radius: 5px;
    background-color: #e50914;
    color: black;
}

</style>