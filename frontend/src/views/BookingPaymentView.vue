<script setup>
import { watch, onBeforeUnmount, onMounted, reactive, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import BeatLoader from 'vue-spinner/src/BeatLoader.vue';
import {useAuth0} from "@auth0/auth0-vue";
import { getBooking, deleteBooking } from '@/api/bookings';
import NavigateBackButton from "@/components/NavigateBackButton.vue";
import {useAppToast} from "@/use/useToast.js";
import {authenticatedFetch} from "@/api/general.js";

const {isAuthenticated, isLoading, error, getAccessTokenSilently } = useAuth0();

const {successToast, errorToast} = useAppToast();
let timerIntervalId;
const timer = ref(null);
const paymentProcessActive = ref(false);

const route = useRoute();
const router = useRouter();

const bookingResult = ref(null);
const fetchComplete = ref(false);
const paymentComplete = ref(false);

const decrementTimer = () => {
  if(!paymentProcessActive.value) {
    timer.value--;
    if(timer.value <= 0) {
      router.push('/')
    }
  }
}


const formData = reactive({
  ssn: "20040808-3252",
  password: "R0dy&a1wy*LbuV",
  account: 265217004,
  amount: 10000,
})

async function fetchBooking() {
  try {
    const token = await getAccessTokenSilently();
    bookingResult.value = await getBooking(route.params.id, token);

    formData.amount = bookingResult.value.total_price

    if(bookingResult.value.status == 'complete') {
      paymentComplete.value = true;
      router.push("/");
    } else {
      fetchComplete.value = true;

    }

  } catch(e) {
      router.push("/");
  }
}


const cancelBooking = async () => {
  try {
    const token = await getAccessTokenSilently();
    await deleteBooking({id: bookingResult.value.id, screening_id: bookingResult.value.screening_id}, token);
  } catch (e) {
    errorToast("Booking cancellation failed")
  }
};


watch(bookingResult, (newVal) => {
  if(newVal && newVal.expires_at) {
    timer.value =  Math.floor(( new Date(bookingResult.value.expires_at + "Z").getTime()  -  Date.now()) / 1000)
    timerIntervalId = setInterval(decrementTimer, 1000);
  }
})
onMounted(async () => {
  await fetchBooking();
})

onBeforeUnmount(async () => {
  if(!paymentComplete.value && bookingResult.value) {
    await cancelBooking();
  }

  clearInterval(timerIntervalId)
});




const payBooking = async () => {
  try {
    paymentProcessActive.value = true;
    fetchComplete.value = false;
    const token = await getAccessTokenSilently();
    const res = await authenticatedFetch("/api/pay-booking", token, {
      method: "POST",
      body: JSON.stringify({
        booking_id: Number(route.params.id),
        username: formData.ssn,
        password: formData.password,
        from_account: formData.account,
        amount: formData.amount,
      }),
    });

    if (!res.ok) {
      errorToast("Payment failed")
      return;
    }

    setTimeout(() => {
      fetchComplete.value = true
      paymentComplete.value = true;
      router.push({path: "/profile", query: {state: "new-booking", bookingId: route.params.id}});

    }, 1500)
  } catch (e) {
    alert("Something went wrong: " + e.message);
  }
  finally {
    paymentProcessActive.value = false;
  }
};
</script>

<template>
  <main>
    <div v-if="!paymentComplete" class="booking-confirmation">
      <span>
      <NavigateBackButton
          v-if="fetchComplete"
          :target="`/booking/`+bookingResult.screening_id"
          text="Go Back To Booking"
      >
      </NavigateBackButton>
      </span>
      <h1>Payment Information</h1>
      <form v-if="fetchComplete" @submit.prevent="payBooking()">
        <label for="social-security-nr">Social security number:</label>
        <input
            type="text"
            id="social-security-nr"
            v-model="formData.ssn"
            required
            disabled
        />
        <label for="password">Password</label>
        <input
            type="password"
            id="password"
            v-model="formData.password"
            required
            disabled
        />
        <label for="account">Account ID</label>
        <input type="number" id="account" disabled v-model="formData.account" required />
        <p>Total price: <br />{{ formData.amount }} SEK</p>
        <h3 class="timer-header"><i class="pi pi-clock"></i>Pay within: {{timer}}s</h3>
        <button type="submit">Submit payment</button>
      </form>
      <BeatLoader class="fetch-loading" :color="'#bdc7bf'" v-else />
    </div>
    <div v-else>Payment already processed.</div>
  </main>
</template>

<style scoped>

.timer-header {
  margin-top: 16px;
  margin-bottom: 16px;
  i {
    margin-right: 8px;
  }
}
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


label {
  display: block;
}

input {
  padding: 10px;
  border-radius: 6px;
  opacity: 50%;
  border: 1px solid rgba(255, 255, 255, 0.2);
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

@media screen and (max-width: 1200px) {
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
