import { createRouter, createWebHistory } from 'vue-router';
import { User, authGuard, useAuth0 } from '@auth0/auth0-vue';

const HomeView = () => import('@/views/HomeView.vue');
const MoviesView = () => import('@/views/MoviesView.vue')
const MovieView = () => import('@/views/MovieView.vue')
const BookingView = () => import('@/views/BookingView.vue')
const AdminView = () => import('@/views/AdminView.vue')
const AboutView = () => import('@/views/AboutView.vue')
const ProfileView = () => import('@/views/ProfileView.vue')
const NotFoundView = () => import('@/views/NotFoundView.vue')
const BookingPaymentView = () => import('@/views/BookingPaymentView.vue')


const Callback = () => import('@/components/Callback.vue')
const LoginCallback = () => import('@/components/LoginCallback.vue')
const AdminDiscovery = () => import('@/components/AdminDiscovery.vue')
const AdminMovieDB = () => import('@/components/AdminMovieDB.vue')
const AdminScreenings = () => import('@/components/AdminScreenings.vue')
const AdminCustomers = () => import('@/components/AdminCustomers.vue')

const LoginGuard = async (to, from) => {
    const { user, isLoading, isAuthenticated } = useAuth0();

    while (isLoading.value) {
      await new Promise(resolve => setTimeout(resolve, 50))
    }

    if(! (isAuthenticated.value)) {
        return from.name ? { name: from.name } : { name: 'home' };
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
          path: '/logining',
          name: 'login-callback',
          component: LoginCallback,
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
                if(! (user.value['http://localhost:8000/roles'].includes('admin'))) {
                    return from.name ? { name: from.name } : { name: 'home' };
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