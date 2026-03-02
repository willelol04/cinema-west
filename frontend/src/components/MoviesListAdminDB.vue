<script setup>
import { RouterLink } from 'vue-router';
import { ref, computed, onMounted } from 'vue';
import MoviesView from '@/views/MoviesView.vue';
import MovieDetails from './MovieDetails.vue';
import ConfirmDeleteModal from './ConfirmDeleteModal.vue';
import {useAuth0} from "@auth0/auth0-vue";
const { user, isAuthenticated, isLoading, error, getAccessTokenSilently } = useAuth0();

const start_ind = ref(0);
const fetchComplete = ref(false);
const confirmDelete = ref(false)

const emit = defineEmits("update")

const props = defineProps({
    title: {
        type: String,
        default: 'Movies',
    },
    theatres: Array,
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


const addMovie = async (movie) => {
    const token = await getAccessTokenSilently();
    const response = await fetch("http://localhost:8000/movies/", {
        method: "POST",
        body: JSON.stringify(movie),
        headers: {
            "Content-Type": "application/json",
            "authorization": `Bearer ${token}`,
        }

    });

    console.log(response);
    emit('update')

};

const deleteMovie = async (movie) => {
    try {
    const token = await getAccessTokenSilently();
    const response = await fetch("http://localhost:8000/movies/", {
        method: "DELETE",
        body: JSON.stringify(movie),
        headers: {
          "Content-Type": "application/json",
          "authorization": `Bearer ${token}`,
        }

    });
    
    if (!response.ok) {
        const error = await response.json();
        alert(`Error: ${error.detail}`)
        console.log(error)
        return null
    }
    
    emit('update');
    alert("Movie removed");

    } catch(e) {
        console.log(e)
    }

};


const updateScreening = async (screening) => {
    try {
    const token = await getAccessTokenSilently();
    const response = await fetch("http://localhost:8000/screenings", {
        method: "PATCH",
        body: JSON.stringify({id: screening.id, start_time: screening.start_time}),
        headers: {
          "Content-Type": "application/json",
          "authorization": `Bearer ${token}`,
        }

    });
    
    if (!response.ok) {
        const error = await response.json();
        alert(`Error: ${error.detail}`)
        console.log(error)
        return null
    }
    
    emit('update');
    alert("Screening updated");

    } catch(e) {
        console.log(e)
    }

};


const deleteScreening = async (screening_id) => {
    if(confirm("Are you sure you want to delete this screening?")) {
    try {
    const token = await getAccessTokenSilently();
    const response = await fetch("http://localhost:8000/screenings", {
        method: "DELETE",
        body: JSON.stringify({id: screening_id}),
        headers: {
          "Content-Type": "application/json",
          "authorization": `Bearer ${token}`,
        }

    });
    
    if (!response.ok) {
        const error = await response.json();
        alert(`Error: ${error.detail}`)
        console.log(error)
        return null
    }
    
    emit('update');
    alert("Screening removed");

    } catch(e) {
        console.log(e)
    }


    }
};
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
            <img class="movie-poster" v-if=movie.poster_path :src="`https://image.tmdb.org/t/p/original`+movie.poster_path">
            <i v-else class="pi pi-image"></i>
            <div class="movie-details">
            <h2>{{ movie.title }}</h2>
            <p v-if="movie.overview">{{ movie.overview }}...</p>
            <button v-if="movie.screenings && movie.screenings.length > 0" @click="movie.showScreenings = !movie.showScreenings">show Screenings <i v-if="!movie.showScreenings" class="pi pi-chevron-down"></i> <i v-else class="pi pi-chevron-up"></i></button>
            <ul class="screenings-list" v-if="movie.showScreenings && movie.screenings">
                <li  class="screening" v-for="(screening, ind) in movie.screenings">
                    <span v-if="!screening.showEdit">
                    {{ screening.start_time }}
                    <button @click="screening.showEdit = !screening.showEdit"> <i class="pi pi-pen-to-square"></i></button>
                    <button @click="deleteScreening(screening.id)"><i class="pi pi-times"></i></button>                       
                    </span>
                    <span v-else>
                    <form @submit.prevent="updateScreening(screening)">
                    <input type="datetime-local" v-model="screening.start_time" id="time">
                    <input type="submit">
                    <button @click="screening.showEdit = !screening.showEdit">Cancel edit</button>
                    </form>
                    </span>
                </li>
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

.pi-image {
    text-align: center;
    vertical-align: center;
    margin-top: 50px;
}


h1 {
    font-size: 24px;
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




form {
    input, select, option, button {
    background-color: black;
    color: white;
    padding: 10px;
    margin-right: 10px;
}
}

.screening {
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
    width: 100%;
    text-align: left;
    display: block;
    margin: 0 auto;
}

.pi-trash, .pi-plus-circle, .pi-chevron-circle-left, .pi-chevron-circle-right {
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


.movie-card p, .movie-card h2 {
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

.movie-card {
    background-color: #2d2d2d;
    border-radius: 10px;
    border: 1px solid #404040;
    transition: 300ms;
    width: 100%;
    display: grid;
    grid-template-columns: 1fr 7fr 1fr;
    grid-template-rows: auto;


}

.movie-poster {
    border-radius: 10px; 
    width: 100%;
    height: auto;
    border-top-right-radius: 0px;
    border-bottom-right-radius: 0px;
    display: block;
}
</style>