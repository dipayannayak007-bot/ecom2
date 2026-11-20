# CNT-02 — India E-Commerce Market Growth and Consumer Segmentation (Python)

A fully local Python project for India's e-commerce market, initially focused on electronics and appliances. No network calls or APIs are used when running the analysis.

## Run offline

1. Install Python 3.10+.
2. Install dependencies once (internet access or local wheel files are required for first-time installation):

   `python -m pip install -r requirements.txt`

3. Disconnect from the internet and run:

   `python run_project.py`

   On Windows, you can double-click `run_windows.bat`.

The program creates `outputs/figures/` and `outputs/electronics_scenario_forecast.csv`.

## Visualisations and analysis

- India e-commerce market trend line graph.
- Selected electronics category comparison bar chart.
- Conservative, base and optimistic scenario line graph.
- TAM versus illustrative SAM chart.
- Optional transaction-value histogram and category sales chart when `data/transactions.csv` is provided.
- Optional survey charts for category preference, spending band, purchase frequency and price sensitivity when `data/survey_responses.csv` is provided.
- Optional K-means clustering only when pre-coded numeric influence scores are supplied.

## Optional real data

Copy anonymised, consented survey responses to `data/survey_responses.csv` using `data/survey_template.csv` as the schema. For transaction analysis, add a permitted transaction extract to `data/transactions.csv` with at least `quantity` and `unit_price_inr`; recommended additional fields are order_id, customer_id, order_date, category, product, discount_inr and state.

No synthetic survey or transaction observations are included. Do not commit personal data or restricted datasets.

## Evidence and assumptions

- IBEF's August 2025 infographic reports India's total e-commerce market at US$125bn in 2024. The 2025 onward values in the supplied data are forecasts in that publication.
- NITI Aayog Trade Watch Q2 FY2025-26 gives a 2024 estimate of US$27bn for online electronics and appliances and US$39bn for online smartphones. These are separate categories.
- The scenario CAGRs (8%, 12%, 16%) and default SAM reachability factor (30%) are illustrative assumptions, not official forecasts or measured market shares.
- MoSPI HCES measures household consumption expenditure, not online transactions.

## Sources

- NITI Aayog: https://niti.gov.in/sites/default/files/2026-02/Trade-Watch-Quarterly-July-September-Q2-FY-2025-26.pdf
- IBEF: https://www.ibef.org/uploads/industry/Infrographics/large/e-Commerce-%20infographics-august-2025.pdf
- MoSPI HCES: https://microdata.gov.in/NADA/index.php/catalog/CEXP

## Limitations

Convenience survey samples are not nationally representative. Self-reported price sensitivity is not observed price elasticity. The SAM share and growth scenarios must be validated with actual market evidence.
