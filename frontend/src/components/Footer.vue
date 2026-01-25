<script setup>

</script>

<template>
    <footer>
        <div class="descriptions">
            <p>Copyright &copy; 2025 cinema west</p>
            <p>This service uses TMDB and the TMDB APIs but is not endorsed, certified, or otherwise approved by TMDB.</p>
        </div>
        <ul>
            <li><a href="#"><i class="pi pi-facebook"></i></a></li>
            <li><a href="#"><i class="pi pi-twitter"></i></a></li>
            <li><a href="#"><i class="pi pi-instagram"></i></a></li>
        </ul>
    </footer>
</template>


<style scoped>


footer {
    width: 100%;
    display: flex;
    justify-content: space-between;
    flex-direction: row;
    align-items: center;
    padding-left: 200px;
    padding-right: 200px;
    padding-top: 50px;
    padding-bottom: 50px;
    border-bottom: 1px solid black;
    border-top: 1px solid black;
    font-size: 20px;
}



footer ul li {
    display: inline-block;
}



footer ul li:not(:last-child) {
    margin-right: 15px;
}
    
</style>