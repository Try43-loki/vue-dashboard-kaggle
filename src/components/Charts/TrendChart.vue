<script setup lang="ts">
import { computed } from 'vue'
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler,
  type ChartOptions,
} from 'chart.js'
import type { TimeSeriesPoint, FuelType } from '@/types'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, Filler)

const props = defineProps<{
  timeSeries: TimeSeriesPoint[]
  fuelType: FuelType
  theme: 'dark' | 'light'
}>()

const textColor = computed(() => (props.theme === 'dark' ? '#94a3b8' : '#475569'))
const gridColor = computed(() => (props.theme === 'dark' ? '#334155' : '#e2e8f0'))

const worldKey = computed(() => `${props.fuelType}_world` as keyof TimeSeriesPoint)
const asiaKey = computed(() => `${props.fuelType}_asia` as keyof TimeSeriesPoint)

const chartData = computed(() => ({
  labels: props.timeSeries.map((p) => p.date),
  datasets: [
    {
      label: 'World Average',
      data: props.timeSeries.map((p) => p[worldKey.value] as number),
      borderColor: '#4ECDC4',
      backgroundColor: 'rgba(78,205,196,0.12)',
      fill: true,
      tension: 0.4,
      pointRadius: 3,
    },
    {
      label: 'Asia Average',
      data: props.timeSeries.map((p) => p[asiaKey.value] as number),
      borderColor: '#FF6B6B',
      backgroundColor: 'rgba(255,107,107,0.12)',
      fill: true,
      tension: 0.4,
      pointRadius: 3,
    },
  ],
}))

const chartOptions = computed<ChartOptions<'line'>>(() => ({
  responsive: true,
  maintainAspectRatio: false,
  interaction: { mode: 'index', intersect: false },
  plugins: {
    legend: {
      labels: { color: textColor.value, font: { size: 12 } },
    },
    title: {
      display: true,
      text: `${props.fuelType.charAt(0).toUpperCase() + props.fuelType.slice(1)} Price Trend: World vs Asia`,
      color: textColor.value,
      font: { size: 14, weight: 'bold' },
    },
    tooltip: {
      callbacks: {
        label: (ctx) =>
          ` ${ctx.dataset.label}: $${(ctx.parsed.y as number).toFixed(3)}/L`,
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
      <Line :data="chartData" :options="chartOptions" />
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
