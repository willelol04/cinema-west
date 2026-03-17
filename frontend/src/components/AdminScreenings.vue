<script setup>
import MoviesList from './MoviesList.vue';
import { ref, onMounted, reactive } from 'vue';
import {useAuth0} from "@auth0/auth0-vue";
import { getMoviesAll } from '@/api/movies';
import { getTheatres } from '@/api/theatres';
import { addScreening } from '@/api/screenings';
import router from '@/router';
import BeatLoader from "vue-spinner/src/BeatLoader.vue";

import {format} from 'date-fns'
const { user, isAuthenticated, isLoading, error, getAccessTokenSilently } = useAuth0();
    
const movieResults = ref([]);
const theatreResults = ref([]);
const fetchComplete = ref(true);
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

onMounted(async () => {fetchComplete.value = false; await fetchMovies(); await fetchTheatres(); fetchComplete.value = true });
</script>


<template>
    <div class="add-screening" >
    <h1>New Screening</h1>
    <form v-if="fetchComplete" method="POST" @submit.prevent="addScreeningUpdate">
        <label for="movies">Movie:</label>
      <span>
        <select v-model="screening.movie_id" id="movies" required>
            <option :value="null" selected>Select a Movie</option>
            <option v-for="(movie,ind) in movieResults" :value="movie.id">{{ movie.title }}</option>
        </select>

      </span>


        <label for="time">Time:</label>
        <span>
        <input type="datetime-local" v-model="start_time" id="time">
        <button type="button" @click="addStartTime()">Add time</button>
        </span>
        <span>
        <div class="screening_times">
            <h3>Added times:</h3>
            <div class="time" v-for="(time, ind) in screening.start_times"><button type="button" @click="deleteTime(ind)">{{ format(time, 'yyyy-MM-dd, HH:mm') }}<i class="pi pi-times"></i></button></div>
        </div>
        </span>

        <label for="theatres">Theatre:</label>
      <span>
        <select v-model="screening.theatre_id" id="theatres" required>
            <option :value="null" selected>Select a Theatre</option>
            <option v-for="theatre in theatreResults" :value="theatre.id">{{ theatre.name }}</option>
        </select>
      </span>
        <span>
            <input type="submit" value="Add screening">
            <input type="button" @click="resetScreening" value="Reset">
        </span>
    </form>
    <BeatLoader class="fetch-loading" :color="'#bdc7bf'" v-else />

    </div>

</template>
<style scoped>

.add-screening {
    text-align: center;
    margin: 0 auto;
}

form {
    width: 100%;
    display: block;
    text-align: left;

}

.time {
  display: inline-block;
}

.pi {
  margin-left: 20px;
}

label {
  display: block;
}

input, select, option, button {
    border: 1px solid var(--default-border-bg);
    padding: 10px;
    border-radius: 3px;
    background-color: var(--secondary-bg);
    transition: 300ms;
    width: 100%;
}

input:hover, select:hover, button:hover, option:hover {
    cursor: pointer;
    background-color: #494949;
}

span {
  display: block;
  width: 100%;
  margin-bottom: 32px;
}

span > input, span > button {
  width: 50%;
}

label, h3 {
  font-size: 24px;
  font-weight: 200;
}

</style>