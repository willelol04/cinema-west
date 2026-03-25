<script setup>
import { RouterView, useRoute } from 'vue-router';
import { useAuth0 } from '@auth0/auth0-vue'

const {isAuthenticated} = useAuth0;

const isActive = (currentRoutePath) => {
  const route = useRoute();
  return route.path === currentRoutePath;
}
</script>

<template v-if="isAuthenticated?.value === true">
  <main>
    <div class="dashboard-menu">
      <ul>
        <li>
          <RouterLink
              :class="[isActive('/admin/discover') ? 'activeNavLink' : '', 'dashboard-item']"
              to="/admin/discover"
          >Discover Movies<i class="pi pi-globe"></i
          ></RouterLink>
        </li>
        <li>
          <RouterLink
              :class="[isActive('/admin/database') ? 'activeNavLink' : '', 'dashboard-item']"
              to="/admin/database"
          >Our Movies<i class="pi pi-database"></i
          ></RouterLink>
        </li>
        <li>
          <RouterLink
              :class="[isActive('/admin/screenings') ? 'activeNavLink' : '', 'dashboard-item']"
              to="/admin/screenings"
          >Movie Screenings<i class="pi pi-calendar"></i
          ></RouterLink>
        </li>
        <li>
          <RouterLink
              :class="[isActive('/admin/customers') ? 'activeNavLink' : '', 'dashboard-item']"
              to="/admin/customers"
          >Customers<i class="pi pi-user"></i
          ></RouterLink>
        </li>
      </ul>
    </div>

    <RouterView class="main-content" />
  </main>
</template>

<style scoped>
.main-content {
  width: 1000px;
  margin: 0 auto;
}

main {
  width: 100vw;
  padding: 20px;
  background-color: var(--main-bg);
  min-height: 70vh;
  margin: 0 auto;
}

section {
  width: 100%;
  text-align: center;
  display: block;
  margin: 0 auto;
}

i {
  margin-left: 15px;
}

.dashboard-menu {
  width: 1000px;
  text-align: right;
  border-radius: 7px;
  margin: 0 auto 50px;
}

ul {
  width: 100%;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 15px;
}


li a {
  width: 100%;
  display: block;
}

.dashboard-item {
  width: 100%;
  padding: 20px;
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  transition: 300ms;
  opacity: 30%;
  border-radius: 10px;
  border: 1px solid #706d6d;
  background-color: var(--secondary-bg)
}

.dashboard-item:hover {
  opacity: 100%;
}

.activeNavLink {
  opacity: 100%;
}

@media screen and (max-width: 1200px) {
  .main-content {
    width: 100%;
  }

  .dashboard-menu {
    width: 100%;
    left: auto;
    margin: 0 auto;
    text-align: left;
    gap: 0;
  }

  i {
    margin-left: 0;
  }
  ul {
    gap: 0;
  }
  .dashboard-item {
    flex-direction: column-reverse;
    text-align: center;
    margin: 0;
    justify-content: center;
    font-size: 11px;
    height: 100%;
  }
}

@media screen and (max-width: 768px) {
  main {
    padding: 10px;
  }

  section {
    padding: 0;
  }

  a {
    text-overflow: clip;
  }

  .main-content {
    padding: 10px;
  }

  .dashboard-menu ul li:first-child .dashboard-item {
    border-top-right-radius: 7px;
  }

  .dashboard-menu ul li:last-child .dashboard-item {
    border-bottom-right-radius: 7px;
  }
}
</style>
