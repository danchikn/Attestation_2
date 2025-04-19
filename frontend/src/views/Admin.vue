<template>
  <div>
    <h1>Admin Panel</h1>
    <button @click="logout">Logout</button>
    <ul>
      <li v-for="item in items" :key="item.id">
        {{ item.name }} — {{ item.description }}
        <button @click="deleteItem(item.id)">Delete</button>
      </li>
    </ul>
  </div>
</template>

<script>
import { mapActions, mapState } from 'vuex';
import axios from 'axios';

export default {
  name: 'AdminView',
  data() {
    return {
      items: [],
    };
  },
  computed: {
    ...mapState(['token']),
  },
  async created() {
    try {
      const response = await axios.get('http://127.0.0.1:8000/api/items/', {
        headers: { Authorization: `Bearer ${this.token}` },
      });
      this.items = response.data;
    } catch (error) {
      alert('Ошибка при загрузке данных');
    }
  },
  methods: {
    ...mapActions(['logout']),
    async deleteItem(id) {
      try {
        await axios.delete(`http://127.0.0.1:8000/api/items/${id}/`, {
          headers: { Authorization: `Bearer ${this.token}` },
        });
        this.items = this.items.filter(item => item.id !== id);
      } catch (error) {
        alert('Не удалось удалить элемент');
      }
    },
  },
};
</script>
