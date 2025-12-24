import random

import numpy as np
import pandas as pd
import json

class GenerateDataStructure():
    
    def __init__(self):
        
        self.load_json()
        
    def load_json(self):
        with open("config.json", "r") as f:
            self.config = json.load(f)

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)

# Generate months for years in config

def generate_months()
months = pd.date_range("2026-01-01", "2026-12-01", freq="MS")



record_id = 1

for dept in departments:
    # Annual budget for department
    annual_budget = random.randint(*dept_budget_ranges[dept])

    for account in gl_accounts:
        # Not all accounts apply to all departments
        if account == "Marketing Campaigns" and dept != "Marketing":
            continue
        if account == "Cloud Infrastructure" and dept not in ["Engineering", "Product"]:
            continue
        if account == "Recruiting Fees" and dept != "HR":
            continue

        # Account budget is portion of department budget
        account_annual_budget = annual_budget * gl_account_weights.get(account, 0.02)

        # Distribute across months with some seasonality
        for month in months:
            month_idx = month.month

            # Add seasonality (Q4 spending typically higher, Q1 lower)
            seasonality_factor = 1.0
            if month_idx in [1, 2]:
                seasonality_factor = 0.85
            elif month_idx in [11, 12]:
                seasonality_factor = 1.25
            elif month_idx in [6, 7]:  # Mid-year push
                seasonality_factor = 1.10

            monthly_budget = (account_annual_budget / 12) * seasonality_factor

            # Generate actuals with realistic variance
            # Most items within ±15%, some outliers
            variance_pct = np.random.normal(0, 8)  # Mean 0, std dev 8%

            # Occasionally bigger variances
            if random.random() < 0.10:  # 10% chance of bigger variance
                variance_pct = np.random.normal(0, 20)

            monthly_actual = monthly_budget * (1 + variance_pct / 100)

            # Ensure no negative values
            monthly_actual = max(0, monthly_actual)

            # Round to nearest dollar
            monthly_budget = round(monthly_budget, 2)
            monthly_actual = round(monthly_actual, 2)

            # Add to budget data
            budget_data.append(
                {
                    "record_id": record_id,
                    "department": dept,
                    "gl_account": account,
                    "month": month.strftime("%Y-%m-%d"),
                    "budget_amount": monthly_budget,
                }
            )

            # Add to actuals data
            actuals_data.append(
                {
                    "record_id": record_id,
                    "department": dept,
                    "gl_account": account,
                    "month": month.strftime("%Y-%m-%d"),
                    "actual_amount": monthly_actual,
                }
            )

            record_id += 1

# Create DataFrames
budget_df = pd.DataFrame(budget_data)
actuals_df = pd.DataFrame(actuals_data)


def save_to_csv(budget_df: pd.DataFrame, actuals_df: pd.DataFrame) -> None:
    """
    Writes dataframes to csv.
    """

    budget_df.to_csv("budget_plan.csv", index=False)
    actuals_df.to_csv("actuals.csv", index=False)
