<script setup>
import { reactive, defineProps, onMounted} from 'vue'; // probably want to use ref instead
    
  
</script>

<template>
        <div class="booking">
        <form method="POST" @submit.prevent="toggleModal()" action="#">
        <h3>Star Wars: The Last Jedi - 21 Januari 17.00</h3>
        <div class="screen">Bioduk</div>
            <div class="row" v-for="n in [0,1,2,3,4]">
                <label v-for="n in ['x','x','o','x','o','x','o','x','o','x','o','x','o']" class="checkbox-label">
                    <input v-if="n === 'o'" type="checkbox" disabled>
                    <input v-else type="checkbox">
                    <span class="check">
                        <i v-if="n === 'x'" class="pi pi-circle available"></i>
                        <i v-else class="pi pi-ban"></i>
                    </span>
                </label>
            </div>
        <input type="submit" value="Bok xx biljetter">
        </form>
        </div>

</template>
<!--
            <div class="row"><span><input type="checkbox" name="" id="">x</span><span><input type="checkbox" name="" id="">x</span><span><input type="checkbox" name="" id="">x</span><span><input type="checkbox" name="" id="">x</span><span><input type="checkbox" name="" id="">x</span><span><input type="checkbox" name="" id="">x</span><span><input type="checkbox" name="" id="">x</span><span><input type="checkbox" name="" id="">x</span><span><input type="checkbox" name="" id="">x</span><span><input type="checkbox" name="" id="">x</span></div>
            <div class="row"><span><input type="checkbox" name="" id="">x</span><span><input type="checkbox" name="" id="">x</span><span><input type="checkbox" name="" id="">x</span><span><input type="checkbox" name="" id="">x</span><span><input type="checkbox" name="" id="">x</span><span><input type="checkbox" name="" id="">x</span><span><input type="checkbox" name="" id="">x</span><span><input type="checkbox" name="" id="">x</span><span><input type="checkbox" name="" id="">x</span><span><input type="checkbox" name="" id="">x</span></div>
            <div class="row"><span><input type="checkbox" name="" id="">x</span><span><input type="checkbox" name="" id="">x</span><span><input type="checkbox" name="" id="">x</span><span><input type="checkbox" name="" id="">x</span><span><input type="checkbox" name="" id="">x</span><span><input type="checkbox" name="" id="">x</span><span><input type="checkbox" name="" id="">x</span><span><input type="checkbox" name="" id="">x</span><span><input type="checkbox" name="" id="">x</span><span><input type="checkbox" name="" id="">x</span></div>
            <div class="row"><span><input type="checkbox" name="" id="">x</span><span><input type="checkbox" name="" id="">x</span><span><input type="checkbox" name="" id="">x</span><span><input type="checkbox" name="" id="">x</span><span><input type="checkbox" name="" id="">x</span><span><input type="checkbox" name="" id="">x</span><span><input type="checkbox" name="" id="">x</span><span><input type="checkbox" name="" id="">x</span><span><input type="checkbox" name="" id="">x</span><span><input type="checkbox" name="" id="">x</span></div>
            <div class="row"><span><input type="checkbox" name="" id="">x</span><span><input type="checkbox" name="" id="">x</span><span><input type="checkbox" name="" id="">x</span><span><input type="checkbox" name="" id="">x</span><span><input type="checkbox" name="" id="">x</span><span><input type="checkbox" name="" id="">x</span><span><input type="checkbox" name="" id="">x</span><span><input type="checkbox" name="" id="">x</span><span><input type="checkbox" name="" id="">x</span><span><input type="checkbox" name="" id="">x</span></div>
-->

<style scoped>

.booking {
    width: 100%;
    background-position: center; 
    background-size: cover;
    position: relative;
    padding: 20px 10vw;
}

.screen {
    width: 45%;
    border: 1px solid white;
    display: block;
    margin: 0 auto;
    font-size: 24px;
    text-align: center;
    border-radius: 10px;
    margin-bottom: 45px;
}

form {
    text-align: center;
    display: block;
    margin: 0 auto;
    padding: 20px;
    
}

.checkbox-label {
    font-size: 16px;
    padding: 0;
    height: 16px;
    width: 16px;
    margin: 10px;
}

.row {
    margin-top: 80px;
}

input[type="checkbox"] {
    position: absolute;
    opacity: 0;
    padding: 0;
    font-size: 16px;
    width: 48px;
    height: 48px;

}

.check i {
    border-radius: 5px;
    padding: 0;
    font-size: 48px;
    border-radius: 50%;
}



input[type="checkbox"]:not(:disabled):hover {
    cursor: pointer;
}
input[type="checkbox"]:disabled + .check {
    opacity: 70%;
}


input[type="checkbox"]:hover + .check> .available {
    cursor: pointer;
    background-color: grey;
    color: grey;

}
input[type="checkbox"]:checked + .check .available {
    background-color: white;
    color: white;
}




</style>