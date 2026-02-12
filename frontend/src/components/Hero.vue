<script setup>
import { format, formatDistance, formatRelative, subDays } from 'date-fns';
import { RouterLink } from 'vue-router';
import { onMounted, ref } from 'vue';
import Timeline from 'primevue/timeline';
import Carousel from 'primevue/carousel';
import BeatLoader from 'vue-spinner/src/BeatLoader.vue';

const goToMovie = () => {
    window.location.href = "/movie/3";
}

const upcomingMovies = ref([]);
const fetchComplete = ref(false);
    

    
onMounted(async function fetchUpcoming(numbers_tried = 1) {
    const num = numbers_tried;
    try {
        const upcomingMoviePromise = await fetch("http://localhost:8000/tmdb/movies/upcoming")
        const upcomingMovieObject = await upcomingMoviePromise.json();
        upcomingMovies.value = upcomingMovieObject.results;
        console.log(upcomingMovies.value);
        fetchComplete.value = true;
        console.log("successful - ", num);
    } catch(e) {
        console.log(e);
        setTimeout(() => {fetchUpcoming(1+num)}, 20000);
        console.log("failed - ", num);
    } finally {
        console.log("quit");
    }
})

</script>

<template>
    <section>
    <h1 style="text-align: center;">Coming soon</h1>
 <Carousel3d v-if="fetchComplete" class="carousel" :space="600" :display="3" :autoplay-timeout="10000" :autoplay="true" :controls-visible="false" :onMainSlideClick="goToMovie" :clickable="true" :width="500" :height="326">
    <Slide v-for="(item, ind) in upcomingMovies" class="slide" :index="ind">
    <div class="upcoming-movie">
    <img v-if="item.poster_path" :src="`https://image.tmdb.org/t/p/original`+item.poster_path" height="326" width="auto">
    <img v-else src="../assets/poster_examples/jack1.jpg" height="326" width="auto">
    <div class="right">
        <h3 class="upcoming-movie-title">{{ item.title }}</h3>
        <br>
        <h4 class="upcoming-movie-date">{{ format(item.release_date, 'MMMM do yyyy') }}</h4>
        <br>
        <p class="upcoming-movie-overview">{{ item.overview.length < 200 ? item.overview : item.overview.slice(0,200)+"..." }} </p>
    </div>
    </div>
    </Slide>


  </Carousel3d>
  <BeatLoader class="fetch-loading" :color="'#bdc7bf'" v-else />
  </section>
</template>

<style scoped>


.fetch-loading {
    margin: 0 auto;
    text-align: center;
    padding: 100px;
}
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

</style>
