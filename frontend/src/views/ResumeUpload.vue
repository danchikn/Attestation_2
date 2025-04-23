<template>
  <div class="max-w-md mx-auto mt-20 p-6 border rounded shadow">
    <h1 class="text-2xl font-bold mb-4">Upload Resume</h1>
    <form @submit.prevent="uploadResume">
      <input type="file" accept=".pdf,.docx" @change="onFileChange" class="mb-4" />
      <button :disabled="loading" class="bg-green-600 text-white py-2 px-4 rounded w-full">
        {{ loading ? "Uploading..." : "Upload" }}
      </button>
    </form>

    <p v-if="message" class="mt-4 text-center text-green-600 font-semibold">
      {{ message }}
    </p>

    <ul class="mt-6 space-y-2">
     <li v-for="res in resumes" :key="res.id" class="flex justify-between items-center">
  <span>{{ res.filename }}</span>
  <button @click="deleteResume(res.id)" class="text-red-600 hover:underline">Delete</button>
</li>

    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from '../api'

const file = ref(null)
const loading = ref(false)
const message = ref('')
const resumes = ref([])

const onFileChange = (e) => {
  file.value = e.target.files[0]
}

const uploadResume = async () => {
  if (!file.value) return alert('Choose a file first')
  loading.value = true
  message.value = ''
  const formData = new FormData()
  formData.append('file', file.value)
  try {
    await axios.post('resumes/', formData)
    message.value = 'Resume uploaded successfully!'
    await fetchResumes()
  } catch (err) {
    message.value = 'Upload failed!'
    console.error(err)
  } finally {
    loading.value = false
  }
}

const deleteResume = async (id) => {
  try {
    await axios.delete(`resumes/${id}/`)
    message.value = 'Resume deleted!'
    await fetchResumes()
  } catch (err) {
    console.error(err)
    message.value = 'Delete failed'
  }
}

const fetchResumes = async () => {
  try {
    const res = await axios.get('analysis/')
    resumes.value = res.data.map((item, index) => ({
      ...item,
      id: index + 1 // ⛔ здесь возможно стоит заменить на `item.id`, если `id` приходит с бэка
    }))
  } catch (err) {
    console.error('Failed to fetch resumes:', err)
  }
}

onMounted(fetchResumes)
</script>
