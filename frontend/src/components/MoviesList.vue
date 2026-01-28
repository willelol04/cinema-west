<script setup>
    import { RouterLink } from 'vue-router';
    
    defineProps({
        title: {
            type: String,
            default: 'Movies',
        }
    });
</script>

<template>
    <section>
    <h1>{{ title }}</h1>
    <div class="movies-container">
        <div class="movie-card">
            <img src="../assets/poster_examples/jack2.jpg">
            <h2>Jack Reacher 2</h2>
            <p>17.00 - Salong A</p>
            <RouterLink class="link" :to="`/movie/${2+1}`">Läs mer...</RouterLink>
        </div>

        <div class="movie-card">
            <img src="../assets/poster_examples/jack2.jpg">
            <h2>Jack Reacher 2</h2>
            <p>17.00 - Salong A</p>
            <RouterLink class="link" :to="`/movie/${2+1}`">Läs mer...</RouterLink>
        </div>
        
        <div class="movie-card">
            <img src="../assets/poster_examples/jack2.jpg">
            <h2>Jack Reacher 2</h2>
            <p>17.00 - Salong A</p>
            <RouterLink class="link" :to="`/movie/${2+1}`">Läs mer...</RouterLink>
        </div>

        <div class="movie-card">
            <img src="../assets/poster_examples/jack2.jpg">
            <h2>Jack Reacher 2</h2>
            <p>17.00 - Salong A</p>
            <RouterLink class="link" :to="`/movie/${2+1}`">Läs mer...</RouterLink>
        </div>
        <div class="movie-card">
            <img src="../assets/poster_examples/jack2.jpg">
            <h2>Jack Reacher 2</h2>
            <p>17.00 - Salong A</p>
            <RouterLink class="link" :to="`/movie/${2+1}`">Läs mer...</RouterLink>
        </div>
        <div class="movie-card">
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
    text-align: center;
    display: block;
    padding: 20px 200px;
}

section h1 {
    margin-bottom: 50px;
}

.movies-container {
    width: 100%;
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    margin: 0 auto;

}

.movie-card img {
    width: 100%;
    border-radius: 10px;
    border-bottom-left-radius: 0px;
    border-bottom-right-radius: 0px;
    
}

.link {
    background-color: #e50914;
    color: white;
    width: 80%;
    display: block;
    margin: 0 auto;
    padding: 15px;
    margin-top: 15px;
    margin-bottom: 15px;
    border-radius: 10px;
    transition: 300ms;

}

.link:hover {
    background-color: rgb(233, 222, 222);
    color: #e50914;
}

.movie-card {
    width: 250px;
    background-color: #2d2d2d;
    border-radius: 10px;
    transition: 300ms;
    border: 1px solid #404040;
    margin: 30px 30px;
}

.movie-card:hover {
    transform: translateY(-10px);
}


.movie-card p, .movie-card h2 {
    padding: 5px 10px;
    text-align: left;
}


</style>