<script setup lang="ts">
import { ref, computed } from 'vue'
import type { FuelPrice, FuelType } from '@/types'

const props = defineProps<{
  fuelPrices: FuelPrice[]
  fuelType: FuelType
}>()

const search = ref('')
const sortKey = ref<keyof FuelPrice>('country')
const sortDir = ref<1 | -1>(1)
const page = ref(1)
const pageSize = 15

function toggleSort(key: keyof FuelPrice) {
  if (sortKey.value === key) {
    sortDir.value = sortDir.value === 1 ? -1 : 1
  } else {
    sortKey.value = key
    sortDir.value = 1
  }
  page.value = 1
}

const filtered = computed(() => {
  const q = search.value.toLowerCase()
  return props.fuelPrices.filter(
    (r) =>
      r.country.toLowerCase().includes(q) || r.region.toLowerCase().includes(q)
  )
})

const sorted = computed(() =>
  [...filtered.value].sort((a, b) => {
    const av = a[sortKey.value]
    const bv = b[sortKey.value]
    if (av == null) return 1
    if (bv == null) return -1
    return av < bv ? -sortDir.value : av > bv ? sortDir.value : 0
  })
)

const totalPages = computed(() => Math.max(1, Math.ceil(sorted.value.length / pageSize)))

const paged = computed(() => {
  const start = (page.value - 1) * pageSize
  return sorted.value.slice(start, start + pageSize)
})

function fmt(v: number | null) {
  return v == null ? '—' : `$${v.toFixed(3)}`
}

function priceClass(v: number | null) {
  if (v == null) return ''
  if (v < 0.6) return 'low'
  if (v > 1.8) return 'high'
  return ''
}

function sortIcon(key: keyof FuelPrice) {
  if (sortKey.value !== key) return '⇅'
  return sortDir.value === 1 ? '↑' : '↓'
}
</script>

<template>
  <section class="data-table-section">
    <div class="table-header">
      <h2 class="table-title">📋 Country Data</h2>
      <div class="table-controls">
        <input
          v-model="search"
          class="search-input"
          placeholder="Search country or region…"
          @input="page = 1"
        />
        <span class="table-count">{{ filtered.length }} countries</span>
      </div>
    </div>

    <div class="table-wrap">
      <table class="data-table">
        <thead>
          <tr>
            <th @click="toggleSort('country')">Country {{ sortIcon('country') }}</th>
            <th @click="toggleSort('region')">Region {{ sortIcon('region') }}</th>
            <th @click="toggleSort('gasoline')">Gasoline {{ sortIcon('gasoline') }}</th>
            <th @click="toggleSort('diesel')">Diesel {{ sortIcon('diesel') }}</th>
            <th @click="toggleSort('lpg')">LPG {{ sortIcon('lpg') }}</th>
            <th @click="toggleSort('cng')">CNG {{ sortIcon('cng') }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="row in paged" :key="row.country">
            <td class="bold">{{ row.country }}</td>
            <td>
              <span class="region-badge">{{ row.region }}</span>
            </td>
            <td :class="['price', priceClass(row.gasoline)]">{{ fmt(row.gasoline) }}</td>
            <td :class="['price', priceClass(row.diesel)]">{{ fmt(row.diesel) }}</td>
            <td :class="['price', priceClass(row.lpg)]">{{ fmt(row.lpg) }}</td>
            <td :class="['price', priceClass(row.cng)]">{{ fmt(row.cng) }}</td>
          </tr>
          <tr v-if="paged.length === 0">
            <td colspan="6" class="empty">No results found</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="totalPages > 1" class="pagination">
      <button :disabled="page === 1" class="page-btn" @click="page--">‹ Prev</button>
      <span class="page-info">Page {{ page }} of {{ totalPages }}</span>
      <button :disabled="page === totalPages" class="page-btn" @click="page++">Next ›</button>
    </div>
  </section>
</template>

<style scoped>
.data-table-section {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius);
  padding: 1.25rem;
  box-shadow: var(--shadow);
  margin-top: 0.5rem;
}

.table-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: 1rem;
  flex-wrap: wrap;
}

.table-title {
  font-size: 1rem;
  font-weight: 700;
  color: var(--text-primary);
}

.table-controls {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.search-input {
  padding: 0.4rem 0.75rem;
  border-radius: var(--radius-sm);
  border: 1px solid var(--border-color);
  background: var(--bg-primary);
  color: var(--text-primary);
  font-size: 0.85rem;
  width: 220px;
  outline: none;
  transition: border-color 0.15s;
}

.search-input:focus {
  border-color: var(--accent);
}

.table-count {
  font-size: 0.78rem;
  color: var(--text-muted);
  white-space: nowrap;
}

.table-wrap {
  overflow-x: auto;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.85rem;
}

.data-table th {
  text-align: left;
  padding: 0.625rem 0.875rem;
  background: var(--bg-primary);
  color: var(--text-muted);
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  cursor: pointer;
  user-select: none;
  white-space: nowrap;
  border-bottom: 1px solid var(--border-color);
  transition: color 0.15s;
}

.data-table th:hover {
  color: var(--accent);
}

.data-table td {
  padding: 0.6rem 0.875rem;
  border-bottom: 1px solid var(--border-color);
  color: var(--text-secondary);
}

.data-table tbody tr:hover td {
  background: var(--bg-secondary);
}

.bold {
  font-weight: 600;
  color: var(--text-primary) !important;
}

.region-badge {
  font-size: 0.72rem;
  padding: 0.2rem 0.5rem;
  border-radius: 999px;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  white-space: nowrap;
}

.price {
  font-family: 'Courier New', monospace;
  font-weight: 500;
}

.price.high {
  color: #ff6b6b;
}

.price.low {
  color: #34d399;
}

.empty {
  text-align: center;
  color: var(--text-muted);
  padding: 2rem;
}

.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  margin-top: 1rem;
}

.page-btn {
  padding: 0.35rem 0.875rem;
  border-radius: var(--radius-sm);
  border: 1px solid var(--border-color);
  background: var(--bg-primary);
  color: var(--text-primary);
  cursor: pointer;
  font-size: 0.85rem;
  transition: border-color 0.15s;
}

.page-btn:hover:not(:disabled) {
  border-color: var(--accent);
  color: var(--accent);
}

.page-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.page-info {
  font-size: 0.82rem;
  color: var(--text-muted);
}
</style>
