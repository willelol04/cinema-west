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
                <p>Payment status: <span :class="ticket.booking.status === 'pending' ? 'pending' : 'complete'">{{ ticket.booking.status }}</span></p>
                <p v-if="ticket.booking.status == 'pending'" >Payment due at: {{ ticket.booking.expires_at }}<RouterLink class="pay" :to="`/payment/${ticket.booking.id}`">Pay now</RouterLink></p>
            </div>
            <!--
            <div class="topright">
                <button><i class="pi pi-times"></i></button>
            </div>
            -->
    </div>
</template>

<style scoped>

.pay {
    display: block;
    color: red;
    text-decoration: underline;
}

.pending {
    color: red;
}

.complete {
    color: green;
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
    border-radius: 8px;
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