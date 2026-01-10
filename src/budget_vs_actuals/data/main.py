import polars as pl

from budget_vs_actuals.db.db import DuckDB


def get_dict_with_data() -> dict:
    return {
        "types": "src/budget_vs_actuals/data/sample/types.csv",
        "values": "src/budget_vs_actuals/data/sample/values.csv",
        "commercial_mutation_types": "src/budget_vs_actuals/data/sample/commercial_mutation_types.csv",
        "commercial_mutations": "src/budget_vs_actuals/data/sample/commercial_mutations.csv",
        "gl_accounts": "src/budget_vs_actuals/data/sample/gl_accounts.csv",
        "periods": "src/budget_vs_actuals/data/sample/periods.csv",
    }


def create_db_and_insert_sample_data() -> None:
    sample_data = get_dict_with_data()

    commercial_mutation_types_df = pl.read_csv(sample_data["commercial_mutation_types"])
    types_df = pl.read_csv(sample_data["types"])
    periods_df = pl.read_csv(sample_data["periods"])
    commercial_mutations_df = pl.read_csv(sample_data["commercial_mutations"])

    gl_accounts_df = pl.read_csv(sample_data["gl_accounts"])
    gl_parents_df = gl_accounts_df.filter(pl.col("parent_gl").is_null())
    gl_children_df = gl_accounts_df.filter(pl.col("parent_gl").is_not_null())

    values_df = pl.read_csv(sample_data["values"])

    with DuckDB() as db:
        print("Inserting sample data...")
        db.insert_data(commercial_mutation_types_df, "commercial_mutations_types")
        db.insert_data(types_df, "types")
        db.insert_data(periods_df, "periods")
        db.insert_data(commercial_mutations_df, "commercial_mutations")
        db.insert_data(gl_parents_df, "gl_accounts")
        db.insert_data(gl_children_df, "gl_accounts")
        db.insert_data(values_df, "values")
        print("Sample data inserted!")
