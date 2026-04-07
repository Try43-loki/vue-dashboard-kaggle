<script setup lang="ts">
import type { FilterState, FuelType, Region } from '@/types'

const props = defineProps<{
  filters: FilterState
  regions: string[]
}>()

const emit = defineEmits<{
  change: [filters: FilterState]
}>()

const fuelTypes: { value: FuelType; label: string }[] = [
  { value: 'gasoline', label: '⛽ Gasoline' },
  { value: 'diesel', label: '🚛 Diesel' },
  { value: 'lpg', label: '🔥 LPG' },
  { value: 'cng', label: '💨 CNG' },
]

function update(key: keyof FilterState, value: unknown) {
  emit('change', { ...props.filters, [key]: value })
}
</script>

<template>
  <section class="filters-bar">
    <div class="filter-group">
      <label class="filter-label">Fuel Type</label>
      <div class="btn-group">
        <button
          v-for="ft in fuelTypes"
          :key="ft.value"
          :class="['btn-filter', { active: props.filters.fuelType === ft.value }]"
          @click="update('fuelType', ft.value)"
        >
          {{ ft.label }}
        </button>
      </div>
    </div>

    <div class="filter-group">
      <label class="filter-label" for="region-select">Region</label>
      <select
        id="region-select"
        class="filter-select"
        :value="props.filters.region"
        @change="update('region', ($event.target as HTMLSelectElement).value as Region)"
      >
        <option value="All">🌍 All Regions</option>
        <option v-for="r in props.regions" :key="r" :value="r">{{ r }}</option>
      </select>
    </div>
  </section>
</template>

<style scoped>
.filters-bar {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius);
  padding: 1rem 1.25rem;
  display: flex;
  align-items: center;
  gap: 2rem;
  flex-wrap: wrap;
  margin-bottom: 0.5rem;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.filter-label {
  font-size: 0.78rem;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  white-space: nowrap;
}

.btn-group {
  display: flex;
  gap: 0.25rem;
  flex-wrap: wrap;
}

.btn-filter {
  padding: 0.35rem 0.875rem;
  border-radius: 999px;
  border: 1px solid var(--border-color);
  background: var(--bg-primary);
  color: var(--text-secondary);
  font-size: 0.82rem;
  cursor: pointer;
  transition:
    background 0.15s,
    color 0.15s,
    border-color 0.15s;
}

.btn-filter:hover {
  border-color: var(--accent);
  color: var(--accent);
}

.btn-filter.active {
  background: var(--accent);
  color: var(--bg-primary);
  border-color: var(--accent);
  font-weight: 600;
}

.filter-select {
  padding: 0.35rem 0.75rem;
  border-radius: var(--radius-sm);
  border: 1px solid var(--border-color);
  background: var(--bg-primary);
  color: var(--text-primary);
  font-size: 0.85rem;
  cursor: pointer;
  outline: none;
  transition: border-color 0.15s;
}

.filter-select:focus {
  border-color: var(--accent);
}
</style>
