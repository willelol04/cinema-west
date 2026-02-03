<script setup>
    
    import { useRoute, RouterLink } from 'vue-router';
    import { ref, reactive, watch } from 'vue';
    
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
    

    const isDesktop = true;
    const showSideNav = ref(false)
    

    const toggleSidenav = () => {
        showSideNav.value = !showSideNav.value;
    }

</script>

<template>
        <nav>
        <div v-if="isDesktop" class="desktop-nav">
        <h1><RouterLink to="/">cinema west</RouterLink></h1>
            <ul>
                <li ><RouterLink :class="[isActive('/') ? 'activeNavLink' : '', 'nav-item']" to="/">Home</RouterLink></li>
                <li ><RouterLink :class="[isActive('/movies') ? 'activeNavLink' : '', 'nav-item']" to="/movies">Movies</RouterLink></li>
                <li ><RouterLink :class="[isActive('/about') ? 'activeNavLink' : '', 'nav-item']" to="/about">About</RouterLink></li>
            </ul>
        <div class="nav-dropdown">
        <button @click="toggleDropdown()" class="nav-item user-btn">{{ userType }}<i v-if="returnDropDownState()" class="pi pi-chevron-down"></i><i v-else class="pi pi-chevron-right"></i></button>
        <ul :class="[returnDropDownState() ? 'displayDropdown' : '', 'dropdown-list']" >
            <li><RouterLink class="nav-item" to="/admin/movies" >My profile</RouterLink></li>
            <li><a class="nav-item" href="#">My tickets</a></li>
            <li v-if="props.isLoggedIn"><a class="nav-item" href="#">Log out</a></li>
            <li v-else ><RouterLink :class="[isActive('/login') ? 'activeNavLink' : '', 'nav-item']" to="/login">Log in/Sign up</RouterLink></li>
        </ul>
        </div>

        </div>
        <div v-else class="mobile-nav">
        <h1><RouterLink to="/">cinema west</RouterLink></h1>
            <button v-if="!showSideNav" @click="toggleSidenav()"><i class="pi pi-bars sidenav-toggle"></i></button>
            <button v-else @click="toggleSidenav()"><i class="pi pi-times sidenav-toggle"></i></button>
        </div>
        </nav>
        <Transition name="fade">
        <div v-if="showSideNav" class="side-nav">
            <ul>
                <li><RouterLink to="#">Home</RouterLink></li>
                <li><RouterLink to="#">Movies</RouterLink></li>
                <li><RouterLink to="#">About</RouterLink></li>
                <li><RouterLink to="#">My profile</RouterLink></li>
                <li><RouterLink to="#">Log out</RouterLink></li>
            </ul>
        </div>
        </Transition>
        
</template>


<style scoped>

.sidenav-toggle {
    z-index: 3;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
.side-nav {
    height: 100vh;
    width: 400px;
    position:fixed;
    top: 0;
    left: 0;
    text-align: center;
    background-color: black;
    z-index: 1;
}

.side-nav li {
    display: block;
}

.activeNavLink {
    color: #e50914;
}

* {
    box-sizing: border-box;
}

.desktop-nav {
    width: 100%;
    display: flex;
    justify-content: space-between;
    flex-direction: row;
    align-items: center;
    color: white;
    border-bottom: 1px solid #404040;
    padding-bottom: 20px;
    padding: 20px 20vw;
}

header h1 {
    font-size: 35px;
}

nav ul li {
    display:inline-block;
    font-size: 18px;
}


.mobile-nav {
    width: 100%;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    padding: 20px 20vw;
}



li .nav-item {
    transition: 300ms;
    margin-right: 20px;
    width: 100%;
    
}
    
.nav-item:hover {
    color: #e50914;
}
    

.pi {
    color: white;
    margin-left: 15px;
    
}
    

.dropdown-list {
    width: 175px;
    position: fixed;
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
    border-top-right-radius: 0px;
    border-top-right-radius: 0px;
    
}

.nav-dropdown ul li a {
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



    
</style>