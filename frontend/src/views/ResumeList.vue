<template>
  <div class="max-w-2xl mx-auto mt-10 p-6 border rounded shadow">
    <h1 class="text-2xl font-bold mb-4">Your Uploaded Resumes</h1>

    <div v-if="loading">Loading...</div>
    <div v-else-if="resumes.length === 0">No resumes uploaded yet.</div>

    <ul v-else class="space-y-4">
      <li
        v-for="resume in resumes"
        :key="resume.id"
        class="p-4 border rounded bg-gray-50 shadow-sm"
      >
        <p><strong>File:</strong> {{ resume.file.split('/').pop() }}</p>
        <p><strong>Parsed:</strong> {{ resume.parsed ? '✅ Yes' : '❌ No' }}</p>
        <p><strong>Uploaded:</strong> {{ formatDate(resume.created_at) }}</p>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import axios from '@/api'

const resumes = ref([])
const loading = ref(true)

onMounted(async () => {
  try {
    const res = await axios.get('resumes/')
    resumes.value = res.data
  } catch (err) {
    console.error('Error loading resumes:', err)
  } finally {
    loading.value = false
  }
})

function formatDate(dateStr) {
  const date = new Date(dateStr)
  return date.toLocaleString()
}
</script>
