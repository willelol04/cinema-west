<script setup>
import { format, formatDistance, formatRelative, subDays } from 'date-fns';
import { RouterLink, useRouter } from 'vue-router';
import { onMounted, ref } from 'vue';
import Timeline from 'primevue/timeline';
import Carousel from 'primevue/carousel';
import BeatLoader from 'vue-spinner/src/BeatLoader.vue';
import router from '@/router';

const Router = useRouter();

const props = defineProps({
    upcomingMovies: Array,
});
    
const goToMovie = (slide) => {
    const movie_id = props.upcomingMovies[slide.index].id;
    Router.push(`/movies/${movie_id}`);
}



const carousel = ref({
    space: 600,
    display: 3,
    controlsVisible: false,
    clickable: true,
    width: 550,
    height: 326,
});



const updateColumns = () => {
  const width = window.innerWidth;

  if (width < 768) {
    carousel.value = {
    space: 200,
    display: 1,
    controlsVisible: true,
    clickable: false,
    width: 217,
    height: 326,
    };
  }
  else carousel.value = {
    space: 600,
    display: 3,
    controlsVisible: false,
    clickable: true,
    width: 500,
    height: 326,
    
  };
    
}

onMounted(() => {
  updateColumns();
  window.addEventListener("resize", updateColumns);
});

</script>

<template>
    <section>
    <h1 style="text-align: center;">Coming soon</h1>
 <Carousel3d class="carousel" :space="carousel.space" :display="carousel.display" :autoplay-timeout="10000" :autoplay="true" :controls-visible="carousel.controlsVisible" :onMainSlideClick="goToMovie" :clickable="carousel.clickable" :width="carousel.width" :height="carousel.height">
    <Slide v-for="(movie, ind) in props.upcomingMovies" class="slide" :index="ind">
    <div class="upcoming-movie">
    <img :src="(movie.poster_path ? `https://image.tmdb.org/t/p/original`+movie.poster_path : `https://placehold.co/400x600/000000/000000/png`)" height="326" width="auto">
    <div class="right">
        <h3 class="upcoming-movie-title">{{ movie.title }}</h3>
        <br>
        <h4 class="upcoming-movie-date">{{ format(movie.release_date, 'MMMM do yyyy') }}</h4>
        <br>
        <p class="upcoming-movie-overview">{{ movie.overview.length < 200 ? movie.overview : movie.overview.slice(0,200)+"..." }} </p>
    </div>
    </div>
    </Slide>


  </Carousel3d>
  </section>
</template>

<style scoped>


section {
    padding: 20px 10vw;
}

.slide, .current {
    background-color: rgba(43, 43, 43, 0.753);
    border-radius: 5px;
    transition: 300ms;
}

.slide:hover {
    cursor:pointer;
}

.upcoming-movie {
    display: flex;
    flex-direction: row;
    justify-content: space-between;

}


.right {
    padding: 20px;
}


 
.upcoming-movie-date {
    opacity: 80%;
    font-weight: 200;
}


@media screen and (max-width: 768px) {
    section {
        padding: 0;
    }
}



</style>
