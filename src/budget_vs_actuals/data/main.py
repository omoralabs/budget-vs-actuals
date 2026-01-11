from typing import Tuple

from budget_vs_actuals.data.utils import get_dfs, get_gl_split, get_paths
from budget_vs_actuals.db.db import DuckDB


def prep_dfs_to_insert(paths: dict) -> Tuple:
    dfs = get_dfs(paths)
    gl_accounts_dfs = get_gl_split(dfs)
    del dfs["gl_accounts"]

    return gl_accounts_dfs, dfs


def create_db_and_insert_sample_data() -> None:
    sample_data = get_paths()
    gl_accounts_dfs, dfs = prep_dfs_to_insert(sample_data)

    with DuckDB() as db:
        print("Inserting sample data...")
        for key, df in gl_accounts_dfs.items():
            db.insert_data(df, "gl_accounts")
        for key, df in dfs.items():
            db.insert_data(df, f"{key}")
        print("Sample data inserted!")
