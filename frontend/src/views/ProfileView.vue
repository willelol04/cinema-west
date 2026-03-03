<script setup>
    
import Profile from '@/components/Profile.vue';
import TicketCard from '@/components/TicketCard.vue';
import { onMounted, ref } from 'vue';
import { useAuth0, User } from '@auth0/auth0-vue';

const { user, isAuthenticated, isLoading, error, getAccessTokenSilently } = useAuth0();

const bookings = ref([])

const fetchBookings = async () => { 
    try {
    const token = await getAccessTokenSilently();
    const bookingsPromise = await fetch("http://localhost:8000/my-bookings/", {
      headers: {
        "Content-type": "application/json",
        "Authorization": `Bearer ${token}`
      }
    })

    bookings.value = await bookingsPromise.json();

    console.log(bookings.value);

    } catch(e) {
        alert(e);
    }    
}

onMounted(async () => {await fetchBookings()})


</script>

<template>
    
    <div class="my-profile">
        <Profile v-if="isAuthenticated" :isMyProfile="false" :user="{email: user.email, sub: user.sub}"/>
    <h2 class="bookings-header">My Bookings</h2>
        <div class="booking" v-for="(booking, ind) in bookings">
        <h2>Booking - {{ ind }}</h2>
    <div class="tickets">
        <TicketCard class="ticket-card" v-for="(t,ind) in booking.tickets" :ticket="t"/>
    </div>
        </div>
    </div>
    

</template>

<style scoped>

.bookings-header {
    margin-bottom: 50px;

}

.my-profile {
    width: 100%;
    padding: 20px 200px;
    margin: 0 auto;
}

.tickets {
    margin-top: 50px;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(450px, 1fr));
    gap: 1rem;
}
      
.ticket-card {
    box-sizing: border-box;
    width: 100%;
    margin-bottom: 10px;
}
      
.booking {
    border: 1px solid white;
    border-radius: 10px;
    padding: 10px;
}

.booking:not(:last-child) {
    margin-bottom: 20px;
}

@media screen and (max-width: 1200px) {
    .my-profile {
        padding: 10px;
    }
}

</style>