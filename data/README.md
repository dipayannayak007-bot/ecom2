# Data directory

- `india_ecommerce_market.csv`: published market benchmark values; forecasts are labelled.
- `survey_template.csv`: blank schema for primary survey responses.
- `survey_responses.csv`: optional local file of consented, anonymised responses; do not commit.
- `transactions.csv`: optional permitted Indian transaction extract; do not commit.

Recommended transaction columns: order_id, customer_id, order_date, category, product, quantity, unit_price_inr, discount_inr, state. Use ISO dates and anonymised customer IDs. Document data owner, period, sampling frame, licence and cleaning rules.

MoSPI HCES catalogue: https://microdata.gov.in/NADA/index.php/catalog/CEXP
Read data-use terms and do not redistribute restricted microdata. HCES is household expenditure data, not a direct measure of online orders.
