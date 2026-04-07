#!/usr/bin/env python3
"""
EDA Script for World vs Asia Fuel Prices Dataset
Dataset: zkskhurram/world-vs-asia-fuel-prices (Kaggle)

This script performs comprehensive Exploratory Data Analysis on the fuel prices dataset
and exports summary statistics for the Vue.js dashboard.
"""

import os
import json
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")

# Try to import optional packages
try:
    import kagglehub
    KAGGLE_AVAILABLE = True
except ImportError:
    KAGGLE_AVAILABLE = False
    print("kagglehub not installed. Using local data if available.")

try:
    import pandas as pd
    import numpy as np
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False
    print("pandas/numpy not installed. Install with: pip install pandas numpy")

try:
    import matplotlib
    matplotlib.use("Agg")  # Non-interactive backend
    import matplotlib.pyplot as plt
    import seaborn as sns
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("matplotlib/seaborn not installed. Skipping visualizations.")

# ─── Paths ────────────────────────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).parent
REPO_ROOT = SCRIPT_DIR.parent
DATA_RAW_DIR = REPO_ROOT / "data" / "raw"
DATA_PROCESSED_DIR = REPO_ROOT / "data" / "processed"
ANALYSIS_DIR = REPO_ROOT / "analysis"

DATA_RAW_DIR.mkdir(parents=True, exist_ok=True)
DATA_PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)


# ─── 1. Load Dataset ──────────────────────────────────────────────────────────
def load_dataset() -> "pd.DataFrame | None":
    """Download and load the dataset from Kaggle."""
    if not PANDAS_AVAILABLE:
        print("ERROR: pandas is required. Run: pip install pandas")
        return None

    # Try Kaggle download first
    if KAGGLE_AVAILABLE:
        print("Downloading dataset from Kaggle...")
        try:
            path = kagglehub.dataset_download("zkskhurram/world-vs-asia-fuel-prices")
            print(f"Dataset downloaded to: {path}")
            # Look for CSV files in the downloaded path
            csv_files = list(Path(path).glob("**/*.csv"))
            if csv_files:
                df = pd.read_csv(csv_files[0])
                print(f"Loaded: {csv_files[0].name} — shape: {df.shape}")
                return df
        except Exception as e:
            print(f"Kaggle download failed: {e}")

    # Fallback: look for local CSV files
    local_csvs = list(DATA_RAW_DIR.glob("*.csv"))
    if local_csvs:
        df = pd.read_csv(local_csvs[0])
        print(f"Loaded local file: {local_csvs[0].name} — shape: {df.shape}")
        return df

    print("No dataset found. Generating synthetic data for demonstration.")
    return generate_synthetic_data()


def generate_synthetic_data() -> "pd.DataFrame":
    """Generate synthetic fuel price data for demonstration purposes."""
    import numpy as np
    np.random.seed(42)

    countries_asia = [
        ("Japan", "Asia"), ("South Korea", "Asia"), ("China", "Asia"),
        ("India", "Asia"), ("Singapore", "Asia"), ("Thailand", "Asia"),
        ("Vietnam", "Asia"), ("Indonesia", "Asia"), ("Malaysia", "Asia"),
        ("Philippines", "Asia"), ("Hong Kong", "Asia"), ("Taiwan", "Asia"),
        ("Pakistan", "Asia"), ("Bangladesh", "Asia"), ("Sri Lanka", "Asia"),
    ]
    countries_world = [
        ("Germany", "Europe"), ("France", "Europe"), ("United Kingdom", "Europe"),
        ("Italy", "Europe"), ("Spain", "Europe"), ("Netherlands", "Europe"),
        ("Norway", "Europe"), ("Sweden", "Europe"),
        ("United States", "North America"), ("Canada", "North America"), ("Mexico", "North America"),
        ("Brazil", "South America"), ("Argentina", "South America"), ("Colombia", "South America"),
        ("Saudi Arabia", "Middle East"), ("UAE", "Middle East"), ("Iran", "Middle East"),
        ("Kuwait", "Middle East"), ("Iraq", "Middle East"),
        ("South Africa", "Africa"), ("Nigeria", "Africa"), ("Egypt", "Africa"), ("Kenya", "Africa"),
        ("Australia", "Oceania"), ("New Zealand", "Oceania"),
    ]

    all_countries = countries_asia + countries_world
    quarters = [
        f"{y}-{m:02d}" for y in range(2019, 2025)
        for m in [1, 4, 7, 10]
        if not (y == 2024 and m > 1)
    ]

    records = []
    for country, region in all_countries:
        base_gas = np.random.uniform(0.3, 2.5)
        for quarter in quarters:
            trend = 0.02 * quarters.index(quarter)
            shock = -0.4 if "2020-04" <= quarter <= "2020-07" else 0.0
            price_gas = max(0.1, base_gas + trend + shock + np.random.normal(0, 0.05))
            records.append({
                "country": country,
                "region": region,
                "date": quarter,
                "gasoline_price": round(price_gas, 3),
                "diesel_price": round(price_gas * 0.88, 3),
                "lpg_price": round(price_gas * 0.52, 3),
                "cng_price": round(price_gas * 0.41, 3) if region in ("Asia", "Europe") else None,
            })

    return pd.DataFrame(records)


# ─── 2. EDA Functions ─────────────────────────────────────────────────────────
def basic_info(df: "pd.DataFrame") -> dict:
    """Collect basic dataset information."""
    info = {
        "shape": list(df.shape),
        "columns": list(df.columns),
        "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
        "missing_values": df.isnull().sum().to_dict(),
        "missing_pct": (df.isnull().sum() / len(df) * 100).round(2).to_dict(),
        "total_records": len(df),
        "unique_countries": int(df["country"].nunique()) if "country" in df.columns else 0,
        "unique_regions": int(df["region"].nunique()) if "region" in df.columns else 0,
    }
    if "date" in df.columns:
        info["date_range"] = [str(df["date"].min()), str(df["date"].max())]
    return info


def descriptive_stats(df: "pd.DataFrame") -> dict:
    """Compute descriptive statistics for numeric columns."""
    numeric_cols = df.select_dtypes(include=[float, int]).columns.tolist()
    stats = {}
    for col in numeric_cols:
        series = df[col].dropna()
        stats[col] = {
            "count": int(series.count()),
            "mean": round(float(series.mean()), 4),
            "median": round(float(series.median()), 4),
            "std": round(float(series.std()), 4),
            "min": round(float(series.min()), 4),
            "max": round(float(series.max()), 4),
            "q25": round(float(series.quantile(0.25)), 4),
            "q75": round(float(series.quantile(0.75)), 4),
            "skewness": round(float(series.skew()), 4),
            "kurtosis": round(float(series.kurtosis()), 4),
        }
    return stats


def correlation_analysis(df: "pd.DataFrame") -> dict:
    """Compute correlation matrix for numeric columns."""
    numeric_df = df.select_dtypes(include=[float, int])
    if numeric_df.empty:
        return {}
    corr = numeric_df.corr().round(4)
    return {col: corr[col].to_dict() for col in corr.columns}


def regional_analysis(df: "pd.DataFrame") -> list:
    """Aggregate statistics by region."""
    if "region" not in df.columns:
        return []
    price_cols = [c for c in df.columns if "price" in c.lower()]
    group = df.groupby("region")[price_cols].mean().round(4)
    result = []
    for region, row in group.iterrows():
        entry = {"region": region}
        entry.update({col.replace("_price", "_avg"): v for col, v in row.items()})
        entry["countries"] = int(df[df["region"] == region]["country"].nunique())
        result.append(entry)
    return result


def time_series_analysis(df: "pd.DataFrame") -> list:
    """Aggregate average prices over time."""
    if "date" not in df.columns:
        return []
    price_cols = [c for c in df.columns if "price" in c.lower()]
    ts = df.groupby("date")[price_cols].mean().round(4).reset_index()
    return ts.rename(columns={c: c.replace("_price", "") for c in price_cols}).to_dict(orient="records")


# ─── 3. Visualizations ────────────────────────────────────────────────────────
def create_visualizations(df: "pd.DataFrame"):
    """Generate and save plots."""
    if not MATPLOTLIB_AVAILABLE:
        print("Skipping visualizations (matplotlib not available).")
        return

    sns.set_theme(style="darkgrid", palette="husl")
    price_cols = [c for c in df.columns if "price" in c.lower()]

    # --- Distribution plots ---
    if price_cols:
        fig, axes = plt.subplots(1, len(price_cols), figsize=(5 * len(price_cols), 4))
        if len(price_cols) == 1:
            axes = [axes]
        for ax, col in zip(axes, price_cols):
            sns.histplot(df[col].dropna(), bins=30, kde=True, ax=ax, color="#4ECDC4")
            ax.set_title(f"{col.replace('_', ' ').title()} Distribution")
            ax.set_xlabel("Price (USD/litre)")
        plt.tight_layout()
        fig.savefig(ANALYSIS_DIR / "distributions.png", dpi=120, bbox_inches="tight")
        plt.close(fig)
        print("Saved: distributions.png")

    # --- Correlation heatmap ---
    numeric_df = df.select_dtypes(include=[float, int])
    if numeric_df.shape[1] >= 2:
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(
            numeric_df.corr(), annot=True, fmt=".2f", cmap="coolwarm",
            square=True, ax=ax, linewidths=0.5
        )
        ax.set_title("Correlation Matrix — Fuel Prices")
        fig.savefig(ANALYSIS_DIR / "correlation_heatmap.png", dpi=120, bbox_inches="tight")
        plt.close(fig)
        print("Saved: correlation_heatmap.png")

    # --- Regional bar chart ---
    if "region" in df.columns and price_cols:
        region_avg = df.groupby("region")[price_cols[0]].mean().sort_values(ascending=False)
        fig, ax = plt.subplots(figsize=(10, 5))
        region_avg.plot(kind="bar", ax=ax, color="#45B7D1", edgecolor="white")
        ax.set_title(f"Average {price_cols[0].replace('_', ' ').title()} by Region")
        ax.set_ylabel("Price (USD/litre)")
        ax.set_xlabel("")
        plt.xticks(rotation=30, ha="right")
        fig.savefig(ANALYSIS_DIR / "regional_comparison.png", dpi=120, bbox_inches="tight")
        plt.close(fig)
        print("Saved: regional_comparison.png")

    # --- Time series ---
    if "date" in df.columns and price_cols:
        ts = df.groupby("date")[price_cols].mean()
        fig, ax = plt.subplots(figsize=(12, 5))
        for col in price_cols:
            ax.plot(ts.index, ts[col], marker="o", label=col.replace("_price", "").title(), linewidth=2)
        ax.set_title("Average Fuel Prices Over Time")
        ax.set_ylabel("Price (USD/litre)")
        ax.set_xlabel("Quarter")
        ax.legend()
        plt.xticks(rotation=45, ha="right")
        fig.savefig(ANALYSIS_DIR / "time_series.png", dpi=120, bbox_inches="tight")
        plt.close(fig)
        print("Saved: time_series.png")


# ─── 4. Export JSON ───────────────────────────────────────────────────────────
def export_json(data: dict | list, filename: str):
    """Write data to a JSON file."""
    path = DATA_PROCESSED_DIR / filename
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Exported: {path}")


# ─── 5. HTML Report ───────────────────────────────────────────────────────────
def generate_html_report(info: dict, stats: dict, regional: list):
    """Create a simple HTML EDA report."""
    rows_info = "".join(
        f"<tr><td>{k}</td><td>{v}</td></tr>" for k, v in info.items()
    )
    rows_stats = ""
    for col, s in stats.items():
        rows_stats += f"""
        <tr>
          <td>{col}</td><td>{s['count']}</td>
          <td>{s['mean']}</td><td>{s['median']}</td>
          <td>{s['std']}</td><td>{s['min']}</td><td>{s['max']}</td>
        </tr>"""

    regional_rows = "".join(
        f"<tr>{''.join(f'<td>{v}</td>' for v in r.values())}</tr>"
        for r in regional
    )
    regional_headers = "".join(
        f"<th>{k}</th>" for k in (regional[0].keys() if regional else [])
    )

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>EDA Report — World vs Asia Fuel Prices</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 2rem; background: #0f172a; color: #e2e8f0; }}
    h1, h2 {{ color: #4ECDC4; }}
    table {{ border-collapse: collapse; width: 100%; margin-bottom: 2rem; }}
    th {{ background: #1e293b; color: #4ECDC4; padding: 10px; text-align: left; }}
    td {{ border-bottom: 1px solid #334155; padding: 8px; }}
    tr:hover td {{ background: #1e293b; }}
    img {{ max-width: 100%; border-radius: 8px; margin: 1rem 0; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); gap: 1rem; }}
  </style>
</head>
<body>
  <h1>📊 EDA Report: World vs Asia Fuel Prices</h1>
  <p>Dataset: <a href="https://www.kaggle.com/datasets/zkskhurram/world-vs-asia-fuel-prices"
    style="color:#4ECDC4">zkskhurram/world-vs-asia-fuel-prices</a></p>

  <h2>1. Dataset Overview</h2>
  <table>
    <tr><th>Property</th><th>Value</th></tr>
    {rows_info}
  </table>

  <h2>2. Descriptive Statistics</h2>
  <table>
    <tr><th>Column</th><th>Count</th><th>Mean</th><th>Median</th>
        <th>Std</th><th>Min</th><th>Max</th></tr>
    {rows_stats}
  </table>

  <h2>3. Regional Analysis</h2>
  <table>
    <tr>{regional_headers}</tr>
    {regional_rows}
  </table>

  <h2>4. Visualizations</h2>
  <div class="grid">
    <div><h3>Price Distributions</h3><img src="distributions.png" alt="Distributions"/></div>
    <div><h3>Correlation Heatmap</h3><img src="correlation_heatmap.png" alt="Heatmap"/></div>
    <div><h3>Regional Comparison</h3><img src="regional_comparison.png" alt="Regional"/></div>
    <div><h3>Price Trends Over Time</h3><img src="time_series.png" alt="Time Series"/></div>
  </div>
</body>
</html>"""

    report_path = ANALYSIS_DIR / "eda_report.html"
    report_path.write_text(html, encoding="utf-8")
    print(f"Report saved: {report_path}")


# ─── Main ─────────────────────────────────────────────────────────────────────
def main():
    print("=" * 60)
    print("  EDA: World vs Asia Fuel Prices Dataset")
    print("=" * 60)

    if not PANDAS_AVAILABLE:
        print("ERROR: Install requirements with:\n  pip install -r requirements-analysis.txt")
        return

    # 1. Load
    df = load_dataset()
    if df is None:
        return

    print(f"\nDataset shape: {df.shape}")
    print(df.head(3).to_string())

    # 2. Analyse
    info = basic_info(df)
    stats = descriptive_stats(df)
    corr = correlation_analysis(df)
    regional = regional_analysis(df)
    ts = time_series_analysis(df)

    # 3. Visualize
    print("\nGenerating visualizations...")
    create_visualizations(df)

    # 4. Export JSON for frontend
    print("\nExporting JSON files for dashboard...")
    export_json({"metadata": info, "summary_stats": stats}, "summary.json")
    export_json(regional, "regional_stats.json")
    export_json(ts, "time_series.json")
    export_json(corr, "correlations.json")

    # Country-level data
    price_cols = [c for c in df.columns if "price" in c.lower()]
    if "country" in df.columns and "region" in df.columns and price_cols:
        latest = df.sort_values("date").groupby(["country", "region"])[price_cols].last()
        latest_records = latest.reset_index().rename(
            columns={c: c.replace("_price", "") for c in price_cols}
        ).to_dict(orient="records")
        export_json(latest_records, "fuel_prices.json")

    # 5. HTML report
    print("\nGenerating HTML report...")
    generate_html_report(info, stats, regional)

    print("\n✅ EDA complete!")
    print(f"   Processed data: {DATA_PROCESSED_DIR}")
    print(f"   EDA report:     {ANALYSIS_DIR / 'eda_report.html'}")


if __name__ == "__main__":
    main()
