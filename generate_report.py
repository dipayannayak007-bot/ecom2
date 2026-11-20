#!/usr/bin/env python3
"""Generate a PDF project report for CNT-02.

Run:  python generate_report.py

Produces  outputs/CNT02_Project_Report.pdf
No internet connection is needed at runtime.
"""
from pathlib import Path
from datetime import date
import os
import sys
import subprocess

try:
    from fpdf import FPDF
except ImportError:
    print("fpdf2 not found. Installing now...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "fpdf2"])
    from fpdf import FPDF

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
OUT = ROOT / "outputs"
FIG = OUT / "figures"
REPORT_PATH = OUT / "CNT02_Project_Report.pdf"


class ReportPDF(FPDF):
    """Custom FPDF subclass with header / footer branding."""

    def header(self):
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(100, 100, 100)
        self.cell(0, 8, "CNT-02  |  India E-Commerce Market Growth & Consumer Segmentation", align="L")
        self.ln(4)
        self.set_draw_color(60, 130, 100)
        self.set_line_width(0.4)
        self.line(10, self.get_y(), self.w - 10, self.get_y())
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(140, 140, 140)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

    # ---- helper methods ----

    def chapter_title(self, number, title):
        """Add a numbered chapter heading."""
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(30, 80, 60)
        self.cell(0, 12, f"{number}. {title}", new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(60, 130, 100)
        self.set_line_width(0.3)
        self.line(10, self.get_y(), 90, self.get_y())
        self.ln(6)

    def section_title(self, title):
        """Add a sub-section heading."""
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(50, 50, 50)
        self.cell(0, 8, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def body_text(self, text):
        """Add body paragraph text."""
        self.set_font("Helvetica", "", 10)
        self.set_text_color(40, 40, 40)
        self.multi_cell(0, 5.5, text)
        self.ln(3)

    def bullet(self, text):
        """Add a bullet-point line."""
        self.set_font("Helvetica", "", 10)
        self.set_text_color(40, 40, 40)
        x = self.get_x()
        self.cell(6, 5.5, "-")
        self.multi_cell(0, 5.5, text)
        self.ln(1)

    def add_figure(self, path, caption, width=170):
        """Embed a PNG figure with a caption.  Skips if the file is missing."""
        if not path.exists():
            self.body_text(f"[Figure not found: {path.name}]")
            return
        # Check remaining space; add page if tight
        if self.get_y() > self.h - 100:
            self.add_page()
        self.image(str(path), x=20, w=width)
        self.ln(2)
        self.set_font("Helvetica", "I", 9)
        self.set_text_color(80, 80, 80)
        self.cell(0, 5, caption, align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(6)

    def add_table(self, headers, rows, col_widths=None):
        """Draw a simple table."""
        if col_widths is None:
            col_widths = [self.epw / len(headers)] * len(headers)
        # Header row
        self.set_font("Helvetica", "B", 9)
        self.set_fill_color(60, 130, 100)
        self.set_text_color(255, 255, 255)
        for w, h in zip(col_widths, headers):
            self.cell(w, 7, h, border=1, align="C", fill=True)
        self.ln()
        # Data rows
        self.set_font("Helvetica", "", 9)
        self.set_text_color(40, 40, 40)
        fill = False
        for row in rows:
            if fill:
                self.set_fill_color(235, 245, 240)
            for w, val in zip(col_widths, row):
                self.cell(w, 6.5, str(val), border=1, align="C", fill=fill)
            self.ln()
            fill = not fill
        self.ln(4)


def build_report():
    pdf = ReportPDF(orientation="P", unit="mm", format="A4")
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)

    # =====================================================================
    #  TITLE PAGE
    # =====================================================================
    pdf.add_page()
    pdf.ln(40)
    pdf.set_font("Helvetica", "B", 28)
    pdf.set_text_color(30, 80, 60)
    pdf.cell(0, 14, "Project Report", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
    pdf.set_font("Helvetica", "", 18)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(0, 10, "CNT-02: India E-Commerce Market Growth", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 10, "and Consumer Segmentation", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(8)

    pdf.set_draw_color(60, 130, 100)
    pdf.set_line_width(0.6)
    pdf.line(60, pdf.get_y(), pdf.w - 60, pdf.get_y())
    pdf.ln(10)

    pdf.set_font("Helvetica", "", 12)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 8, "A Fully Offline Python Analysis", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, "Electronics & Appliances Segment Focus", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(16)

    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 7, f"Date: {date.today().strftime('%B %d, %Y')}", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 7, "Language: Python 3.10+", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 7, "Runtime: Fully offline (no APIs / no network calls)", align="C", new_x="LMARGIN", new_y="NEXT")

    # =====================================================================
    #  TABLE OF CONTENTS
    # =====================================================================
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 20)
    pdf.set_text_color(30, 80, 60)
    pdf.cell(0, 12, "Table of Contents", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(6)

    toc_items = [
        ("1", "Executive Summary"),
        ("2", "Introduction & Objectives"),
        ("3", "Data Sources & Evidence"),
        ("4", "Methodology"),
        ("5", "Market Analysis & Visualisations"),
        ("6", "Scenario Forecasting"),
        ("7", "Survey Design"),
        ("8", "Consumer Segmentation Approach"),
        ("9", "Project Architecture"),
        ("10", "Results Summary"),
        ("11", "Limitations & Future Work"),
        ("12", "References"),
    ]
    pdf.set_font("Helvetica", "", 12)
    pdf.set_text_color(50, 50, 50)
    for num, title in toc_items:
        pdf.cell(10, 8, num + ".")
        pdf.cell(0, 8, title, new_x="LMARGIN", new_y="NEXT")

    # =====================================================================
    #  1. EXECUTIVE SUMMARY
    # =====================================================================
    pdf.add_page()
    pdf.chapter_title("1", "Executive Summary")
    pdf.body_text(
        "This report documents the CNT-02 project, an offline Python-based analysis of India's "
        "e-commerce market with an initial focus on the electronics and appliances segment. "
        "The project combines publicly available market data from IBEF and NITI Aayog with "
        "an original consumer survey instrument to study market growth trends, build illustrative "
        "scenario forecasts, and explore consumer segmentation."
    )
    pdf.body_text(
        "Key findings from the market data analysis show that India's total e-commerce market "
        "reached US$125 billion in 2024 (IBEF), with the online electronics and appliances "
        "sub-segment estimated at US$27 billion and online smartphones at US$39 billion "
        "(NITI Aayog). The project generates three growth scenarios (Conservative at 8% CAGR, "
        "Base at 12% CAGR, and Optimistic at 16% CAGR) projecting the electronics TAM from "
        "2024 to 2030, alongside an illustrative SAM at 30% reachable share."
    )
    pdf.body_text(
        "A 14-question consumer survey has been designed covering demographics, online shopping "
        "behaviour, spending patterns, price sensitivity, and purchase influences (EMI, exchange "
        "offers, delivery cost). An optional K-means clustering pipeline is included for "
        "exploratory consumer segmentation when numeric influence scores are collected."
    )

    # =====================================================================
    #  2. INTRODUCTION & OBJECTIVES
    # =====================================================================
    pdf.add_page()
    pdf.chapter_title("2", "Introduction & Objectives")
    pdf.body_text(
        "India's e-commerce market has experienced rapid growth, driven by rising internet "
        "penetration, affordable smartphones, digital payment infrastructure (UPI), and a large "
        "young population. The electronics and appliances category is one of the highest-value "
        "segments in online retail, making it a compelling area for academic study."
    )
    pdf.section_title("Project Objectives")
    pdf.bullet("Visualise the trajectory of India's total e-commerce market (2021-2035) using official data.")
    pdf.bullet("Benchmark the electronics & appliances and smartphones sub-segments.")
    pdf.bullet("Build illustrative growth scenario projections (Conservative, Base, Optimistic).")
    pdf.bullet("Estimate a Total Addressable Market (TAM) and Serviceable Addressable Market (SAM).")
    pdf.bullet("Design a consumer survey instrument for primary data collection.")
    pdf.bullet("Provide an exploratory K-means clustering pipeline for consumer segmentation.")
    pdf.bullet("Ensure the entire analysis runs fully offline with no API or internet dependencies.")

    # =====================================================================
    #  3. DATA SOURCES & EVIDENCE
    # =====================================================================
    pdf.add_page()
    pdf.chapter_title("3", "Data Sources & Evidence")

    pdf.section_title("3.1 India E-Commerce Market Data")
    pdf.body_text(
        "The primary market dataset (data/india_ecommerce_market.csv) contains 11 observations "
        "drawn from two authoritative sources:"
    )

    headers = ["Year", "Value (US$ bn)", "Status", "Scope", "Source"]
    rows = [
        ["2021", "67", "Reported", "Total e-commerce", "IBEF"],
        ["2022", "84", "Reported", "Total e-commerce", "IBEF"],
        ["2023", "102", "Reported", "Total e-commerce", "IBEF"],
        ["2024", "125", "Reported", "Total e-commerce", "IBEF"],
        ["2025", "145", "Forecast", "Total e-commerce", "IBEF"],
        ["2026", "163", "Forecast", "Total e-commerce", "IBEF"],
        ["2030", "345", "Forecast", "Total e-commerce", "IBEF"],
        ["2035", "550", "Forecast", "Total e-commerce", "IBEF"],
        ["2024", "27", "Estimate", "Online electronics", "NITI Aayog"],
        ["2024", "39", "Estimate", "Online smartphones", "NITI Aayog"],
    ]
    col_w = [18, 28, 24, 48, 44]
    # Check space
    if pdf.get_y() > pdf.h - 100:
        pdf.add_page()
    pdf.add_table(headers, rows, col_w)

    pdf.section_title("3.2 Key Assumptions")
    pdf.bullet("Scenario CAGRs (8%, 12%, 16%) are illustrative, not official forecasts.")
    pdf.bullet("Default SAM reachability factor of 30% is an assumption for sizing exercises.")
    pdf.bullet("IBEF's 2025+ values are forecasts published in that source, not measured outcomes.")
    pdf.bullet("NITI Aayog's electronics and smartphones are separate, non-overlapping categories.")

    # =====================================================================
    #  4. METHODOLOGY
    # =====================================================================
    pdf.add_page()
    pdf.chapter_title("4", "Methodology")

    pdf.section_title("4.1 Market Trend Analysis")
    pdf.body_text(
        "Historical and forecast market values are plotted as a time-series line chart, "
        "distinguishing reported values from forecast projections using different series. "
        "This allows visual assessment of the growth trajectory and the gap between actuals "
        "and forecasts."
    )

    pdf.section_title("4.2 Category Benchmarking")
    pdf.body_text(
        "A horizontal bar chart compares the 2024 market sizes of the two electronics "
        "sub-categories (Electronics & Appliances at US$27bn versus Smartphones at US$39bn) "
        "to contextualise the target segment within the broader electronics vertical."
    )

    pdf.section_title("4.3 Scenario Forecasting")
    pdf.body_text(
        "Three compound annual growth rate (CAGR) scenarios are applied to the 2024 electronics "
        "TAM (US$27bn) and projected forward to 2030:"
    )
    pdf.bullet("Conservative: 8% CAGR - yields US$42.8bn by 2030")
    pdf.bullet("Base: 12% CAGR - yields US$53.3bn by 2030")
    pdf.bullet("Optimistic: 16% CAGR - yields US$65.8bn by 2030")
    pdf.body_text(
        "The formula used is:  TAM(year) = TAM(2024) x (1 + CAGR) ^ (year - 2024). "
        "An illustrative SAM is computed as 30% of the projected TAM."
    )

    pdf.section_title("4.4 Consumer Segmentation (Optional)")
    pdf.body_text(
        "When survey data with numeric influence scores is available, a K-means clustering "
        "algorithm (k=3) is applied after StandardScaler normalisation. Features used include "
        "discount_importance, emi_influence_score, exchange_influence_score, and "
        "delivery_cost_influence_score. A minimum of 10 valid observations is required."
    )

    # =====================================================================
    #  5. MARKET ANALYSIS & VISUALISATIONS
    # =====================================================================
    pdf.add_page()
    pdf.chapter_title("5", "Market Analysis & Visualisations")

    pdf.section_title("5.1 India E-Commerce Market Trend")
    pdf.body_text(
        "The chart below shows India's total e-commerce market from 2021 to 2035, "
        "distinguishing reported values (2021-2024) from IBEF forecasts (2025 onwards). "
        "The market grew from US$67bn in 2021 to US$125bn in 2024 and is forecast to "
        "reach US$550bn by 2035."
    )
    pdf.add_figure(FIG / "01_india_market_trend.png",
                   "Figure 1: India e-commerce market - reported values and forecasts (Source: IBEF)")

    pdf.section_title("5.2 Electronics Category Benchmark")
    pdf.body_text(
        "The horizontal bar chart compares the two online electronics categories reported "
        "by NITI Aayog for 2024. Smartphones (US$39bn) is a larger category than Electronics "
        "& Appliances (US$27bn), though they are classified as separate segments."
    )
    pdf.add_figure(FIG / "02_category_benchmark.png",
                   "Figure 2: Selected online electronics categories in India, 2024 (Source: NITI Aayog)")

    # =====================================================================
    #  6. SCENARIO FORECASTING
    # =====================================================================
    pdf.add_page()
    pdf.chapter_title("6", "Scenario Forecasting")

    pdf.section_title("6.1 Growth Scenario Projections")
    pdf.body_text(
        "The three growth scenarios project the electronics & appliances TAM from 2024 to 2030. "
        "Under the base case (12% CAGR), the market roughly doubles to US$53.3bn by 2030. "
        "The conservative and optimistic scenarios bracket this at US$42.8bn and US$65.8bn "
        "respectively."
    )
    pdf.add_figure(FIG / "03_tam_scenarios.png",
                   "Figure 3: Electronics & appliances - illustrative growth scenarios (2024-2030)")

    pdf.section_title("6.2 Scenario Forecast Data")
    # Condensed table - 2024 and 2030 endpoints only
    headers2 = ["Scenario", "CAGR", "TAM 2024", "TAM 2030", "SAM 2030"]
    rows2 = [
        ["Conservative", "8%", "$27.0bn", "$42.8bn", "$12.9bn"],
        ["Base", "12%", "$27.0bn", "$53.3bn", "$16.0bn"],
        ["Optimistic", "16%", "$27.0bn", "$65.8bn", "$19.7bn"],
    ]
    pdf.add_table(headers2, rows2, [34, 20, 34, 34, 34])

    pdf.section_title("6.3 TAM vs SAM Sizing")
    pdf.body_text(
        "The chart below compares the 2024 Total Addressable Market (US$27bn) to the "
        "illustrative Serviceable Addressable Market (US$8.1bn), computed at a 30% reachable "
        "share. This SAM factor is an assumption and must be validated with actual market "
        "evidence and competitive analysis."
    )
    pdf.add_figure(FIG / "04_tam_sam.png",
                   "Figure 4: 2024 India electronics & appliances - TAM vs illustrative SAM")

    # =====================================================================
    #  7. SURVEY DESIGN
    # =====================================================================
    pdf.add_page()
    pdf.chapter_title("7", "Survey Design")

    pdf.body_text(
        "A 14-question consumer survey instrument has been designed to collect primary data "
        "on online electronics shopping behaviour in India. The survey is structured in five "
        "sections with built-in consent and privacy protections."
    )

    pdf.section_title("7.1 Survey Structure")
    headers3 = ["Section", "Questions", "Focus Area"]
    rows3 = [
        ["1. Consent", "Q1", "Informed voluntary consent"],
        ["2. Demographics", "Q2-Q4", "State/UT, residence type, age band"],
        ["3. Shopping Behaviour", "Q5-Q7", "Online purchase history, category, frequency"],
        ["4. Spending & Sensitivity", "Q8-Q10", "Spend band, price sensitivity, discount importance"],
        ["5. Purchase Influences", "Q11-Q14", "EMI, exchange, delivery cost, price threshold"],
    ]
    pdf.add_table(headers3, rows3, [32, 24, 110])

    pdf.section_title("7.2 Key Design Principles")
    pdf.bullet("Anonymous: no name, phone number, exact address, or payment details collected.")
    pdf.bullet("Voluntary: respondents may skip any question or stop at any time.")
    pdf.bullet("Brief: estimated completion time of 3-5 minutes to maximise response rates.")
    pdf.bullet("Categorical responses: ordinal scales and bands used for quantitative analysis.")

    pdf.section_title("7.3 Data Schema")
    pdf.body_text(
        "Survey responses are stored in data/survey_responses.csv following the schema defined "
        "in data/survey_template.csv with 14 fields: respondent_id, state_ut, residence_type, "
        "age_band, online_purchase_12m, preferred_category, purchase_frequency_12m, "
        "spend_band_inr, price_sensitivity, discount_importance, emi_influence, "
        "exchange_influence, delivery_cost_influence, and consent."
    )

    # =====================================================================
    #  8. CONSUMER SEGMENTATION APPROACH
    # =====================================================================
    pdf.add_page()
    pdf.chapter_title("8", "Consumer Segmentation Approach")

    pdf.body_text(
        "The project includes an optional K-means clustering pipeline for exploratory consumer "
        "segmentation. This pipeline activates only when survey data with pre-coded numeric "
        "influence scores is available."
    )

    pdf.section_title("8.1 Clustering Pipeline")
    pdf.bullet("Features: discount_importance, emi_influence_score, exchange_influence_score, delivery_cost_influence_score")
    pdf.bullet("Pre-processing: StandardScaler normalisation to zero mean, unit variance")
    pdf.bullet("Algorithm: K-means with k=3 clusters, random_state=42, n_init=10")
    pdf.bullet("Minimum sample: 10 valid (non-null) observations required")
    pdf.bullet("Output: outputs/exploratory_consumer_segments.csv with cluster assignments")

    pdf.section_title("8.2 Interpretation Guidance")
    pdf.body_text(
        "Clusters should be profiled by examining the mean influence scores within each group "
        "before assigning segment names. The exploratory nature of the analysis means that "
        "segments should not be treated as definitive market segments without validation "
        "through larger, representative samples and additional research."
    )

    # =====================================================================
    #  9. PROJECT ARCHITECTURE
    # =====================================================================
    pdf.add_page()
    pdf.chapter_title("9", "Project Architecture")

    pdf.section_title("9.1 Technology Stack")
    pdf.bullet("Language: Python 3.10+")
    pdf.bullet("Core libraries: NumPy (>=1.24), pandas (>=2.0), Matplotlib (>=3.7)")
    pdf.bullet("Optional: scikit-learn (>=1.3) for K-means clustering")
    pdf.bullet("Report generation: fpdf2")
    pdf.bullet("Runtime: Fully offline - no API calls or internet access at runtime")

    pdf.section_title("9.2 Project Structure")
    structure = [
        ["run_project.py", "Main analysis script - generates all charts and data"],
        ["generate_report.py", "PDF report generator (this script)"],
        ["requirements.txt", "Python package dependencies"],
        ["run_windows.bat", "Windows batch launcher"],
        ["data/", "Input data directory"],
        ["  india_ecommerce_market.csv", "Market data from IBEF and NITI Aayog"],
        ["  survey_template.csv", "Schema for survey responses"],
        ["docs/", "Documentation"],
        ["  survey_questionnaire.md", "Full survey instrument (14 questions)"],
        ["outputs/", "Generated outputs"],
        ["  figures/", "PNG chart files (01-04 core, 05-10 optional)"],
        ["  electronics_scenario_forecast.csv", "Scenario projection data"],
        ["  CNT02_Project_Report.pdf", "This project report"],
    ]
    headers4 = ["File / Directory", "Description"]
    pdf.add_table(headers4, structure, [70, 96])

    pdf.section_title("9.3 Execution Flow")
    pdf.body_text(
        "1. setup() creates the output directories.\n"
        "2. market_data() loads the CSV dataset.\n"
        "3. save_market_trend() generates the time-series line chart (Figure 1).\n"
        "4. save_category_chart() generates the category benchmark bar chart (Figure 2).\n"
        "5. scenario_table() computes and exports the 3-scenario forecast CSV.\n"
        "6. save_scenario_chart() generates the scenario projection chart (Figure 3).\n"
        "7. save_tam_sam() generates the TAM vs SAM chart (Figure 4).\n"
        "8. analyse_transactions() processes optional transaction data (Figures 5-6).\n"
        "9. analyse_survey() processes optional survey data (Figures 7-10) and clustering."
    )

    # =====================================================================
    #  10. RESULTS SUMMARY
    # =====================================================================
    pdf.add_page()
    pdf.chapter_title("10", "Results Summary")

    pdf.section_title("10.1 Market Growth")
    pdf.bullet("India's total e-commerce market grew from US$67bn (2021) to US$125bn (2024) - an 86% increase over 3 years.")
    pdf.bullet("IBEF forecasts project growth to US$345bn by 2030 and US$550bn by 2035.")
    pdf.bullet("The online electronics & appliances segment was estimated at US$27bn in 2024.")

    pdf.section_title("10.2 Scenario Projections")
    pdf.bullet("Conservative (8% CAGR): Electronics TAM reaches US$42.8bn by 2030.")
    pdf.bullet("Base (12% CAGR): Electronics TAM reaches US$53.3bn by 2030.")
    pdf.bullet("Optimistic (16% CAGR): Electronics TAM reaches US$65.8bn by 2030.")
    pdf.bullet("At 30% SAM share, the base-case addressable market is US$16.0bn by 2030.")

    pdf.section_title("10.3 Outputs Generated")
    pdf.bullet("4 core visualisation charts (Figures 1-4)")
    pdf.bullet("Scenario forecast CSV with 21 data points (3 scenarios x 7 years)")
    pdf.bullet("Survey instrument with 14 questions across 5 sections")
    pdf.bullet("Optional: transaction analysis charts and consumer segment clusters")

    # =====================================================================
    #  11. LIMITATIONS & FUTURE WORK
    # =====================================================================
    pdf.add_page()
    pdf.chapter_title("11", "Limitations & Future Work")

    pdf.section_title("11.1 Limitations")
    pdf.bullet("Convenience survey samples are not nationally representative of India's population.")
    pdf.bullet("Self-reported price sensitivity is not the same as observed price elasticity.")
    pdf.bullet("The SAM share (30%) and growth scenario CAGRs are assumptions, not measured values.")
    pdf.bullet("IBEF forecast values for 2025+ are projections, not observed market outcomes.")
    pdf.bullet("MoSPI HCES measures household consumption expenditure, not online transactions.")
    pdf.bullet("The K-means segmentation (k=3) is exploratory; optimal k should be validated.")

    pdf.section_title("11.2 Future Work")
    pdf.bullet("Collect primary survey data across diverse Indian states and demographic groups.")
    pdf.bullet("Validate scenario assumptions against additional industry reports and analyst forecasts.")
    pdf.bullet("Incorporate transaction data analysis for empirical purchasing pattern insights.")
    pdf.bullet("Test multiple values of k and use silhouette analysis for optimal cluster selection.")
    pdf.bullet("Add regional (state-level) analysis of e-commerce adoption and category preferences.")
    pdf.bullet("Integrate time-series forecasting models (ARIMA, Prophet) for more rigorous projections.")

    # =====================================================================
    #  12. REFERENCES
    # =====================================================================
    pdf.add_page()
    pdf.chapter_title("12", "References")

    refs = [
        ("IBEF (2025)", "India E-Commerce Infographic, August 2025.",
         "https://www.ibef.org/uploads/industry/Infrographics/large/e-Commerce-infographics-august-2025.pdf"),
        ("NITI Aayog (2026)", "Trade Watch Quarterly, Q2 FY 2025-26, July-September.",
         "https://niti.gov.in/sites/default/files/2026-02/Trade-Watch-Quarterly-July-September-Q2-FY-2025-26.pdf"),
        ("MoSPI", "Household Consumer Expenditure Survey (HCES).",
         "https://microdata.gov.in/NADA/index.php/catalog/CEXP"),
    ]
    for i, (author, title, url) in enumerate(refs, 1):
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(40, 40, 40)
        pdf.cell(8, 6, f"[{i}]")
        pdf.cell(0, 6, f"{author}", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "I", 10)
        pdf.cell(8, 6, "")
        pdf.cell(0, 6, title, new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(50, 100, 150)
        pdf.cell(8, 6, "")
        pdf.cell(0, 6, url, new_x="LMARGIN", new_y="NEXT")
        pdf.ln(4)

    # ---- End matter ----
    pdf.ln(10)
    pdf.set_draw_color(60, 130, 100)
    pdf.set_line_width(0.4)
    pdf.line(10, pdf.get_y(), pdf.w - 10, pdf.get_y())
    pdf.ln(6)
    pdf.set_font("Helvetica", "I", 10)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 6, "End of Report", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 6, f"Generated on {date.today().strftime('%B %d, %Y')}", align="C")

    # ---- Save ----
    OUT.mkdir(parents=True, exist_ok=True)
    pdf.output(str(REPORT_PATH))
    print(f"\nReport saved: {REPORT_PATH}")
    print(f"Pages: {pdf.page_no()}")
    if sys.platform == "win32":
        os.startfile(str(REPORT_PATH))


if __name__ == "__main__":
    build_report()
