<script setup>

import { ref } from 'vue';


const emit = defineEmits(["close"]);


const props = defineProps({
    message: {
        Type: String,
        default: "Are you sure you want to delete this item?"
    },
    show: {
        Type: Boolean,
        default: false,
    }
    
    


})



const emitYes = () => (emit("yes"))
const emitCancel = () => (emit("cancel"))

</script>


<template v-if="show">
    <div class="modal-container">
        <div class="modal">
            <h3 class="modal-title">{{ props.message }}</h3>
            <div class="modal-buttons">
                <button @click="emitYes">Yes</button>
                <button @click="emitCancel">Cancel</button>
            </div>
        </div>
    </div>

</template>

<style scoped>

.modal-container {
    inset: 0;
    position: fixed;
    background-color: rgba(128, 128, 128, 0.466);
    z-index: 100;
    overflow: hidden;
}
    
.modal {
    width: 30vw;
    min-height: 200px;
    margin: 0 auto;
    margin-top: 20vh;
    background-color: #2b2b2b;
    padding: 20px;
    text-align: center;
    border-radius: 10px;
}
    
.modal-buttons {
    vertical-align: bottom;
    margin-top: 30px;
}

button {
    background-color: white;
    color: black;
    padding: 5px 20px;
    border-radius: 5px;
}

button:hover {
    opacity: 60%;
}
    
button:first-child {
    margin-right: 50px;
}

</style>