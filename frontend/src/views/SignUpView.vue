<script setup>
import { RouterLink } from 'vue-router';
import { reactive, ref } from 'vue';


const post_status = ref('');

const formData = reactive({
    f_name: '',
    l_name: '',
    email: '',
    password: '',
});


const onSubmit = async () => {
    console.log(formData);
    await adduser();
};

const adduser = async () => {
    const response = await fetch("http://localhost:8000/adduser", {
        method: "POST",
        body: JSON.stringify(formData),
        headers: {
            "Content-Type": "application/json"
        }

    });
    const message = await response.text();
    post_status.value = message;
};

</script>

<template>
    <section>
        <div class="signup">
            <div class="signup-box">
                <h1>Sign Up</h1>
                <form @submit.prevent="onSubmit">
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

.signup {
  min-height: 73vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
}

.signup-box {
  max-width: 700px;
  width: 100%;
  margin: 0 auto;
  padding: 24px 28px;
  border-radius: 16px;

  background-color: #1a1a1a;
  border: 1px solid rgba(255, 255, 255, 0.12);

  text-align: center;

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

.signup-form {
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