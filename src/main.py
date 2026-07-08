import duckdb
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
file_path = project_root / "data" / "2019Q1.csv"

#Open csv file
df = duckdb.query(f"""
    SELECT *
    FROM read_csv_auto('{file_path}', delim= '|', header = False)
    LIMIT 100000
""").df()

lppub_column_names = [
    "POOL_ID",
    "LOAN_ID",
    "ACT_PERIOD",
    "CHANNEL",
    "SELLER",
    "SERVICER",
    "MASTER_SERVICER",
    "ORIG_RATE",
    "CURR_RATE",
    "ORIG_UPB",
    "ISSUANCE_UPB",
    "CURRENT_UPB",
    "ORIG_TERM",
    "ORIG_DATE",
    "FIRST_PAY",
    "LOAN_AGE",
    "REM_MONTHS",
    "ADJ_REM_MONTHS",
    "MATR_DT",
    "OLTV",
    "OCLTV",
    "NUM_BO",
    "DTI",
    "CSCORE_B",
    "CSCORE_C",
    "FIRST_FLAG",
    "PURPOSE",
    "PROP",
    "NO_UNITS",
    "OCC_STAT",
    "STATE",
    "MSA",
    "ZIP",
    "MI_PCT",
    "PRODUCT",
    "PPMT_FLG",
    "IO",
    "FIRST_PAY_IO",
    "MNTHS_TO_AMTZ_IO",
    "DLQ_STATUS",
    "PMT_HISTORY",
    "MOD_FLAG",
    "MI_CANCEL_FLAG",
    "ZERO_BAL_CODE",
    "ZB_DTE",
    "LAST_UPB",
    "RPRCH_DTE",
    "CURR_SCHD_PRNCPL",
    "TOT_SCHD_PRNCPL",
    "UNSCHD_PRNCPL_CURR",
    "LAST_PAID_INSTALLMENT_DATE",
    "FORECLOSURE_DATE",
    "DISPOSITION_DATE",
    "FORECLOSURE_COSTS",
    "PROPERTY_PRESERVATION_AND_REPAIR_COSTS",
    "ASSET_RECOVERY_COSTS",
    "MISCELLANEOUS_HOLDING_EXPENSES_AND_CREDITS",
    "ASSOCIATED_TAXES_FOR_HOLDING_PROPERTY",
    "NET_SALES_PROCEEDS",
    "CREDIT_ENHANCEMENT_PROCEEDS",
    "REPURCHASES_MAKE_WHOLE_PROCEEDS",
    "OTHER_FORECLOSURE_PROCEEDS",
    "NON_INTEREST_BEARING_UPB",
    "PRINCIPAL_FORGIVENESS_AMOUNT"
]

df = df.iloc[:, :len(lppub_column_names)]
df.columns = lppub_column_names[:df.shape[1]]

print(df.shape)
print(len(lppub_column_names))

print(df[["LOAN_ID", "ACT_PERIOD", "CURRENT_UPB"]].head(20))