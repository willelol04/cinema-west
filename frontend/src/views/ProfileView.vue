<script setup>
    
import Profile from '@/components/Profile.vue';
import BookingCard from '@/components/BookingCard.vue';
import { onMounted, ref } from 'vue';
import { useAuth0, User } from '@auth0/auth0-vue';

const { user, isAuthenticated, isLoading, error, getAccessTokenSilently } = useAuth0();

const bookings = ref([])
const fetchBookings = async () => { 
    try {
    const token = await getAccessTokenSilently();
    const bookingsPromise = await fetch("/api/my-bookings/", {
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


const cancelBooking = async (booking) => {
    try {
        const token = await getAccessTokenSilently();
        const res = await fetch("/api/bookings", {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({
                id: booking.id, 
                screening_id: booking.screening.id
            }),
        });

        if (!res.ok) {
            const err = await res.json();
            alert("Booking cancellation failed: ", err);
            return;
        }

        const result = await res.json();
        console.log(result);
        fetchBookings();
    } catch (e) {
        console.log(e);
        alert("Something went wrong: " + e.message);
    }
};
</script>

<template>
    
    <div class="my-profile">
        <Profile v-if="isAuthenticated" :isMyProfile="true" :user="{email: user.email, sub: user.sub}"/>
        <div class="bookings">
        <BookingCard class="booking" v-for="(booking, ind) in bookings" @delete="cancelBooking(booking)" :booking="booking"/>
        </div>
    </div>
    

</template>

<style scoped>
.my-profile {
    width: 100%;
    padding: 20px 200px;
    margin: 0 auto;
}

.bookings {
    margin: 0 auto;
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    justify-items: center;
    grid-auto-rows: 1fr;
    gap: 1%;
}
    
.booking {
    width: 100%;
}
    
@media screen and (max-width: 768px) {
    .bookings {
        grid-template-columns: repeat(1, 1fr);
    }
}
  
 
@media screen and (max-width: 1200px) {
    .my-profile {
        padding: 10px;
    }
}

</style>