<script setup lang="ts">
import type { DataMetadata } from '@/types'

const props = defineProps<{
  theme: 'dark' | 'light'
  metadata: DataMetadata | null
}>()

const emit = defineEmits<{
  toggleTheme: []
}>()
</script>

<template>
  <header class="app-header">
    <div class="header-inner">
      <div class="header-brand">
        <span class="header-icon">⛽</span>
        <div>
          <h1 class="header-title">World vs Asia Fuel Prices</h1>
          <p class="header-subtitle">
            Interactive EDA Dashboard &nbsp;·&nbsp;
            <a
              href="https://www.kaggle.com/datasets/zkskhurram/world-vs-asia-fuel-prices"
              target="_blank"
              rel="noopener noreferrer"
            >
              Kaggle Dataset
            </a>
          </p>
        </div>
      </div>

      <div class="header-meta">
        <template v-if="props.metadata">
          <span class="meta-badge">
            📊 {{ props.metadata.total_records.toLocaleString() }} records
          </span>
          <span class="meta-badge">
            🗓️ {{ props.metadata.date_range?.[0] }} – {{ props.metadata.date_range?.[1] }}
          </span>
          <span class="meta-badge">
            🌍 {{ props.metadata.regions?.length }} regions
          </span>
        </template>

        <button
          class="theme-toggle"
          :title="`Switch to ${props.theme === 'dark' ? 'light' : 'dark'} mode`"
          @click="emit('toggleTheme')"
        >
          {{ props.theme === 'dark' ? '☀️' : '🌙' }}
        </button>
      </div>
    </div>
  </header>
</template>

<style scoped>
.app-header {
  background: var(--bg-secondary);
  border-bottom: 1px solid var(--border-color);
  position: sticky;
  top: 0;
  z-index: 100;
  backdrop-filter: blur(8px);
}

.header-inner {
  max-width: 1400px;
  margin: 0 auto;
  padding: 1rem 1.5rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  flex-wrap: wrap;
}

.header-brand {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.header-icon {
  font-size: 2rem;
}

.header-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--accent);
  line-height: 1.2;
}

.header-subtitle {
  font-size: 0.8rem;
  color: var(--text-muted);
}

.header-subtitle a {
  color: var(--accent-2);
}

.header-meta {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.meta-badge {
  font-size: 0.75rem;
  padding: 0.25rem 0.625rem;
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: 999px;
  color: var(--text-secondary);
  white-space: nowrap;
}

.theme-toggle {
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: 999px;
  width: 36px;
  height: 36px;
  cursor: pointer;
  font-size: 1.1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: border-color 0.2s;
}

.theme-toggle:hover {
  border-color: var(--accent);
}

@media (max-width: 640px) {
  .meta-badge {
    display: none;
  }
}
</style>
