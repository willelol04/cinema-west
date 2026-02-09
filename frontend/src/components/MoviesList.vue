<script setup>
import { RouterLink } from 'vue-router';
import { ref, computed, onMounted } from 'vue';
import MoviesView from '@/views/MoviesView.vue';

const start_ind = ref(0);
const props = defineProps({title: {
        type: String,
        default: 'Movies',
    },
    movies: {
        type: Array,
        default: [
            {
                title: 'Jack reacher 0',
                times: ['22.43', '19.00', '14.00'],
            },
            {
                title: 'Jack reacher 1',
                times: ['22.43', '19.00', '14.00'],
            },
            {
                title: 'Jack reacher 2',
                times: ['22.43', '19.00', '14.00'],
            },
            {
                title: 'Jack reacher 3',
                times: ['22.43', '19.00', '14.00'],
            },
            {
                title: 'Jack reacher 4',
                times: ['22.43', '19.00', '14.00'],
            },
            {
                title: 'Jack reacher 5',
                times: ['22.43', '19.00', '14.00'],
            },
            {
                title: 'Jack reacher 6',
                times: ['22.43', '19.00', '14.00'],
            },
            {
                title: 'Jack reacher 7',
                times: ['22.43', '19.00', '14.00'],
            },
            {
                title: 'Jack reacher 8',
                times: ['22.43', '19.00', '14.00'],
            },
            {
                title: 'Jack reacher 9',
                times: ['22.43', '19.00', '14.00'],
            },
            {
                title: 'Jack reacher 10',
                times: ['22.43', '19.00', '14.00'],
            },
            {
                title: 'Jack reacher 11',
                times: ['22.43', '19.00', '14.00'],
            },
        ],
    },
    limit: {
        type: Number,
        default: 200,
    },
    display: Number,
    showTimes: {
        type: Boolean,
        default: false,
    }
});
    
const visibleMovies = computed(() => {
    if(props.display) {
        const visible = props.movies.slice(start_ind.value * props.display, start_ind.value * props.display + props.display);
        return visible;

    } else { 
        return props.movies;
    }

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
}

const scrollLeft = () => {
    if(canScrollLeft()) { 
        start_ind.value--;
    }

};

const scrollRight = () => {
    if(canScrollRight()) { 
        start_ind.value++;
    }
}

console.log(props.movies);
    
</script>

<template>
    <section>
    <div class="movies-header">
    <h1 class="title">{{ props.title }}</h1>
    <div v-if="movies.length > display" class="scroll">
        <button class="scroll-left scroll-button" :disabled="!canScrollLeft()"  @click="scrollLeft()" ><i class="pi pi-chevron-circle-left" ></i></button>
        <button class="scroll-right scroll-button"  :disabled="!canScrollRight()" @click="scrollRight()" ><i class="pi pi-chevron-circle-right" ></i></button>
    </div>
    </div>
        <TransitionGroup name="list" tag="div" class="movies-container">
        <div class="movie-card" v-for="(movie, index) in visibleMovies" :key="movie">
        <RouterLink :to="`/movie/`+ (movie.id ? movie.id : index) ">
            <img v-if="movie.poster_path && movie.poster_path !== 'None'" :src="`https://image.tmdb.org/t/p/original`+movie.poster_path">
            <img v-else src="../assets/poster_examples/jack2.jpg">
            <h2 class="movie-card-title">{{ movie.title }}</h2>
            <ul class="time-list" v-if="showTimes">
                <li class="time" v-for="time in movie.times">{{ time }}</li>
            </ul>
        </RouterLink>
        </div>
        </TransitionGroup>

    </section>

</template>

<style scoped>
.list-enter-active,
.list-leave-active {
  transition: all 0.5s ease;
}
.list-enter-from,
.list-leave-to {
  opacity: 0;
  transform: translateX(30px);
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
    margin-bottom: 25px;
    margin-top: 40px;
}


section {
    width: 80%;
    text-align: left;
    display: block;
    padding: 20px 10vw;
    margin: 0 auto;
}

.pi {
    font-size: 2rem;
    background-color: #2b2b2b;
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

.movies-container, .movies-grid {
    width: 100%;
    display: grid;
    grid-template-columns: repeat(5, minmax(100px, 1fr));
    margin: 0 auto;
    gap: 30px;
    padding-top: 10px;

}

.movie-card img {
    width: 100%;
    border-radius: 16px;
    border-bottom-left-radius: 0px;
    border-bottom-right-radius: 0px;
    
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

.movie-card {
    background-color: #2d2d2d;
    border-radius: 16px;
    border: 1px solid #404040;
    transition: 300ms;
    position: relative;


}



.movie-card:hover {
    transform: translateY(-5px);
    cursor: pointer;
    box-shadow: 1px 1px 35px 0px rgba(255,255,255,0.75);
    -webkit-box-shadow: 1px 1px 35px 0px rgba(255,255,255,0.75);
    -moz-box-shadow: 1px 1px 35px 0px rgba(255,255,255,0.75);
}


.movie-card p, .movie-card h2 {
    padding: 15px 10px;
    text-align: left;
}

.movie-card h2 {
    text-align: center;
    font-size: 16px;
    bottom: 0;
    width: 100%;
}

.list-move, 
.list-enter-active,
.list-leave-active {
  transition: all 0.5s ease;
}

.list-enter-from,
.list-leave-to {
  transform: translateX(60px);
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

</style>