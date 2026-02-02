<script setup>

defineProps({
        movie: {
            type: Object,
            default: {"id": "234", "title": "this is a title", "overview": "this is an overview"},
        },
    });
    
</script>

<template>
    <div class="movie-container">
    <img v-if="movie.poster_path" :src="`https://image.tmdb.org/t/p/original`+movie.poster_path" alt="movie-poster">
    <div class="right">
        <div class="movie-details">
            <h2 class="movie-title">{{ movie.title}}</h2>
            <h3>Längd: 2h 17min</h3>
            <h3>Genre: Sci-fi, Action</h3>
            <h3>Åldersgräns: 7+</h3>
            <h3>Språk: {{ movie.language }}</h3>
        </div>
        <div class="movie-description">{{ movie.overview }}</div>
        <div class="movie-screenings">
            <h3>Boka biljetter:</h3>
            <button class="movie-date-btn">14 januari 14.00</button>
            <button class="movie-date-btn">31 januari 19.00</button>
            <button class="movie-date-btn">1 februari 21.00</button>
            <button class="movie-date-btn">1 februari 21.00</button>
            <button class="movie-date-btn">1 februari 21.00</button>
            <button class="movie-date-btn">1 februari 21.00</button>
            <button class="movie-date-btn">1 februari 21.00</button>
        </div>
    </div>
    </div>
    

</template>

<style scoped>

.movie-container {
    width: 100%;
    height: 100%;
    padding-right: 200px;
    padding-left: 200px;
    display: flex;
    flex-direction: row;
    justify-content: center;
    gap: 20px;


}

.movie-container img {
    width: 350px;
    height: auto;
}

.right {
    display: flex;
    flex-direction: column;
    justify-content: space-around;
    align-items: start;


}


button {
    background-color: #2d2d2d;
    color: white;
    padding: 30px;
    border: 1px solid #404040;
}

button {
    margin: 15px;
}

.movie-date-btn:hover {
    background: #e50914;
}

.movie-date-btn {
    border-radius: 5px;
    transition: 250ms;
}


.movie-details h3 {
    opacity: 60%;
}

.movie-title {
    margin-bottom: 10px;
}

</style>