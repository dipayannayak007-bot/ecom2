#!/usr/bin/env python3
"""CNT-02 India E-Commerce Market Growth and Consumer Segmentation.
Run: python run_project.py
No internet connection or API access is used at runtime.
"""
from pathlib import Path
import argparse
import os
import subprocess
import sys
import warnings
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
OUT = ROOT / "outputs"
FIG = OUT / "figures"


def open_image(path):
    """Open an image file with the default Windows viewer."""
    if sys.platform == "win32" and path.exists():
        os.startfile(str(path))


def setup():
    FIG.mkdir(parents=True, exist_ok=True)

def market_data():
    return pd.read_csv(DATA / "india_ecommerce_market.csv")

def save_market_trend(df):
    d = df[df.market_scope.eq("India total e-commerce")].sort_values("year")
    fig, ax = plt.subplots(figsize=(10, 6))
    for status, part in d.groupby("status"):
        ax.plot(part.year, part.market_value_usd_bn, marker="o", lw=2, label=status)
    ax.set(title="India e-commerce market: reported values and forecasts",
           xlabel="Year", ylabel="Market value (US$ billion)")
    ax.grid(alpha=.25); ax.legend()
    path = FIG / "01_india_market_trend.png"
    fig.tight_layout(); fig.savefig(path, dpi=220); plt.close(fig)
    open_image(path)
    print(f"  -> Opened: {path.name}")

def save_category_chart(df):
    d = df[df.market_scope.isin([
        "India online electronics and appliances",
        "India online smartphones (separate category)"
    ])].copy()
    labels = {
        "India online electronics and appliances": "Electronics & appliances",
        "India online smartphones (separate category)": "Smartphones"
    }
    d["label"] = d.market_scope.map(labels)
    fig, ax = plt.subplots(figsize=(9, 5.5))
    bars = ax.barh(d.label, d.market_value_usd_bn, color="#39856A")
    ax.bar_label(bars, labels=[f"${v:.0f}bn" for v in d.market_value_usd_bn], padding=5)
    ax.set(title="Selected online electronics categories in India (2024)",
           xlabel="Market value (US$ billion)")
    ax.set_xlim(0, max(d.market_value_usd_bn) * 1.25); ax.grid(axis="x", alpha=.2)
    path = FIG / "02_category_benchmark.png"
    fig.tight_layout(); fig.savefig(path, dpi=220); plt.close(fig)
    open_image(path)
    print(f"  -> Opened: {path.name}")

def scenario_table(tam, sam_share):
    rows = []
    for name, rate in [("Conservative", .08), ("Base", .12), ("Optimistic", .16)]:
        for year in range(2024, 2031):
            value = tam * (1 + rate) ** (year - 2024)
            rows.append({"year": year, "scenario": name, "cagr": rate,
                         "tam_usd_bn": value, "illustrative_sam_usd_bn": value * sam_share})
    d = pd.DataFrame(rows)
    d.to_csv(OUT / "electronics_scenario_forecast.csv", index=False)
    return d

def save_scenario_chart(d):
    fig, ax = plt.subplots(figsize=(10, 6))
    for name, part in d.groupby("scenario"):
        ax.plot(part.year, part.tam_usd_bn, marker="o", lw=2, label=name)
    ax.set(title="Electronics & appliances: illustrative growth scenarios",
           xlabel="Year", ylabel="Projected TAM (US$ billion)")
    ax.set_xticks(range(2024, 2031)); ax.grid(alpha=.25); ax.legend(title="Scenario")
    path = FIG / "03_tam_scenarios.png"
    fig.tight_layout(); fig.savefig(path, dpi=220); plt.close(fig)
    open_image(path)
    print(f"  -> Opened: {path.name}")

def save_tam_sam(tam, share):
    labels, values = ["TAM", "Illustrative SAM"], [tam, tam * share]
    fig, ax = plt.subplots(figsize=(8, 5.5))
    bars = ax.bar(labels, values, color=["#4C78A8", "#F2A541"], width=.58)
    ax.bar_label(bars, labels=[f"${v:.1f}bn" for v in values], padding=5)
    ax.set(title="2024 India electronics & appliances market sizing",
           ylabel="Market value (US$ billion)")
    ax.text(.5, .94, f"SAM assumes {share:.0%} reachable share",
            transform=ax.transAxes, ha="center", va="top", fontsize=9)
    ax.set_ylim(0, tam * 1.25); ax.grid(axis="y", alpha=.2)
    path = FIG / "04_tam_sam.png"
    fig.tight_layout(); fig.savefig(path, dpi=220); plt.close(fig)
    open_image(path)
    print(f"  -> Opened: {path.name}")

def analyse_transactions():
    path = DATA / "transactions.csv"
    if not path.exists() or path.stat().st_size == 0:
        print("No transaction data supplied: skipping empirical transaction charts.")
        return
    d = pd.read_csv(path)
    if not {"quantity", "unit_price_inr"}.issubset(d.columns):
        warnings.warn("transactions.csv requires quantity and unit_price_inr.")
        return
    d["gross_value_inr"] = pd.to_numeric(d.quantity, errors="coerce") * pd.to_numeric(d.unit_price_inr, errors="coerce")
    discount = pd.to_numeric(d.discount_inr, errors="coerce").fillna(0) if "discount_inr" in d else 0
    d["net_value_inr"] = d.gross_value_inr - discount
    d = d.replace([np.inf, -np.inf], np.nan).dropna(subset=["net_value_inr"])
    d = d[d.net_value_inr >= 0]
    if d.empty:
        print("No valid transaction values.")
        return
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(d.net_value_inr, bins=30, color="#4C78A8", edgecolor="white")
    ax.set(title="Distribution of transaction values", xlabel="Net transaction value (INR)", ylabel="Records")
    ax.grid(axis="y", alpha=.2); fig.tight_layout()
    img_path = FIG / "05_transaction_value_histogram.png"
    fig.savefig(img_path, dpi=220); plt.close(fig)
    open_image(img_path)
    if "category" in d:
        bycat = d.groupby("category").net_value_inr.sum().sort_values()
        fig, ax = plt.subplots(figsize=(9, 6))
        bycat.plot(kind="barh", ax=ax, color="#39856A")
        ax.set(title="Net sales by category", xlabel="Net sales (INR)", ylabel="")
        img_path2 = FIG / "06_transaction_sales_by_category.png"
        fig.tight_layout(); fig.savefig(img_path2, dpi=220); plt.close(fig)
        open_image(img_path2)
    pd.DataFrame([{
        "records": len(d),
        "orders": d.order_id.nunique() if "order_id" in d else np.nan,
        "customers": d.customer_id.nunique() if "customer_id" in d else np.nan,
        "net_sales_inr": d.net_value_inr.sum()
    }]).to_csv(OUT / "transaction_summary.csv", index=False)

def analyse_survey():
    path = DATA / "survey_responses.csv"
    if not path.exists() or path.stat().st_size == 0:
        print("No survey responses supplied: skipping empirical consumer charts.")
        return
    d = pd.read_csv(path)
    charts = [
        ("purchase_frequency_12m", "07_purchase_frequency.png", "Online purchase frequency", "#E39C37"),
        ("preferred_category", "08_preferred_category.png", "Preferred online shopping category", "#39856A"),
        ("spend_band_inr", "09_spending_bands.png", "Respondent spending bands", "#8064A2"),
        ("price_sensitivity", "10_price_sensitivity.png", "Self-reported price sensitivity", "#4C78A8"),
    ]
    for col, filename, title, color in charts:
        if col not in d:
            continue
        counts = d[col].dropna().astype(str).str.strip()
        counts = counts[counts.ne("")].value_counts()
        if counts.empty:
            continue
        fig, ax = plt.subplots(figsize=(9, max(4.5, .45 * len(counts))))
        counts.sort_values().plot(kind="barh", ax=ax, color=color)
        ax.set(title=title, xlabel="Respondents", ylabel="")
        img_path = FIG / filename
        fig.tight_layout(); fig.savefig(img_path, dpi=220); plt.close(fig)
        open_image(img_path)

    # Optional K-means: requires numeric, pre-coded influence-score columns.
    candidates = [c for c in ["discount_importance", "emi_influence_score",
                  "exchange_influence_score", "delivery_cost_influence_score"] if c in d]
    if len(candidates) >= 2:
        numeric = d[candidates].apply(pd.to_numeric, errors="coerce").dropna()
        if len(numeric) >= 10:
            try:
                from sklearn.cluster import KMeans
                from sklearn.preprocessing import StandardScaler
                labels = KMeans(n_clusters=3, random_state=42, n_init=10).fit_predict(
                    StandardScaler().fit_transform(numeric))
                result = numeric.copy(); result["cluster"] = labels + 1
                result.to_csv(OUT / "exploratory_consumer_segments.csv", index=False)
                print("Exploratory clusters saved. Review cluster profiles before naming segments.")
            except ImportError:
                print("Optional clustering requires scikit-learn.")

def main():
    parser = argparse.ArgumentParser(description="Run CNT-02 offline Python analysis.")
    parser.add_argument("--tam", type=float, default=27.0, help="2024 category TAM in US$bn")
    parser.add_argument("--sam-share", type=float, default=.30, help="Illustrative SAM share (0 to 1)")
    args = parser.parse_args()
    if args.tam <= 0 or not 0 <= args.sam_share <= 1:
        parser.error("--tam must be positive and --sam-share must be between 0 and 1")
    setup()
    df = market_data()
    save_market_trend(df); save_category_chart(df)
    scenarios = scenario_table(args.tam, args.sam_share)
    save_scenario_chart(scenarios); save_tam_sam(args.tam, args.sam_share)
    analyse_transactions(); analyse_survey()
    print("\nAnalysis complete.")
    print(f"Charts: {FIG}")
    print(f"Scenario table: {OUT / 'electronics_scenario_forecast.csv'}")
    print("Forecast years and scenario assumptions are not observed outcomes.")

if __name__ == "__main__":
    main()
