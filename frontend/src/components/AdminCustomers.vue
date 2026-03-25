<script setup>
import Profile from '@/components/Profile.vue';
import { ref } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import BeatLoader from 'vue-spinner/src/BeatLoader.vue';
import Search from '@/components/Search.vue'
import { searchUsers} from '../api/users';
import { deleteBooking } from '../api/bookings';
import {useAuth0 } from '@auth0/auth0-vue';
import {useAppToast} from "@/use/useToast.js";

const { user, isAuthenticated, isLoading, error, getAccessTokenSilently } = useAuth0();
const fetchComplete = ref(true);
const customerResults = ref([]);

const route = useRoute();
const router = useRouter();

const {successToast, errorToast} = useAppToast();

async function fetchCustomerResults() {
  if(route.query.q) {

    fetchComplete.value = false;
    try {
      const token = await getAccessTokenSilently();
      customerResults.value = await searchUsers(route.query.q, token);

    } catch(e) {
      errorToast("Error fetching customers from database. Try refreshing the page.")
    }
    finally {
      fetchComplete.value = true;
    }
  }
}


const cancelBooking = async (booking_cancel, customer) => {
  try {
    if (confirm("Do you want to cancel the booking?")) {
      const token = await getAccessTokenSilently();
      await deleteBooking({id: booking_cancel.id, screening_id: booking_cancel.screening.id}, token)
      customer.bookings = customer.bookings.filter(booking => (booking.id !== booking_cancel.id))
      successToast("Booking cancelled.")
    }
  } catch (e) {
    errorToast("Error cancelling booking. Try refreshing the page.")
  }
};

const handleCustomerDelete = (customer_delete) => {
  customerResults.value = customerResults.value.filter(customer => (customer.sub !== customer_delete.sub))
  successToast("User deleted successfully.")


}

</script>


<template>

  <div class="search-customers">
    <h1>Customers</h1>
    <Search :header="`Search Customers:`" :searchFunction="fetchCustomerResults"/>

    <div class="customer-results" v-if="fetchComplete">
      <div class="customer" v-for="customer in customerResults" :key="customer.id">
        <Profile class="profile" v-if="fetchComplete"  @delete="handleCustomerDelete" :user="{email: customer.email, sub: customer.sub}"/>
        <h3>Bookings:</h3>
        <ul class="bookings">
          <li class="booking" v-for="booking in customer.bookings" :key="booking.id">
            <span class="booking-name">
            {{ booking.tickets.length}} tickets to {{ booking.screening.movie.title }}, Booking ID:{{ booking.id }}
            </span>
            <button @click="cancelBooking(booking, customer)" class="delete-booking"><i class="pi pi-times"></i>Cancel</button>
          </li>
        </ul>
      </div>
    </div>


    <BeatLoader v-if="!fetchComplete" class="fetch-loading" :color="'#bdc7bf'"/>
    <div v-if="fetchComplete && customerResults.length === 0 && route.query.q" class="empty">No results were found</div>
  </div>

</template>


<style scoped>

h1 {
  margin-bottom: 24px;
  margin-top: 24px;
}

.booking {
  width: 100%;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  padding-top: 5px;
  padding-bottom: 5px;
  border-top: 1px solid white;
}

.bookings {
  width: 100%;
  height: 200px;
  overflow-y: auto;
  padding: 10px;
}


.booking > button {
  background-color: var(--selected-default-color);
  padding: 5px;
}

.customer-results {
  width: 100%;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 25px 25px;

}

.customer {
  border: 1px solid var(--default-border-bg);
  border-radius: 10px;
  padding: 20px;

  background-color: var(--secondary-bg);
}

.profile {
  width: 100%;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  width: fit-content;
}

.fetch-loading {
  margin-top: 200px;
  text-align: center;
}

h1 {
  display: block;
}




form {
  margin-bottom: 50px;
}



.booking-name {
  width: 100%;
}

@media screen and (max-width: 1200px) {
  .customer {
    width: 100%;
  }

  .customer-results {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;

  }


}

</style>
