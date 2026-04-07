# ⛽ World vs Asia Fuel Prices — EDA Dashboard

A full-stack data analytics dashboard built with **Vue 3 + TypeScript** that explores and visualises the Kaggle dataset [zkskhurram/world-vs-asia-fuel-prices](https://www.kaggle.com/datasets/zkskhurram/world-vs-asia-fuel-prices).

---

## 📁 Project Structure

```
vue-dashboard-kaggle/
├── analysis/
│   ├── eda.py                 # EDA script (Python)
│   └── eda_report.html        # Generated HTML report (after running EDA)
├── scripts/
│   └── process_data.py        # Data processing pipeline
├── data/
│   ├── raw/                   # Place raw CSV files here
│   └── processed/             # Pre-generated JSON for the dashboard
│       ├── summary.json
│       ├── regional_stats.json
│       ├── time_series.json
│       └── fuel_prices.json
├── src/
│   ├── components/
│   │   ├── Header.vue
│   │   ├── KeyMetrics.vue
│   │   ├── Filters.vue
│   │   ├── DataTable.vue
│   │   └── Charts/
│   │       ├── PriceComparison.vue   # Bar chart — regional averages
│   │       ├── TrendChart.vue        # Line chart — World vs Asia trend
│   │       ├── FuelDistribution.vue  # Doughnut — price distribution
│   │       └── RegionalHeatmap.vue   # Bar chart — top countries
│   ├── views/
│   │   └── Dashboard.vue
│   ├── services/
│   │   └── dataService.ts
│   ├── types/
│   │   └── index.ts
│   ├── assets/
│   │   └── main.css
│   ├── App.vue
│   └── main.ts
├── public/
│   ├── favicon.svg
│   └── data/processed/        # JSON files served by Vite
├── package.json
├── vite.config.ts
├── tsconfig.json
├── index.html
├── .env.example
├── .gitignore
└── requirements-analysis.txt
```

---

## 🚀 Quick Start

### Prerequisites

- **Node.js** ≥ 18
- **Python** ≥ 3.9 (for EDA / data processing)

### 1. Install frontend dependencies

```bash
npm install
```

### 2. Run the development server

```bash
npm run dev
```

Open [http://localhost:5173](http://localhost:5173) in your browser.

### 3. Build for production

```bash
npm run build
```

---

## 🔬 EDA & Data Processing (Python)

### Install Python dependencies

```bash
pip install -r requirements-analysis.txt
```

### Run EDA

```bash
python analysis/eda.py
```

This will:
- Download the dataset from Kaggle (requires Kaggle API credentials)
- Generate descriptive statistics, correlation analysis, and time-series analysis
- Create visualisation plots (PNG)
- Export `data/processed/*.json` for the frontend
- Generate `analysis/eda_report.html`

### Run data processing pipeline

```bash
python scripts/process_data.py
```

This will:
- Load and clean the raw CSV
- Impute missing values (regional median → global median fallback)
- Min-max normalise price columns
- Export aggregated JSON files for the frontend

### Kaggle API credentials

Create `~/.kaggle/kaggle.json` or set environment variables:

```bash
export KAGGLE_USERNAME=your_username
export KAGGLE_KEY=your_api_key
```

See `.env.example` for reference.

---

## 📊 Dashboard Features

| Feature | Description |
|---|---|
| **Key Metrics Panel** | Average, highest, and lowest prices per fuel type |
| **Price Comparison Chart** | Bar chart comparing regional average prices |
| **Trend Chart** | Line chart — World vs Asia price trends 2019–2024 |
| **Fuel Distribution** | Doughnut chart — price distribution by region |
| **Country Comparison** | Top-15 countries bar chart (Gasoline vs Diesel) |
| **Data Table** | Sortable, searchable, paginated country-level table |
| **Filters** | Filter by fuel type (Gasoline/Diesel/LPG/CNG) and region |
| **Dark/Light Theme** | Toggle with smooth CSS variable transitions |
| **Responsive Design** | Mobile, tablet, and desktop layouts |

---

## 🧪 EDA Insights

Key findings from the dataset:

- **Middle East** has the lowest fuel prices globally (Iran ~$0.24/L gasoline)
- **Europe** has the highest average prices due to heavy fuel taxes (Netherlands, Norway ~$2.00+/L)
- **COVID-19 shock** (Q2 2020) caused a ~35% average price drop globally
- **Post-2021 recovery** brought prices to record highs by mid-2022 (Ukraine conflict)
- **Asia** consistently tracks 15–20% below the world average
- **Gasoline** and **Diesel** are highly correlated (r > 0.95)

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| Frontend Framework | Vue 3 (Composition API + `<script setup>`) |
| Language | TypeScript 5 |
| Build Tool | Vite 4 |
| Charts | Chart.js 4 + vue-chartjs 5 |
| Styling | CSS custom properties (no framework) |
| EDA | Python, pandas, numpy, matplotlib, seaborn |
| Data Source | Kaggle (kagglehub) |

---

## 📝 Scripts

| Command | Description |
|---|---|
| `npm run dev` | Start Vite development server |
| `npm run build` | Type-check and build for production |
| `npm run preview` | Preview production build locally |
| `npm run lint` | Lint with ESLint |
| `npm run format` | Format with Prettier |

---

## 📄 License

MIT
