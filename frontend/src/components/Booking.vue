<script setup>
    import { reactive, defineProps, onMounted} from 'vue'; // probably want to use ref instead
    
    const state = reactive({
        hideModal: false,
        selectedSeatsNumber: 0,

    });
    
    
    const toggleModal = () => {
        state.hideModal = true;
        console.log("pressed");
    }
    
    
</script>

<template>
    <div :class="[state.hideModal ? 'hideModal' : '', 'modal-container']">
        <div class="modal">
        <h3>Star Wars: The Last Jedi - 21 Januari 17.00</h3>
        <div class="screen">Bioduk</div>
        <form method="POST" @submit.prevent="toggleModal()" action="#">
        <div class="row"><input type="checkbox" name="" id="" class="seat-1"><input type="checkbox" name="" id="" class="seat-2"><input type="checkbox" name="" id="" class="seat-3"><input type="checkbox" name="" id="" class="seat-4"><input type="checkbox" name="" id="" class="seat-5"><input type="checkbox" name="" id="" class="seat-6"><input type="checkbox" name="" id="" class="seat-7"><input type="checkbox" name="" id="" class="seat-8"><input type="checkbox" name="" id="" class="seat-9"><input type="checkbox" name="" id="" class="seat-10"></div>
        <div class="row"><input type="checkbox" name="" id="" class="seat-1"><input type="checkbox" name="" id="" class="seat-2"><input type="checkbox" name="" id="" class="seat-3"><input type="checkbox" name="" id="" class="seat-4"><input type="checkbox" name="" id="" class="seat-5"><input type="checkbox" name="" id="" class="seat-6"><input type="checkbox" name="" id="" class="seat-7"><input type="checkbox" name="" id="" class="seat-8"><input type="checkbox" name="" id="" class="seat-9"><input type="checkbox" name="" id="" class="seat-10"></div>
        <div class="row"><input type="checkbox" name="" id="" class="seat-1"><input type="checkbox" name="" id="" class="seat-2"><input type="checkbox" name="" id="" class="seat-3"><input type="checkbox" name="" id="" class="seat-4"><input type="checkbox" name="" id="" class="seat-5"><input type="checkbox" name="" id="" class="seat-6"><input type="checkbox" name="" id="" class="seat-7"><input type="checkbox" name="" id="" class="seat-8"><input type="checkbox" name="" id="" class="seat-9"><input type="checkbox" name="" id="" class="seat-10"></div>
        <div class="row"><input type="checkbox" name="" id="" class="seat-1"><input type="checkbox" name="" id="" class="seat-2"><input type="checkbox" name="" id="" class="seat-3"><input type="checkbox" name="" id="" class="seat-4"><input type="checkbox" name="" id="" class="seat-5"><input type="checkbox" name="" id="" class="seat-6"><input type="checkbox" name="" id="" class="seat-7"><input type="checkbox" name="" id="" class="seat-8"><input type="checkbox" name="" id="" class="seat-9"><input type="checkbox" name="" id="" class="seat-10"></div>
        <div class="row"><input type="checkbox" name="" id="" class="seat-1"><input type="checkbox" name="" id="" class="seat-2"><input type="checkbox" name="" id="" class="seat-3"><input type="checkbox" name="" id="" class="seat-4"><input type="checkbox" name="" id="" class="seat-5"><input type="checkbox" name="" id="" class="seat-6"><input type="checkbox" name="" id="" class="seat-7"><input type="checkbox" name="" id="" class="seat-8"><input type="checkbox" name="" id="" class="seat-9"><input type="checkbox" name="" id="" class="seat-10"></div>
        <input type="submit" value="Bok xx biljetter">
        </form>
        </div>
    </div>

</template>


<style scoped>

.modal-container {
    position: fixed;
    width: 100%;
    height: 100%;
    top: 0;
    left: 0;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    background: white;

}

.modal {
    padding: 50px;
    border: 5px solid grey;
    border-radius: 5px;
}

.screen {
    width: 60%;
    display: block;
    margin: 0 auto;
    text-align: center;
    padding: 20px;
    border: 3px solid black;
    
}

.hideModal {
    display: none;
}

input[type=checkbox] {
    zoom: 2;
    margin: 5px;
}

input[type=submit] {
    background: black;
    color: white;
    padding: 25px;
    margin: 5px;
    float: right;
}

</style>