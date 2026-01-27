<script setup>
    import MoviesList from './MoviesList.vue';
    
</script>


<template>
    <div class="add-screening">
    <h1>Admin - Movie Screenings</h1>
    <h2>New Screening</h2>
    <form method="POST" @submit.prevent="onSubmit">
        <div class="grid">
        <label for="movies">Movie:</label>
        <select id="movies">
            <option value="HP 1">HP 1</option>
            <option value="HP 2">HP 2</option>
            <option value="HP 3">HP 3</option>
        </select>


        <label for="time">Time:</label>
        <input type="datetime-local" id="time">

        <label for="theatres">Theatre:</label>
        <select id="theatres">
            <option value="Salong Aurora">Salong Aurora</option>
            <option value="Salong Panorama">Salong Panorama</option>
            <option value="Salong Nova">Salong Nova</option>
        </select>
        
        <input type="submit" value="Add screening">
        </div>
    </form>
        
    </div>
    

    <div class="added-movies">
    <MoviesList title="Upcoming screenings:"/>
    </div>
    
</template>



<style scoped>

form {
    margin: 0 auto;
    width: 800px;
    text-align: left;

}

.grid {
    display: grid;
    grid-template-columns: 1fr 9fr;
    gap: 8px 5px;
}

label {
    padding: 10px;
    padding-left: 0px;
}

input, select, option {
    border: 1px solid black;
    padding: 10px;
    border-radius: 3px;
}

input[type="submit"] {
    grid-column: span 2;
}


</style>