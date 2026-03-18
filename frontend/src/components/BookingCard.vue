<script setup>

import {format} from 'date-fns'

defineProps({
  booking: Object,
});

const emits = defineEmits(['delete']);
</script>

<template>
  <div
      class="booking"
      :id="`booking-`+booking.id"
      :style="{
    backgroundImage: `linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)), url(https://image.tmdb.org/t/p/original${booking.screening.movie.poster_path})`,
    backgroundSize: 'cover',
    backgroundPosition: 'top',
    backgroundRepeat: 'no-repeat'
    }"
  >
    <div class="booking-header">
      <h2>{{ booking.screening.movie.title }}</h2>
      <h3>{{  format(booking.screening.start_time, "EEEE, MMMM do HH:mm")}}</h3>
    </div>
    <div class="booking-body">
      <div class="booking-info">
        <span class="theatre-label label">Theatre</span>
        <span class="theatre-info">{{ booking.screening.theatre.name }}</span>
      </div>
      <div class="booking-info">
        <span class="seats-label label">Seats</span>
        <span class="seats-info"
        ><span class="seat-info" v-for="(ticket, ind) in booking.tickets"
        >{{ ticket.seat.id
          }}<span v-if="ind < booking.tickets.length - 1">, </span></span
        ></span
        >
      </div>
      <div class="booking-info">
        <span class="price-label label">Total Price</span>
        <span class="price-info">{{ booking.total_price }}kr</span>
      </div>
    </div>
    <button class="cancel-booking-button" @click="emits('delete')">
      Cancel booking
    </button>
  </div>
</template>

<style scoped>
.booking {
  border: 2px solid var(--default-border-bg);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  border-radius: 10px;
  padding: 20px;
  height: 100%;
}

.booking-info {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
}

.booking-info:first-child {
  padding-top: 16px;
  border-top: 1px solid var(--default-border-bg);
}

.label {
  margin-right: 10px;
}

.booking-info {
  margin-bottom: 16px;
  padding-bottom: 16px;
  border-bottom: 1px solid var(--default-border-bg);
}

.cancel-booking-button {
  width: 100%;
  background-color: var(--selected-default-color);
  color: white;
  vertical-align: middle;
  padding: 5px;
  border-radius: 5px;
}

.booking-header {
  margin-bottom: 50px;
}

h3 {
  margin-top: 20px;
  font-weight: 100;
}
</style>
