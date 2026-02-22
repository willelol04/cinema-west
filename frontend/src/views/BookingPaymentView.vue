<script setup>
import { onMounted, reactive, ref } from 'vue';
import { routeLocationKey, useRoute } from 'vue-router';
import BeatLoader from 'vue-spinner/src/BeatLoader.vue';

const timer = ref(300);

const route = useRoute();

const bookingResult = ref(null);
const fetchComplete = ref(false);

const decrementTimer = () => {
    timer.value--;
}


const formData = reactive({
    ssn: "20040714-7377",
    password: "bruh",
    account: 52,
    amount: 100000000000000,
})

async function fetchBooking() {
    const promise = await fetch('http://localhost:8000/bookings/'+route.params.id);
    bookingResult.value = await promise.json();
    formData.amount = bookingResult.value.total_price
    console.log(bookingResult.value);
    if(bookingResult.value.status == 'complete') {
        alert("Payment already made!")
    } else {
        fetchComplete.value = true;

    }
}



onMounted(async () => {
    setInterval(decrementTimer, 1000)
    await fetchBooking()
})




const payBooking = async () => {
    try {
        fetchComplete.value = false;
        const res = await fetch("http://localhost:8000/pay-booking", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                booking_id: route.params.id, 
                username: formData.ssn,
                password: formData.password,
                from_account: formData.account,
                amount: formData.amount,
            }),
        });

        if (!res.ok) {
            const err = await res.json();
            alert("Payment failed: " + err.detail.detail);
            return;
        }

        const result = await res.json();
        console.log(result);
        fetchComplete.value = true;
        alert("Payment successful!");
    } catch (e) {
        console.log(e);
        alert("Something went wrong: " + e.message);
    }
};
</script>

<template>
    <div class="booking-confirmation">
        <h1>Congratulations User! You have successfully booked seat(s)! {{ timer }}</h1>
        <form v-if="fetchComplete" @submit.prevent="payBooking()">
            <label for="social-security-nr">Social security number:</label>
            <input type="text" id="social-security-nr" v-model="formData.ssn">
            <label for="password">Password</label>
            <input type="password" id="password" v-model="formData.password">
            <label for="account">Account ID</label>
            <input type="text" id="account" v-model="formData.account">
            <label for="amount">Price</label>
            <input type="number" id="amount" v-model="formData.amount" disabled>
            <input type="submit">
            {{ formData }}
        </form>
        <BeatLoader class="fetch-loading" :color="'#bdc7bf'" v-else />
    </div>
</template>

<style scoped>

.fetch-loading {
    margin: 0 auto;
    text-align: center;
    color: #bdc7bf;
    padding: 100px;
}

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

input {
    border: 1px solid white;
    display: block;
}

</style>