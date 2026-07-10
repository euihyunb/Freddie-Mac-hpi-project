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

| # | Project | Status  |
|---|---------|---------|
| 1 | Exploratory Data Analysis of Loan Performance | Done    |
| 2 | Home Value Trend Index (vs. FHFA HPI benchmark) | Done    |
| 3 | Default / Prepayment Prediction Models | Done    |
| 4 | Model Backtesting & Stress Testing | Planned |

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

## Repository Structure
```├──data/           # raw and processed data (not tracked in git — see Data Source)
├── notebooks/       # exploratory analysis notebooks
├── src/             # reusable Python modules
├── outputs/
│   ├── figures/     # charts and visualizations
│   └── reports/     # written summaries of findings
``` 

## How to Reproduce
1. Request access to the Freddie Mac SFLLD sample dataset (link above)
2. Place downloaded files in `data/raw/sample_YYYY/`
3. Install dependencies: `pip install -r requirements.txt`
4. Run notebooks in `notebooks/` in numerical order

## Tools Used
Python, pandas, numpy, matplotlib, seaborn, Jupyter

## Author
Euihyun Bae — [LinkedIn: https://www.linkedin.com/in/euihyun-bae/ / euihyunb@gmail.com]