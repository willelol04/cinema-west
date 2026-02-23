<script setup>
    
const props = defineProps({
    ticket: {
        id: Number,
        screening: Object,
        seat: Object,
    }
})


</script>

<template>
    <div v-if="ticket.id" class="ticket-card">
            <img :src="`https://image.tmdb.org/t/p/original`+ticket.screening.movie.poster_path" alt="movie-poster">
            <div class="ticket-details">
                <h3>{{ticket.screening.movie.title}}</h3>
                <p>Theatre: {{ ticket.seat.theatre.name }}</p>
                <p>Seat: {{ ticket.seat.id }}</p>
                <p>Time: {{ ticket.screening.start_time }}</p>
                <p :class="ticket.status == 'pending' ? 'pending' : 'complete'">Payment status: {{ ticket.booking.status }}</p>
                <p v-if="ticket.booking.status == 'pending'" class="pay"><RouterLink :to="`/payment/${ticket.booking.id}`" >Pay</RouterLink> no later than {{ ticket.booking.expires_at }}</p>
            </div>
            <div class="yes">
                <button><i class="pi pi-times"></i></button>
            </div>
    </div>
</template>

<style scoped>

.pay, .pay > * {
    color: red;
}

.ticket-card {
    width: 100%;
    display: flex;
    justify-content: start;
    align-items: stretch;
    border-radius: 8px;
    border: 1px solid white;
    margin: 0 auto;
    position: relative;
;
}

.ticket-card img {
    width: 200px;
}

.ticket-details {
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding-left: 20px;
    gap: 10px;
    width: fit-content;
}
    
button {
    padding: 10px;
    top: 0;
    right: 0;
    position: absolute;
}
    
button:hover {
    i {
    color: red;
    }
}

</style>