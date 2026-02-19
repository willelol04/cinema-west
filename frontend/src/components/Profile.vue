
<script setup>
import LogoutButton from './LogoutButton.vue';


const props = defineProps({
    user: {
        Type: Object,
        default: {email: 'hej'},
    }
})
</script>

<template>
    <div class="profile">
    <div class="left">
    <i class="pi pi-user"></i>       
    </div>
    <div class="right">
        <h2 class="user-name">{{ props.user.email }}</h2>
        <LogoutButton class="profile-logout" />
        <button class="delete-acc" value="Delete account">Delete Account</button>
    </div>
    </div>

    
</template>

<style scoped>

.profile {
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    gap: 50px;
    width: 100%;
    margin-bottom: 20px;
}

.delete-acc {
    font-size: 18px;
    font-family: 'Inter', Tahoma, Geneva, Verdana, sans-serif;
    color: #e50914;
    border: 1px solid #c90912;
    padding: 5px;
    border-radius: 8px;
    margin-left: 15px;
}


.profile-logout {
    padding: 5px;
    border-radius: 8px;
    border: 1px solid white;
}

.pi-user {
    font-size: 64px;
}


</style>