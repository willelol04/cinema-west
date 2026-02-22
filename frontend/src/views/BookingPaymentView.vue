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
        /*
        const tokenPromise = await fetch("https://darwinbank.duckdns.org/api/token", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: `username=${formData.ssn}&password=${formData.password}`,
            credentials: "include",
        });
        
        const tokenRes = await tokenPromise.json();
        */            
        if(true || tokenRes.ok) {
        //console.log(token.message);
        //alert(token.message);
        console.log("ye")
        try {
            const transactionPromise = await fetch("https://darwinbank.duckdns.org/api/transaction/new", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    body: JSON.stringify({
                        from_account: formData.account,
                        to_account: 63,
                        amount: formData.price,
                        transaction_type: "cinema",
                        message: "Stonks goin up for cinema west frfr",
                        amount_currency: "SEK",
                    })
                },
                credentials: "include",
            });

            const transactionRes = await transactionPromise.json();
            if(transactionRes.ok) {
            console.log(transactionRes);
            alert(transactionRes);
            } else {
                alert("Bad status transaction", transactionRes.detail)
            }
        } catch(e) {
            console.log(e)
            alert(e)
        }
    
    } else {
        alert("Bad status token: ", tokenRes.detail);
    }
    } catch(e) {
        console.log(e)
        alert(e)
    }
    return

}
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
            <label for="price">Price</label>
            <input type="number" id="price" v-model="formData.price" disabled>
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