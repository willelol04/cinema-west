<script setup>
import { onMounted, reactive, ref } from 'vue';

const timer = ref(300);


const decrementTimer = () => {
    timer.value--;
}


const formData = reactive({
    ssn: "20040714-7377",
    password: "bruh",
    account: 52,
    price: 400,
})


onMounted(() => {
    setInterval(decrementTimer, 1000)
})




const payBooking = async () => {
    try {
        const res = await fetch("http://localhost:8000/pay-booking", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                username: formData.ssn,
                password: formData.password,
                from_account: formData.account,
                amount: formData.amount,
            }),
        });

        if (!res.ok) {
            const err = await res.json();
            alert("Payment failed: " + err.detail);
            return;
        }

        const result = await res.json();
        console.log(result);
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
        <form @submit.prevent="payBooking()">
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

input {
    border: 1px solid white;
    display: block;
}

</style>