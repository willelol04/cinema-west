<script setup>
    import { RouterLink } from 'vue-router';
    import { ref, computed, onMounted } from 'vue';
import MoviesView from '@/views/MoviesView.vue';
    
    const start_ind = ref(0);

    const props = defineProps({
        title: {
            type: String,
            default: 'Movies',
        },
        limit: {
            type: Number,
            default: 200,
        },
        display: {
            type: Number,
            default: 5,
        }
    });
    
    
    const movies = [
        {
            title: 'Jack reacher 0',
        },
        {
            title: 'Jack reacher 1',
        },
        {
            title: 'Jack reacher 2',
        },
        {
            title: 'Jack reacher 3',
        },
        {
            title: 'Jack reacher 4',
        },
        {
            title: 'Jack reacher 5',
        },
        {
            title: 'Jack reacher 6',
        },
        {
            title: 'Jack reacher 7',
        },
        {
            title: 'Jack reacher 8',
        },
        {
            title: 'Jack reacher 9',
        },
        {
            title: 'Jack reacher 10',
        },
        {
            title: 'Jack reacher 11',
        },
    ];
    
    
    const visibleMovies = computed(() => {
        const slice = movies.slice(start_ind.value * props.display, start_ind.value * props.display + props.display);
        return slice;

    });
    
    const canScrollLeft = () => {
        if(start_ind.value > 0) {
        return true;

        }
        return false;
    };

    const canScrollRight = () => {
        if((start_ind.value + 1) * props.display < movies.length) {
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
    
    
    
</script>

<template>
    <section>
    <div class="movies-header">
    <h1 class="title">{{ props.title }}</h1>
    <div v-if="movies.length > display" class="scroll">
        <button :class="[!canScrollLeft() ? 'disabled-scroll-button': '', 'scroll-left']"  @click="scrollLeft()" ><i class="pi pi-chevron-circle-left" ></i></button>
        <button :class="[!canScrollRight() ? 'disabled-scroll-button': '', 'scroll-right']"  @click="scrollRight()" ><i class="pi pi-chevron-circle-right" ></i></button>
    </div>
    </div>
    <div class="movies-container">
        <div class="movie-card" v-for="(movie, index) in visibleMovies" :key="index">
        <RouterLink :to="`/movie/`+ index ">
            <img src="../assets/poster_examples/jack2.jpg">
            <h2>{{ movie.title }}</h2>
        </RouterLink>
        </div>

    </div>

    </section>

</template>

<style scoped>


.movies-header {
    width: 100%;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    vertical-align: middle;
    margin-bottom: 50px;
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

.disabled-scroll-button {
    opacity: 50%;
}
.disabled-scroll-button:hover {
    cursor: default;
}

.movies-container {
    width: 100%;
    display: grid;
    margin: 0 auto;
    grid-template-columns: repeat(5, minmax(100px, 1fr));
    gap: 30px;
    overflow: auto;
    padding-top: 10px;

}

.movie-card img {
    width: 100%;
    border-radius: 10px;
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
    border-radius: 10px;
    transition: 300ms;
    border: 1px solid #404040;
    border-bottom: none;

}



.movie-card:hover {
    transform: translateY(-10px);
    cursor: pointer;
}


.movie-card p, .movie-card h2 {
    padding: 15px 10px;
    text-align: left;
}

.movie-card h2 {
    text-align: center;
}

</style>