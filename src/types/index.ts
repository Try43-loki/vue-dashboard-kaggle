// TypeScript types for the Fuel Prices Dashboard

export interface FuelPrice {
  country: string
  region: string
  gasoline: number | null
  diesel: number | null
  lpg: number | null
  cng: number | null
  year: number
}

export interface RegionalStat {
  region: string
  gasoline_avg: number
  diesel_avg: number
  lpg_avg: number
  cng_avg: number
  countries: number
  color: string
}

export interface TimeSeriesPoint {
  date: string
  gasoline_world: number
  gasoline_asia: number
  diesel_world: number
  diesel_asia: number
}

export interface FuelStat {
  mean: number
  median: number
  std: number
  min: number
  max: number
  currency: string
}

export interface PriceExtreme {
  country: string
  region: string
  price: number
  currency: string
}

export interface DataMetadata {
  dataset: string
  source: string
  last_updated: string
  total_records: number
  date_range: [string, string]
  fuel_types: string[]
  regions: string[]
}

export interface SummaryData {
  metadata: DataMetadata
  summary_stats: {
    gasoline: FuelStat
    diesel: FuelStat
    lpg: FuelStat
    cng: FuelStat
  }
  highest_gasoline: PriceExtreme
  lowest_gasoline: PriceExtreme
  highest_diesel: PriceExtreme
  lowest_diesel: PriceExtreme
}

export type FuelType = 'gasoline' | 'diesel' | 'lpg' | 'cng'
export type Region =
  | 'All'
  | 'Asia'
  | 'Europe'
  | 'North America'
  | 'South America'
  | 'Middle East'
  | 'Africa'
  | 'Oceania'

export interface FilterState {
  region: Region
  fuelType: FuelType
  dateRange: [string, string] | null
}

export interface DashboardData {
  summary: SummaryData
  regionalStats: RegionalStat[]
  timeSeries: TimeSeriesPoint[]
  fuelPrices: FuelPrice[]
}
