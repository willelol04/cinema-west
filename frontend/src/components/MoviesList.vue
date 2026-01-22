<script setup>
    import { RouterLink } from 'vue-router';
</script>

<template>
    <section>
    <div class="movies-today-container">
        <div class="movie-today">
            <img src="../assets/poster_examples/jack2.jpg">
            <h2>Jack Reacher 2</h2>
            <p>17.00 - Salong A</p>
            <RouterLink class="link" :to="`/movie/${2+1}`">Läs mer...</RouterLink>
        </div>

        <div class="movie-today">
            <img src="../assets/poster_examples/jack2.jpg">
            <h2>Jack Reacher 2</h2>
            <p>17.00 - Salong A</p>
            <RouterLink class="link" :to="`/movie/${2+1}`">Läs mer...</RouterLink>
        </div>
        
        <div class="movie-today">
            <img src="../assets/poster_examples/jack2.jpg">
            <h2>Jack Reacher 2</h2>
            <p>17.00 - Salong A</p>
            <RouterLink class="link" :to="`/movie/${2+1}`">Läs mer...</RouterLink>
        </div>

        <div class="movie-today">
            <img src="../assets/poster_examples/jack2.jpg">
            <h2>Jack Reacher 2</h2>
            <p>17.00 - Salong A</p>
            <RouterLink class="link" :to="`/movie/${2+1}`">Läs mer...</RouterLink>
        </div>
    </div>

    </section>

</template>

<style scoped>


section {
    width: 100%;
    padding-left: 200px;
    padding-right: 200px;
    margin-bottom: 50px;
    margin-top: 50px;
    text-align: center;
    display: block;
}

section h1 {
    margin-bottom: 50px;
}

.movies-today-container {
    display: flex;
    flex-direction: row;
    justify-content: space-between;

}

.movies-today-container img {
    height: 300px;
}

.link {
    background-color: black;
    color: white;
    width: 100%;
    display: block;
    padding: 15px;
    margin-top: 20px;
}


</style>