<script setup>
import { onMounted, ref } from 'vue';

const timer = ref(300);


const decrementTimer = () => {
    timer.value--;
}


onMounted(() => {
    setInterval(decrementTimer, 1000)
})
</script>

<template>
    <div class="booking-confirmation">
        <h1>Congratulations User! You have successfully booked seat(s)! {{ timer }}</h1>
    </div>
</template>

<style scoped>

.ticket {
    width: 300px;
    padding: 20px;
    border: 1px solid white;
    border-radius: 5px;
}


.tickets {
    width: 100%;
    display: flex;
    flex-direction: column;
    justify-content: space-around;
    align-items: center;
    gap: 15px;
}


.booking-confirmation {
    width: 700px;
    min-height: 500px;
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