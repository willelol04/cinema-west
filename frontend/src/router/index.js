import { createRouter, createWebHistory } from 'vue-router';
import { authGuard } from '@auth0/auth0-vue';

import HomeView from '@/views/HomeView.vue';
import MoviesView from '@/views/MoviesView.vue';
import MovieView from '@/views/MovieView.vue';
import BookingView from '@/views/BookingView.vue';
import AdminView from '@/views/AdminView.vue';
import AboutView from '@/views/AboutView.vue';
import ProfileView from '@/views/ProfileView.vue';
import NotFoundView from '@/views/NotFoundView.vue';


import AdminDiscovery from '@/components/AdminDiscovery.vue';
import AdminMovieDB from '@/components/AdminMovieDB.vue';
import AdminScreenings from '@/components/AdminScreenings.vue';
import AdminCustomers from '@/components/AdminCustomers.vue';
import BookingPaymentView from '@/views/BookingPaymentView.vue';


const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: 'home',
            component: HomeView,
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
            beforeEnter: authGuard,
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
            beforeEnter: authGuard,
        },
        {
            path: '/admin',
            component: AdminView,
            beforeEnter: authGuard,
            children: [
                {
                    path: 'discover', 
                    component: AdminDiscovery,
                },
                {
                    path: 'database', 
                    component: AdminMovieDB,
                },
                {
                    path: 'screenings',
                    component: AdminScreenings,
                },
                {
                    path: 'customers',
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