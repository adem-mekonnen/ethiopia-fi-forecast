### 1. Repository Folder Structure

```text
ethiopia-fi-forecast/
├── .github/workflows/
│   └── unittests.yml
├── dashboard/
│   └── app.py                  # Streamlit application (Task 5)
├── data/
│   ├── raw/                    # Original starter files
│   │   ├── Additional Data Points Guide.xlsx
│   │   ├── ethiopia_fi_unified_data.xlsx
│   │   └── reference_codes.xlsx
│   ├── processed/              # Output from Task 1
│   │   └── ethiopia_fi_enriched.csv
│   └── data_enrichment_log.md  # Documentation for Task 1
├── models/                     # Saved models (Task 3/4)
├── notebooks/
│   ├── 01_data_enrichment.ipynb
│   └── 02_exploratory_data_analysis.ipynb
├── reports/
│   ├── figures/                # Exported charts from EDA
│   └── eda_insights.md         # Summary of at least 5 key insights
├── src/
│   ├── __init__.py
│   └── task1_enrichment.py     # Python script for data processing
├── tests/
│   └── __init__.py
├── .gitignore                  # Environment and data ignore rules
├── README.md                   # Main Project Documentation
├── requirements.txt            # Project dependencies
└── venv/                       # Virtual environment (ignored by git)
```

---

### 2. Main Project README (`README.md`)

```markdown
# Ethiopia Financial Inclusion Forecasting System

## Project Overview
This repository contains a data science project aimed at tracking and forecasting Ethiopia's digital financial transformation. Using the World Bank Global Findex framework, we model the trajectory of **Access** (Account Ownership) and **Usage** (Digital Payment Adoption) from 2011 to 2027.

## Business Need
The consortium of stakeholders (DFIs, NBE, and Mobile Money Operators) requires an understanding of:
1. Drivers of financial inclusion in Ethiopia.
2. The impact of product launches (Telebirr, M-Pesa) and policy changes (Digital ID).
3. Projections for 2026 and 2027.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/ethiopia-fi-forecast.git
   ```
2. Set up virtual environment:
   ```bash
   python -m venv venv
   source venv/Scripts/activate # Windows
   pip install -r requirements.txt
   ```

## Tasks Progress
- [x] **Task 1: Data Exploration & Enrichment** - Complete
- [x] **Task 2: Exploratory Data Analysis** - Complete
- [ ] **Task 3: Event Impact Modeling** - In Progress
- [ ] **Task 4: Forecasting** - Planned
- [ ] **Task 5: Dashboard** - Planned
```

---

### 3. Task 1 README (`data/data_enrichment_log.md`)

```markdown
# Task 1: Data Enrichment Log

## Objective
Enrich the unified starter dataset with high-frequency infrastructure data and key national events to improve model sensitivity.

## Schema Rules
- **Observations:** Must include `pillar`, `indicator_code`, and `value_numeric`.
- **Events:** Must include `category` (policy, infrastructure, etc.) and `event_name`. `pillar` is left empty.
- **Impact Links:** Must use `parent_id` to link back to a specific `event_id`.

## Additions
| Date Added | Type | Code | Description | Rationale |
| :--- | :--- | :--- | :--- | :--- |
| 2026-01-30 | Observation | `USG_MM_VOL` | Mobile Money Transaction Volume (4.8T ETB) | Captures the depth of usage not seen in % rates. |
| 2026-01-30 | Event | `EVT_FAYDA_2024` | Fayda Digital ID Mass Enrollment | Primary enabler for solving KYC issues. |
| 2026-01-30 | Observation | `INF_4G_COVERAGE` | 4G Network Expansion % | Leading indicator for digital payment growth. |
| 2026-01-30 | Impact Link | `LNK_FAYDA_ACC` | Fayda -> ACC_OWNERSHIP | Models a 6-month lag for ID to bank account conversion. |

## Data Quality Assessment
- **High Confidence:** NBE Annual reports, Ethio Telecom infrastructure stats.
- **Medium Confidence:** Projected impact magnitudes based on India (Aadhaar) proxy studies.
```

---

### 4. Task 2 README (`reports/eda_insights.md`)

```markdown
# Task 2: Exploratory Data Analysis Insights

## Executive Summary
Analysis reveals an "Inclusion Paradox" in Ethiopia between 2021 and 2024. While digital payment usage surged, formal account ownership grew by only 3 percentage points.

## 5 Key Insights
1. **The Stagnation Paradox:** Account ownership slowed (+3pp) despite 54M+ Telebirr users. This suggests a transition in *how* current users pay, rather than *new* users entering the system.
2. **Dormancy Gap:** A significant gap exists between total registered mobile money accounts and Findex-reported usage, suggesting many accounts are "Multi-SIM" or inactive.
3. **Leading Infrastructure:** 4G expansion shows a strong positive correlation (0.8+) with Digital Payment Adoption, acting as a predictor for 2026 usage.
4. **P2P Dominance:** Digital P2P transfers have surpassed ATM withdrawals for the first time, signaling a shift away from cash-out behavior.
5. **Gender Gap:** Findex microdata suggests a persistent 10% gender gap in rural areas, primarily driven by lower smartphone ownership among women.

## Data Quality Limitations
- **Sparsity:** Findex data only provides 5 data points over 13 years, necessitating the use of the "Event Impact Model" in Task 3.
- **Mixed Formats:** Date formats required normalization from string to datetime objects.
```

