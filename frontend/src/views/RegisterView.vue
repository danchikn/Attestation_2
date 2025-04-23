<template>
  <div class="max-w-md mx-auto mt-20 p-6 border rounded shadow">
    <h1 class="text-2xl font-bold mb-4">Register</h1>
    <form @submit.prevent="register">
      <input v-model="username" placeholder="Username" class="input mb-2" />
      <input v-model="password" type="password" placeholder="Password" class="input mb-4" />
      <button class="bg-green-600 text-white py-2 px-4 rounded w-full">Register</button>
    </form>
    <p class="text-sm mt-4">Already have an account? <router-link to="/login">Login</router-link></p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from '@/api'
import { useRouter } from 'vue-router'

const username = ref('')
const password = ref('')
const router = useRouter()

const register = async () => {
  try {
    const response = await axios.post('register/', {
      username: username.value,
      password: password.value,
    })
    alert('Registration successful!')
    router.push('/login')
  } catch (err) {
    console.error('Registration error:', err)
    const detail =
      err?.response?.data?.error ||
      JSON.stringify(err?.response?.data) ||
      'Registration failed!'
    alert(`Registration failed: ${detail}`)
  }
}
</script>

<style scoped>
.input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 6px;
}
</style>
