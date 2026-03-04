
<script setup>
import { onMounted } from 'vue';
import LogoutButton from './LogoutButton.vue';

import { useAuth0, User } from '@auth0/auth0-vue';

const { user, isAuthenticated, isLoading, logout, error, getAccessTokenSilently } = useAuth0();

const props = defineProps({
    user: {
        Type: Object,
        default: {email: 'hej', sub: 'yes'},
    },
    isMyProfile: {
        Type: Boolean,
        default: false,
    }
})


const deleteUser = async () => {
        try {
        const token = await getAccessTokenSilently()
        const response = await fetch("http://localhost:8000/auth0/users/", {
            method: "DELETE",
            body: JSON.stringify(props.user),
            headers: {
                "Content-Type": "application/json",
                "authorization": `Bearer ${token}`,
            }

        });
        
        
        if (!response.ok) {
            const error = await response.json();
            alert(`Error: ${error.detail}`)
            console.log(error)
            return null
        }
        
        if(props.isMyProfile === true) {
            logout();
        }

            
        } catch(e) {
            alert(`Error: ${e}`)
            console.log(e)
        } finally {
            
        }

}



</script>

<template>
    <div class="profile">
    <div class="left">
    <i class="pi pi-user"></i>       
    </div>
    <div class="right">
        <h2 class="user-name">{{ props.user.email }}</h2>
        <LogoutButton v-if="props.isMyProfile" class="profile-logout" />
        <button class="delete-acc" @click="deleteUser()" value="Delete account">Delete Account</button>
    </div>
    </div>

    
</template>

<style scoped>

.profile {
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    gap: 20px;
    width: 100%;
    margin: 0 auto;
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
    transition: 300ms;
}

.delete-acc:hover, .profile-logout:hover {
    opacity: 60%;
}


.profile-logout {
    padding: 5px;
    border-radius: 8px;
    border: 1px solid white;
    transition: 300ms;
}

.pi-user {
    font-size: 64px;
    padding: 15px;
    border-radius: 25%;
    border: 1px solid white;
}


.user-name {
    margin-bottom: 10px;
}

</style>