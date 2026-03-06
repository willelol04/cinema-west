import { createRouter, createWebHistory } from 'vue-router';
import { User, authGuard, useAuth0 } from '@auth0/auth0-vue';

import HomeView from '@/views/HomeView.vue';
import MoviesView from '@/views/MoviesView.vue';
import MovieView from '@/views/MovieView.vue';
import BookingView from '@/views/BookingView.vue';
import AdminView from '@/views/AdminView.vue';
import AboutView from '@/views/AboutView.vue';
import ProfileView from '@/views/ProfileView.vue';
import NotFoundView from '@/views/NotFoundView.vue';
import BookingPaymentView from '@/views/BookingPaymentView.vue';


import Callback from '@/components/Callback.vue';
import AdminDiscovery from '@/components/AdminDiscovery.vue';
import AdminMovieDB from '@/components/AdminMovieDB.vue';
import AdminScreenings from '@/components/AdminScreenings.vue';
import AdminCustomers from '@/components/AdminCustomers.vue';

const LoginGuard = (to, from) => {
    const { user, isLoading, isAuthenticated } = useAuth0();
    if(! (isAuthenticated.value && to.name !== from.name)) {
        return {name: 'home'};
    } 
                
}

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: 'home',
            component: HomeView,
        },
        {
            path: '/callback',
            name: 'redirect-callback',
            component: Callback,
        },
        {
            path: '/about',
            name: 'about',
            component: AboutView,
        },
        {
            path: '/movies',
            name: 'movies',
            component: MoviesView,
        },
        {
            path: '/movies/:id',
            name: 'movie',
            component: MovieView,
        },
        {
            path: '/booking/:id',
            name: 'booking',
            component: BookingView,
        },
        {
            path: '/payment/:id',
            name: 'booking payment',
            component: BookingPaymentView,
            beforeEnter: LoginGuard,
        },
        {
            path: '/about',
            name: 'about',
            component: AboutView,
        },
        {
            path: '/profile',
            name: 'profile',
            component: ProfileView,
            beforeEnter: LoginGuard,
        },
        {
            path: '/admin',
            name: 'admin',
            component: AdminView,
            beforeEnter: [LoginGuard, (to, from) => {
                const { user, isLoading } = useAuth0();
                if(! (user.value['http://localhost:8000/roles'].includes('admin') && to.name !== from.name)) {
                    return {name: 'home'};
                } 
                
            }
                
            ],
            children: [
                {
                    path: 'discover', 
                    name: 'admin-discover',
                    component: AdminDiscovery,
                },
                {
                    path: 'database', 
                    name: 'admin-database',
                    component: AdminMovieDB,
                },
                {
                    path: 'screenings',
                    name: 'admin-screenings',
                    component: AdminScreenings,
                },
                {
                    path: 'customers',
                    name: 'admin-customers',
                    component: AdminCustomers,
                },
            ],
        },
        {
            path: '/:catchAll(.*)',
            name: 'not-found',
            component: NotFoundView,
        },
    ],
});

export default router;