import { createRouter, createWebHistory } from 'vue-router';
import { authGuard } from '@auth0/auth0-vue';

import HomeView from '@/views/HomeView.vue';
import MoviesView from '@/views/MoviesView.vue';
import MovieView from '@/views/MovieView.vue';
import BookingView from '@/views/BookingView.vue';
import AdminView from '@/views/AdminView.vue';
import AboutView from '@/views/AboutView.vue';
import TestView from '@/views/TestView.vue';

import NotFoundView from '@/views/NotFoundView.vue';
import SignUpView from '@/views/SignUpView.vue';
import LoginView from '@/views/LoginView.vue';


import AdminDiscovery from '@/components/AdminDiscovery.vue';
import AdminMovieDB from '@/components/AdminMovieDB.vue';
import AdminScreenings from '@/components/AdminScreenings.vue';
import AdminTickets from '@/components/AdminTickets.vue';


const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: 'home',
            component: HomeView,
        },
        {
            path: '/signup',
            name: 'signup',
            component: SignUpView,
        },
        {
            path: '/login',
            name: 'login',
            component: LoginView,
        },
        {
            path: '/about',
            name: 'about',
            component: AboutView,
        },
        {
            path: '/test',
            name: 'test',
            component: TestView,
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
            path: '/about',
            name: 'about',
            component: AboutView,
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
                    path: 'tickets',
                    component: AdminTickets,
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