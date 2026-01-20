<script setup>

</script>

<template>
    <section>
        <div class="hero-description">
        <h2>Star wars</h2>
        <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Blanditiis deleniti sed accusantium amet sint a minima quisquam molestias laboriosam eum natus ut ex eius consequatur doloremque architecto dolorum, incidunt odio!</p>
        <a href="#">Bläddra bland filmer...</a>
        </div>
        <img src="../assets/movie1.webp">
    </section>

</template>

<style scoped>
    section img {
        width: 100%;

    }
    
    .hero-description {
        position: absolute;
        top: 50%;
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