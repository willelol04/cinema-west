<script setup>
import MoviesList from './MoviesList.vue';
import { ref, onMounted, reactive } from 'vue';
    
const movieResults = ref([]);
const theatreResults = ref([]);
const fetchComplete = ref(false);
const screening = reactive({
    movie_id: 0,
    theatre_id: 0,
    start_time: '',
})

const fetchMovies = async () => {
    const promise = await fetch('http://localhost:8000/movies/all');
    movieResults.value = await promise.json();
    console.log(movieResults.value);
}

const fetchTheatres = async () => {
    const promise = await fetch('http://localhost:8000/theatres/all');
    theatreResults.value = await promise.json();
    console.log(theatreResults.value);
}

const addScreening = async () => {
    const response = await fetch("http://localhost:8000/addscreening", {
        method: "POST",
        body: JSON.stringify(screening),
        headers: {
            "Content-Type": "application/json"
        }

    });
    
    console.log(await response.text());

}

onMounted(fetchMovies);
onMounted(fetchTheatres);
</script>


<template>
    <div class="add-screening">
    <h1>Admin - Movie Screenings</h1>
    <h2>New Screening</h2>
    <form method="POST" @submit.prevent="addScreening">
        <div class="grid">
        <label for="movies">Movie:</label>
        <select v-model="screening.movie_id" id="movies">
            <option v-for="(movie,ind) in movieResults" :value="movie.id">{{ movie.title }}</option>
        </select>


        <label for="time">Time:</label>
        <input type="datetime-local" v-model="screening.start_time" id="time">
        <label for="theatres">Theatre:</label>
        <select v-model="screening.theatre_id" id="theatres">
            <option v-for="theatre in theatreResults" :value="theatre.id">{{ theatre.name }}</option>
        </select>
        
        <input type="submit" value="Add screening">
        </div>
    </form>
        
    </div>
    <div class="added-movies">
    <MoviesList v-if="false" title="Upcoming screenings:"/>
    </div>
    
</template>
<style scoped>

form {
    margin: 0 auto;
    width: 800px;
    text-align: left;

}

.grid {
    display: grid;
    grid-template-columns: 1fr 9fr;
    gap: 8px 5px;
}

label {
    padding: 10px;
    padding-left: 0px;
}

input, select, option {
    border: 1px solid black;
    padding: 10px;
    border-radius: 3px;
    background-color: #2b2b2b;
}

input:hover, select:hover, option:hover {
    cursor: pointer;
}

input[type="submit"] {
    grid-column: span 2;
}


</style>