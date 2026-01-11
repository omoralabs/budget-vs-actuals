import polars as pl


def get_paths() -> dict:
    return {
        "value_types": "src/budget_vs_actuals/data/sample/value_types.csv",
        "periods": "src/budget_vs_actuals/data/sample/periods.csv",
        "commercial_mutations_types": "src/budget_vs_actuals/data/sample/commercial_mutation_types.csv",
        "gl_accounts": "src/budget_vs_actuals/data/sample/gl_accounts.csv",
        "pnl": "src/budget_vs_actuals/data/sample/pnl.csv",
        "commercial_mutations": "src/budget_vs_actuals/data/sample/commercial_mutations.csv",
    }


def get_dfs(paths: dict) -> dict:
    dfs = {}
    for key, path in paths.items():
        dfs[key] = pl.read_csv(path)
    return dfs


def get_gl_split(dfs: dict) -> dict:
    gl_accounts_df = dfs["gl_accounts"]
    gl_accounts_dfs = {}
    gl_accounts_dfs["gl_parents"] = gl_accounts_df.filter(pl.col("parent_gl").is_null())
    gl_accounts_dfs["gl_children"] = gl_accounts_df.filter(
        pl.col("parent_gl").is_not_null()
    )

    return gl_accounts_dfs
