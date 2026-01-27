<script setup>
    
    import { useRoute, RouterLink } from 'vue-router';
    import { reactive } from 'vue';
    
    const props = defineProps(['userType'])
    
    
    const state = reactive({
        dropDownState: false,

    });

    const isActive = (currentRoutePath) => {
        const route = useRoute();
        return route.path === currentRoutePath;
    }
    

    const toggleDropdown = () => {
        state.dropDownState = !state.dropDownState;
        console.log(state.dropDownState);
        console.log("click");
    };
    

    function returnDropDownState() {
        return state.dropDownState;
    }
    
    const userType = "Min profil";

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
        <button @click="toggleDropdown()" class="nav-item user-btn"><i style="color: black; margin-right: 10px;" class="pi pi-user"></i>{{ userType }}<i v-if="state.dropDownState" style="color: black; margin-left: 10px;" class="pi pi-chevron-down"></i><i v-else style="color: black; margin-left: 10px;" class="pi pi-chevron-right"></i></button>
        <ul :class="[state.dropDownState ? 'displayDropdown' : '', 'dropdown-list']" >
            <li><RouterLink class="nav-item" to="/admin/movies" >Min profil</RouterLink></li>
            <li><a class="nav-item" href="#">Mina biljetter</a></li>
            <li><a class="nav-item" href="#">Logga ut</a></li>
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