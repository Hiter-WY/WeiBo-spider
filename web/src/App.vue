<template>
  <NavBar />
  <router-view />
</template>

<script>
import NavBar from "./components/NavBar.vue";

export default {
  name: "App",
  components: {
    NavBar,
  },
};
</script>

<style>
body {
  background-image: url("./assets/leaves.webp");
  background-repeat: repeat;
  background-size: auto;
}
</style>
