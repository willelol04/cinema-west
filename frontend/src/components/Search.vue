<script setup>

import {debounce} from 'lodash';
import {watch} from "vue";
import {useRoute, useRouter} from "vue-router";


const props = defineProps({
  header: {
    Type: String,
    default: 'Search',
  },
  searchFunction: Function
})

const search_field = defineModel('Bing');

const route = useRoute();
const router = useRouter();
const debounceUpdateData = debounce((newValue) => {
  console.log(newValue)
  if (search_field.value) {
    router.push({query: {q: search_field.value}});
  }

}, 300)

watch(search_field, debounceUpdateData, {deep: true})

watch(
    () => route.query.q,
    async () => {if(route.query.q) await props.searchFunction()},
    {immediate: true},

)
</script>

<template>
  <form method="GET" @submit.prevent>
    <label for="search"></label>
    <input type="search" v-model="search_field" id="search" :placeholder="props.header">
  </form>
</template>

<style scoped>

input {
  padding: 10px;
  background: var(--secondary-bg);
  color: white;
  height: 50px;
  vertical-align: middle;
  border: 1px solid var(--default-border-bg);
  border-radius: 7px;
  margin: 0;
  width: 100%;

}
</style>