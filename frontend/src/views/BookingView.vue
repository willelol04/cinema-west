<script setup>
import { reactive, defineProps, onMounted, ref, onBeforeUnmount} from 'vue'; // probably want to use ref instead
import MovieDetails from '@/components/MovieDetails.vue';
import { useRoute, useRouter } from 'vue-router';
import {useAuth0} from "@auth0/auth0-vue";
import { format, formatDistance, formatRelative, subDays } from 'date-fns';
import {getScreening} from '@/api/screenings';
import {addBooking} from '@/api/bookings';


const { user, isAuthenticated, isLoading, error, getAccessTokenSilently } = useAuth0();

const screeningResult = ref(null);
const checkedSeats = ref([]);
const booked_seat_ids = ref([])

const route = useRoute();
const router = useRouter();
let ws = null;

async function fetchScreening() {
    screeningResult.value = await getScreening(route.params.id);
    booked_seat_ids.value = screeningResult.value.booked_seat_ids;
}

const bookTickets = async () => {
    if(checkedSeats.value.length > 0) {
        try {
        const token = await getAccessTokenSilently();
        const bookingId = await addBooking({seats: checkedSeats.value, screening_id: screeningResult.value.id}, token);

        console.log(bookingId);
        if(ws) {
            ws.send(JSON.stringify({msg: "update"}))
        } else {
            alert("WS not found");
        }

        console.log("Sent")

        if(bookingId) {
            router.push(`/payment/${bookingId}`)
        }
            
        } catch(e) {
            alert(`Error: ${e}`)
            console.log(e)
        } finally {
        checkedSeats.value = [];
        await fetchScreening();
            
        }

    }

}

onBeforeUnmount(() => {
    if(ws) {
        ws.close()
    }
})

  
onMounted(async () => {
        await fetchScreening();

        if(!ws) {
            ws = new WebSocket(`http://localhost:8000/ws/${route.params.id}`);
        }

        ws.onmessage = async (event) => {
            console.log(JSON.parse(event.data))
            booked_seat_ids.value = JSON.parse(event.data).booked_seat_ids
            checkedSeats.value = checkedSeats.value.filter((seat) => !booked_seat_ids.value.includes(seat.id)) 
        };
});
</script>

<template>
        <div v-if="screeningResult" class="booking">
        <h3>{{ screeningResult.movie.title }} - {{ format(screeningResult.start_time, "EEEE, MMMM do HH:mm") }}</h3>
        <form method="POST" @submit.prevent="bookTickets()" action="#">
        <div class="screen">Movie Screen</div>
        <div :style="`grid-template-columns: repeat(${screeningResult.theatre.seats_per_row}, 1fr)`" class="seat-grid">
        <label v-for="(seat, ind) in screeningResult.theatre.seats" :key="ind" class="checkbox-label">
            <div class="seat">
            <input v-model="checkedSeats" type="checkbox" :value="seat" :disabled="booked_seat_ids?.includes(seat.id)">
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

<style scoped>
h3 {
    text-align: center;
}
.seat-grid {
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
    padding: 20px 200px;
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
    width: 100%;
    display: block;
    text-align: center;
    margin: 0 auto;
    
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
    .check i {
        font-size: 12px;

    }

}

@media only screen and (max-width: 1200px) {

    input[type="checkbox"] {
        width: 12px;
        height: 12px

    }

    .seat-grid {
        gap: 5px 3px;
    }

    .check i {
        font-size: 12px;

    }


    .booking {
        padding: 10px;
    }
}


</style>