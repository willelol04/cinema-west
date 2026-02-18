<script setup>
import AdminScreenings from '@/components/AdminScreenings.vue';
import { ProgressSpinner } from 'primevue';

const props = defineProps({
    seatNames: [],
    screeningName: ''
})

</script>

<template>
    <div class="booking-confirmation">
        <h1>Congratulations User! You have successfully booked seat(s) {{ props.seatNames }} to {{ props.screeningName }}</h1>
    </div>

</template>

<style scoped>



.booking-confirmation {
    width: 700px;
    text-align: left;
    margin: 0 auto;
}

h2 i {
    vertical-align: middle;

}

.booking-confirmation h1 {
    font-size: 24px;
}

</style>