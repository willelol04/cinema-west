<script setup>
import { reactive, defineProps, onMounted, ref, onBeforeUnmount} from 'vue'; // probably want to use ref instead
import MovieDetails from '@/components/MovieDetails.vue';
import Booking from '@/components/Booking.vue';
import { useRoute, useRouter } from 'vue-router';
import {useAuth0} from "@auth0/auth0-vue";
import { format, formatDistance, formatRelative, subDays } from 'date-fns';

const { user, isAuthenticated, isLoading, error, getAccessTokenSilently } = useAuth0();

const screeningResult = ref(null);
const checkedSeats = ref([]);
const intervalID = ref(null)

const route = useRoute();
const router = useRouter();

async function fetchScreening() {
    const promise = await fetch('http://localhost:8000/screenings/'+route.params.id);
    screeningResult.value = await promise.json();
    console.log(screeningResult.value);

}

const bookTickets = async () => {
    if(checkedSeats.value.length > 0) {
        try {
        const token = await getAccessTokenSilently();
        const response = await fetch("http://localhost:8000/tickets", {
            method: "POST",
            body: JSON.stringify({seats: checkedSeats.value, screening_id: screeningResult.value.id}),
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

        console.log(await response.json());
        router.push('/payment')
            
        } catch(e) {
            alert(`Error: ${e}`)
            console.log(e)
        } finally {
        checkedSeats.value = [];
        await fetchScreening();
            
        }

    }

}

onMounted(async () => {
  await fetchScreening()
  intervalID.value = setInterval(async () => { 
    await fetchScreening()
  }, 5000)
  console.log(intervalID.value)
})

onBeforeUnmount(() => {clearInterval(intervalID.value); intervalID.value = null})
  
</script>

<template>
        <div v-if="screeningResult" class="booking">
        <h3>{{ screeningResult.movie.title }} - {{ format(screeningResult.start_time, "EEEE, MMMM do HH:mm") }}</h3>
        <form method="POST" @submit.prevent="bookTickets()" action="#">
        <div class="screen">Movie Screen</div>
        <div :style="`grid-template-columns: repeat(${screeningResult.theatre.seats_per_row}, 1fr)`" class="gridding">
        <label v-for="(seat, ind) in screeningResult.theatre.seats" :key="ind" class="checkbox-label">
            <div class="seat">
            <input v-model="checkedSeats" type="checkbox" :value="seat" :disabled="screeningResult.booked_seat_ids.includes(seat.id)">
            <span class="check">
                <i  class="pi pi-stop available"></i>
            </span>
            </div>
        </label>

        </div>
            
        <input v-if="isAuthenticated"  type="submit" :value="`Book ${checkedSeats.length} seats`">
        </form>
        </div>
</template>
<!--
            <div class="row"><span><input type="checkbox" name="" id="">x</span><span><input type="checkbox" name="" id="">x</span><span><input type="checkbox" name="" id="">x</span><span><input type="checkbox" name="" id="">x</span><span><input type="checkbox" name="" id="">x</span><span><input type="checkbox" name="" id="">x</span><span><input type="checkbox" name="" id="">x</span><span><input type="checkbox" name="" id="">x</span><span><input type="checkbox" name="" id="">x</span><span><input type="checkbox" name="" id="">x</span></div>
            <div class="row"><span><input type="checkbox" name="" id="">x</span><span><input type="checkbox" name="" id="">x</span><span><input type="checkbox" name="" id="">x</span><span><input type="checkbox" name="" id="">x</span><span><input type="checkbox" name="" id="">x</span><span><input type="checkbox" name="" id="">x</span><span><input type="checkbox" name="" id="">x</span><span><input type="checkbox" name="" id="">x</span><span><input type="checkbox" name="" id="">x</span><span><input type="checkbox" name="" id="">x</span></div>
            <div class="row"><span><input type="checkbox" name="" id="">x</span><span><input type="checkbox" name="" id="">x</span><span><input type="checkbox" name="" id="">x</span><span><input type="checkbox" name="" id="">x</span><span><input type="checkbox" name="" id="">x</span><span><input type="checkbox" name="" id="">x</span><span><input type="checkbox" name="" id="">x</span><span><input type="checkbox" name="" id="">x</span><span><input type="checkbox" name="" id="">x</span><span><input type="checkbox" name="" id="">x</span></div>
            <div class="row"><span><input type="checkbox" name="" id="">x</span><span><input type="checkbox" name="" id="">x</span><span><input type="checkbox" name="" id="">x</span><span><input type="checkbox" name="" id="">x</span><span><input type="checkbox" name="" id="">x</span><span><input type="checkbox" name="" id="">x</span><span><input type="checkbox" name="" id="">x</span><span><input type="checkbox" name="" id="">x</span><span><input type="checkbox" name="" id="">x</span><span><input type="checkbox" name="" id="">x</span></div>
            <div class="row"><span><input type="checkbox" name="" id="">x</span><span><input type="checkbox" name="" id="">x</span><span><input type="checkbox" name="" id="">x</span><span><input type="checkbox" name="" id="">x</span><span><input type="checkbox" name="" id="">x</span><span><input type="checkbox" name="" id="">x</span><span><input type="checkbox" name="" id="">x</span><span><input type="checkbox" name="" id="">x</span><span><input type="checkbox" name="" id="">x</span><span><input type="checkbox" name="" id="">x</span></div>
-->

<style scoped>
h3 {
    text-align: center;
}
.gridding {
    width: 100%;
    display: grid;
    margin: 0 auto;
    gap: 15px 5px;
}

.booking {
    width: 100%;
    background-position: center; 
    background-size: cover;
    position: relative;
}

.screen {
    border: 1px solid white;
    display: block;
    margin: 0 auto;
    font-size: 24px;
    text-align: center;
    border-radius: 10px;
    margin-bottom: 45px;
    padding: 20px 0px;
}

form {
    display: block;
    text-align: center;
    margin: 0 auto;
    padding: 20px;
    width: fit-content;
    
}

.checkbox-label {
    font-size: 24px;
    padding: 0;
}
.row {
    margin-top: 40px;
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    flex-wrap: nowrap;
}

input[type="checkbox"] {
    position: absolute;
    opacity: 0;
    padding: 0;
    width: 24px;
    height: 24px;

}

.check i {
    border-radius: 10px;
    padding: 0;
    font-size: 24px;
    transition: 150ms;

}



input[type="checkbox"]:not(:disabled):hover {
    cursor: pointer;
}

input[type="checkbox"]:disabled + .check {
    opacity: 30%;
}


input[type="checkbox"]:not(:disabled):hover + .check> .available {
    cursor: pointer;
    color: green;

}
input[type="checkbox"]:checked + .check i {
    background-color: green;
    color: green;
}

input[type="submit"] {
    background-color: #2d2d2d;
    border: 1px solid #404040;
    border-radius: 7px;
    padding: 20px;
    transition: 300ms;
}

input[type="submit"]:hover { 
    cursor: pointer;
    background-color: #4e4d4d;

}
@media only screen and (max-width: 768px) {


input[type="checkbox"] {
    width: 16px;
    height: 16px

}

.check i {
    font-size: 16px;

}
}


</style>