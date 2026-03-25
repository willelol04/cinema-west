<script setup>

import { useRoute, RouterLink } from 'vue-router';
import { ref, reactive, watch, onMounted } from 'vue';

import { useAuth0, User } from '@auth0/auth0-vue';
import LoginButton from './LoginButton.vue';
import LogoutButton from './LogoutButton.vue';

const { user, isAuthenticated, isLoading, error } = useAuth0()



const dropDownState = ref(false);
const route = useRoute();

const isActive = (...validRoutes) => {
  for(const validRoute of validRoutes) {
    if(route.name === validRoute) {
      return true
    }
  }

  return false
}


const toggleDropdown = () => {
  dropDownState.value = !dropDownState.value;
};


function returnDropDownState() {
  return dropDownState.value === true;
}


watch(
    () => route.fullPath,
    () => {
      dropDownState.value = false
    }
);
</script>

<template>
  <nav id="nav">
    <div class="top">
      <h1>
        <RouterLink to="/"
        ><img
            src="../public/favicon.ico"
            style="vertical-align: middle; margin-right: 15px"
            height="50"
        /><span class="logo-text">cinema west</span></RouterLink
        >
      </h1>
      <div class="nav-dropdown">
        <button
            v-if="isAuthenticated && !isLoading && user"
            @click="toggleDropdown()"
            class="nav-item user-btn"
        >
          <i class="pi pi-user"></i>{{ user.name.slice(0,7) }}...<i
            v-if="returnDropDownState()"
            class="pi pi-chevron-up"
        ></i
        ><i v-else class="pi pi-chevron-down"></i>
        </button>
        <LoginButton v-else></LoginButton>
        <ul
            :class="[returnDropDownState() ? 'displayDropdown' : '', 'dropdown-list']"
        >
          <li>
            <RouterLink class="nav-item" to="/profile">My profile</RouterLink>
          </li>
          <li class="nav-item" v-if="!isAuthenticated">
            <LoginButton class="login-btn" />
          </li>
          <li class="nav-item" v-else><LogoutButton class="logout-btn" /></li>
        </ul>
      </div>
    </div>
    <ul>
      <li>
        <RouterLink
            :class="[isActive('home') ? 'activeNavLink' : '', 'nav-item']"
            to="/"
        >Home</RouterLink
        >
      </li>
      <li>
        <RouterLink
            :class="[isActive('movies', 'movie', 'booking') ? 'activeNavLink' : '', 'nav-item']"
            to="/movies"
        >Movies</RouterLink
        >
      </li>
      <li>
        <RouterLink
            :class="[isActive('about') ? 'activeNavLink' : '', 'nav-item']"
            to="/about"
        >About</RouterLink
        >
      </li>
      <li
          v-if="user && user['http://localhost:8000/roles']?.includes('admin')"
      >
        <RouterLink
            :class="[isActive('admin-screenings', 'admin-customers', 'admin-database', 'admin-discover') ? 'activeNavLink' : '', 'nav-item']"
            class="nav-item" to="/admin/discover">Admin</RouterLink>
      </li>
    </ul>
  </nav>
</template>

<style scoped>
nav {
  width: 100%;
  background: var(--primary-bg);
  z-index: 20;
  padding-bottom: 0;
}

nav ul li {
  font-size: 18px;
  width: 100%;
}


.nav-item {
  transition: 300ms;
  width: 100%;
  border-bottom: 2px solid transparent;
}

.activeNavLink {
  color: var(--selected-default-color);
  border-bottom: 2px solid var(--selected-default-color);
  transition: 300ms;
}

.nav-item:hover,
.dropdown-list button {
  color: var(--selected-default-color);
}

.nav-item:hover i {
  color: var(--selected-default-color);
}

.pi {
  color: var(--text-default-color);
  margin-left: 15px;
  transition: 300ms;
}

.pi-user {
  margin-right: 10px;
}

.dropdown-list {
  width: 175px;
  position: absolute;
  background-color: var(--secondary-bg);
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
  color: var(--text-default-color);
  padding: 5px;
  display: block;
}

.displayDropdown {
  display: block;
}

.user-btn {
  width: fit-content;
  background-color: var(--secondary-bg);
  color: var(--text-default-color);
  padding: 8px 5px;
  border-radius: 5px;
  font-size: 18px;
  border: 1px solid var(--default-border-bg);
  margin: 0;
}

nav {
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
  border-bottom: 1px solid var(--default-border-bg);
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
  padding-top: 40px;
}

.top {
  width: 100%;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
}
.login-btn {
  padding: 8px 5px;
  border: 1px solid var(--text-default-color);
}

@media screen and (max-width: 1200px) {
  nav {
    padding: 0;
  }

  .top {
    padding: 10px;
  }

  .logo-text {
    display: none;
  }
}
</style>
