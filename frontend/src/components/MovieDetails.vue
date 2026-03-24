<script setup>

import { format, formatDistance, formatRelative, subDays } from 'date-fns';
import NavigateBackButton from "@/components/NavigateBackButton.vue";

defineProps({
  movie: {
    type: Object,
    default: {"id": "234", "title": "this is a title", "overview": "this is an overview"},
  },
});
</script>

<template v-if="movie">
  <section
      :style="{
    backgroundImage: `linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)), url(https://image.tmdb.org/t/p/original${movie.backdrop_path})`,
    backgroundSize: 'cover',
    backgroundPosition: 'top',
    backgroundRepeat: 'no-repeat'
    }"
  >
    <NavigateBackButton
        target="/movies"
        text="Go Back to Movies"
    ></NavigateBackButton>

    <div class="movie-container">
      <img
          class="movie-poster"
          :src="(movie.poster_path ? `https://image.tmdb.org/t/p/original`+movie.poster_path : `https://placehold.co/400x600/000000/000000/png`)"
      />

      <div class="right">
        <div class="movie-details">
          <h2 v-if="movie.release_date" class="movie-title">
            {{ movie.title}} ({{ format(movie.release_date, "yyyy")}})
          </h2>
          <div class="movie-info">
            <h3>Release date</h3>
            <span v-if="movie.release_date">
              {{format(movie.release_date, 'yyy.MM.d')}}</span
            ><span v-else>N/A</span>
          </div>
          <div class="movie-info">
            <h3>Length</h3>
            <span v-if="movie.runtime > 0"
            >{{ Math.floor(movie.runtime / 60) }}h
              {{ movie.runtime - Math.floor(movie.runtime / 60)*60 }}min</span
            ><span v-else>N/A</span>
          </div>
          <div
              class="movie-info"
              v-if="movie.genres && movie.genres.length > 0"
          >
            <h3>Genres</h3>
            <span
                v-for="(genre, index) in movie.genres.slice(0, movie.genres.length - 1)"
            >{{ genre.name }} | </span
            ><span>{{movie.genres[movie.genres.length -1].name}}</span>
          </div>
          <div class="movie-info">
            <h3>Rating</h3>
            <span>{{movie.rating ? movie.rating : 'N/A'}}</span>
          </div>
          <div class="movie-info">
            <h3>Language</h3>
            <span>{{ movie.language }}</span>
          </div>
        </div>
        <div class="movie-description">
          <h3>Description</h3>
          <span>{{ movie.overview }}</span>
        </div>
        <div class="movie-screenings">
          <h3>Book tickets</h3>
          <div
              v-if="movie.screenings && movie.screenings.length !== 0"
              class="screenings"
          >
            <RouterLink
                v-for="(screening, ind) in movie.screenings"
                :to="`/booking/`+screening.id"
                :key="screening"
                class="screening"
            ><h3>{{ format(screening.start_time, "HH:mm") }}</h3>
              {{ format(screening.start_time, "EEEE, MMM d") }}</RouterLink
            >
          </div>
          <p v-else>No scheduled screenings for this movie.</p>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
section {
  padding: 20px 200px;
  flex: 1;
}

.movie-container {
  width: 100%;
  margin: 0 auto;
  height: 100%;
  display: flex;
  flex-direction: row;
  justify-content: start;
  gap: 20px;
  align-items: flex-start;
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
  gap: 30px;
}

.screening {
  background-color: var(--secondary-bg);
  color: white;
  padding: 15px;
  border: 3px solid var(--default-border-bg);
  border-radius: 5px;
  transition: 250ms;
  padding: 15px;
  width: 200px;
}

.screening:hover {
  background: white;
  background-color: var(--default-border-bg);
}

.movie-screenings {
  width: 100%;
}

.movie-details h3 {
  opacity: 60%;
}

.movie-title {
  margin-bottom: 10px;
}

.screenings {
  display: flex;
  width: 100%;
  align-items: stretch;
  justify-content: start;
  gap: 20px;
  flex-wrap: wrap;
}

.movie-info {
  margin-bottom: 12px;
}

@media screen and (max-width: 1200px) {
  section {
    padding: 10px;
  }
  .screening {
    width: 120px;
  }
}
@media screen and (max-width: 768px) {
  .movie-container {
    flex-direction: column;
    justify-content: start;
    align-items: center;
  }

  section {
    padding: 50px;
  }

  .movie-container img {
    width: 100%;
  }

  .right {
    gap: 50px;
  }
}
</style>
