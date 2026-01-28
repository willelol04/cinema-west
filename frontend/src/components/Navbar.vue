<script setup>
    
    import { useRoute, RouterLink } from 'vue-router';
    import { ref, reactive, watch } from 'vue';
    
    const props = defineProps(['userType'])
    
    
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
    
    const userType = "Min profil";
    
    watch(
      () => route.fullPath,
      () => {
        dropDownState.value = false
      }
    );
</script>

<template>
        <nav>
        <h1><RouterLink to="/">cinema west</RouterLink></h1>
            <ul>
                <li ><RouterLink :class="[isActive('/') ? 'activeNavLink' : '', 'nav-item']" to="/">Home</RouterLink></li>
                <li ><RouterLink :class="[isActive('/movies') ? 'activeNavLink' : '', 'nav-item']" to="/movies">Movies</RouterLink></li>
                <li ><RouterLink :class="[isActive('/about') ? 'activeNavLink' : '', 'nav-item']" to="/about">About</RouterLink></li>
            </ul>
        <div class="nav-dropdown">
        <button @click="toggleDropdown()" class="nav-item user-btn"><i style="color: black; margin-right: 10px;" class="pi pi-user"></i>{{ userType }}<i v-if="returnDropDownState()" style="color: black; margin-left: 10px;" class="pi pi-chevron-down"></i><i v-else style="color: black; margin-left: 10px;" class="pi pi-chevron-right"></i></button>
        <ul :class="[returnDropDownState() ? 'displayDropdown' : '', 'dropdown-list']" >
            <li><RouterLink class="nav-item" to="/admin/movies" >My profile</RouterLink></li>
            <li><a class="nav-item" href="#">My tickets</a></li>
            <li><a class="nav-item" href="#">Log out</a></li>
        </ul>
        </div>
        </nav>
        
</template>


<style scoped>

.activeNavLink {
    color: #e50914;
}

* {
    box-sizing: border-box;
}

nav {
    width: 100%;
    display: flex;
    justify-content: space-between;
    flex-direction: row;
    align-items: center;
    color: white;
    border-bottom: 1px solid #404040;
    padding-bottom: 20px;
    padding: 20px 200px;
}

header h1 {
    font-size: 35px;
}

nav ul li {
    display:inline-block;
    font-size: 18px;
}

.nav-item:not(:last-child) {
    margin-right: 10px;
}


.nav-item {
    transition: 300ms;
    margin-right: 20px;
    width: 100%;
    
}
    
.nav-item:hover {
    color: #e50914;
}
    
.user-btn {
    width: 175px;
    background-color: white;
    color: #1a1a1a;
    padding: 8px 5px;
    border-radius: 5px;
    font-size: 18px;
}
    

.dropdown-list {
    width: 175px;
    position: fixed;
    background-color: white;
    color: #1a1a1a;
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
    color: #1a1a1a;
    padding: 5px;
    display: block;
    
}
    

.displayDropdown {
    display: block;
}
    
    



    
</style>