#!/usr/bin/env python3
"""
Data Processing Pipeline for World vs Asia Fuel Prices Dataset.

Steps:
  1. Load raw CSV (or synthetic data)
  2. Clean & validate
  3. Handle missing values
  4. Normalise numerical features
  5. Aggregate by region, time period, fuel type
  6. Export JSON files for the Vue frontend
"""

import json
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")

try:
    import pandas as pd
    import numpy as np
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False
    print("ERROR: pandas/numpy not installed. Run: pip install pandas numpy")

# ─── Paths ────────────────────────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).parent
REPO_ROOT = SCRIPT_DIR.parent
DATA_RAW_DIR = REPO_ROOT / "data" / "raw"
DATA_PROCESSED_DIR = REPO_ROOT / "data" / "processed"

DATA_RAW_DIR.mkdir(parents=True, exist_ok=True)
DATA_PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

PRICE_COLS = ["gasoline_price", "diesel_price", "lpg_price", "cng_price"]
FUEL_RENAME = {
    "gasoline_price": "gasoline",
    "diesel_price": "diesel",
    "lpg_price": "lpg",
    "cng_price": "cng",
}
REGION_COLORS = {
    "Asia": "#4ECDC4",
    "Europe": "#45B7D1",
    "North America": "#96CEB4",
    "South America": "#FFEAA7",
    "Middle East": "#DDA0DD",
    "Africa": "#F0A500",
    "Oceania": "#FF6B6B",
}


# ─── Helpers ──────────────────────────────────────────────────────────────────
def save_json(data, filename: str):
    path = DATA_PROCESSED_DIR / filename
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False, default=_json_default)
    print(f"  Saved: {path}")


def _json_default(obj):
    if isinstance(obj, float) and (obj != obj):   # NaN
        return None
    raise TypeError(f"Not serialisable: {type(obj)}")


# ─── 1. Load ──────────────────────────────────────────────────────────────────
def load_raw() -> "pd.DataFrame":
    """Load raw CSV or fall back to synthetic data."""
    csv_files = sorted(DATA_RAW_DIR.glob("*.csv"))
    if csv_files:
        df = pd.read_csv(csv_files[0])
        print(f"Loaded raw file: {csv_files[0].name} — {df.shape}")
        return df

    print("No raw CSV found — generating synthetic data.")
    return _synthetic_data()


def _synthetic_data() -> "pd.DataFrame":
    np.random.seed(42)
    base_prices = {
        ("Japan", "Asia"): 1.38,
        ("South Korea", "Asia"): 1.44,
        ("China", "Asia"): 1.14,
        ("India", "Asia"): 1.04,
        ("Singapore", "Asia"): 2.08,
        ("Thailand", "Asia"): 0.94,
        ("Vietnam", "Asia"): 0.84,
        ("Indonesia", "Asia"): 0.68,
        ("Malaysia", "Asia"): 0.44,
        ("Philippines", "Asia"): 1.01,
        ("Hong Kong", "Asia"): 2.84,
        ("Taiwan", "Asia"): 0.94,
        ("Pakistan", "Asia"): 0.74,
        ("Bangladesh", "Asia"): 0.84,
        ("Sri Lanka", "Asia"): 0.91,
        ("Germany", "Europe"): 1.84,
        ("France", "Europe"): 1.80,
        ("United Kingdom", "Europe"): 1.88,
        ("Italy", "Europe"): 1.87,
        ("Spain", "Europe"): 1.68,
        ("Netherlands", "Europe"): 2.08,
        ("Norway", "Europe"): 2.04,
        ("Sweden", "Europe"): 1.90,
        ("United States", "North America"): 1.00,
        ("Canada", "North America"): 1.17,
        ("Mexico", "North America"): 1.04,
        ("Brazil", "South America"): 1.08,
        ("Argentina", "South America"): 0.90,
        ("Colombia", "South America"): 0.84,
        ("Saudi Arabia", "Middle East"): 0.44,
        ("UAE", "Middle East"): 0.74,
        ("Iran", "Middle East"): 0.20,
        ("Kuwait", "Middle East"): 0.34,
        ("Iraq", "Middle East"): 0.54,
        ("South Africa", "Africa"): 1.14,
        ("Nigeria", "Africa"): 0.50,
        ("Egypt", "Africa"): 0.44,
        ("Kenya", "Africa"): 1.24,
        ("Australia", "Oceania"): 1.48,
        ("New Zealand", "Oceania"): 1.57,
    }
    quarters = [
        f"{y}-{m:02d}" for y in range(2019, 2025)
        for m in [1, 4, 7, 10]
        if not (y == 2024 and m > 1)
    ]
    records = []
    for (country, region), base in base_prices.items():
        for i, q in enumerate(quarters):
            trend = 0.018 * i
            shock = -0.38 if "2020-04" <= q <= "2020-07" else 0.0
            gas = max(0.1, base + trend + shock + np.random.normal(0, 0.04))
            records.append({
                "country": country, "region": region, "date": q,
                "gasoline_price": round(gas, 3),
                "diesel_price": round(gas * 0.87, 3),
                "lpg_price": round(gas * 0.51, 3),
                "cng_price": round(gas * 0.40, 3) if region in ("Asia", "Europe", "South America") else None,
            })
    return pd.DataFrame(records)


# ─── 2. Clean ─────────────────────────────────────────────────────────────────
def clean(df: "pd.DataFrame") -> "pd.DataFrame":
    """Validate, coerce and deduplicate."""
    df = df.copy()

    # Standardise column names
    df.columns = (df.columns.str.strip().str.lower()
                  .str.replace(r"\s+", "_", regex=True)
                  .str.replace(r"[^\w]", "", regex=True))

    # Ensure price columns exist
    for col in PRICE_COLS:
        if col not in df.columns:
            df[col] = np.nan

    # Coerce numeric
    for col in PRICE_COLS:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Remove impossible values (negative or > $10/litre)
    for col in PRICE_COLS:
        df.loc[~df[col].between(0, 10, inclusive="both"), col] = np.nan

    # Drop exact duplicates
    df = df.drop_duplicates()

    print(f"  After cleaning: {df.shape}")
    return df


# ─── 3. Impute missing values ─────────────────────────────────────────────────
def impute(df: "pd.DataFrame") -> "pd.DataFrame":
    """Fill missing price values with regional median per quarter."""
    df = df.copy()
    for col in PRICE_COLS:
        if col not in df.columns:
            continue
        # Group median imputation
        medians = df.groupby(["region", "date"])[col].transform("median")
        df[col] = df[col].fillna(medians)
        # Fall back to global median
        df[col] = df[col].fillna(df[col].median())
    print("  Missing values imputed.")
    return df


# ─── 4. Normalise ─────────────────────────────────────────────────────────────
def normalise(df: "pd.DataFrame") -> "pd.DataFrame":
    """Min-max normalise price columns and store as *_norm."""
    df = df.copy()
    for col in PRICE_COLS:
        if col not in df.columns:
            continue
        col_min, col_max = df[col].min(), df[col].max()
        denom = col_max - col_min if col_max != col_min else 1.0
        df[f"{col}_norm"] = ((df[col] - col_min) / denom).round(4)
    print("  Normalisation complete.")
    return df


# ─── 5. Aggregations ──────────────────────────────────────────────────────────
def regional_aggregation(df: "pd.DataFrame") -> list:
    available = [c for c in PRICE_COLS if c in df.columns]
    group = df.groupby("region")[available].mean().round(4)
    result = []
    for region, row in group.iterrows():
        entry = {
            "region": region,
            "color": REGION_COLORS.get(region, "#888888"),
            "countries": int(df[df["region"] == region]["country"].nunique()),
        }
        for col in available:
            entry[FUEL_RENAME.get(col, col) + "_avg"] = row[col]
        result.append(entry)
    return sorted(result, key=lambda x: x.get("gasoline_avg", 0), reverse=True)


def time_series_aggregation(df: "pd.DataFrame") -> list:
    available = [c for c in PRICE_COLS if c in df.columns]
    ts = df.groupby("date")[available].mean().round(4).reset_index()
    # Also split world vs Asia
    asia = df[df["region"] == "Asia"].groupby("date")[available].mean().round(4)
    world = df.groupby("date")[available].mean().round(4)

    records = []
    for _, row in ts.iterrows():
        date = row["date"]
        entry = {"date": date}
        for col in available:
            short = FUEL_RENAME.get(col, col)
            entry[f"{short}_world"] = row[col]
            entry[f"{short}_asia"] = round(float(asia.loc[date, col]), 4) if date in asia.index else None
        records.append(entry)
    return records


def country_latest(df: "pd.DataFrame") -> list:
    available = [c for c in PRICE_COLS if c in df.columns]
    latest_date = df["date"].max()
    latest_df = df[df["date"] == latest_date][["country", "region"] + available].copy()
    latest_df = latest_df.rename(columns=FUEL_RENAME)
    # Replace NaN with None for JSON serialisation
    latest_df = latest_df.where(pd.notna(latest_df), None)
    latest_df["year"] = int(latest_date[:4])
    return latest_df.sort_values("country").to_dict(orient="records")


def summary_export(df: "pd.DataFrame") -> dict:
    available = [c for c in PRICE_COLS if c in df.columns]
    stats: dict = {}
    for col in available:
        series = df[col].dropna()
        fuel = FUEL_RENAME.get(col, col)
        stats[fuel] = {
            "mean": round(float(series.mean()), 4),
            "median": round(float(series.median()), 4),
            "std": round(float(series.std()), 4),
            "min": round(float(series.min()), 4),
            "max": round(float(series.max()), 4),
            "currency": "USD/liter",
        }

    # Extremes (latest snapshot)
    latest = df[df["date"] == df["date"].max()]
    extremes = {}
    for col in available[:2]:   # gasoline & diesel
        fuel = FUEL_RENAME.get(col, col)
        if latest[col].notna().any():
            hi = latest.loc[latest[col].idxmax()]
            lo = latest.loc[latest[col].idxmin()]
            extremes[f"highest_{fuel}"] = {
                "country": hi["country"], "region": hi["region"],
                "price": round(float(hi[col]), 3), "currency": "USD/liter",
            }
            extremes[f"lowest_{fuel}"] = {
                "country": lo["country"], "region": lo["region"],
                "price": round(float(lo[col]), 3), "currency": "USD/liter",
            }

    return {
        "metadata": {
            "dataset": "World vs Asia Fuel Prices",
            "source": "Kaggle - zkskhurram/world-vs-asia-fuel-prices",
            "last_updated": df["date"].max(),
            "total_records": len(df),
            "date_range": [df["date"].min(), df["date"].max()],
            "fuel_types": [FUEL_RENAME.get(c, c).title() for c in available],
            "regions": sorted(df["region"].unique().tolist()),
        },
        "summary_stats": stats,
        **extremes,
    }


# ─── Main ─────────────────────────────────────────────────────────────────────
def main():
    print("=" * 60)
    print("  Data Processing: World vs Asia Fuel Prices")
    print("=" * 60)

    if not PANDAS_AVAILABLE:
        print("ERROR: Install requirements with:\n  pip install -r requirements-analysis.txt")
        return

    print("\n[1] Loading raw data...")
    df_raw = load_raw()

    print("\n[2] Cleaning data...")
    df_clean = clean(df_raw)

    print("\n[3] Imputing missing values...")
    df_imputed = impute(df_clean)

    print("\n[4] Normalising features...")
    df_norm = normalise(df_imputed)

    print("\n[5] Exporting processed datasets...")
    save_json(regional_aggregation(df_norm), "regional_stats.json")
    save_json(time_series_aggregation(df_norm), "time_series.json")
    save_json(country_latest(df_norm), "fuel_prices.json")
    save_json(summary_export(df_norm), "summary.json")

    # Full processed dataset as CSV for optional inspection
    csv_path = DATA_PROCESSED_DIR / "fuel_prices_processed.csv"
    df_norm.to_csv(csv_path, index=False)
    print(f"  Saved: {csv_path}")

    print("\n✅ Processing complete!")
    print(f"   Output directory: {DATA_PROCESSED_DIR}")


if __name__ == "__main__":
    main()
