<script setup lang="ts">
import { computed } from 'vue'
import { Bar } from 'vue-chartjs'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  type ChartOptions,
} from 'chart.js'
import type { FuelPrice } from '@/types'

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend)

const props = defineProps<{
  fuelPrices: FuelPrice[]
  theme: 'dark' | 'light'
}>()

const textColor = computed(() => (props.theme === 'dark' ? '#94a3b8' : '#475569'))
const gridColor = computed(() => (props.theme === 'dark' ? '#334155' : '#e2e8f0'))

// Top 15 countries by gasoline price
const top15 = computed(() =>
  [...props.fuelPrices]
    .filter((p) => p.gasoline != null)
    .sort((a, b) => (b.gasoline ?? 0) - (a.gasoline ?? 0))
    .slice(0, 15)
)

const COLORS: Record<string, string> = {
  Asia: '#4ECDC4',
  Europe: '#45B7D1',
  'North America': '#96CEB4',
  'South America': '#FFEAA7',
  'Middle East': '#DDA0DD',
  Africa: '#F0A500',
  Oceania: '#FF6B6B',
}

const chartData = computed(() => ({
  labels: top15.value.map((p) => p.country),
  datasets: [
    {
      label: 'Gasoline (USD/L)',
      data: top15.value.map((p) => p.gasoline),
      backgroundColor: top15.value.map((p) => (COLORS[p.region] ?? '#888') + 'cc'),
      borderColor: top15.value.map((p) => COLORS[p.region] ?? '#888'),
      borderWidth: 2,
      borderRadius: 4,
    },
    {
      label: 'Diesel (USD/L)',
      data: top15.value.map((p) => p.diesel),
      backgroundColor: top15.value.map((p) => (COLORS[p.region] ?? '#888') + '66'),
      borderColor: top15.value.map((p) => COLORS[p.region] ?? '#888'),
      borderWidth: 1,
      borderRadius: 4,
    },
  ],
}))

const chartOptions = computed<ChartOptions<'bar'>>(() => ({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      labels: { color: textColor.value, font: { size: 11 } },
    },
    title: {
      display: true,
      text: 'Top 15 Countries — Gasoline vs Diesel Price',
      color: textColor.value,
      font: { size: 14, weight: 'bold' },
    },
    tooltip: {
      callbacks: {
        label: (ctx) =>
          ` ${ctx.dataset.label}: $${(ctx.parsed.y as number)?.toFixed(3) ?? 'N/A'}`,
      },
    },
  },
  scales: {
    x: {
      ticks: { color: textColor.value, font: { size: 10 }, maxRotation: 45 },
      grid: { color: gridColor.value },
    },
    y: {
      ticks: {
        color: textColor.value,
        callback: (v) => `$${Number(v).toFixed(2)}`,
      },
      grid: { color: gridColor.value },
    },
  },
}))
</script>

<template>
  <div class="chart-card">
    <div class="chart-wrap">
      <Bar :data="chartData" :options="chartOptions" />
    </div>
  </div>
</template>

<style scoped>
.chart-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius);
  padding: 1.25rem;
  box-shadow: var(--shadow);
}

.chart-wrap {
  position: relative;
  height: 300px;
}
</style>
