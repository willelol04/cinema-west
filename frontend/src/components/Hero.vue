<script setup>
    import { RouterLink } from 'vue-router';
</script>

<template>
    <section>
        <button onclick="console.log('hej')"><i class="pi pi-chevron-left"></i></button>
        <div class="hero-description">
        <h1>Jack Reacher</h1>
        <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Blanditiis deleniti sed accusantium amet sint a minima quisquam molestias laboriosam eum natus ut ex eius consequatur doloremque architecto dolorum, incidunt odio!</p>
        <RouterLink to="/movies">Bläddra bland filmer...</RouterLink>
        </div>
        
        <img src="https://image.tmdb.org/t/p/original/cOg3UT2NYWHZxp41vpxAnVCOC4M.jpg">
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
    
    section img {
        width: 20%;
    }
    
    section div {
        width: 70%;
    }
    
    .hero-description >:not(:last-child) {
        margin-bottom: 50px;
    }
    
    
    .hero-description a {
        padding: 20px;
        background-color: black;
        border-radius: 7px;
        color: white;
        transition: 300ms;
    }
    
    .hero-description h1 {
        font-size: 25px;
    }
    
    .hero-description a:hover {
        text-decoration: underline;
    }
    

    
</style>


<!--

<style scoped>

section {
    height: 50vh;
    background: black;
    padding-left: 200px;
    padding-right: 200px;
    color: white;
    display: flex;
    justify-content: space-between;
    flex-direction: row;
    align-items: center;
    gap: 5%;
    width: 100%;
}

section img {
    width: 60%;
    height: auto;
}


.hero-description a {
    width: 33%;
    display: block;
    background: white;
    color: black;
    padding: 25px;
    border-radius: 10px;
}

.hero-description a:hover {
    text-decoration: underline;
}

.hero-description {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: start;
    gap: 10%;
    height: 100%;

}
</style>

-->