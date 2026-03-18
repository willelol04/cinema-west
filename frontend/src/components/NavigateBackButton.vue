<script setup>


defineProps({
  target: String,
  text: String,
})
</script>

<template>
  <div class="navigate-back">
    <RouterLink :to="target"
    ><i class="pi pi-arrow-circle-left"></i>{{text}}</RouterLink
    >
  </div>
</template>

<style scoped>
.navigate-back {
  width: 100%;
  margin-bottom: 24px;
  font-size: 18px;
}

a {
  width: 100%;
  transition: 300ms;
  color: var(--text-default-color);
}

a:hover {
  color: var(--selected-default-color);
  i {
    color: var(--selected-default-color);
  }
}

i {
  margin-right: 15px;
  transition: 300ms;
}
</style>
