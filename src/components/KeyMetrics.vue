<script setup lang="ts">
import type { SummaryData, FuelType } from '@/types'

const props = defineProps<{
  summary: SummaryData
  fuelType: FuelType
}>()

interface Metric {
  label: string
  value: string
  sub: string
  icon: string
  color: string
}

function fmt(n: number | null | undefined) {
  return n == null ? 'N/A' : `$${n.toFixed(3)}`
}

const metrics: Metric[] = [
  {
    label: 'Avg Gasoline Price',
    value: fmt(props.summary.summary_stats.gasoline?.mean),
    sub: 'Global average (USD/L)',
    icon: '⛽',
    color: '#4ECDC4',
  },
  {
    label: 'Avg Diesel Price',
    value: fmt(props.summary.summary_stats.diesel?.mean),
    sub: 'Global average (USD/L)',
    icon: '🚛',
    color: '#45B7D1',
  },
  {
    label: 'Highest Gasoline',
    value: fmt(props.summary.highest_gasoline?.price),
    sub: props.summary.highest_gasoline
      ? `${props.summary.highest_gasoline.country} (${props.summary.highest_gasoline.region})`
      : '',
    icon: '📈',
    color: '#FF6B6B',
  },
  {
    label: 'Lowest Gasoline',
    value: fmt(props.summary.lowest_gasoline?.price),
    sub: props.summary.lowest_gasoline
      ? `${props.summary.lowest_gasoline.country} (${props.summary.lowest_gasoline.region})`
      : '',
    icon: '📉',
    color: '#34D399',
  },
  {
    label: 'Avg LPG Price',
    value: fmt(props.summary.summary_stats.lpg?.mean),
    sub: 'Global average (USD/L)',
    icon: '🔥',
    color: '#DDA0DD',
  },
  {
    label: 'Data Coverage',
    value: props.summary.metadata.regions?.length
      ? `${props.summary.metadata.regions.length} regions`
      : 'N/A',
    sub: `${props.summary.metadata.total_records?.toLocaleString()} records`,
    icon: '🌍',
    color: '#FBBF24',
  },
]
</script>

<template>
  <section class="key-metrics">
    <div v-for="m in metrics" :key="m.label" class="metric-card" :style="{ '--accent-c': m.color }">
      <div class="metric-icon">{{ m.icon }}</div>
      <div class="metric-body">
        <p class="metric-label">{{ m.label }}</p>
        <p class="metric-value">{{ m.value }}</p>
        <p class="metric-sub">{{ m.sub }}</p>
      </div>
    </div>
  </section>
</template>

<style scoped>
.key-metrics {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1rem;
  margin: 1.5rem 0;
}

.metric-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius);
  padding: 1.25rem;
  display: flex;
  align-items: flex-start;
  gap: 0.875rem;
  box-shadow: var(--shadow);
  transition: transform 0.2s;
  border-left: 3px solid var(--accent-c);
}

.metric-card:hover {
  transform: translateY(-2px);
}

.metric-icon {
  font-size: 1.75rem;
  line-height: 1;
  flex-shrink: 0;
}

.metric-body {
  min-width: 0;
}

.metric-label {
  font-size: 0.75rem;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.04em;
  margin-bottom: 0.25rem;
}

.metric-value {
  font-size: 1.4rem;
  font-weight: 700;
  color: var(--accent-c);
  line-height: 1.2;
}

.metric-sub {
  font-size: 0.75rem;
  color: var(--text-secondary);
  margin-top: 0.25rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>
