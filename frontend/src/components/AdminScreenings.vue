<script setup>
import MoviesList from './MoviesList.vue';
import { ref, onMounted, reactive } from 'vue';
import {useAuth0} from "@auth0/auth0-vue";
import { getMoviesAll } from '@/api/movies';
import { getTheatres } from '@/api/theatres';
import { addScreening } from '@/api/screenings';
import router from '@/router';

const { user, isAuthenticated, isLoading, error, getAccessTokenSilently } = useAuth0();
    
const movieResults = ref([]);
const theatreResults = ref([]);
const start_time = ref(null)
const screening = reactive({
    movie_id: null,
    theatre_id: null,
    start_times: [],

})

const fetchMovies = async () => {
    try {
        movieResults.value = await getMoviesAll();
    } catch (e) {
        console.log(e)
    }
}

const fetchTheatres = async () => {
    try {
        const token = await getAccessTokenSilently();
        theatreResults.value = await getTheatres(token);
    } catch(e) {
        console.log(e);
    }
}

const resetScreening = () => {
  screening.movie_id = null;
  screening.theatre_id = null;
  screening.start_times = [];
  start_time.value = null;
}

const addScreeningUpdate = async () => {
    if (screening.start_times.length > 0 && screening.movie_id !== null && screening.theatre_id !== null) {
        try {
            const token = await getAccessTokenSilently();
            await addScreening(screening, token);
            alert("Screening(s) added.");
            resetScreening();

        } catch(e) {
            console.log(e);
        }
    } 

}

const addStartTime = () => {
    if (!screening.start_times.includes(start_time.value)) {
        screening.start_times.push(start_time.value);
    }
}

const deleteTime = (ind) => {
    screening.start_times.splice(ind, 1);
}

onMounted(fetchMovies);
onMounted(fetchTheatres);
</script>


<template>
    <div class="add-screening">
    <form method="POST" @submit.prevent="addScreeningUpdate">
    <h1>New Screening</h1>
        <div class="grid">
        <label for="movies">Movie:</label>
        <select v-model="screening.movie_id" id="movies" required>
            <option :value="null" selected>Select a Movie</option>
            <option v-for="(movie,ind) in movieResults" :value="movie.id">{{ movie.title }}</option>
        </select>


        <label for="time">Time:</label>
        <span>
        <input type="datetime-local" v-model="start_time" id="time">
        <button type="button" @click="addStartTime()">Add time</button>
        <div class="screening_times">
            <div class="time" v-for="(time, ind) in screening.start_times">{{ time }}<button type="button" @click="deleteTime(ind)"><i class="pi pi-times"></i></button></div>
        </div>

        </span>
        <label for="theatres">Theatre:</label>
        <select v-model="screening.theatre_id" id="theatres" required>
            <option :value="null" selected>Select a Theatre</option>
            <option v-for="theatre in theatreResults" :value="theatre.id">{{ theatre.name }}</option>
        </select>
          <span class="buttons">
            <input type="submit" value="Add screening">
            <input type="button" @click="resetScreening" value="Reset">
          </span>
        </div>
    </form>
        
    </div>
    
</template>
<style scoped>

.add-screening {
    width: 60%;
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
    text-align: left;
}

input, select, option, button {
    border: 1px solid var(--default-border-bg);
    padding: 10px;
    border-radius: 3px;
    background-color: var(--secondary-bg);
    transition: 300ms;
}

input:hover, select:hover, button:hover, option:hover {
    cursor: pointer;
    background-color: #494949;
}

.buttons {
    grid-column: span 2;
}

h1 {
    text-align: center;
    margin-bottom: 20px;
}

span > input, span > button {
    width: 50%;
}


</style>