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
    padding-top: 100px;
    border-right: 1px solid #404040;
}

main {
    text-align: center;
    width: 100%;
    display: flex;
    flex-direction: column;
    justify-content: space-around;
}

.activeNavLink {
    color: #e50914;
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
    transition: 300ms;
}
    
a:hover {
    color:#e50914;
}



</style>