<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { dataService } from '@/services/dataService'
import type { DashboardData, FilterState } from '@/types'
import AppHeader from '@/components/Header.vue'
import KeyMetrics from '@/components/KeyMetrics.vue'
import Filters from '@/components/Filters.vue'
import PriceComparison from '@/components/Charts/PriceComparison.vue'
import TrendChart from '@/components/Charts/TrendChart.vue'
import FuelDistribution from '@/components/Charts/FuelDistribution.vue'
import RegionalHeatmap from '@/components/Charts/RegionalHeatmap.vue'
import DataTable from '@/components/DataTable.vue'

const props = defineProps<{
  theme: 'dark' | 'light'
}>()

const emit = defineEmits<{
  toggleTheme: []
}>()

const data = ref<DashboardData | null>(null)
const loading = ref(true)
const error = ref<string | null>(null)

const filters = ref<FilterState>({
  region: 'All',
  fuelType: 'gasoline',
  dateRange: null,
})

onMounted(async () => {
  await loadData()
})

async function loadData() {
  loading.value = true
  error.value = null
  try {
    data.value = await dataService.loadAll()
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Failed to load data'
  } finally {
    loading.value = false
  }
}

const filteredPrices = computed(() => {
  if (!data.value) return []
  let rows = data.value.fuelPrices
  if (filters.value.region !== 'All') {
    rows = rows.filter((r) => r.region === filters.value.region)
  }
  return rows
})

const filteredTimeSeries = computed(() => {
  if (!data.value) return []
  let ts = data.value.timeSeries
  if (filters.value.dateRange) {
    const [from, to] = filters.value.dateRange
    ts = ts.filter((p) => p.date >= from && p.date <= to)
  }
  return ts
})

function reload() {
  void loadData()
}

function onFilterChange(newFilters: FilterState) {
  filters.value = newFilters
}
</script>

<template>
  <div class="dashboard">
    <AppHeader
      :theme="props.theme"
      :metadata="data?.summary?.metadata ?? null"
      @toggle-theme="emit('toggleTheme')"
    />

    <main class="dashboard-main">
      <!-- Loading -->
      <div v-if="loading" class="state-overlay">
        <div class="spinner" />
        <p>Loading dataset…</p>
      </div>

      <!-- Error -->
      <div v-else-if="error" class="state-overlay error">
        <span class="error-icon">⚠️</span>
        <p>{{ error }}</p>
        <button class="btn-retry" @click="reload">Retry</button>
      </div>

      <!-- Content -->
      <template v-else-if="data">
        <KeyMetrics :summary="data.summary" :fuel-type="filters.fuelType" />

        <Filters :filters="filters" :regions="data.summary.metadata.regions" @change="onFilterChange" />

        <section class="charts-grid">
          <PriceComparison
            :regional-stats="data.regionalStats"
            :fuel-type="filters.fuelType"
            :theme="props.theme"
          />
          <TrendChart :time-series="filteredTimeSeries" :fuel-type="filters.fuelType" :theme="props.theme" />
          <FuelDistribution :regional-stats="data.regionalStats" :theme="props.theme" />
          <RegionalHeatmap :fuel-prices="filteredPrices" :theme="props.theme" />
        </section>

        <DataTable :fuel-prices="filteredPrices" :fuel-type="filters.fuelType" />
      </template>
    </main>
  </div>
</template>

<style scoped>
.dashboard {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.dashboard-main {
  flex: 1;
  max-width: 1400px;
  margin: 0 auto;
  padding: 1.5rem 1rem 3rem;
  width: 100%;
}

.state-overlay {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  padding: 4rem;
  color: var(--text-secondary);
}

.state-overlay.error {
  color: var(--danger);
}

.error-icon {
  font-size: 3rem;
}

.spinner {
  width: 48px;
  height: 48px;
  border: 4px solid var(--border-color);
  border-top-color: var(--accent);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.btn-retry {
  padding: 0.5rem 1.5rem;
  background: var(--accent);
  color: var(--bg-primary);
  border: none;
  border-radius: var(--radius-sm);
  cursor: pointer;
  font-weight: 600;
  font-size: 0.9rem;
}

.charts-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
  margin: 1.5rem 0;
}

@media (max-width: 1024px) {
  .charts-grid {
    grid-template-columns: 1fr;
  }
}
</style>
