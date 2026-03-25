<script setup>
import { RouterLink } from 'vue-router';
</script>

<template>
  <main>
    <h2>404 Page not found</h2>
    <RouterLink to="/">Go back to home</RouterLink>
  </main>
</template>

<style scoped>
main {
  padding: 20px 200px;
  width: 100%;
  margin: 0 auto;
  text-align: center;
  flex: 1;
}

a {
  padding: 5px 10px;
  display: block;
  width: fit-content;
  margin: 30px auto 0;
  border-radius: 5px;
  background-color: var(--selected-default-color);
  color: white;
  transition: 300ms;
}

a:hover {
  color: var(--selected-default-color);
  background-color: white;
}
</style>
