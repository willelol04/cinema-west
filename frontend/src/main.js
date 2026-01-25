import './assets/main.css'

import { createApp } from 'vue';
import App from './App.vue';
import 'primeicons/primeicons.css';
import router from './router';

const app = createApp(App)

app.use(router);


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