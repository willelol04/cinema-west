<script setup>
import { ref, onMounted, reactive } from 'vue';
import { getMoviesAll } from '@/api/movies';
import { getTheatres } from '@/api/theatres';
import { addScreening, deleteScreening } from '@/api/screenings';
import {useAuth0} from "@auth0/auth0-vue";
import {useRoute} from 'vue-router';
import BeatLoader from "vue-spinner/src/BeatLoader.vue";
import {format} from 'date-fns';
import {useAppToast} from "@/use/useToast.js";
import Search from '@/components/Search.vue'


const route = useRoute();
const {successToast, errorToast} = useAppToast();

import {normalFetch} from "@/api/general.js";
const { user, isAuthenticated, isLoading, error, getAccessTokenSilently } = useAuth0();

const movieResults = ref([]);
const displayForm = ref(false)
const screeningResults = ref(null);
const theatreResults = ref([]);
const fetchComplete = ref(false);
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
    errorToast("Error fetching movies. Try refreshing the page.")
  }
}

const fetchScreenings = async () => {
  try {
    fetchComplete.value = false;
    const searchParams = new URLSearchParams();
    if (route.query.q) {
      searchParams.append('title', route.query.q);
    }
    screeningResults.value = await normalFetch(`/api/screenings?${searchParams}`);
  } catch (e) {
    errorToast("Error fetching screenings. Try refreshing the page.")
  } finally {
    fetchComplete.value = true;
  }
}

const fetchTheatres = async () => {
  try {
    const token = await getAccessTokenSilently();
    theatreResults.value = await getTheatres(token);
  } catch(e) {
    errorToast("Error fetching theatres. Try refreshing the page.")
  }
}

const resetScreening = () => {
  screening.movie_id = null;
  screening.theatre_id = null;
  screening.start_times = [];
  start_time.value = null;
  displayForm.value = false;
}

const addScreeningUpdate = async () => {
  if (screening.start_times.length > 0 && screening.movie_id !== null && screening.theatre_id !== null) {
    try {
      const token = await getAccessTokenSilently();
      await addScreening(screening, token);
      resetScreening();
      await fetchScreenings();
      successToast("Screening added to database.")

    } catch(e) {
      errorToast("Error adding screening. Try refreshing the page.")
    }
  }
}

const handleDeleteScreening = async (screening) => {
    if(confirm("Do you want to delete this screening?")) {
      try {
        const token = await getAccessTokenSilently();
        await deleteScreening(screening, token);
        successToast("Screening deleted from database.");
        screeningResults.value = screeningResults.value.filter(
            s => s.id !== screening.id
        );

      } catch(e) {
        errorToast("Error deleting screening. Try refreshing the page.");
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

onMounted(async () => {fetchComplete.value = false; await fetchMovies(); await fetchTheatres(); await fetchScreenings(); fetchComplete.value = true });
</script>

<template>
  <div class="screenings">

    <h1>Movie Screenings</h1>
    <Search
        :header="`Search screenings by movie title`"
        :searchFunction="fetchScreenings"
    />
    <button class="add-screening-btn" @click="displayForm = true"><i class="pi pi-plus-circle"></i> Add screening</button>
    <table  v-if="fetchComplete" class="screenings-table">
      <thead>
      <tr>
        <th class="th-movie">Movie</th>
        <th class="th-date">Date</th>
        <th class="th-time">Time</th>
        <th class="th-theatre">Theatre</th>
        <th class="th-price">Ticket price</th>
        <th class="th-delete"></th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="(screening, ind) in screeningResults" :key="screening.id">
        <td class="td-movie">{{screening.movie.title}}</td>
        <td class="td-date">{{format(screening.start_time, 'yyyy-MM-dd')}}</td>
        <td class="td-time">{{format(screening.start_time, 'HH:mm')}}</td>
        <td class="td-theatre">{{screening.theatre.name}}</td>
        <td class="td-price">100 SEK</td>
        <td class="td-delete"><button @click="handleDeleteScreening(screening)">Delete</button></td>
      </tr>
      </tbody>
    </table>
    <BeatLoader class="fetch-loading" :color="'#bdc7bf'" v-else/>
    <div v-if="displayForm" class="add-screening">
      <form
          v-if="fetchComplete"
          @submit.prevent="addScreeningUpdate"
      >
        <h1>New Screening</h1>
        <div class="form-row">
          <label for="movies">Movie:</label>
        <select v-model="screening.movie_id" id="movies" required>
          <option :value="null" selected>Select a Movie</option>
          <option v-for="(movie,ind) in movieResults" :value="movie.id" :key="movie.id">
            {{ movie.title }}
          </option>
        </select>
      </div>

        <div class="form-row">
          <label for="time">Time:</label>
        <input type="datetime-local" v-model="start_time" id="time" />
        <button type="button" @click="addStartTime()">Add time</button>
      </div>
        <div class="form-row">
          <h3>Added times:</h3>
          <div class="time" v-for="(time, ind) in screening.start_times" :key="time">
            <button type="button" class="time-btn" @click="deleteTime(ind)">
              {{format(time, 'yyyy-MM-dd HH:mm')}}<i class="pi pi-times"></i>
            </button>
          </div>
        </div>

        <div class="form-row">
        <label for="theatres">Theatre:</label>
        <select v-model="screening.theatre_id" id="theatres" required>
          <option :value="null" selected>Select a Theatre</option>
          <option v-for="theatre in theatreResults" :value="theatre.id" :key="theatre.id">
            {{ theatre.name }}
          </option>
        </select>
      </div>
        <div class="form-row">
        <input type="submit" value="Submit" />
        <input type="button" @click="resetScreening" value="Cancel" />
      </div>
      </form>
    </div>

  </div>
</template>
<style scoped>


.add-screening {
  text-align: center;
  margin: 0 auto;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  position: fixed;
  z-index: 1000;
  background: rgba(0, 0, 0, 0.9);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;

}

.add-screening > form {
  width: 600px;
  top: 50%;
  margin: 0 auto;
  display: block;
  text-align: left;
  background-color: var(--secondary-bg);
  padding: 50px;
  border-radius: 10px;
}

.time {
  display: inline-block;
}


label {
  display: block;
}

input,
select,
option,
button {
  border: 1px solid var(--default-border-bg);
  padding: 10px;
  border-radius: 3px;
  background-color: var(--secondary-bg);
  transition: 300ms;
  width: 100%;
}

input:hover,
select:hover,
button:hover,
option:hover {
  cursor: pointer;
  background-color: #494949;
}

.form-row {
  display: block;
  width: 100%;
  margin-top: 16px;
}

 input,
 button {
  width: 50%;
}

label,
h3 {
  font-size: 24px;
  font-weight: 200;
}

.screenings-table {
  width: 100%;
  box-sizing: border-box;
  background-color: var(--main-bg);
  min-height: 100px;
  text-align: left;
  border-collapse: separate;
  border-spacing: 0;
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid var(--default-border-bg);
  margin: 0 auto;
}

td {
  background-color: var(--secondary-bg);
  padding: 10px;
}

th {
  padding: 10px;

}

thead {
  position: sticky;
  top: 0;
}

tr {
  background-color: var(--primary-bg);
  border-bottom: 1px solid white;
}

.screenings > button {
  width: fit-content;
  margin-top: 24px;
  margin-bottom: 24px;
  i {
    vertical-align: middle;
    margin: 0;
    padding: 0;
  }
}

h1 {
  display: block;
  margin-top: 24px;
  margin-bottom: 24px;
}



@media screen and (max-width: 1200px) {
  .td-theatre, .th-theatre, .td-price, .th-price {
    display: none;
  }
}

@media screen and (max-width: 768px) {

  .add-screening > form {
    width: 90%;

  }


}

.add-screening-btn {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  align-items: center;
  gap: 5px;
  justify-content: space-between;
}

.time-btn {
  width: 100%;
}

</style>
