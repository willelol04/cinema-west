<script setup>
import { format, formatDistance, formatRelative, subDays } from 'date-fns';
import { RouterLink } from 'vue-router';
import { ref, computed, onMounted } from 'vue';
import MoviesView from '@/views/MoviesView.vue';
import MovieDetails from './MovieDetails.vue';
import {addMovie, deleteMovie} from '../api/movies'
import {useAuth0} from "@auth0/auth0-vue";

'../use/useToast.js';
const { isAuthenticated, isLoading, error, getAccessTokenSilently } = useAuth0();
import {useAppToast} from "@/use/useToast.js";
const {successToast, errorToast} = useAppToast();

const start_ind = ref(0);
const fetchComplete = ref(false);

const emit = defineEmits(["add", "delete"])

const props = defineProps({
  title:  String,
  movies: Array,
  action: String,
  limit: {
    type: Number,
    default: 200,
  },
  display: {
    type: Number,
    default: 5,
  },
  showTimes: {
    type: Boolean,
    default: false,
  }
});

const visibleMovies = computed(() => {
  const visible = props.movies.slice(start_ind.value * props.display, start_ind.value * props.display + props.display);
  return visible;

});

const canScrollLeft = () => {
  if(start_ind.value > 0) {
    return true;

  }
  return false;
};

const canScrollRight = () => {
  if((start_ind.value + 1) * props.display < props.movies.length) {
    return true;
  }
  return false;
};

const scrollLeft = () => {
  if(canScrollLeft()) {
    start_ind.value--;
  }

};

const scrollRight = () => {
  if(canScrollRight()) {
    start_ind.value++;
  }
};


const addMovieUpdate = async (movie) => {
  try {
    if (confirm("Add this movie?")) {
      const token = await getAccessTokenSilently();
      await addMovie({id: movie.id}, token);
      emit('add', movie)
      successToast("Movie added to database")
    }
  } catch (e) {
    errorToast("Error adding movie to database. Try refreshing the page.")
  }

};

const deleteMovieUpdate = async (movie) => {
  try {
    if(confirm("Delete this movie?")) {
      const token = await getAccessTokenSilently();
      await deleteMovie({id: movie.id}, token);
      emit('delete', movie);
      successToast("Movie deleted from database.")
    }
  } catch (e) {
    errorToast("Error deleting movie from database. Try refreshing the page.")
  }

};
</script>

<template>
  <section>
    <div class="movies-header">
      <h1 class="title">{{ props.title ? props.title : '' }}</h1>
      <div v-if="movies.length > display" class="scroll">
        <button
            class="scroll-left scroll-button"
            :disabled="!canScrollLeft()"
            @click="scrollLeft()"
        >
          <i class="pi pi-chevron-circle-left"></i>
        </button>
        <button
            class="scroll-right scroll-button"
            :disabled="!canScrollRight()"
            @click="scrollRight()"
        >
          <i class="pi pi-chevron-circle-right"></i>
        </button>
      </div>
    </div>
    <TransitionGroup name="list" tag="div" class="movies-container">
      <div
          class="movie-card"
          v-for="(movie, index) in visibleMovies"
          :key="movie.id"
      >
        <img
            class="movie-poster"
            :src="(movie.poster_path ? `https://image.tmdb.org/t/p/original`+movie.poster_path : `https://placehold.co/400x600/000000/000000/png`)"
        />
        <div class="movie-details">
          <h2>{{ movie.title }}</h2>
          <p v-if="movie.overview">{{ movie.overview.slice(0, 300) }}...</p>
          <ul class="time-list" v-if="showTimes">
            <li class="time" v-for="time in movie.times">{{ time }}</li>
          </ul>
        </div>
        <div class="movie-actions">
          <button
              @click="addMovieUpdate(movie)"
              v-if="props.action=='add'"
              class="movie-action movie-add"
          >
            <i class="pi pi-plus-circle"></i>Lägg till
          </button>
          <button
              @click="deleteMovieUpdate(movie)"
              v-else
              class="movie-action movie-remove"
          >
            <i class="pi pi-trash"></i>Ta bort
          </button>
        </div>
      </div>
    </TransitionGroup>
  </section>
</template>

<style scoped>
.pi-image {
  text-align: center;
  vertical-align: center;
  margin-top: 50px;
}


.list-enter-active,
.list-leave-active {
  transition: all 0.5s ease;
}
.list-enter-from,
.list-leave-to {
  opacity: 0;
  transform: translateX(30px);
}

.movie-actions {
  border-left: 1px solid var(--default-border-bg);
  text-align: center;
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
}

.movie-action {
  width: 100%;
  height: 100%;
}

.time {
  display: inline-block;
  margin-right: 20px;
}

.movies-header {
  width: 100%;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  vertical-align: middle;
  margin-top: 24px;
  margin-bottom: 24px;
}

section {
  width: 100%;
  text-align: left;
  display: block;
  margin: 0 auto;
}

.pi {
  font-size: 2rem;
  background-color: none;
  color: white;
  border-radius: 100%;
  font-weight: 100;
}

.scroll-left {
  margin-right: 8px;
}

.scroll button:disabled {
  cursor: default;
  opacity: 50%;
}

.movies-container,
.movies-grid {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 0 auto;
  gap: 30px;
  padding-top: 10px;
}

.link {
  background-color: #e50914;
  color: white;
  width: 100%;
  display: block;
  margin: 0 auto;
  padding: 15px;
  border-radius: 10px;
  transition: 300ms;
}

.link:hover {
  background-color: rgb(233, 222, 222);
  color: #e50914;
}

.movie-card:hover {
  transform: translateY(-10px);
  cursor: default;
}

.movie-card p,
.movie-card h2 {
  padding: 15px 10px;
  text-align: left;
}

.movie-card h2 {
  text-align: left;
}

.list-move,
.list-enter-active,
.list-leave-active {
  transition: all 0.5s ease;
}

.list-enter-from,
.list-leave-to {
  opacity: 0;
  transform: translateX(30px);
}

/* ensure leaving items are taken out of layout flow so that moving
   animations can be calculated correctly. */
.list-leave-active {
  visibility: hidden;
  transition: none;
}

.scroll-button i {
  transition: 300ms;
  color: white;
}

.movie-details {
  padding: 20px;
  text-align: left;
}

.movie-add i {
  color: green;
  display: block;
}

.movie-remove i {
  color: var(--selected-default-color);
  display: block;
}

.movie-actions,
.movie-action i {
  transition: 300ms;
  border-radius: inherit;
  border-bottom-left-radius: 0px;
  border-top-left-radius: 0px;
}

.movie-actions:hover {
  background-color: rgb(112, 109, 109);
}

.movie-card {
  background-color: var(--secondary-bg);
  border-radius: 10px;
  border: 1px solid var(--default-border-bg);
  transition: 300ms;
  width: 100%;
  display: grid;
  grid-template-columns: 1fr 7fr 1fr;
  grid-template-rows: auto;
}

.movie-poster {
  border-radius: 10px;
  border-top-right-radius: 0px;
  border-bottom-right-radius: 0px;
  display: block;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.scroll {
  display: flex;
  flex-direction: row;
  flex-wrap: nowrap;
  align-items: center;
}
@media screen and (max-width: 768px) {


  .movie-details h2 {
    text-align: center;
  }


  .movie-poster {
    height: 100%;
  }

  .movie-details {
    padding: 5px;
  }

  .movie-actions {
    padding: 10px;

  }

  .movie-action i {
    font-size: 24px;
  }

  .movies-header {
    padding: 0;
    margin-left: auto;
    margin-right: auto;
  }
}
</style>
