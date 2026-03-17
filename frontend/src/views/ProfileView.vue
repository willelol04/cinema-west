<script setup>
import Profile from '@/components/Profile.vue';
import BookingCard from '@/components/BookingCard.vue';
import { nextTick, onMounted, ref } from 'vue';
import { useAuth0, User } from '@auth0/auth0-vue';

import {useRoute, useRouter} from 'vue-router';
import { deleteBooking, getMyBookings } from '@/api/bookings'
import BeatLoader from "vue-spinner/src/BeatLoader.vue";

const route = useRoute();
const router = useRouter();
const { user, isAuthenticated, isLoading, error, getAccessTokenSilently } = useAuth0();

const bookings = ref([])
const showAlert = ref(false);
const bookingsFetchComplete = ref(true)
const fetchBookings = async () => {
    try {
    bookingsFetchComplete.value = false;
    const token = await getAccessTokenSilently();
    bookings.value = await getMyBookings(token);
    bookingsFetchComplete.value = true;

    } catch(e) {
        alert(e);
    }    
}


onMounted(async () => {
    await fetchBookings();

    await nextTick();

    if(route.query.state=='new-booking' && route.query.bookingId) {
        showAlert.value = true;
    }
})

const goToBooking = (bookingId) => {
    console.log(bookingId);
    const element = document.querySelector(`#booking-${bookingId}`)
      if (element) {
        element.scrollIntoView({ behavior: 'smooth' })
      }
}

const cancelBooking = async (booking) => {
    try {
        const token = await getAccessTokenSilently();
        const result = await deleteBooking({id: booking.id, screening_id: booking.screening_id}, token)
        console.log(result);
        fetchBookings();
    } catch (e) {
        console.log(e);
        alert("Something went wrong: " + e.message);
    }
};
</script>

<template>

   <main>
     <div v-if="bookingsFetchComplete && isAuthenticated" class="my-profile">
       <Profile class="profile-info" :isMyProfile="true" :user="{email: user.email, sub: user.sub}"/>
       <div v-if="showAlert" class="new-booking-alert"><button @click="showAlert=false" class="close-alert-btn"><i class="pi pi-times"></i></button>Alert: You have a new booking added to your account! <button class="go-to-booking-btn" @click="goToBooking(route.query.bookingId)" > Go to booking</button></div>
       <div class="bookings">
         <BookingCard class="booking" v-for="(booking, ind) in bookings" @delete="cancelBooking(booking)" :booking="booking"/>
       </div>
     </div>
     <BeatLoader class="fetch-loading" :color="'#bdc7bf'" v-else />

   </main>


</template>

<style scoped>
main {
  background-color: var(--main-bg);
}

.my-profile {
    width: 100%;
    padding: 20px 200px;
    margin: 0 auto;    
    height: 100%;
}

.new-booking-alert button {
    vertical-align: middle;
}

.close-alert-btn {
    margin-right: 20px;
}

.go-to-booking-btn {
    text-decoration: underline;
    background: black;
    color: white;
    padding: 10px;
    border-radius: 10px;
}

    

.new-booking-alert {
    width: 100%;
    background: rgb(46, 138, 81);
    color: white;
    padding: 20px;
    border-radius: 8px;
    margin-top: 20px;
    margin-bottom: 20px;
}

.bookings {
    margin: 0 auto;
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    justify-items: center;
    grid-auto-rows: 1fr;
    height: 100%;
    gap: 15px;
}
    
.booking {
    width: 100%;
}
    
  
 
@media screen and (max-width: 1200px) {
    .my-profile {
        padding: 10px;
    }

    .bookings {
        grid-template-columns: repeat(1, 1fr);
    }

    .profile-info {
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: middle;
    }
}

</style>