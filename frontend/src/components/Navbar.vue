<script setup>

</script>

<template>
    <header>
        <img src="../assets/logo-big.png" alt="cinema-west logo">
        <nav>
            <ul>
                <li class="nav-item"><a href="#">Home</a></li>
                <li class="nav-item"><a href="#">Movies</a></li>
                <li class="nav-item"><a href="#">Log in</a></li>
            </ul>
        </nav>
    </header>
</template>


<style scoped>

* {
    box-sizing: border-box;
    font-family:Arial, Helvetica, sans-serif;
}

header {
    display: flex;
    justify-content: space-between;
    flex-direction: row;
    align-items: center;



}

header img {
    height: 120px;
    width: auto;
}

nav ul li {
    display:inline-block;
    font-size: 1.2rem;
    border-radius: 5px;
    background-color: grey;
}

nav ul li:not(:last-child) {
    margin-right: 10px;
}

nav ul li a {
    padding: 5px 15px 5px 15px;
    width: 100%;
    
}

    
</style>