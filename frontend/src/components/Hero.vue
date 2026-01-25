<script setup>
    import { RouterLink } from 'vue-router';
</script>

<template>
    <section>
        <button onclick="console.log('hej')"><i class="pi pi-chevron-left"></i></button>
        <div class="hero-left">
        <h1>Jack Reacher</h1>
        <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Blanditiis deleniti sed accusantium amet sint a minima quisquam molestias laboriosam eum natus ut ex eius consequatur doloremque architecto dolorum, incidunt odio!</p>
        <RouterLink to="/movies">Bläddra bland filmer...</RouterLink>
        </div>
        
        <div class="hero-right">
        <img class="hero-image" src="https://image.tmdb.org/t/p/original/cOg3UT2NYWHZxp41vpxAnVCOC4M.jpg">
        <div class="tmdb-attribution"><img src="../assets/tmdb-logo-text.svg"></div>
        </div>
        <button><i class="pi pi-chevron-right"></i></button>
    </section>

</template>

<style scoped>

    section{ 
        width: 100%;
        display: flex;
        justify-content: space-between;
        flex-direction: row;
        align-items: center;
        padding-left: 200px;
        padding-right: 200px;
        padding-top: 50px;
        padding-bottom: 50px;
        border-bottom: 1px solid black;
    }
    
    button {
        padding: 10px;
    }
    
    i {
        font-size: 1.2rem;
    }
    
    .hero-right {
        width: 20%;
        position: relative;
    }
    
    .hero-right img {
        width: 100%;
        height: auto;
        text-align: right;
    }
    
    section div {
        width: 70%;
    }
    

    .hero-left > * {
        margin-bottom: 50px;

    }
    
    
    
    .hero-left a {
        padding: 20px;
        background-color: black;
        width: 200px;
        display: block;
        border-radius: 7px;
        color: white;
        transition: 300ms;
    }
    
    
    .hero-left h1 {
        font-size: 25px;
    }
    
    .hero-left a:hover {
        text-decoration: underline;
    }
    
    .tmdb-attribution  {
        right: 0;
        position: absolute;
        width: 100%;
    }
    
    
    

    
</style>
