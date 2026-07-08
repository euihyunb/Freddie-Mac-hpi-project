import pandas as pd
import numpy as np

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