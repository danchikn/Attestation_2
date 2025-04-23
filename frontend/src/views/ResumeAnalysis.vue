<template>
  <div class="max-w-4xl mx-auto mt-10 p-6 border rounded shadow dark:bg-gray-800 dark:text-white">
    <h1 class="text-2xl font-bold mb-6">Analyzed Resumes</h1>

    <input
      v-model="search"
      type="text"
      placeholder="Search by filename or skills..."
      class="w-full p-2 border mb-6 rounded dark:bg-gray-700 dark:border-gray-600"
    />

    <div v-if="loading" class="text-center text-gray-500">🔄 Loading resumes...</div>

    <div v-else-if="filteredResumes.length === 0" class="text-gray-400 text-center">
      No matching resumes found.
    </div>

    <div v-for="(resume, index) in filteredResumes" :key="index" class="mb-6 border-b pb-4 dark:border-gray-600">
      <h2 class="font-semibold text-lg mb-2">
        📄 {{ resume.filename }}
      </h2>

      <p><strong>Extracted Skills:</strong>
        <span v-if="resume.skills.length">{{ resume.skills.join(', ') }}</span>
        <span v-else class="text-gray-400">No skills detected</span>
      </p>

      <details class="mt-2">
        <summary class="cursor-pointer text-blue-600 dark:text-blue-400">▶ View Raw Text</summary>
        <p class="mt-2 whitespace-pre-wrap text-sm text-gray-600 dark:text-gray-300">{{ resume.raw_text }}</p>
      </details>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from '@/api'

const resumes = ref([])
const search = ref('')
const loading = ref(true)

const fetchResumes = async () => {
  try {
    const res = await axios.get('analysis/')
    resumes.value = res.data
  } catch (err) {
    console.error('Failed to fetch analyzed resumes:', err)
  } finally {
    loading.value = false
  }
}

const filteredResumes = computed(() => {
  const term = search.value.toLowerCase()
  return resumes.value.filter((r) => {
    return (
      r.filename.toLowerCase().includes(term) ||
      r.skills.some(skill => skill.toLowerCase().includes(term))
    )
  })
})

onMounted(fetchResumes)
</script>
