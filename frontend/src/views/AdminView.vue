<script setup>
import { RouterView, useRoute } from 'vue-router';

const isActive = (currentRoutePath) => {
    const route = useRoute();
    return route.path === currentRoutePath;
}
</script>

<template>
    <main>
        <div class="dashboard-menu">
            <ul>
                <li>
                    <RouterLink :class="[isActive('/admin/discover') ? 'activeNavLink' : '', 'dashboard-item']" to="/admin/discover">Discover Movies<i class="pi pi-globe"></i></RouterLink>
                </li>
                <li>
                    <RouterLink :class="[isActive('/admin/database') ? 'activeNavLink' : '', 'dashboard-item']" to="/admin/database" >Database<i class="pi pi-database"></i></RouterLink>
                </li>
                <li>
                    <RouterLink :class="[isActive('/admin/screenings') ? 'activeNavLink' : '', 'dashboard-item']" to="/admin/screenings">Movie Screenings<i class="pi pi-calendar"></i></RouterLink>
                </li>
                <li>
                    <RouterLink :class="[isActive('/admin/ticasdfkets') ? 'activeNavLink' : '', 'dashboard-item']" to="/admin/tickets" >Customers<i class="pi pi-user"></i></RouterLink>
                </li>
                <li>
                    <RouterLink :class="[isActive('/admin/ticasdfkets') ? 'activeNavLink' : '', 'dashboard-item']" to="/admin/tickets" >Tickets<i class="pi pi-ticket"></i></RouterLink>
                </li>
            </ul>
        </div>

        <RouterView class="main-content"/>

    </main>


</template>

<style scoped>

.main-content {
    padding: 20px 200px;
}

main {
    width: 100%;
    min-height: 700px;
    display: grid;
    grid-template-columns: 1fr 9fr;
}


section {
    width: 100%;
    text-align: center;
    display: block;
    margin: 0 auto;
}

i {
    margin-left: 15px;
}


.dashboard-menu {
    width: 300px;
    left: 0;
    text-align: center;
    border-right: 1px solid #404040;
    height: 100%;
}


ul {
    width: 100%;
}




li a {
    width: 100%;
    display: block;
    border-right: 2px solid transparent;
}
    
.dashboard-item {
    width: 100%;
    border-bottom: 1px solid #bbb4b4;
    padding: 20px;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    transition: 300ms;
    opacity: 50%;

}

.dashboard-item:hover {

    opacity: 100%;
}
    
.activeNavLink {
    border-right: 2px solid #e50914;
    opacity: 100%;

}
    
    


@media screen and (max-width: 768px) {
    main {
        display: block;
    }
    
    section {
        padding: 0;
    }
    
    .dashboard-menu {
        width: 100%;
        left: auto;
        margin: 0 auto;
        text-align:left;
    }
    
    a {
        text-overflow: clip;
    }

    .activeNavLink {
        border-bottom: 2px solid #e50914;
        border-right: none;
        opacity: 100%;

    }
    
    .main-content {
        padding: 10px;
    }
    
    
}







</style>