<script setup>
import MoviesList from './MoviesList.vue';
import { ref, onMounted, reactive } from 'vue';
import {useAuth0} from "@auth0/auth0-vue";
import { getMoviesAll } from '@/api/movies';
import { getTheatres } from '@/api/theatres';
import { addScreening } from '@/api/screenings';
import router from '@/router';
import BeatLoader from "vue-spinner/src/BeatLoader.vue";

import {useAppToast} from "@/use/useToast.js";
const {successToast, errorToast} = useAppToast();

import {format} from 'date-fns'
import {authenticatedFetch} from "@/api/general.js";
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
    errorToast("Error fetching movies. Try refreshing the page.")
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
const fetchScreenings = async () => {
  try {
    const token = await getAccessTokenSilently();
    scree.value = await authenticatedFetch(token);
  } catch(e) {
    errorToast("Error fetching screenings. Try refreshing the page.")
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
      successToast("Screening added to database.")

    } catch(e) {
      console.log(e);
      errorToast("Error adding screening. Try refreshing the page.")
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

</template>
<style scoped>

</style>

