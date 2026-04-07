<script setup lang="ts">
import { ref } from 'vue'
import Dashboard from '@/views/Dashboard.vue'

const theme = ref<'dark' | 'light'>('dark')

function toggleTheme() {
  theme.value = theme.value === 'dark' ? 'light' : 'dark'
  document.documentElement.setAttribute('data-theme', theme.value)
}
</script>

<template>
  <div :data-theme="theme" class="app">
    <Dashboard :theme="theme" @toggle-theme="toggleTheme" />
  </div>
</template>

<style scoped>
.app {
  min-height: 100vh;
  background-color: var(--bg-primary);
}
</style>
