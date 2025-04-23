import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import ResumeUpload from '../views/ResumeUpload.vue'
import ResumeAnalysis from '../views/ResumeAnalysis.vue'

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', component: LoginView },
  { path: '/register', component: RegisterView },
  { path: '/upload', component: ResumeUpload },
  { path: '/resumes', component: ResumeAnalysis },
  { path: '/analysis', component: ResumeAnalysis }


]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
