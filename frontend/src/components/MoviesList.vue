<script setup>
import { RouterLink } from 'vue-router';
import { ref, computed, onMounted } from 'vue';
import MoviesView from '@/views/MoviesView.vue';

import Sort from '@/components/Sort.vue';

const emit = defineEmits(['update'])

const start_ind = ref(0);
const showScroll = ref(null);

const props = defineProps({
    title: String,
    movies: Array,
    limit: {
        type: Number,
        default: 200,
    },
    scroll: {
        type: Boolean,
        default: false,
    },
    showTimes: {
        type: Boolean,
        default: false,
    }
});

const columns = ref(6);

const updateColumns = () => {
  const width = window.innerWidth;

  if (width < 400) columns.value = 1;
  else if (width < 600) columns.value = 2;
  else if (width < 800) columns.value = 3;
  else if (width < 1000) columns.value = 4;
  else if (width < 1500) columns.value = 5;
  else columns.value = 6;

}

onMounted(() => {
  updateColumns();
  window.addEventListener("resize", updateColumns);
});

const visibleMovies = computed(() => {
    console.log(props.movies.length, columns.value)
    if(props.movies.length > columns.value && props.scroll) {
        const visible = props.movies.slice(start_ind.value * columns.value, start_ind.value * columns.value + columns.value);
        showScroll.value = true;
        return visible;

    } else { 
        showScroll.value = false;
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
    if((start_ind.value + 1) * columns.value < props.movies.length) {
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
    <h1 v-if="props.title" class="title">{{ props.title }}</h1>
    <div v-if="props.scroll && showScroll === true" class="scroll">
        <button class="scroll-left scroll-button" :disabled="!canScrollLeft()"  @click="scrollLeft()" ><i class="pi pi-chevron-circle-left" ></i></button>
        <button class="scroll-right scroll-button"  :disabled="!canScrollRight()" @click="scrollRight()" ><i class="pi pi-chevron-circle-right" ></i></button>
    </div>
    </div>
        <TransitionGroup name="list" tag="div" :style="`grid-template-columns: repeat(${columns}, minmax(100px, 1fr));`" class="movies-container">
        <div class="movie-card" v-for="(movie, index) in visibleMovies" :key="movie">
        <RouterLink class="movie-link" :to="`/movies/`+ (movie.id ? movie.id : index) ">
            <img :src="(movie.poster_path ? `https://image.tmdb.org/t/p/original`+movie.poster_path : `https://placehold.co/400x600/000000/000000/png`)">
            <h2 class="movie-card-title">{{ movie.title }}</h2>
            <ul class="time-list" v-if="showTimes">
                <li class="time" v-for="time in movie.times">{{ time }}</li>
            </ul>
        </RouterLink>
        </div>
        </TransitionGroup>
      <div v-if="movies?.length === 0" class="empty">No results were found</div>

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


.placeholder-img {
    width: 100%;
    text-align: center;
    i {
        font-size: 5rem;
    }
}



.time {
    display: inline-block;
    margin-right: 20px;

}

.movie-link {
    width: 100%;
    height: 100%;
    display: block;
}
.movies-header {
    width: 100%;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    vertical-align: middle;
}


section {
    text-align: left;
    display: block;
    margin: 0 auto;
    width: 100%;
}

.pi {
    font-size: 2rem;
    background-color: var(--primary-bg);
    color: var(--text-default-color);
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
    display: grid;
    grid-template-columns: repeat(5, minmax(100px, 1fr));
    margin: 0 auto;
    gap: 30px;
    padding-top: 10px;
    width: 100%;

}

.movie-card img {
    width: 100%;
    border-radius: 16px;
    border-bottom-left-radius: 0px;
    border-bottom-right-radius: 0px;
    
}

.link {
    background-color: var(--selected-default-color);
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
    background-color: var(--secondary-bg);
    border: 1px solid var(--default-border-bg);
    border-radius: 16px;
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
    color: var(--text-default-color);
}

@media only screen and (max-width: 1208px) {
    section {
        width: 100%;
        padding: 10px;
    }

    
}
</style>