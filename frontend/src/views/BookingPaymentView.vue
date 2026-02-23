<script setup>
import { onMounted, reactive, ref } from 'vue';
import { routeLocationKey, useRoute, useRouter } from 'vue-router';
import BeatLoader from 'vue-spinner/src/BeatLoader.vue';

const timer = ref(300);

const route = useRoute();
const router = useRouter();

const bookingResult = ref(null);
const fetchComplete = ref(false);

const decrementTimer = () => {
    timer.value--;
}


const formData = reactive({
    ssn: "20040714-7377",
    password: "bruh",
    account: 52,
    amount: 2342,
})

async function fetchBooking() {
    const promise = await fetch('http://localhost:8000/bookings/'+route.params.id);
    bookingResult.value = await promise.json();
    formData.amount = bookingResult.value.total_price
    console.log(bookingResult.value);
    if(bookingResult.value.status == 'complete') {
        alert("Payment already made!");
        router.push("/");
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
        router.push("/");
    } catch (e) {
        console.log(e);
        alert("Something went wrong: " + e.message);
    }
};
</script>

<template>
    <section>
    <div class="booking-confirmation">
        <h1>Payment Information</h1>
        <form v-if="fetchComplete" @submit.prevent="payBooking()">
            <label for="social-security-nr">Social security number:</label>
            <input type="text" id="social-security-nr" v-model="formData.ssn" required>
            <label for="password">Password</label>
            <input type="password" id="password" v-model="formData.password" required>
            <label for="account">Account ID</label>
            <input type="text" id="account" v-model="formData.account" required>
            <p>Total price: <br>{{ formData.amount }} SEK</p>
            <button type="submit">Submit payment</button>
        </form>
        <BeatLoader class="fetch-loading" :color="'#bdc7bf'" v-else />
    </div>
    </section>
</template>

<style scoped>

section {
    padding: 24px;
    width: 100%;
    margin: 0 auto;
    min-height: 73vh; 
}

.fetch-loading {
    margin: 0 auto;
    text-align: center;
    color: #bdc7bf;
    padding: 100px;
}



.booking-confirmation {
    width: 700px;
    min-height: 500px;
    margin: 0 auto;
    padding: 24px 28px;
    border: 1px solid rgba(255, 255, 255, 0.12);
    text-align: center;
    border-radius: 16px;
    background-color: #2d2d2d;
}

h2 i {
    vertical-align: middle;
}

.booking-confirmation h1 {
    font-size: 24px;
}

input {
    border: 1px solid white;
}

label {
    display: block;
}

input {
  padding: 10px;
  border-radius: 6px;
  border: 1px solid rgba(255,255,255,0.2);
  background: #111;
  color: white;
}
button {
    padding: 5px 10px;
    display: block;
    width: fit-content;
    margin: 0 auto;
    margin-top: 30px;
    border-radius: 5px;
    background-color: #e50914;
    color: white;
    transition: 300ms;
}


form {
    text-align: center;
}
</style>