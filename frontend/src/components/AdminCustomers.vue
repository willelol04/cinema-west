<script setup>
import MoviesListAdmin from '@/components/MoviesListAdminDiscovery.vue';
import Profile from '@/components/Profile.vue';
import { ref, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import BeatLoader from 'vue-spinner/src/BeatLoader.vue';
import {useAuth0} from "@auth0/auth0-vue";
const { user, isAuthenticated, isLoading, error, getAccessTokenSilently } = useAuth0();


const search_field = defineModel('Bing');
const fetchComplete = ref(true);
const customerResults = ref([]);

const route = useRoute();
const router = useRouter();


async function fetchCustomerResults(numbers_tried = 1) { 
    const num = numbers_tried;
    fetchComplete.value = false;
    try {
    const token = await getAccessTokenSilently();
    const customerResultsPromise = await fetch(`http://localhost:8000/users/search/${route.query.q}`, {
      headers: {
        "Content-type": "application/json",
        "authorization": `Bearer ${token}`,
      }
    })
    const customerResultsObject = await customerResultsPromise.json();

    customerResults.value = customerResultsObject;

    console.log(customerResults.value);
    fetchComplete.value = true;
    console.log(fetchComplete.value)
    search_field.value = '';

    } catch(e) {
    console.log(e);
    setTimeout(() => {fetchCustomerResults(1+num)}, 20000);
    console.log("failed - ", num);
    } finally {
    console.log("quit");
    }
}
watch(
() => route.query.q,    
() => {if(route.query.q) fetchCustomerResults()},
{immediate: true},

)

const onSubmit = () => {
  router.push({query: {q: search_field.value}});
};


const cancelBooking = async (booking) => {
    try {
        const token = await getAccessTokenSilently();
        const res = await fetch("http://localhost:8000/bookings", {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({
                id: booking.id, 
                screening_id: booking.screening.id
            }),
        });

        if (!res.ok) {
            const err = await res.json();
            alert("Booking cancellation failed: ", err);
            return;
        }

        const result = await res.json();
        console.log(result);
        fetchCustomerResults();
    } catch (e) {
        console.log(e);
        alert("Something went wrong: " + e.message);
    }
};

</script>


<template>
    
    <div class="search-customers">
    <form method="GET" @submit.prevent="onSubmit">
    <label for="customer-search"><h1>Search customers:</h1></label>
        <input type="search" v-model="search_field" id="customer-search">
        <input type="submit" value="Sök">
    </form>
   <!--
   <MoviesListAdmin v-if="fetchComplete && route.query.q" :title="`Resultat för: `+ (route.query.q ? route.query.q : '')" :customers="customerResults"  @update="fetchCustomerResults"/> 
   --> 
   
   <div class="customer-results" v-if="fetchComplete">
    <div class="customer" v-for="customer in customerResults">
    <Profile class="profile" v-if="fetchComplete"  :user="{email: customer.email, sub: customer.auth_id}"/>
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
    overflow-y: scroll;
    padding: 10px;
}


.booking > button {
    background-color: rgb(65, 63, 63);
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
    border: 1px solid white;
    border-radius: 10px;
    padding: 20px;
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

input {
    padding: 10px;
    background: white;
    color: black;
    height: 50px;
    vertical-align: middle;
    border-radius: 7px;
    margin: 0;

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