<script setup>
import { onBeforeUnmount, onMounted, reactive, ref } from 'vue';
import { routeLocationKey, useRoute, useRouter } from 'vue-router';
import BeatLoader from 'vue-spinner/src/BeatLoader.vue';
import {useAuth0} from "@auth0/auth0-vue";
import { getBooking, deleteBooking } from '@/api/bookings';
import NavigateBackButton from "@/components/NavigateBackButton.vue";
const {isAuthenticated, isLoading, error, getAccessTokenSilently } = useAuth0();

const timer = ref(300);

const route = useRoute();
const router = useRouter();

const bookingResult = ref(null);
const fetchComplete = ref(false);
const paymentComplete = ref(false);

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
    try {
        const token = await getAccessTokenSilently();
        bookingResult.value = await getBooking(route.params.id, token);

        formData.amount = bookingResult.value.total_price
        console.log(bookingResult.value);
        if(bookingResult.value.status == 'complete') {
            paymentComplete.value = true;
            router.push("/");
        } else {
            fetchComplete.value = true;

        }

    } catch(e) {
        if(e.error_type === "entity_not_found_error") {
          router.push("/");
        }
        else {
          console.log(e);
          alert("Something went wrong.", e.detail);
        }
    }
}


const cancelBooking = async () => {
    try {
        const token = await getAccessTokenSilently();
        await deleteBooking({id: bookingResult.value.id, screening_id: bookingResult.value.screening_id}, token);
    } catch (e) {
        console.log(e);
        alert("Something went wrong: " + e.message);
    }
};


onMounted(async () => {
    console.log(route.params.id);
    setInterval(decrementTimer, 1000);
    await fetchBooking();
})

onBeforeUnmount(async () => {
    if(!paymentComplete.value && bookingResult.value) {
         await cancelBooking();
    }
});




const payBooking = async () => {
    try {
        fetchComplete.value = false;
        const token = await getAccessTokenSilently();
        const res = await fetch("/api/pay-booking", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
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
            alert(`[${err.error_type}: ${err.detail}]`);
            return;
        }

        const result = await res.json();
        console.log(result);
        setTimeout(() => {
            fetchComplete.value = true
            paymentComplete.value = true;
            router.push({path: "/profile", query: {state: "new-booking", bookingId: route.params.id}});
        
        }, 1500)
        //alert("Payment successful!");
    } catch (e) {
        console.log(e);
        alert("Something went wrong: " + e.message);
    }
};
</script>

<template>
    <main>
    <div v-if="!paymentComplete" class="booking-confirmation">
      <NavigateBackButton v-if="fetchComplete" :target="`/booking/`+bookingResult.screening_id" text="Go Back To Booking">
      </NavigateBackButton>
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
      <div v-else>Payment already processed.</div>
    </main>
</template>

<style scoped>

main {
    width: 100%;
    margin: 0 auto;
    background-color: var(--main-bg);
    flex: 1;
    padding: 20px 0px;
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

@media screen and (max-width:1200px) {

    main {
      padding: 10px;
    }

    .booking-confirmation {
        width: 100%;
    }

    section {
        padding: 10px;
    }
}
</style>