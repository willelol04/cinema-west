<script setup>

</script>

<template>
    <footer>
        <div class="descriptions">
            <p>Copyright &copy; 2025 cinema west</p>
            <p>This service uses TMDB and the TMDB APIs but is not endorsed, certified, or otherwise approved by TMDB.</p>
        </div>
        <div class="icons">
            <img src="../assets/tmdb-logo-text.svg">
        <ul>
            <li><a href="#"><i class="pi pi-facebook"></i></a></li>
            <li><a href="#"><i class="pi pi-twitter"></i></a></li>
            <li><a href="#"><i class="pi pi-instagram"></i></a></li>
        </ul>
        </div>
    </footer>
</template>


<style scoped>

.icons img {
    width: 200px;
}

.pi {
    font-size: 18px;
}

.descriptions {
    width: 100%;
}

footer {
    width: 100%;
    display: flex;
    justify-content: space-between;
    flex-direction: row;
    align-items: center;
    padding-left: 200px;
    padding-right: 200px;
    padding-top: 20px;
    padding-bottom: 50px;
    border-top: 1px solid #404040;
    border-bottom: 1px solid #404040;
    font-size: 16px;
    bottom: 0;
    text-align: left;
}


.descriptions p:first-child {
    margin-bottom: 10px;

}



.icons {
    width: 50%;
    display: flex;
    justify-content: end;
    align-items: center;
}

footer ul {
    width: 50%;
    text-align: right;
}

footer ul li {
    display: inline-block;
}


footer ul li:not(:last-child) {
    margin-right: 15px;
}

@media screen and (max-width: 1300px) {
    footer {
        flex-direction: column;
        font-size: 16px;
        padding: 32px;
    }
    
    .icons {
        width: 100%;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 20px;
    }
    

}
    
</style>