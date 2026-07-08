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
| 1 | Exploratory Data Analysis of Loan Performance | In Progress |
| 2 | Home Value Trend Index (vs. FHFA HPI benchmark) | Planned |
| 3 | Default / Prepayment Prediction Models | Planned |
| 4 | Model Backtesting & Stress Testing | Planned |

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
[Your Name] — [LinkedIn / email, optional]