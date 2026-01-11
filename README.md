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
dbt run --profiles-dir .
```

## Project Structure

```
src/budget_vs_actuals/
├── db/              # Database connector and schema setup
├── data/            # Sample data and utilities
└── budget_vs_actuals_dbt/
    └── models/      # dbt analytical models
        ├── intermediate/
        │   └── pnl_rollup.sql      # Recursive hierarchy rollup
        ├── pnl_full.sql            # Enriched P&L with names
        ├── pnl_comparison.sql      # Budget vs actuals side-by-side
        └── pnl_variances.sql       # Variance calculations
```

## Key Metrics Calculated

- **Variance (Absolute)**: Actuals - Budget
- **Variance %**: (Actuals - Budget) / Budget
- **Hierarchical Totals**: Automatic parent account aggregation

## Data Model

### Core Tables

- **gl_accounts**: Chart of accounts with parent-child hierarchy
- **periods**: Time periods (YYYYMM format)
- **value_types**: Budget vs Actuals classifier
- **pnl**: Financial transactions (leaf-level data)

### Analytical Views

- **pnl_rollup**: Recursive hierarchy with all account levels
- **pnl_full**: Human-readable P&L with period/account names
- **pnl_comparison**: Budget and actuals in side-by-side columns
- **pnl_variances**: Variance and variance percentage calculations

## Example Hierarchy

```
revenue (1)
├── subscriptions (2)
├── services (3)
└── others (4)

commercial_costs (8)
├── sales (9)
│   ├── sales_staff (10)
│   └── sales_non_staff (11)
└── marketing (12)
    ├── marketing_staff (13)
    └── marketing_non_staff (14)
```

## License

MIT
