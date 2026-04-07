import type { DashboardData, FuelPrice, RegionalStat, SummaryData, TimeSeriesPoint } from '@/types'

const BASE = import.meta.env.BASE_URL

async function fetchJson<T>(path: string): Promise<T> {
  const res = await fetch(`${BASE}${path}`)
  if (!res.ok) throw new Error(`Failed to load ${path}: ${res.statusText}`)
  return res.json() as Promise<T>
}

export const dataService = {
  async loadAll(): Promise<DashboardData> {
    const [summary, regionalStats, timeSeries, fuelPrices] = await Promise.all([
      fetchJson<SummaryData>('data/processed/summary.json'),
      fetchJson<RegionalStat[]>('data/processed/regional_stats.json'),
      fetchJson<TimeSeriesPoint[]>('data/processed/time_series.json'),
      fetchJson<FuelPrice[]>('data/processed/fuel_prices.json'),
    ])
    return { summary, regionalStats, timeSeries, fuelPrices }
  },
}
