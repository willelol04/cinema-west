<script setup>

</script>

<template>
      <div class="signup-box">
        <h1>Complete signup:</h1>
        <form>
          <label for="f_name">First name:</label><br/>
          <input v-model="formData.f_name" type="text" id="f_name" name="f_name" required/><br/><br/>
          <label for="l_name">Last name:</label><br/>
          <input v-model="formData.l_name" type="text" id="l_name" name="l_name" required/><br/><br/>
          <label for="email">Email:</label><br/>
          <input v-model="formData.email" type="email" id="email" name="email" required/><br/><br/>
          <label for="password">Password:</label><br/>
          <input v-model="formData.password" type="password" id="password" name="password" required/><br/><br/>
          <button type="submit">Sign Up</button>
          <p>{{ post_status }}</p>
        </form>
      </div>

</template>

<style scoped>

</style>