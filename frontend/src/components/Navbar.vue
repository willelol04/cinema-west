<script setup>
    
    import { useRoute, RouterLink } from 'vue-router';
    
    const props = defineProps(['userType'])
    

    const isActive = (currentRoutePath) => {
        const route = useRoute();
        return route.path === currentRoutePath;
    }

</script>

<template>
    <header>
        <h1><RouterLink to="/">cinema west</RouterLink></h1>
        <nav>
            <ul>
                <li ><RouterLink :class="[isActive('/') ? 'activeNavLink' : '', 'nav-item']" to="/">Home</RouterLink></li>
                <li ><RouterLink :class="[isActive('/movies') ? 'activeNavLink' : '', 'nav-item']" to="/movies">Movies</RouterLink></li>
                <li class="nav-item"><a href="#">{{ userType }}</a></li>
            </ul>
        </nav>
    </header>
</template>


<style scoped>

.activeNavLink {
    text-decoration: underline;
    text-decoration-thickness: 2px;
    background-color: black;
    color: white
}

* {
    box-sizing: border-box;
    font-family:Arial, Helvetica, sans-serif;
}

header {
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
}

header h1 {
    font-size: 35px;
}

nav ul li {
    display:inline-block;
    font-size: 20px;
}

nav ul li:not(:last-child) {
    margin-right: 10px;
}


nav ul li a {
    padding-left: 20px;
    padding-right: 20px;
    padding-top: 10px;
    padding-bottom: 10px;
    border-radius: 10px;
    width: 100%;
    transition: 500ms;
    
}


    
</style>