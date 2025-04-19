<template>
  <div>
    <h2>Login</h2>
    <form @submit.prevent="handleLogin">
      <input v-model="username" placeholder="Username" required />
      <input v-model="password" type="password" placeholder="Password" required />
      <button type="submit">Login</button>
    </form>
  </div>
</template>

<script>
export default {
  name: 'LoginView',
  data() {
    return {
      username: '',
      password: '',
    };
  },
  methods: {
    async handleLogin() {
      try {
        const credentials = {
          username: this.username,
          password: this.password,
        };
        console.log('Логин:', credentials);

        await this.$store.dispatch('login', credentials); // Vuex login action

        console.log('Успешно залогинились');

        await this.$store.dispatch('fetchUser');

        if (this.$store.state.user.role === 'admin') {
          this.$router.push('/admin');
        } else {
          alert('У вас нет доступа');
          this.$store.dispatch('logout');
        }
      } catch (error) {
        console.error('Ошибка логина:', error.response?.data || error.message);
        alert('Login failed. Проверь логин или пароль.');
      }
    },
  },
};
</script>
