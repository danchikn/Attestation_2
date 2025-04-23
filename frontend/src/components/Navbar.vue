<template>
  <nav class="bg-gray-800 text-white py-3 px-6 flex justify-between items-center">
    <span class="font-semibold">👤 {{ username }}</span>
    <button @click="logout" class="bg-red-500 hover:bg-red-600 px-4 py-1 rounded">
      Logout
    </button>
  </nav>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const username = ref('')

onMounted(() => {
  username.value = localStorage.getItem('user') || 'Unknown'
})

const logout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('refresh')
  localStorage.removeItem('user')
  router.push('/login')
}
</script>
