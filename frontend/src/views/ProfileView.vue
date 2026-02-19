<script setup>
    
import Profile from '@/components/Profile.vue';
import TicketCard from '@/components/TicketCard.vue';
import { onMounted, ref } from 'vue';
import { useAuth0, User } from '@auth0/auth0-vue';

const { user, isAuthenticated, isLoading, error } = useAuth0();

const movieResults = ref([])

async function fetchTickets() { 
    try {
    const movieResultsPromise = await fetch("httpaaa://localhost:8000/movies", {
      headers: {
        "Content-type": "application/json",
      }
    })
    const movieResultsObject = await movieResultsPromise.json();
    movieResults.value = movieResultsObject;

    console.log(movieResults.value);

    } catch(e) {
        alert(e);
    }    
}

</script>

<template>
    
    <div class="my-profile">
        <Profile v-if="isAuthenticated" :user="{email: user.email}"/>
    <h2>My Tickets</h2>
    <div class="tickets">
        <TicketCard class="ticket-card" v-for="n in [1,1,1,1]"/>
    </div>
    </div>
    

</template>

<style scoped>

.my-profile {
    width: 60vw;
    padding: 20px 200px;
    margin: 0 auto;
}

.tickets {
    margin-top: 50px;
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    margin: 0 auto;
    gap: 10px;
}

</style>