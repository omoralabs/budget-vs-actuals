# Budget vs Actuals Variance Analysis

A financial variance analysis system built with DuckDB/MotherDuck and dbt for comparing budgeted vs actual P&L performance with hierarchical account rollup.

## Features

- **Hierarchical P&L Rollup**: Recursive CTEs automatically aggregate child accounts to parent levels
- **Variance Analysis**: Side-by-side budget vs actuals comparison with variance calculations
- **Automatic Calculations**: Variance percentages with zero-division protection
- **Multi-Level Hierarchy**: Support for unlimited account hierarchy depth
- **Cloud-Native**: Built on MotherDuck (cloud DuckDB) for scalable analytics

## Tech Stack

- **Database**: DuckDB / MotherDuck
- **Data Transformation**: dbt-core with dbt-duckdb adapter
- **Data Processing**: Polars with PyArrow backend
- **Package Management**: uv

## Installation

```bash
# Install dependencies
uv sync

# Set up environment variables
cp .env.example .env
# Add your MOTHERDUCK_TOKEN to .env
```

## Usage

```bash
# Load sample data and create database schema
uv run python -m budget_vs_actuals.main

# Run dbt transformations
cd src/budget_vs_actuals/budget_vs_actuals_dbt
uv run dbt run
```

## Project Structure

```
src/budget_vs_actuals/
├── db/              # Database connector and schema setup
├── data/            # Sample data and utilities
└── budget_vs_actuals_dbt/
    └── models/      # dbt analytical models
        ├── intermediate/
        │   ├── pnl_rollup.sql      # Recursive hierarchy rollup
        │   └── pnl_base_data.sql   # Enriched P&L with names
        ├── pnl_full.sql            # Base data + derived metrics
        └── pnl_pivot.sql           # Budget vs actuals + variances
```

## Key Metrics Calculated

### Derived Metrics
- **Gross Margin**: Revenue - COGS
- **Gross Margin %**: Gross Margin / Revenue
- **COGS %**: COGS / Revenue
- **Total Cost**: COGS + Commercial Costs + Fixed Costs
- **Total Cost %**: Total Cost / Revenue
- **Commercial Costs %**: Commercial Costs / Revenue
- **Contribution Margin**: Gross Margin - Commercial Costs
- **Contribution Margin %**: Contribution Margin / Revenue
- **Fixed Costs %**: Fixed Costs / Revenue
- **EBITDA**: Contribution Margin - Fixed Costs
- **EBITDA %**: EBITDA / Revenue

### Variance Analysis
- **Variance (Absolute)**: Actuals - Budget
- **Variance %**: (Actuals - Budget) / Budget
- **Hierarchical Totals**: Automatic parent account aggregation

## Data Model

### Core Tables

- **gl_accounts**: Chart of accounts with parent-child hierarchy
- **periods**: Time periods (YYMM format with YYYY-MM-DD date column)
- **value_types**: Budget vs Actuals classifier
- **pnl**: Financial transactions (leaf-level data)

### Analytical Views

- **pnl_rollup**: Recursive CTE that aggregates child accounts to parents
- **pnl_base_data**: Joins rollup with periods, accounts, and value types for human-readable output
- **pnl_full**: Base data + derived metrics (gross margin, contribution margin, EBITDA) using incremental CTEs
- **pnl_pivot**: Pivots budget/actuals side-by-side and calculates variance metrics

## Example Hierarchy

GL accounts use spaced IDs (1000, 2000, 4000, 6000) with gaps for calculated metrics:

```
revenue (1000)
├── subscriptions (1010)
├── services (1020)
└── others (1030)

cogs (2000)
├── payment_fees (2010)
└── other_costs (2020)
[cogs_pct (2001) - calculated]

[gross_margin (3000) - calculated]
[gross_margin_pct (3001) - calculated]

commercial_costs (4000)
├── sales (4010)
│   ├── sales_staff (4011)
│   └── sales_non_staff (4012)
├── marketing (4020)
│   ├── marketing_staff (4021)
│   └── marketing_non_staff (4022)
└── csm (4030)
    ├── csm_staff (4031)
    └── csm_non_staff (4032)
[commercial_costs_pct (4001) - calculated]

[contribution_margin (5000) - calculated]
[contribution_margin_pct (5001) - calculated]

fixed_costs (6000)
├── development (6010)
├── product (6020)
├── talent (6030)
├── general_and_admin (6040)
└── data (6050)
[fixed_costs_pct (6001) - calculated]

[total_cost (7000) - calculated]
[total_cost_pct (7001) - calculated]

[ebitda (8000) - calculated]
[ebitda_pct (8001) - calculated]
```

## License

This project is licensed under the [MIT License](https://opensource.org/license/MIT)

---

Built with care by the Omora Labs team.
