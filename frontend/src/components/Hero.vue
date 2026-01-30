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
        const upcomingMoviePromise = await fetch("http://localhost:8000/getupcoming")
        const upcomingMovieObject = await upcomingMoviePromise.json();
        upcomingMovies.value = upcomingMovieObject.results;
        fetchComplete.value = true;
        console.log("successful - ", num);
//        const today = Date.now();
//        const movie_one = Date.parse(upcomingMovies.value[3].release_date);
//        if (today > movie_one) {
//            console.log("movie already out");
//        } else {
//            console.log("movie not out");
//        }
//        
//        console.log(upcomingMovies.value.filter((movie) => Date.parse(movie.release_date) > today))

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
    <img :src="`https://image.tmdb.org/t/p/original`+item.poster_path" height="326" width="auto">
    <div class="right">
        {{ item.title }}
        <br>
        <br>
        {{ format(item.release_date, 'MMMM do yyyy') }}
        <br>
        <br>
        {{ item.overview }}
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


 

</style>

<!--

<template>
    <section>
    <h1>Kommande filmpremiärer:</h1>
    <Timeline class="timeline" :value="upcomingPremieres" layout="horizontal" align="middle">
        <div class="timeline-item">
            
        </div>
        <template #marker="slotProps">
            <RouterLink to="/movie/3">
            <div class="timeline-marker">
            <img :src="slotProps.item.image">
            <p>{{ slotProps.item.title }}</p>
            <p class="premiere">Premiär: {{ slotProps.item.date }}</p>
            </div>
            </RouterLink>
        </template>
        <template #content="slotProps">
        </template>
    </Timeline>
    </section>
</template>

<style scoped>

section {
    width: 100%;
    height: 550px;
    background-image: url('../assets/space.jpg');
    background: linear-gradient(circle, rgba(99, 97, 97, 0.63), rgba(0, 0, 0, 0.5)),
    url('../assets/space.jpg');
    background-repeat: no-repeat;
    background-size: cover;

    text-align: left;
    padding: 20px 200px;
    backdrop-filter: blur(10px)
}

.timeline {
    width: 100%;
    color:white;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.8)

}

p {
    display: block;
    text-align: center;
}

.timeline img {
    display: block;
    width: 250px;
    left: 0;
    transition: 300ms;
}

.premiere {
    color: #e50914d5;
}
.timeline img:hover{
    box-shadow: 2px 2px 61px 0px rgba(245,239,239,0.75);
    -webkit-box-shadow: 2px 2px 61px 0px rgba(245,239,239,0.75);
    -moz-box-shadow: 2px 2px 61px 0px rgba(245,239,239,0.75);
    cursor:pointer;
    transform: translateY(-5px);

}

</style>




-->