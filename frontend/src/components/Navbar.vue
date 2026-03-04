<script setup>
    
import { useRoute, RouterLink } from 'vue-router';
import { ref, reactive, watch, onMounted } from 'vue';

import { useAuth0, User } from '@auth0/auth0-vue';
import LoginButton from './LoginButton.vue';
import LogoutButton from './LogoutButton.vue';

const { user, isAuthenticated, isLoading, error } = useAuth0()

const props = defineProps(['isLoggedIn'])


const dropDownState = ref(false);
const route = useRoute();

const isActive = (currentRoutePath) => {
    return route.path === currentRoutePath;
}


const toggleDropdown = () => {
    dropDownState.value = !dropDownState.value;
    console.log(dropDownState.value);
    console.log("click");
};


function returnDropDownState() {
    return dropDownState.value === true;
}

const userType = "My profile";

watch(
  () => route.fullPath,
  () => {
    dropDownState.value = false
  }
);

watch(
    () => user?.value,
    (value) => {
        if(value) {
            console.log("----", value);
        }
    }
)


const isDesktop = true;
const showSideNav = ref(false)


const toggleSidenav = () => {
    showSideNav.value = !showSideNav.value;
}

console.log("without watcher", user["http://localhost:8000/roles"]);


</script>

<template>
        <nav>
        <div class="top">
        <h1><RouterLink to="/"><img src="../public/favicon.ico" style="vertical-align: middle; margin-right: 15px;" height="50">cinema west</RouterLink></h1>
        <div class="nav-dropdown first">
        <button v-if="isAuthenticated && !isLoading && user" @click="toggleDropdown()" class="nav-item user-btn"><i class="pi pi-user"></i>{{ user.name.slice(0,7) }}...<i v-if="returnDropDownState()" class="pi pi-chevron-up"></i><i v-else class="pi pi-chevron-down"></i></button>
        <LoginButton v-else></LoginButton>
        <ul :class="[returnDropDownState() ? 'displayDropdown' : '', 'dropdown-list']" >
            <li v-if="user && user['http://localhost:8000/roles']?.includes('admin')"><RouterLink class="nav-item" to="/admin/discover" >Admin</RouterLink></li>
            <li><RouterLink class="nav-item" to="/profile" >My profile</RouterLink></li>
            <li class="nav-item" v-if="!isAuthenticated"><LoginButton class="login-btn"/></li>
            <li class="nav-item" v-else><LogoutButton class="logout-btn"/></li>
        </ul>
        </div>
        </div>
            <ul>
                <li ><RouterLink :class="[isActive('/') ? 'activeNavLink' : '', 'nav-item']" to="/">Home</RouterLink></li>
                <li ><RouterLink :class="[isActive('/movies') ? 'activeNavLink' : '', 'nav-item']" to="/movies">Movies</RouterLink></li>
                <li ><RouterLink :class="[isActive('/about') ? 'activeNavLink' : '', 'nav-item']" to="/about">About</RouterLink></li>
            </ul>

        </nav>
        
</template>

<style scoped>



* {
    box-sizing: border-box;
}

nav {
    position: sticky;
    width: 100%;
    top: 0;
    background: #1a1a1a;
    z-index: 20;
    padding-bottom: 0;
}

header h1 {
    font-size: 35px;
}

nav ul li {
    font-size: 18px;
    width: 100%;
}

.activeNavLink {
    color: #e50914;
    border-bottom: 2px solid red;
    transition: 300ms;
}

.nav-item {
    transition: 300ms;
    margin-right: 20px;
    width: 100%;
}

.nav-item:hover,
.dropdown-list button {
    color: #e50914;
}

.nav-item:hover i {
    color: #e50914;
}

.sidenav-toggle {
    z-index: 3;
}

.pi {
    color: white;
    margin-left: 15px;
    transition: 300ms;
}

.pi-user {
    margin-right: 10px;
}

.dropdown-list {
    width: 175px;
    position: absolute;
    background-color: rgba(43, 43, 43, 0.753);
    color: white;
    padding: 10px 15px;
    border-radius: 5px;
    display: none;
    transition: 500ms;
    z-index: 2;
}

.dropdown-list li {
    display: block;
}

.nav-dropdown ul li a,
.nav-dropdown ul button {
    color: white;
    padding: 5px;
    display: block;
}

.displayDropdown {
    display: block;
}

.user-btn {
    width: 175px;
    background-color: rgba(43, 43, 43, 0.753);
    color: white;
    padding: 8px 5px;
    border-radius: 5px;
    font-size: 18px;
    border: 1px solid #404040;
    margin: 0;
}

nav {
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 100%;
    border-bottom: 1px solid #404040;
    padding: 20px 200px;
    padding-bottom: 0;
}

nav > ul {
    width: 100%;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    vertical-align: middle;
}

nav > ul li a {
    text-align: center;
    display: block;
    padding-bottom: 10px;
}


.top {
    width: 100%;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    padding: 10px;
}
.login-btn {
    padding: 8px 5px;
    border: 1px solid white;
}

@media screen and (max-width: 1200px) {
    nav {
        padding: 50px;
        padding-bottom: 0;
    }
}

</style>