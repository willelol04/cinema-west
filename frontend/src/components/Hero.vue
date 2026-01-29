<script setup>
    import { RouterLink } from 'vue-router';
    import { onMounted, ref } from 'vue';
    import Timeline from 'primevue/timeline';
    import Carousel from 'primevue/carousel';
    
    const upcomingPremieres = [
        {
            title: "Star wars: the last jedi",
            description: 'Lorem ipsum ipsum, dolor sit atmuet.Lorem ipsum ipsum, dolor sit atmuet.Lorem ipsum ipsum, dolor sit atmuet.Lorem ipsum ipsum, dolor sit atmuet.Lorem ipsum ipsum, dolor sit atmuet.',
            date: '2024-01-01',
            image: './src/assets/poster_examples/jack1.jpg',

        },
        {
            title: "Star wars: the last jedi",
            description: 'Lorem ipsum ipsum, dolor sit atmuet.Lorem ipsum ipsum, dolor sit atmuet.Lorem ipsum ipsum, dolor sit atmuet.Lorem ipsum ipsum, dolor sit atmuet.Lorem ipsum ipsum, dolor sit atmuet.',
            date: '2024-01-01',
            image: './src/assets/poster_examples/starwars.png',

        },
        {
            title: "Star wars: the last jedi",
            description: 'Lorem ipsum ipsum, dolor sit atmuet.Lorem ipsum ipsum, dolor sit atmuet.Lorem ipsum ipsum, dolor sit atmuet.Lorem ipsum ipsum, dolor sit atmuet.Lorem ipsum ipsum, dolor sit atmuet.',
            date: '2024-01-01',
            image: './src/assets/poster_examples/starwars.png',

        },
    ];
    

    const goToMovie = () => {
        window.location.href = "/movie/3";
    }
    
    const upcomingMovies = ref([]);
    const fetchComplete = ref(false);
    
    
onMounted(async function fetchUpcoming() {
    const upcomingMoviePromise = await fetch("http://localhost:8000/getupcoming")
    const upcomingMovieObject = await upcomingMoviePromise.json();
    upcomingMovies.value = upcomingMovieObject.results.slice(0,5);
    console.log(upcomingMovies.value[0])
    console.log(upcomingMovies.value[1].title)
    fetchComplete.value = true;

})



    


</script>

<template>
    <section>
    <h1 style="text-align: center;">Kommande premiärer:</h1>
 <Carousel3d v-if="fetchComplete" class="carousel" :space="600" :display="3" :controls-visible="false" :onMainSlideClick="goToMovie" :clickable="true" :width="500" :height="326">
    <Slide v-for="(item, ind) in upcomingMovies" class="slide" :index="ind">
    <div class="upcoming-movie">
    <img :src="`https://image.tmdb.org/t/p/original`+item.poster_path" height="326" width="auto">
    <div class="right">
        {{ item.title }}
        <br>
        <br>
        {{ item.release_date }}
        <br>
        <br>
        {{ item.overview }}
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