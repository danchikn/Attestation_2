<template>
  <Navbar v-if="isLoggedIn" />
  <router-view />
</template>

<script setup>
import Navbar from './components/Navbar.vue'
import { ref, onMounted } from 'vue'

const isLoggedIn = ref(false)

onMounted(() => {
  isLoggedIn.value = !!localStorage.getItem('token')
})
</script>
