import pandas as pd
import numpy as np

def loan_per_year_calculations(
        data:pd.DataFrame
        
):
    first_opening_balance = data.iloc[0,0]
    year = [('20' + data.columns.str.split('-')[i][0]) for i in range(len(data.columns))]
    data = data.T
    data.index = year
    opening_balances = np.array(
        np.zeros(
            len(data.index.unique())
        )
    )
    opening_balances[0] = first_opening_balance
    sum_per_year = data.groupby(data.index)[
    ["New Disbursements", "Repayments", "Interest Income"]
    ].sum()
    sum_per_year["Opening Balance"] = opening_balances
    sum_per_year.reset_index(inplace=True, names="")

    for i in range(len(sum_per_year)):
        sum_per_year["Closing Balance"] = sum_per_year[
            ["Opening Balance", "New Disbursements", "Repayments", "Interest Income"]
        ].sum(axis=1)
        sum_per_year.loc[i + 1, "Opening Balance"] = sum_per_year.loc[i, "Closing Balance"]
    sum_per_year = sum_per_year[
    [   '',
        "Opening Balance",
        "New Disbursements",
        "Repayments",
        "Interest Income",
        "Closing Balance",
    ]
]
    sum_per_year.set_index('',inplace=True)
    

    return sum_per_year.T.iloc[:,:-1]
