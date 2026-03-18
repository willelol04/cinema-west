<script setup>

import { eachMinuteOfInterval } from 'date-fns';
import {ref, onMounted, reactive, watch} from 'vue';
import {debounce} from 'lodash';
import { normalFetch } from '@/api/general';

import {useAppToast} from "@/use/useToast.js";
const {successToast, errorToast} = useAppToast();
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
    filters.value = await normalFetch("/api/filters");
    console.log(filters.value);
    } catch(e){
      errorToast("Error fetching sort filters.")

    }
    finally {
      fetchComplete.value = true;
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
  <div v-if="filters" class="sort-container">
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
  border: 2px solid var(--default-border-bg);
  background-color: var(--primary-bg);
}

.sort-container select {
  padding: 0.5rem;
  border-radius: 4px;
  border: 2px solid var(--default-border-bg);
}
select {
  background-color: var(--secondary-bg);
  color: white;
}

select option {
  background-color: var(--secondary-bg);
  color: var(--text-default-color);
}
    
.reset-button {
  padding: 0.5rem;
  border-radius: 4px;
  background-color: white;
  border: 2px solid var(--default-border-bg);
  color: black;
}

.reset-button:hover {
    cursor: pointer;
    opacity: 60%;

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