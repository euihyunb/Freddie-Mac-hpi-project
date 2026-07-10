import pandas as pd
import numpy as np

#01_Data_exploration Notebook
org_columns = [
    'credit_score', 'first_payment_date', 'first_time_homebuyer_flag',
    'maturity_date', 'msa', 'mi_percent', 'number_of_units',
    'occupancy_status', 'original_cltv', 'original_dti', 'original_upb',
    'original_ltv', 'original_interest_rate', 'channel', 'ppm_flag',
    'amortization_type', 'property_state', 'property_type', 'postal_code',
    'loan_sequence_number', 'loan_purpose', 'original_loan_term',
    'number_of_borrowers', 'seller_name', 'servicer_name',
    'super_conforming_flag', 'pre_harp_loan_sequence_number',
    'program_indicator', 'harp_indicator', 'property_valuation_method',
    'interest_only_indicator', 'mi_cancellation_indicator'
]

def load_orig_data(year):
    file_path = f'../data/raw/sample_{year}/sample_orig_{year}.txt'

    df = pd.read_csv(
        file_path,
        sep='|',
        header=None,
        names=org_columns,
        dtype={'pre_harp_loan_sequence_number': str, 'harp_indicator': str},
        low_memory=False
    )
    return df

def clean_orig_data(df):
    df = df.copy()

    df['credit_score'] = df['credit_score'].replace(9999, np.nan)
    df['original_dti'] = df['original_dti'].replace(999, np.nan)
    df['original_cltv'] = df['original_cltv'].replace(999, np.nan)
    df['original_ltv'] = df['original_ltv'].replace(999, np.nan)

    df['implied_property_val'] = df['original_upb'] / (df['original_ltv']/100) / 1000000

    return df

#02 Default Modeling Notebook

svcg_columns = [
    'loan_sequence_number', 'monthly_reporting_period', 'current_actual_upb',
    'current_loan_delinquency_status', 'loan_age', 'remaining_months_to_maturity',
    'defect_settlement_date', 'modification_flag', 'zero_balance_code',
    'zero_balance_effective_date', 'current_interest_rate', 'current_deferred_upb',
    'ddlpi', 'mi_recoveries', 'net_sales_proceeds', 'non_mi_recoveries',
    'expenses', 'legal_costs', 'maintenance_preservation_costs', 'taxes_insurance',
    'miscellaneous_expenses', 'actual_loss_calculation', 'modification_cost',
    'step_modification_flag', 'deferred_payment_plan', 'estimated_ltv',
    'zero_balance_removal_upb', 'delinquent_accrued_interest',
    'delinquency_due_to_disaster', 'borrower_assistance_status_code',
    'current_month_modification_cost', 'interest_bearing_upb'
]

def load_svcg_data(year):
    file_path = f'../data/raw/sample_{year}/sample_svcg_{year}.txt'

    df = pd.read_csv(
        file_path,
        sep='|',
        header=None,
        names=svcg_columns,
        low_memory=False
    )

    return df

def get_default_labels(year):
    df_svcg = load_svcg_data(year)

    #Convert delinquency status to numeric & non-numeric codes becomes NaN
    df_svcg['delinquency_status_numeric'] = pd.to_numeric(
        df_svcg['current_loan_delinquency_status'], errors='coerce'
    )

    #For each loan, find the maximum delinquency status ever observed
    max_delinquency_status = df_svcg.groupby('loan_sequence_number')['delinquency_status_numeric'].max()

    # Default = ever reached 3+ months delinquent
    default_flag = (max_delinquency_status >= 3).astype(int)

    default_labels_df = default_flag.reset_index()
    default_labels_df.columns = ['loan_sequence_number', 'default_flag']

    return default_labels_df

def build_model_dataset(year):
    df_orig = load_orig_data(year)
    df_orig = clean_orig_data(df_orig)
    df_orig['vintage_year'] = year

    default_labels_df = get_default_labels(year)

    df_model = df_orig.merge(default_labels_df, on='loan_sequence_number', how='left')

    return  df_model

#03 Prepayment Modeling Notebook
def get_prepayment_labels(year):
    df_svcg = load_svcg_data(year)

    max_prepay_flag = df_svcg.groupby('loan_sequence_number')['zero_balance_code'].apply(
        lambda x: (x == 1).any()
    )

    prepay_flag = max_prepay_flag.astype(int)

    prepay_labels_df = prepay_flag.reset_index()
    prepay_labels_df.columns = ['loan_sequence_number', 'prepay_flag']

    return prepay_labels_df

def build_prepayment_dataset(year):
    df_orig = load_orig_data(year)
    df_orig = clean_orig_data(df_orig)
    df_orig['vintage_year'] = year

    prepay_labels_df = get_prepayment_labels(year)

    df_model = df_orig.merge(prepay_labels_df, on='loan_sequence_number', how='left')

    return df_model
