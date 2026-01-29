import './assets/main.css'

import { createApp } from 'vue';
import App from './App.vue';
import 'primeicons/primeicons.css';
import PrimeVue from 'primevue/config';
import Aura from '@primeuix/themes/aura';
import '@nanoandrew4/vue3-carousel-3d/dist/style.css';
import { Carousel3dPlugin } from '@nanoandrew4/vue3-carousel-3d';

import router from './router';

const app = createApp(App)

app.use(router);
app.use(PrimeVue, {
    theme: {
        preset: Aura,
        options: {
            prefix: 'p',
            darkModeSelector: 'system',
            cssLayer: false
        }
    }
 });

app.use(Carousel3dPlugin);

app.mount('#app');


//console.log("yoo")
//
//const promise = await fetch("http://localhost:8000/")
//const returnedText = await promise.json();
//console.log(returnedText.message);
//
//const fastapiParagraph = document.querySelector("#fastapi-test");
//fastapiParagraph.innerText = returnedText.message;
//