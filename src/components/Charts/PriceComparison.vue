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
import type { RegionalStat, FuelType } from '@/types'

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend)

const props = defineProps<{
  regionalStats: RegionalStat[]
  fuelType: FuelType
  theme: 'dark' | 'light'
}>()

const textColor = computed(() => (props.theme === 'dark' ? '#94a3b8' : '#475569'))
const gridColor = computed(() => (props.theme === 'dark' ? '#334155' : '#e2e8f0'))

const chartData = computed(() => ({
  labels: props.regionalStats.map((r) => r.region),
  datasets: [
    {
      label: `Avg ${props.fuelType.charAt(0).toUpperCase() + props.fuelType.slice(1)} Price (USD/L)`,
      data: props.regionalStats.map((r) => r[`${props.fuelType}_avg` as keyof RegionalStat] as number),
      backgroundColor: props.regionalStats.map((r) => r.color + 'cc'),
      borderColor: props.regionalStats.map((r) => r.color),
      borderWidth: 2,
      borderRadius: 6,
    },
  ],
}))

const chartOptions = computed<ChartOptions<'bar'>>(() => ({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { display: false },
    title: {
      display: true,
      text: `Average ${props.fuelType.charAt(0).toUpperCase() + props.fuelType.slice(1)} Price by Region`,
      color: textColor.value,
      font: { size: 14, weight: 'bold' },
    },
    tooltip: {
      callbacks: {
        label: (ctx) => ` $${(ctx.parsed.y as number).toFixed(3)} / litre`,
      },
    },
  },
  scales: {
    x: {
      ticks: { color: textColor.value, font: { size: 11 } },
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
