<script setup>
import MoviesList from './MoviesList.vue';
import { ref, onMounted, reactive } from 'vue';
import {useAuth0} from "@auth0/auth0-vue";

const { user, isAuthenticated, isLoading, error, getAccessTokenSilently } = useAuth0();
    
const movieResults = ref([]);
const theatreResults = ref([]);
const fetchComplete = ref(false);
const screening = reactive({
    movie_id: 0,
    theatre_id: 0,
    start_time: '',
})

const fetchMovies = async () => {
    const promise = await fetch('http://localhost:8000/movies');
    movieResults.value = await promise.json();
    console.log(movieResults.value);
}

const fetchTheatres = async () => {
    const promise = await fetch('http://localhost:8000/theatres');
    theatreResults.value = await promise.json();
    console.log(theatreResults.value);
}

const addScreening = async () => {
    const token = await getAccessTokenSilently();
    const response = await fetch("http://localhost:8000/screenings", {
        method: "POST",
        body: JSON.stringify(screening),
        headers: {
            "Content-Type": "application/json",
            "authorization": `Bearer ${token}`,
        }

    });
    
    console.log(await response.text());

}

onMounted(fetchMovies);
onMounted(fetchTheatres);
</script>


<template>
    <div class="add-screening">
    <form method="POST" @submit.prevent="addScreening">
    <h1>New Screening</h1>
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
    
</template>
<style scoped>

.add-screening {
    width: 60%;
    padding: 20px 10vw;
    text-align: center;
    margin: 0 auto;
}

form {
    width: 100%;
    display: block;
    text-align: center;

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
    transition: 300ms;
}

input:hover, select:hover, option:hover {
    cursor: pointer;
    background-color: #494949;
}

input[type="submit"] {
    grid-column: span 2;
}

h1 {
    text-align: center;
    margin-bottom: 20px;
}

</style>