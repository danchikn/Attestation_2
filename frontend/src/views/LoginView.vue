<template>
  <div class="max-w-md mx-auto mt-20 p-6 border rounded shadow">
    <h1 class="text-2xl font-bold mb-4">Login</h1>
    <form @submit.prevent="login">
      <input
        v-model="username"
        placeholder="Username"
        class="input mb-2"
      />
      <input
        v-model="password"
        type="password"
        placeholder="Password"
        class="input mb-4"
      />
      <button class="bg-blue-600 text-white py-2 px-4 rounded w-full">
        Login
      </button>
    </form>
    <p class="text-sm mt-4">
      Don’t have an account?
      <router-link to="/register">Register</router-link>
    </p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from '@/api'
import { useRouter } from 'vue-router'

const username = ref('')
const password = ref('')
const router = useRouter()

const login = async () => {
  try {
    const response = await axios.post('login/', {
      username: username.value,
      password: password.value,
    })

    // Сохраняем все нужные данные в localStorage
    localStorage.setItem('token', response.data.access)
    localStorage.setItem('refresh', response.data.refresh)
    localStorage.setItem('user', username.value)


    alert('Login successful!')
    router.push('/upload')
  } catch (err) {
    console.error('Login error:', err)
    const detail =
      err?.response?.data?.detail ||
      JSON.stringify(err?.response?.data) ||
      'Unknown error'
    alert(`Login failed: ${detail}`)
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
