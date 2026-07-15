# Freddie Mac Mortgage Analytics Portfolio

## Overview
This repository is a collection of data analysis and modeling projects built on 
Freddie Mac's publicly available Single-Family Loan-Level Dataset (SFLLD). The goal 
is to explore mortgage performance, house price trends, and credit risk through a 
progression of projects — starting with exploratory data analysis and simple 
price-trend indices, and building toward predictive default/prepayment models and 
model validation (backtesting, stress testing).

## Motivation
This portfolio was built to develop hands-on experience in quantitative mortgage 
and housing analytics, combining a background in macro-financial research with 
applied data science and modeling skills relevant to mortgage credit risk and 
house price modeling roles.

## Data Source
- Freddie Mac Single-Family Loan-Level Dataset (Sample), origination vintages 2018–2025
- Includes origination files (`sample_orig_YYYY`) and monthly performance files (`sample_svcg_YYYY`)
- **Note:** Raw data is not included in this repository due to Freddie Mac's data 
  licensing terms. To reproduce this analysis, request access and download the 
  sample dataset directly from 
  [Freddie Mac's Single-Family Loan-Level Dataset page](https://www.freddiemac.com/research/datasets/sf-loanlevel-dataset).

## Projects

| # | Project | Status |
|---|---------|--------|
| 1 | Exploratory Data Analysis of Loan Performance | Done   |
| 2 | Home Value Trend Index (vs. FHFA HPI benchmark) | Done   |
| 3 | Default / Prepayment Prediction Models | Done   |
| 4 | Default Model Improvement | Done   |
| 5 | Prepayment Rate Sensitivity & Stress Testing | Done   |

### Project 1: Exploratory Data Analysis of Loan Performance

Explored Freddie Mac's Single-Family Loan-Level Dataset (2018–2025 sample 
vintages), examining credit score distributions, geographic concentration of 
loan volume, and the distribution of loan-implied property values. Built the 
core reusable data-loading and cleaning pipeline (`src/data_loader.py`) used 
throughout the rest of this portfolio, including handling of special missing-
value codes and construction of the `implied_property_value` metric (Original 
UPB ÷ Original LTV) used as the starting point for Project 2.

Full analysis in `notebooks/01_data_exploration.ipynb`.

### Project 2: Home Value Trend Index

Built a simplified house-price proxy using Freddie Mac loan-level origination 
data (implied property value = Original UPB ÷ Original LTV), then benchmarked 
it against the official FHFA House Price Index (2018–2025). The comparison 
revealed that a simple average of loan-implied values diverges substantially 
from the true repeat-sales FHFA HPI throughout the period — driven largely by 
shifts in loan-purpose composition (e.g., the sharp swing toward purchase 
loans during the 2022 rate-hike cycle). This highlights why repeat-sales 
methodologies exist and is documented in detail in `notebooks/01_data_exploration.ipynb`.

### Project 3: Default & Prepayment Prediction Modeling

Built and compared Logistic Regression and Random Forest models to predict 
two mortgage outcomes — default (90+ days delinquent) and prepayment 
(voluntary payoff) — using origination-time loan characteristics, restricted 
to vintage years (2018–2022) with sufficient performance history.

- **Default model** (`02_default_modeling.ipynb`): Logistic Regression and 
  Random Forest performed similarly (ROC-AUC ~0.76), suggesting the modeling 
  ceiling is driven by limited feature scope rather than model complexity. 
  Credit score, interest rate, and DTI account for ~75% of feature importance.
- **Prepayment model** (`03_prepayment_modeling.ipynb`): Random Forest 
  substantially outperformed Logistic Regression (ROC-AUC 0.747 vs. 0.633), 
  and interest rate alone accounts for 76% of feature importance — confirming 
  a strong "lock-in effect" where borrowers with historically low rates have 
  little incentive to refinance.

Together, these two models illustrate a meaningful contrast: default risk is 
primarily explained by static borrower characteristics, while prepayment 
behavior is driven more by the interest rate environment and its interaction 
with loan characteristics — a distinction with practical relevance for 
mortgage risk and prepayment speed modeling.

Full analysis in `notebooks/03_prepayment_modeling.ipynb`.

### Project 4: Default Model Improvement

Tested whether the baseline default model could be meaningfully improved 
through richer features (categorical variables, macroeconomic indicators) or 
more realistic validation (time-based backtest). Neither categorical features 
(ROC-AUC 0.774) nor macroeconomic features — rate spread, state unemployment, 
and HPI change, all sourced via the FRED API (ROC-AUC 0.772) — meaningfully 
outperformed the original baseline (0.769), consistent with academic 
literature suggesting default is dominated by core underwriting variables 
(credit score, LTV, DTI). A time-based backtest (train 2018-2020, test 
2021-2022) showed a modest, expected performance decline (ROC-AUC 0.746), 
reflecting a genuine shift in default rates between the two periods.

This project's negative/marginal results are, in their own way, a meaningful 
finding: they highlight a real contrast with the prepayment model (Project 5), 
where a single engineered feature drove a large improvement — illustrating 
that default and prepayment are fundamentally different prediction problems 
requiring different modeling strategies.

Full analysis in `notebooks/04_default_model_improvement.ipynb`.

### Project 5: Prepayment Rate Sensitivity & Stress Testing

Extended the baseline prepayment model by engineering a "rate spread" feature 
(market rate 24 months post-origination minus original rate), empirically 
grounded by analyzing when prepayment activity actually peaks in the data. 
This feature substantially improved prediction (ROC-AUC 0.747 → 0.814) and 
became the dominant predictor, confirming that refinancing incentive is 
better captured by the *relative* gap between a loan's rate and prevailing 
market rates than by the raw origination rate alone.

Using the trained model, simulated interest rate shocks (±2 percentage points) 
to stress-test prepayment behavior. Results revealed vintage-specific ceiling 
and floor effects — loans from low-rate periods (2020-2022) are highly 
sensitive to further rate declines (a -2pp shock nearly triples predicted 
prepayment probability for 2022 loans), while loans from higher-rate periods 
(2018) show the opposite pattern. This illustrates the "convexity risk" 
central to mortgage servicing and MBS investment risk management.

Full analysis in `notebooks/05_prepayment_rate_sensitivity.ipynb`.

## Repository Structure
```├──data/           # raw and processed data (not tracked in git — see Data Source)
├── notebooks/       # exploratory analysis notebooks
├── src/             # reusable Python modules
├── outputs/
│   ├── figures/     # charts and visualizations
│   └── reports/     # written summaries of findings
``` 

## How to Reproduce

### 1. Clone and set up the environment

Clone the repository and install dependencies:

`git clone https://github.com/euihyunb/Freddie-Mac-hpi-project.git`
`cd freddie-mac-hpi-project`
`pip install -r requirements.txt`

### 2. Download required data

**Freddie Mac SFLLD (required for all notebooks)**
- Register and download the Sample Dataset (2018–2025 vintages) from 
  [Freddie Mac's Clarity Data Intelligence portal](https://claritydownload.fmapps.freddiemac.com/CRT/#/sflld)
- Place each year's `sample_orig_YYYY` and `sample_svcg_YYYY` files in 
  `data/raw/sample_YYYY/`

**FHFA House Price Index (required for notebooks 01, 04)**
- Download the Annual, All-Transactions, National HPI from 
  [FHFA](https://fhfa.gov/hpi/download/annual/hpi_at_national.xlsx)
- Place in `data/raw/fhfa/hpi_at_national.xlsx`

**FRED Market Mortgage Rates (required for notebooks 04, 05)**
- Download the monthly 30-Year Fixed Rate Mortgage Average (MORTGAGE30US) 
  from [FRED](https://fred.stlouisfed.org/series/MORTGAGE30US)
- Place in `data/raw/fred/MORTGAGE30US.csv`

**FRED State Unemployment Rates (required for notebook 04)**
- Obtain a free FRED API key: https://fred.stlouisfed.org/docs/api/api_key.html
- Create a `.env` file in the project root: `FRED_API_KEY=your_key_here` 
  (excluded from git via `.gitignore`)
- Run the data retrieval code in `notebooks/04_default_model_improvement.ipynb` 
  to fetch and save `data/raw/fred/state_unemployment.csv`

### 3. Run notebooks sequentially

Run the notebooks in order, 01 through 05. Each notebook uses reusable 
functions from `src/data_loader.py` for data loading, cleaning, and feature 
engineering, and later notebooks build on data/features established earlier.

- `01_data_exploration.ipynb`
- `02_default_modeling.ipynb`
- `03_prepayment_modeling.ipynb`
- `04_default_model_improvement.ipynb`
- `05_prepayment_rate_sensitivity.ipynb`

### 1. Clone and set up the environment
git clone <repo-url>
cd freddie-mac-mortgage-analytics-portfolio
pip install -r requirements.txt
## Tools Used
- **Language:** Python
- **Data manipulation:** pandas, numpy
- **Visualization:** matplotlib
- **Machine learning:** scikit-learn (Logistic Regression, Random Forest)
- **File formats:** openpyxl (Excel), requests via fredapi (API)
- **External data sources:** FRED API (fredapi), FHFA HPI (Excel download)
- **Environment & secrets management:** python-dotenv (for FRED API key)
- **Development environment:** Jupyter Notebook (via PyCharm), Git/GitHub

## Author
Euihyun Bae — [LinkedIn: https://www.linkedin.com/in/euihyun-bae/ / euihyunb@gmail.com]