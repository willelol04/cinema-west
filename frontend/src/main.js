import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'

createApp(App).mount('#app')

console.log("yoo")

const promise = await fetch("http://localhost:8000/")
const returnedText = await promise.json();
console.log(returnedText.message);

const fastapiParagraph = document.querySelector("#fastapi-test");
fastapiParagraph.innerText = returnedText.message;