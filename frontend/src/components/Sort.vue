<script setup>

import { eachMinuteOfInterval } from 'date-fns';
import {ref, onMounted, reactive, watch} from 'vue';
import {debounce} from 'lodash';

const filters = ref(null)
const fetchComplete = ref(false)
const emit = defineEmits(['update'])

const sortData = reactive({
    title: null,
    genre: null,
    rating: null,
});


const resetSortData = () => {
    sortData.title = null;
    sortData.genre = null;
    sortData.rating = null;
}

async function fetchFilters() {
    try {
    fetchComplete.value = false;
    const promise = await fetch('http://localhost:8000/filters');
    filters.value = await promise.json();
    fetchComplete.value = true;
    console.log(filters.value);
    } catch(e){
       alert(e) 
       fetchComplete.value = false;
    }
}





onMounted(async () => await fetchFilters())

const debounceUpdateData = debounce((newValue) => {
    console.log(newValue)
    emit('update', sortData)
  
}, 300)

watch(sortData, debounceUpdateData, {deep: true})

</script>
<template>
  <div v-if="fetchComplete" class="sort-container">
    <input
      type="search"
      class="search-input"
      placeholder="Search movies..."
      v-model="sortData.title"
    />

    <select class="genre-select" v-model="sortData.genre">
      <option :value="null">All genres</option>
      <option v-for="(genre, ind) in filters.genres" :value="genre.id">{{ genre.name }}</option>
    </select>

    <select class="rating-select" v-model="sortData.rating">
      <option :value="null">All ratings</option>
      <option v-for="(rating, ind) in filters.ratings" :value="rating">{{ rating }}</option>
    </select>
    <input class="reset-button" type="button" value="Reset" @click="resetSortData">
  </div>
</template>

<script setup>

</script>

<style scoped>
.sort-container {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  align-items:center;
  max-width: 600px;
  justify-content: start; 
}

.search-input {
  flex: 1 1 200px;
  padding: 0.5rem;
  border-radius: 4px;
  border: 1px solid #ccc;
}

.sort-container select {
  padding: 0.5rem;
  border-radius: 4px;
  border: 1px solid #ccc;
}
select {
  background-color: #1a1a1a;
  color: white;
}

select option {
  background-color: white;
  color: black;
}
    
.reset-button {
  padding: 0.5rem;
  border-radius: 4px;
  background-color: white;
  border: 1px solid black;
  color: black;
}

.reset-button:hover {
    cursor: pointer;
    background-color: #ccc;
    
}

option {
    border-radius: 0;
}


@media screen and (max-width:768px) {
  .sort-container {
    justify-content: space-between;
  }

  input[type="search"] {
    flex: 1 1 100%;
    width: 100%;
  }
}

</style>