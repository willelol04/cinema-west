<script setup>

import { format, formatDistance, formatRelative, subDays } from 'date-fns';

defineProps({
        movie: {
            type: Object,
            default: {"id": "234", "title": "this is a title", "overview": "this is an overview"},
        },
    });
    
</script>

<template v-if="movie">
    <div class="movie-container">
    <img v-if="movie && movie.poster_path" :src="`https://image.tmdb.org/t/p/original`+movie.poster_path" alt="movie-poster">
    <div class="right">
        <div class="movie-details">
            <h2 class="movie-title">{{ movie.title}} {{ movie.release_date}}</h2>
            <h3>Length: {{ movie.length }}</h3>
            <h3 v-if="movie.genres && movie.genres.length > 0">Genres: <span v-for="(genre, index) in movie.genres.slice(0, movie.genres.length - 1)">{{ genre.name + ", "}} </span> <span>{{ movie.genres[movie.genres.length - 1].name }}</span></h3>
            <h3>Rating: 7+</h3>
            <h3>Language: {{ movie.language }}</h3>
        </div>
        <div class="movie-description">{{ movie.overview }}</div>
        <div class="movie-screenings">
        <h3>Book tickets:</h3>
            <div v-if="movie.screenings && movie.screenings.length !== 0" class="screenings">
            <RouterLink v-for="(screening, ind) in movie.screenings" :to="`/booking/`+screening.id" :key=screening class="screening">{{ format(screening.start_time, "EEEE, MMMM do HH:mm") }}</RouterLink>               
            </div>
            <p v-else>No scheduled screenings for this movie.</p>

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
    justify-content: start;
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


.screening {
    background-color: #2d2d2d;
    color: white;
    padding: 15px;
    border: 3px solid #404040;
    margin: 15px;
    border-radius: 5px;
    transition: 250ms;
    width: 100%;
    padding: 30px;
}


.screening:hover {
    background: white;
    background-color: #404040;
    border-color: #2d2d2d;

}



.movie-details h3 {
    opacity: 60%;
}

.movie-title {
    margin-bottom: 10px;
}

.screenings {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    width: 100%;
    gap: 20px;
    
}

</style>