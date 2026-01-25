<script setup>
    import { RouterView, useRoute } from 'vue-router';

    const isActive = (currentRoutePath) => {
        const route = useRoute();
        return route.path === currentRoutePath;
    }
</script>

<template>
    <div class="separator-container">
        <div class="side-nav">
            <ul>
                <li>
                    <RouterLink :class="[isActive('/admin/movies') ? 'activeNavLink' : '', '']" to="/admin/movies">Movie Database<i class="pi pi-database"></i></RouterLink>
                </li>
                <li>
                    <RouterLink :class="[isActive('/admin/screenings') ? 'activeNavLink' : '', '']" to="/admin/screenings">Movie Screenings<i class="pi pi-calendar"></i></RouterLink>
                </li>
                <li>
                    <RouterLink :class="[isActive('/admin/tickets') ? 'activeNavLink' : '', '']" to="/admin/tickets" >Tickets<i class="pi pi-ticket"></i></RouterLink>
                </li>
            </ul>
        </div>
        <main>
            <RouterView />
        </main>
    </div>


</template>

<style scoped>


.separator-container {
    width: 100%;
    min-height: 1000px;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
}

.side-nav {
    width: 15%;
    background: rgb(146, 140, 140);
    padding-top: 100px;
}

main {
    text-align: center;
    width: 100%;
    display: flex;
    flex-direction: column;
    justify-content: space-around;
}
.activeNavLink {
    background-color: rgb(110, 106, 106);
}
    
ul {
    width: 100%;
}
    
li {
    width: 100%;
}

i {
    margin-left: 20px;
}
    
li a {
    width: 100%;
    display: block;
    padding: 15px;
}
    
a:hover {
    text-decoration: none;
    background-color: rgb(110, 106, 106);
}



</style>