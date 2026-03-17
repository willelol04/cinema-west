<script setup>
import MoviesListAdmin from '@/components/MoviesListAdminDiscovery.vue';
import Profile from '@/components/Profile.vue';
import { ref, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import BeatLoader from 'vue-spinner/src/BeatLoader.vue';
import {debounce} from 'lodash';
import Search from '@/components/Search.vue'

import { Auth0Plugin, useAuth0, User } from '@auth0/auth0-vue';
const { user, isAuthenticated, isLoading, error, getAccessTokenSilently, checkSession } = useAuth0();

import { searchUsers} from '../api/users';
import { deleteBooking } from '../api/bookings';

const fetchComplete = ref(true);
const customerResults = ref([]);

const route = useRoute();
const router = useRouter();


async function fetchCustomerResults() { 
    fetchComplete.value = false;
    try {
        const token = await getAccessTokenSilently();
        customerResults.value = await searchUsers(route.query.q, token);

        fetchComplete.value = true;

    } catch(e) {
        console.log(e);
    } 
}


const cancelBooking = async (booking) => {
    try {
        const token = await getAccessTokenSilently();
        await deleteBooking({id: booking.id, screening_id: booking.screening.id}, token)
        await fetchCustomerResults();
    } catch (e) {
        console.log(e);
    }
};

</script>


<template>
    
    <div class="search-customers">
      <h1>Customers</h1>
      <Search :header="`Search Customers:`" :searchFunction="fetchCustomerResults"/>

   <div class="customer-results" v-if="fetchComplete">
    <div class="customer" v-for="customer in customerResults">
    <Profile class="profile" v-if="fetchComplete"  @delete="fetchCustomerResults" :user="{email: customer.email, sub: customer.sub}"/>
    <h3>Bookings:</h3>
    <ul class="bookings">
        <li class="booking" v-for="booking in customer.bookings"><span class="booking-name"> {{ booking.tickets.length}} tickets to {{ booking.screening.movie.title }}, Booking ID:{{ booking.id }}</span><button @click="cancelBooking(booking)" class="delete-booking"><i class="pi pi-times"></i>Cancel</button></li>
    </ul>
    </div>
   </div>

   
    <BeatLoader v-if="!fetchComplete" class="fetch-loading" :color="'#bdc7bf'"/>
    <div v-if="fetchComplete && customerResults.length === 0 && route.query.q" class="empty">No results were found</div>
    </div>
    

    
    <!--
    <MoviesList title="Already added movies:"/>
    -->

</template>


<style scoped>

h1 {
  text-align: center;
  margin-bottom: 20px;
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
    display: flex;
    flex-direction: row;
    align-items: start;
    justify-content: start;
    flex-wrap: wrap;
    gap: 50px;
    
}

.customer {
    width: 500px;
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


input[type="search"] {
    width: 400px;
    font-size: 16px;
    font-family:sans-serif;
    border-radius: 7px;
    font-weight: 100;

}
      
.booking-name {
    width: 100%;
}
      
@media screen and (max-width: 1200px) {
    .customer {
      width: 100%;
    }

    .customer-results {
        justify-content: center;
        align-items: center;
        flex-direction: column;

    }

    input[type="search"] { 
        width: 90%;
    }
    
    input[type="submit"] {
        width: 10%;
    }
    
}
    
</style>