<script setup>
import { reactive, defineProps, onMounted, ref, onBeforeUnmount, watch} from 'vue'; // probably want to use ref instead
import MovieDetails from '@/components/MovieDetails.vue';
import { useRoute, useRouter } from 'vue-router';
import {useAuth0} from "@auth0/auth0-vue";
import { format, formatDistance, formatRelative, subDays } from 'date-fns';
import {getScreening} from '@/api/screenings';
import {addBooking} from '@/api/bookings';
import NavigateBackButton from "@/components/NavigateBackButton.vue";
import BeatLoader from "vue-spinner/src/BeatLoader.vue";


const {successToast, errorToast} = useAppToast();
import {useAppToast} from "@/use/useToast.js";
import LoginButton from "@/components/LoginButton.vue";

const { user, isAuthenticated, isLoading, error, getAccessTokenSilently } = useAuth0();

const screeningResult = ref(null);
const checkedSeats = ref([]);
const booked_seat_ids = ref([])
const fetchComplete = ref(true)

const route = useRoute();
const router = useRouter();
let ws = null;

async function fetchScreening() {
  try {
    fetchComplete.value = false
    screeningResult.value = await getScreening(route.params.id);
    booked_seat_ids.value = screeningResult.value.booked_seat_ids;

  } catch (e) {
    errorToast("Error fetching booking data. Try refreshing the page.")

  }
  finally {
    fetchComplete.value = true

  }
}

const bookTickets = async () => {
  if(checkedSeats.value.length > 0) {
    try {
      const token = await getAccessTokenSilently();
      const bookingId = await addBooking({seats: checkedSeats.value, screening_id: screeningResult.value.id}, token);

      if(bookingId && ws.readyState === WebSocket.OPEN) {
        try {
          ws.send(JSON.stringify({type: "update", msg: "booking issued."}))
        } catch(e) {
          alert(e, "WS not found");
        }

      }



      if(bookingId) {
        await router.push(`/payment/${bookingId}`)
      }

    } catch(e) {
      console.log(e?.error_type);
      if(e?.error_type === 'conflict' ) {
        errorToast(e.detail)
        checkedSeats.value = [];
        await fetchScreening();
      } else {
        errorToast("Error booking seats. Try refreshing the page.")
      }
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

  if(screeningResult.value) {
    console.log(screeningResult)
    ws = new WebSocket(`/api/ws/${screeningResult.value.id}`);

    ws.onmessage = async (event) => {
      if(JSON.parse(event.data)?.type === 'update') {
        booked_seat_ids.value = JSON.parse(event.data).booked_seat_ids
        checkedSeats.value = checkedSeats.value.filter((seat) => !booked_seat_ids.value.includes(seat.id))
      }

    }
  }

});
</script>

<template>
  <main>
    <div v-if="fetchComplete && screeningResult" class="booking">
      <NavigateBackButton
          :target="`/movies/`+screeningResult.movie.id"
          text="Go Back to Movie Details"
      >
      </NavigateBackButton>
      <form method="POST" @submit.prevent="bookTickets()" action="#">
        <h3>
          {{ screeningResult.movie.title }} -
          {{ format(screeningResult.start_time, "EEEE, MMMM do HH:mm") }}
        </h3>
        <div
            :style="`grid-template-columns: repeat(${screeningResult.theatre.seats_per_row}, 1fr)`"
            class="seat-grid"
        >
          <div
              class="screen"
              :style="{
    backgroundImage: `linear-gradient(rgba(0,0,0,0.3), rgba(0,0,0,0.3)), url(https://image.tmdb.org/t/p/original${screeningResult.movie.backdrop_path})`,
    backgroundSize: '100% 100%',
    backgroundPosition: 'middle',
    backgroundRepeat: 'no-repeat'
    }"
          ></div>
          <label
              v-for="(seat, ind) in screeningResult.theatre.seats"
              :key="ind"
              class="checkbox-label"
          >
            <div class="seat">
              <input
                  v-model="checkedSeats"
                  type="checkbox"
                  :value="seat"
                  :disabled="booked_seat_ids?.includes(seat.id)"
              />
              <span class="check">
                <i class="pi pi-stop available"></i>
              </span>
            </div>
          </label>
        </div>

        <div class="booking-details">
          <div class="booking-info">
            <span class="booking-info-label">Seats selected:</span>
            <span v-for="(seat, ind) in checkedSeats">{{seat.id}}, </span>
          </div>
          <div class="booking-info">
            <span class="booking-info-label">Total price:</span>
            <span>{{checkedSeats.length * 100}}SEK</span>
          </div>
          <input v-if="isAuthenticated" type="submit" value="Go to payment" />
          <LoginButton v-else type="submit" value="Log in to order tickets" />
        </div>
      </form>
      <BeatLoader
          class="fetch-loading"
          :color="'#bdc7bf'"
          v-if="!fetchComplete"
      />
    </div>
  </main>
</template>
<style>
:root {
  --seat-size: 32px;
}

@media only screen and (max-width: 1200px) {
  :root {
    --seat-size: 24px;
  }
}
</style>

<style scoped>
main {
  flex: 1;
}

.booking-details {
  width: 100%;
  margin: 0 auto;
  display: flex;
  text-align: center;
  padding: 50px 20px;
  border-radius: 10px;
  border: 2px solid var(--default-border-bg);
  background: var(--primary-bg);
  margin-top: 50px;
}
.booking-details > * {
  flex: 1;
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
  font-size: 24px;
}
.seat-grid {
  width: fit-content;
  display: grid;
  justify-items: center;
  overflow-x: auto;
  scrollbar-gutter: stable;
  padding: 20px;
  gap: 40px 2px;
  padding: 30px;
  margin: 0 auto;
}
main {
  width: 100%;
  margin: 0 auto;
  padding: 20px 200px;
  background-color: #131212;
}

.booking {
  background-position: center;
  margin: 0 auto;
  background-size: cover;
  position: relative;
  overflow: hidden;
  background: var(--secondary-bg);
  border-radius: 10px;
  padding: 30px;
  text-align: center;
}

.screen {
  display: block;
  margin: 0 auto;
  font-size: 24px;
  text-align: center;
  height: 180px;
  grid-column: 1 / -1;
  width: 100%;
  clip-path: polygon(0% 0%, 100% 0%, 98% 100%, 2% 100%);
  box-shadow: -1px 0px 40px 6px rgba(255, 255, 255, 0.45) inset;
  -webkit-box-shadow: -1px 0px 40px 6px rgba(255, 255, 255, 0.45) inset;
  -moz-box-shadow: -1px 0px 40px 6px rgba(255, 255, 255, 0.45) inset;
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

input[type="checkbox"]:not(:disabled):hover + .check > .available {
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
  font-size: 16px;
}

input[type="submit"]:hover {
  cursor: pointer;
  background-color: #4e4d4d;
}
@media only screen and (max-width: 768px) {
}

@media only screen and (max-width: 1200px) {
  main {
    padding: 20px;
  }

  .booking {
    padding: 10px;
  }

  .seat-grid {
    width: 100%;
    gap: 30px 1px;
    padding: 20px;
  }

  .booking-details {
    flex-direction: column;
    justify-content: start;
    gap: 20px;
    padding: 20px;
  }

  h3 {
    font-size: 24px;
  }
}
</style>
