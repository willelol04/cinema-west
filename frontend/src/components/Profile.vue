
<script setup>
import { onMounted } from 'vue';
import LogoutButton from './LogoutButton.vue';

import { useAuth0, User } from '@auth0/auth0-vue';
import { deleteUser as deleteUserReq } from '@/api/users';

import {useAppToast} from "@/use/useToast.js";
const {successToast, errorToast} = useAppToast();

const { isAuthenticated, user, isLoading, logout, error, getAccessTokenSilently } = useAuth0();

const props = defineProps({
    user: Object,
    isMyProfile: {
        Type: Boolean,
        default: false,
    }
})

const emit = defineEmits(['delete']);

const deleteUser = async () => {
    if(confirm("Are you sure you want to delete account?")) {
        try {
            const token = await getAccessTokenSilently();
            await deleteUserReq({sub: props.user.sub}, token);
            if(props.isMyProfile === true) {
              logout({
                logoutParams: {
                  returnTo: window.location.origin
                }
              });

            }
            emit('delete');
        } catch(e) {
            errorToast("Error deleting account. Try refreshing the page.")
        }

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
    color: var(--selected-default-color);
    border: 1px solid var(--selected-default-color);
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
    border: 1px solid var(--text-default-color);
    transition: 300ms;
}

.pi-user {
    font-size: 64px;
    padding: 15px;
    border-radius: 25%;
    border: 1px solid var(--text-default-color);
}


.user-name {
    margin-bottom: 10px;
}

@media screen and (max-width: 1200px) {
    .right {
        text-align: center;
    }
}

</style>