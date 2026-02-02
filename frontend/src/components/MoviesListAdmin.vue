<script setup>
    import { RouterLink } from 'vue-router';
    import { ref, computed, onMounted } from 'vue';
    import MoviesView from '@/views/MoviesView.vue';
import MovieDetails from './MovieDetails.vue';
    
    const start_ind = ref(0);


    const props = defineProps({
        title: {
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
    
   
    const addMovie = async (movie) => {
        const response = await fetch("http://localhost:8000/addmovie", {
            method: "POST",
            body: JSON.stringify(movie),
            headers: {
                "Content-Type": "application/json"
            }

        });
        
        console.log(response);
        movie.isAdded = true;

    }
    const deleteMovie = async (movie) => {
        const response = await fetch("http://localhost:8000/delete_movie", {
            method: "POST",
            body: JSON.stringify(movie),
            headers: {
                "Content-Type": "application/json"
            }

        });
        
        console.log(response);
        movie.isAdded = false;

    }
    

</script>

<template>
    <section>
    <div class="movies-header">
    <h1 class="title">{{ props.title }}</h1>
    </div>
        <TransitionGroup name="list" tag="div" class="movies-container">
        <div class="movie-card" v-for="(movie, index) in visibleMovies" :key="movie">
            <img v-if=movie.poster_path :src="`https://image.tmdb.org/t/p/original`+movie.poster_path">
            <img v-else src="../assets/poster_examples/jack2.jpg">
            <div class="movie-details">
            <h2>{{ movie.title }}</h2>
            <p v-if="movie.overview">{{ movie.overview }}</p>
            <ul class="time-list" v-if="showTimes">
                <li class="time" v-for="time in movie.times">{{ time }}</li>
            </ul>
            </div>
            <div class="movie-actions">
                <button @click="addMovie(movie)" v-if="!movie.isAdded" class="movie-action movie-add"><i class="pi pi-plus-circle"></i>Lägg till</button>
                <button @click="deleteMovie(movie)" v-else class="movie-action movie-remove"><i class="pi pi-trash"></i>Ta bort</button>
            </div>
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

.movie-actions {
    border-left: 1px solid #404040;
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

.scroll button:disabled {
    cursor: default;
    opacity: 50%;
}

.movies-container, .movies-grid {
    width: 100%;
    display: grid;
    grid-template-columns: 1fr;
    margin: 0 auto;
    gap: 30px;
    padding-top: 10px;

}

.movie-card img {
    height: 300px;
    border-radius: 10px; 
    border-top-right-radius: 0px;
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
    border: 1px solid #404040;
    transition: 300ms;
    width: 100%;
    display: grid;
    grid-template-columns: 1fr 6fr 1fr;


}



.movie-card:hover {
    transform: translateY(-10px);
    cursor: default;
}


.movie-card p, .movie-card h2 {
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
  display: none;
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
    background-color: none;
    display: block;
}

.movie-remove i {
    color: #e50914;
    background-color: none;
    display: block;
}
    
.movie-actions, .movie-action i {
    transition: 300ms;
    border-radius:inherit;
    border-bottom-left-radius: 0px;
    border-top-left-radius: 0px;
}
        

.movie-actions:hover {
    background-color: rgb(112, 109, 109);
    & i {
    background-color: rgb(112, 109, 109);

    }
}
</style>