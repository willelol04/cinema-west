<script setup>
    import { RouterView, useRoute } from 'vue-router';

    const isActive = (currentRoutePath) => {
        const route = useRoute();
        return route.path === currentRoutePath;
    }
</script>

<template>
    <section>
        <div class="dashboard-menu">
            <ul>
                <li>
                    <RouterLink :class="[isActive('/admin/movies') ? 'activeNavLink' : '', 'dashboard-item']" to="/admin/movies">Movie Database<i class="pi pi-database"></i></RouterLink>
                </li>
                <li>
                    <RouterLink :class="[isActive('/admin/screenings') ? 'activeNavLink' : '', 'dashboard-item']" to="/admin/screenings">Movie Screenings<i class="pi pi-calendar"></i></RouterLink>
                </li>
                <li>
                    <RouterLink :class="[isActive('/admin/tickets') ? 'activeNavLink' : '', 'dashboard-item']" to="/admin/tickets" >Tickets<i class="pi pi-ticket"></i></RouterLink>
                </li>
            </ul>
        </div>
        <main>
            <RouterView />
        </main>
    </section>


</template>

<style scoped>


section {
    width: 100%;
    text-align: center;
}

i {
    margin-left: 15px;
}


.dashboard-menu {
    width: 100%;
    display: block;
    margin-bottom: 50px;
    padding: 20px 10vw;
}

.dashboard-menu li {
    display: inline-block;
}
    
.dashboard-item {
    border-bottom: 2px solid #bbb4b4;
    padding: 20px;
    width: 100%;
}
    
.activeNavLink {
    border-bottom: 2px solid #e50914;
}
    
    








</style>