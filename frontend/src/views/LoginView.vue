<script setup>
import { RouterLink } from 'vue-router';
import { reactive } from 'vue';
    

    
</script>

<template>
    <section>
        <div class="login">
            <div class="login-box">
                <h1>Log in</h1>
                <form>
                    <label for="email">Email:</label><br/>
                    <input type="email" id="email" name="email" required/><br/><br/>
                    <label for="password">Password:</label><br/>
                    <input type="password" id="password" name="password" required/><br/><br/>
                    <RouterLink to="/signup">Har du inget konto? Registrera dig nu!</RouterLink>
                    <button type="submit">Log in</button>
                </form>
            </div>
            
            
        </div>
    
    </section>

</template>

<style scoped>

section {
    padding: 20px 200px;
    width: 100%;
    margin: 0 auto;
    text-align: center;
}
.login {
  min-height: 73vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;


}

.login-box {
  max-width: 700px;
  width: 100%;

  padding: 24px 28px;
  border-radius: 16px;

  background-color: #1a1a1a;
  border: 1px solid rgba(255, 255, 255, 0.12);

  text-align: left;

}
h1 {
    text-align: center;
    margin-bottom: 20px;
    font-size: 36px;

}
button {
    padding: 5px 10px;
    display: block;
    width: fit-content;
    margin: 0 auto;
    margin-top: 30px;
    border-radius: 5px;
    background-color: #e50914;
    color: white;
    transition: 300ms;
}

a:hover {
    color: #e50914; 
    background-color: rgb(233, 222, 222);
}

.signin-form {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

input {
  padding: 10px;
  border-radius: 6px;
  border: 1px solid rgba(255,255,255,0.2);
  background: #111;
  color: white;
}
</style>