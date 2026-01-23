<script setup>
    import MoviesList from '@/components/MoviesList.vue';

</script>


<template>
    
    <div class="search-movies">
    <h1>Admin - Movie database</h1>
    <form method="POST" @submit.prevent="onSubmit">
        <label for="movie-search">Sök efter film på TMDB:</label>
        <input type="search" id="movie-search">
        <input type="submit" value="Sök">
    </form>

    </div>
    

    <div class="added-movies">
    <h1>Already added movies:</h1>
    <MoviesList />
    </div>

</template>


<style scoped>

label {
    display: block;
}

form {
    margin-top: 20px;
}

input {
    border: 1px solid black;
    padding: 10px;

}


input[type="search"] {
    width: 50%;
}
    
</style>