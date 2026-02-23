<script setup>
    
import Profile from '@/components/Profile.vue';
import TicketCard from '@/components/TicketCard.vue';
import { onMounted, ref } from 'vue';
import { useAuth0, User } from '@auth0/auth0-vue';

const { user, isAuthenticated, isLoading, error, getAccessTokenSilently } = useAuth0();

const tickets = ref([])

const fetchTickets = async () => { 
    try {
    const token = await getAccessTokenSilently();
    const ticketsPromise = await fetch("http://localhost:8000/tickets/me", {
      headers: {
        "Content-type": "application/json",
        "Authorization": `Bearer ${token}`
      }
    })

    tickets.value = await ticketsPromise.json();

    console.log(tickets.value);

    } catch(e) {
        alert(e);
    }    
}

onMounted(async () => {await fetchTickets()})

</script>

<template>
    
    <div class="my-profile">
        <Profile v-if="isAuthenticated" :user="{email: user.email}"/>
    <h2>My Tickets</h2>
    <div class="tickets">
        <TicketCard class="ticket-card" v-for="(t,ind) in tickets" :ticket="t"/>
    </div>
    </div>
    

</template>

<style scoped>

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
      

@media screen and (max-width: 1200px) {
    .my-profile {
        padding: 10px;
    }
}

</style>