<script setup lang="ts">
import { computed } from 'vue'
import { Doughnut } from 'vue-chartjs'
import { Chart as ChartJS, ArcElement, Tooltip, Legend, Title } from 'chart.js'
import type { RegionalStat } from '@/types'

ChartJS.register(ArcElement, Tooltip, Legend, Title)

const props = defineProps<{
  regionalStats: RegionalStat[]
  theme: 'dark' | 'light'
}>()

const textColor = computed(() => (props.theme === 'dark' ? '#94a3b8' : '#475569'))

// Average of all fuel types per region (relative distribution)
const chartData = computed(() => {
  const totals = props.regionalStats.map(
    (r) => ((r.gasoline_avg ?? 0) + (r.diesel_avg ?? 0) + (r.lpg_avg ?? 0)) / 3
  )
  return {
    labels: props.regionalStats.map((r) => r.region),
    datasets: [
      {
        data: totals.map((v) => Math.round(v * 1000) / 1000),
        backgroundColor: props.regionalStats.map((r) => r.color + 'cc'),
        borderColor: props.regionalStats.map((r) => r.color),
        borderWidth: 2,
        hoverOffset: 8,
      },
    ],
  }
})

const chartOptions = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'right' as const,
      labels: { color: textColor.value, font: { size: 11 }, padding: 12 },
    },
    title: {
      display: true,
      text: 'Average Price Distribution by Region',
      color: textColor.value,
      font: { size: 14, weight: 'bold' as const },
    },
    tooltip: {
      callbacks: {
        label: (ctx: { label: string; parsed: number }) =>
          ` ${ctx.label}: $${ctx.parsed.toFixed(3)}/L avg`,
      },
    },
  },
}))
</script>

<template>
  <div class="chart-card">
    <div class="chart-wrap">
      <Doughnut :data="chartData" :options="chartOptions" />
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
