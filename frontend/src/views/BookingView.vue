<script setup>
import { reactive, defineProps, onMounted, ref, onBeforeUnmount, watch} from 'vue'; // probably want to use ref instead
import MovieDetails from '@/components/MovieDetails.vue';
import { useRoute, useRouter } from 'vue-router';
import {useAuth0} from "@auth0/auth0-vue";
import { format, formatDistance, formatRelative, subDays } from 'date-fns';
import {getScreening} from '@/api/screenings';
import {addBooking} from '@/api/bookings';
import NavigateBackButton from "@/components/NavigateBackButton.vue";


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
        <main>
          <NavigateBackButton v-if="screeningResult" :target="`/movies/`+screeningResult.movie.id" text="Go Back to Movie Details">
          </NavigateBackButton>

          <div v-if="screeningResult" class="booking">
            <form method="POST" @submit.prevent="bookTickets()" action="#">
              <h3>{{ screeningResult.movie.title }} - {{ format(screeningResult.start_time, "EEEE, MMMM do HH:mm") }}</h3>
              <div :style="`grid-template-columns: repeat(${screeningResult.theatre.seats_per_row}, 1fr)`" class="seat-grid">
                <div class="screen" :style="{
    backgroundImage: `linear-gradient(rgba(0,0,0,0.3), rgba(0,0,0,0.3)), url(https://image.tmdb.org/t/p/original${screeningResult.movie.backdrop_path})`,
    backgroundSize: 'cover',
    backgroundPosition: 'middle',
    backgroundRepeat: 'no-repeat'
    }"><i class="pi pi-play-circle"></i></div>
                <label v-for="(seat, ind) in screeningResult.theatre.seats" :key="ind" class="checkbox-label">
                  <div class="seat">
                    <input v-model="checkedSeats" type="checkbox" :value="seat" :disabled="booked_seat_ids?.includes(seat.id)">
                    <span class="check">
                <i  class="pi pi-stop available"></i>
            </span>
                  </div>
                </label>

              </div>

              <div  class="booking-details">
                <div class="booking-info">
                  <span class="booking-info-label">Seats selected:</span>
                  <span v-for="(seat, ind) in checkedSeats">{{seat.id}}, </span>
                </div>
                <div class="booking-info">
                  <span class="booking-info-label">Total price:</span>
                  <span>{{checkedSeats.length * 100}}SEK</span>
                </div>
                <input v-if="isAuthenticated"  type="submit" value="Go to payment">

              </div>
            </form>
          </div>
        </main>
</template>
<style>
:root {
    --seat-size: 32px;
}

</style>

<style scoped>

.pi-play-circle {
  font-size: 48px;
  color: blue;
  background-color: white;
  border-radius: 50%;
}

.booking-details {
  width: 100%;
  margin: 0 auto;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  padding: 50px 20px;
  border-radius: 10px;
  background: #1a1a1a;
  margin-top: 50px;
}

.booking-info {
  text-align: left;
}
.booking-info-label {
  display: block;
  font-size: 24px;
}

h3 {
    text-align: center;
    font-size: 32px;
}
.seat-grid {
    width: 100%;
    display: grid;
    justify-items: center;;
    margin: 0 auto;
    overflow-x: scroll;
    scrollbar-gutter: stable;
    padding: 20px;
    gap: 40px 5px;
}
main {
  padding: 20px 200px;
  background-color: #131212;

}

.booking {
    background-position: center; 
    margin: 0 auto;
    background-size: cover;
    position: relative;
    overflow: hidden;
}

.screen {
    display: block;
    margin: 0 auto;
    font-size: 24px;
    text-align: center;
    margin-bottom: 45px;
    padding: 150px;
    grid-column: 1 / -1;
    width: 100%;
  clip-path: polygon(
      0% 0%,   /* top left */
      100% 0%,   /* top right */
      98% 100%,/* bottom right */
      2% 100%   /* bottom left */
  );
}

form {
    width: 100%;
    display: block;
    text-align: center;
    margin: 0 auto;
    overflow: hidden;
    
}

.seat {
    width: var(--seat-size);
    height: var(--seat-size);
    position: relative;
}

.checkbox-label {
    font-size: var(--seat-size);
    width: var(--seat-size);
    height: var(--seat-size);
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
    width: var(--seat-size);
    height: var(--seat-size);

}

.check i {
    border-radius: 5px;
    padding: 0;
    font-size: var(--seat-size);
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
    font-size: 24px;
}

input[type="submit"]:hover { 
    cursor: pointer;
    background-color: #4e4d4d;

}
@media only screen and (max-width: 768px) {


}

@media only screen and (max-width: 1200px) {
    main {
        padding: 10px;
    }


}


</style>