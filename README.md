<p align="center">
  <img src="public/omora.svg" height="80" alt="Omora Labs" />
</p>

# Plan vs Actuals Variance Analysis

A production-grade financial variance analysis blueprint built on **Omora Labs** components. This system demonstrates how semantic layers, facts, transformations, and reporting work together to deliver automated budget vs actuals analysis with hierarchical P&L rollup.

## What is Omora Labs?

Omora Labs provides reusable finance data components - semantic dimensions, transformations, and reporting blocks - for building production-grade analytics pipelines. Code-first, version-controlled, no vendor lock-in.

**Core principles:**
- **Open Code**: Fully open source components and blocks
- **Composition**: Small, well-defined components assembled into higher-level blocks
- **Single Source of Truth**: All metrics and dimensions live in one place
- **Data Portability**: Built on open formats; your data stays yours
- **Only Best Stack**: Best-in-class open source tools
- **AI Ready**: Structured, readable code that AI can understand

## Architecture

This blueprint follows the Omora Labs five-layer architecture:

### 1. Semantic Layers
Business meaning defined first as contracts. GL Accounts, Periods, and Value Types encode financial hierarchies and classification rules before any data is loaded.

### 2. Facts
Structured observations that conform to semantic contracts. The P&L fact table stores actuals and budget figures classified by period, account, and value type.

### 3. Workers - Not used in this project
Background processes for data ingestion and enrichment (e.g., fetching FX rates, loading ERP data).

### 4. Transformations
Analytical models built using dbt. All business logic is inherited from semantic layers - transformations focus on derivation, not interpretation.

### 5. Reporting & BI
Consumption layer for dashboards and outputs. All business logic is already applied upstream.

## Tech Stack

- **Semantic Layer & Facts**: DuckDB / MotherDuck
- **Transformations**: dbt-core with dbt-duckdb adapter
- **Data Processing**: Polars with PyArrow backend
- **Package Management**: uv

## Installation

```bash
# Install dependencies
uv sync
```

## Usage

```bash
# To create a local db and loaded it with data
uv run plan-db-local

# To create a remote db and loaded it with data
uv run plan-db-remote

# Run dbt transformations
cd src/plan_vs_actuals/plan_vs_actuals_dbt
uv run dbt run
```

## License

This project is licensed under the MIT License.

---

Built with care by the Omora Labs team.
