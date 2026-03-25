<script setup>

</script>

<template>
  <footer>
    <div class="descriptions">
      <p>Copyright &copy; 2026 cinema west</p>
      <p>
        This service uses TMDB and the TMDB APIs but is not endorsed, certified,
        or otherwise approved by TMDB.
      </p>
    </div>
    <div class="icons">
      <img src="../assets/tmdb-logo-text.svg" />
      <ul>
        <li>
          <RouterLink to="#"><i class="pi pi-facebook"></i></RouterLink>
        </li>
        <li>
          <RouterLink to="#"><i class="pi pi-twitter"></i></RouterLink>
        </li>
        <li>
          <RouterLink to="#"><i class="pi pi-instagram"></i></RouterLink>
        </li>
      </ul>
    </div>
  </footer>
</template>

<style scoped>
.icons img {
  width: 200px;
}

.pi {
  font-size: 18px;
}

.descriptions {
  width: 100%;
}

footer {
  width: 100%;
  display: flex;
  justify-content: space-between;
  flex-direction: row;
  align-items: center;
  padding: 20px 200px;
  border-top: 1px solid var(--default-border-bg);
  border-bottom: 1px solid var(--default-border-bg);
  background-color: var(--primary-bg);
  font-size: 16px;
}

.descriptions p:first-child {
  margin-bottom: 10px;
}

.icons {
  width: 50%;
  display: flex;
  justify-content: end;
  align-items: center;
}

footer ul {
  width: 50%;
  text-align: right;
}

footer ul li {
  display: inline-block;
}

footer ul li:not(:last-child) {
  margin-right: 15px;
}

@media screen and (max-width: 1300px) {
  footer {
    flex-direction: column;
    font-size: 16px;
    padding: 32px;
  }

  .icons {
    width: 100%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 20px;
  }
}
</style>
