import { createRouter, createWebHistory } from 'vue-router';

import HomeView from '@/views/HomeView.vue';
import MoviesView from '@/views/MoviesView.vue';
import MovieView from '@/views/MovieView.vue';
import AdminView from '@/views/AdminView.vue';
import AdminMovies from '@/components/AdminMovies.vue';
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
            path: '/movies',
            name: 'movies',
            component: MoviesView,
        },
        {
            path: '/movie/:id',
            name: 'movie',
            component: MovieView,
        },
        {
            path: '/admin',
            component: AdminView,
            children: [
                {
                    path: 'movies', 
                    component: AdminMovies,
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
        
    ],


});

export default router;