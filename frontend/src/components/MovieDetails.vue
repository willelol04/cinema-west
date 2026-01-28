<script setup>
    
</script>

<template>
    <div class="movie-container">
    <img src="../assets/poster_examples/jack1.jpg" alt="movie-poster">
    <div class="right">
        <div class="movie-details">
            <h2 class="movie-title">Star Wars: The Last Jedi</h2>
            <h3>Längd: 2h 17min</h3>
            <h3>Genre: Sci-fi, Action</h3>
            <h3>Åldersgräns: 7+</h3>
            <h3>Språk: Engelska</h3>
        </div>
        <div class="movie-description">
            Lorem, ipsum dolor sit amet consectetur adipisicing elit. Neque quaerat soluta fuga esse nam qui id, sunt sint et vel eius sit obcaecati omnis totam assumenda perferendis consectetur voluptas veniam. Lorem ipsum dolor, sit amet consectetur adipisicing elit. Maxime et quia numquam tenetur laborum eius libero itaque, rem saepe obcaecati vel quod est debitis necessitatibus blanditiis? Non ex officia ipsam.
        </div>
        <div class="movie-screenings">
            <h3>Boka biljetter:</h3>
            <button class="movie-date-btn">14 januari 14.00</button>
            <button class="movie-date-btn">31 januari 19.00</button>
            <button class="movie-date-btn">1 februari 21.00</button>
            <button class="movie-date-btn">1 februari 21.00</button>
            <button class="movie-date-btn">1 februari 21.00</button>
            <button class="movie-date-btn">1 februari 21.00</button>
            <button class="movie-date-btn">1 februari 21.00</button>
        </div>
    </div>
    </div>
    

</template>

<style scoped>

.movie-container {
    width: 100%;
    padding-right: 200px;
    padding-left: 200px;
    display: flex;
    flex-direction: row;
    justify-content: center;
    gap: 20px;


}

.movie-container img {
    width: 350px;
    height: auto;
}

.right {
    display: flex;
    flex-direction: column;
    justify-content: space-around;
    align-items: start;


}


button {
    background-color: #2d2d2d;
    color: white;
    padding: 30px;
    border: 1px solid #404040;
}

button {
    margin: 15px;
}

.movie-date-btn:hover {
    background: #e50914;
}

.movie-date-btn {
    border-radius: 5px;
    transition: 250ms;
}

.movie-details h3 {
    opacity: 60%;
}

.movie-title {
    margin-bottom: 10px;
}

</style>