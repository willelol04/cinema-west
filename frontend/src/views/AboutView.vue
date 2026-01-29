<script setup>
    import { RouterLink } from 'vue-router';

</script>

<template>
    <section>
        <div class="about">
        <div class="about-box">
                <h1>About us</h1>
            <p>
                Cinema West is a modern cinema dedicated to creating a great movie-going experience for everyone. We believe that going to the cinema should feel special — from the moment you browse showtimes to the moment the lights go down and the film begins.

            </p>
            <br/>
            <p>
                Our cinema combines comfortable seating, high-quality sound and projection, and a carefully selected movie lineup that includes everything from the latest blockbusters to smaller releases. Whether you’re visiting with friends, family, or on your own, Cinema West is designed to be a place where films can truly be enjoyed.
            </p>
            <br/>
            <p>
                Alongside the cinema experience itself, we focus on making everything around it simple and intuitive. This website allows visitors to explore movies, check showtimes, and book tickets easily, reflecting our goal of a smooth and modern customer experience.
            </p>
            <br/>
            <p>
                Cinema West is a fictional cinema created as part of a university project, but it is designed to reflect how a real, contemporary cinema could look and function.        
            
            </p>
            </div>
            
            
        </div>
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
.about {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;

background-image: url("@/assets/hero.jpg");
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}

.about-box {
  max-width: 700px;
  width: 100%;

  padding: 24px 28px;
  border-radius: 16px;

  background-color: #1a1a1a;
  border: 1px solid rgba(255, 255, 255, 0.12);

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
    color: white;
    transition: 300ms;
}

a:hover {
    color: #e50914; 
    background-color: rgb(233, 222, 222);
}

</style>