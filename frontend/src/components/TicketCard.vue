<script setup>

</script>

<template>
    <div class="ticket-card">
            <img src="../assets/poster_examples/jack1.jpg">
            <div class="ticket-details">
                <h3>Jack reacher</h3>
                <p>Theatre: Salong A</p>
                <p>Seat: Seat A1</p>
                <p>Time: 26 february 14.00, 2026</p>
            </div>
            <div class="yes">
                <button><i class="pi pi-times"></i></button>
            </div>
    </div>
</template>

<style scoped>

.ticket-card {
    display: grid;
    width: 100%;
    grid-template-columns: 4fr 4fr auto;
    border-radius: 8px;
    border: 1px solid white;
    margin: 0 auto;
;
}

.ticket-card img {
    width: 100%;
    height: auto;
}

.ticket-details {
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding-left: 20px;
    gap: 10px;
}
    
button {
    padding: 10px;
}
    
button:hover {
    i {
    color: red;
    }
}

</style>