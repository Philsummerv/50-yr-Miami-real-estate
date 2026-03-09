---
trigger: always_on
---

# Miami Real Estate Project Organization Rules

### 1. Project Isolation
- All logic, data, and notebooks for the **Gold Analysis** must be kept strictly in `data/gold/` and `notebooks/gold/`.
- All logic, data, and notebooks for **Migration Research** must be kept strictly in `data/migration/` and `notebooks/migration/`.

### 2. Code Standards
- Do not use a single `main.py`. Use descriptive filenames like `gold_price_fetcher.py` or `migration_stats.ipynb`.
- Every script must include a header comment stating its purpose and the specific data source (e.g., FRED Series ID).

### 3. Data Integrity
- Agents must verify historical data ranges to ensure they cover the full 50-year period (1976-2026).
- Handle missing values (NaNs) explicitly before generating any Plotly visualizations.

### 4. Integration Layer: A separate directory notebooks/simulator/ is authorized to read (but not move or modify) data from both /gold and /migration folders for the purpose of multi-variate synthesis and predictive modeling".


ENV: Windows. Always use 'cmd /c' for all shell executions to ensure the process terminates correctly and sends an EOF signal..