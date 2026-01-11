import os

import duckdb
import polars as pl
from dotenv import load_dotenv

load_dotenv()


class DuckDB:
    def __init__(self):
        self._setup_motherduck_token()
        self.db_name = "budget_vs_actuals"
        self.conn = duckdb.connect("md:")
        self.create_and_link_db()

    def __enter__(self):
        self.conn.begin()
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        if exc_type is not None:
            self.conn.rollback()
        else:
            self.conn.commit()
        self.conn.close()
        return False

    def _setup_motherduck_token(self) -> None:
        """Set up MotherDuck token if available."""
        token = os.getenv("MOTHERDUCK_TOKEN")
        if token:
            os.environ["motherduck_token"] = token

    def create_and_link_db(self) -> None:
        self.conn.execute(f"CREATE DATABASE IF NOT EXISTS {self.db_name}")
        self.conn.execute(f"USE {self.db_name}")
        self.drop_schema()
        self.create_tables()

    def drop_schema(self) -> None:
        print("Dropping existing tables and sequences...")
        self.conn.execute("""
            DROP TABLE IF EXISTS pnl CASCADE;
            DROP TABLE IF EXISTS commercial_mutations CASCADE;
            DROP TABLE IF EXISTS periods CASCADE;
            DROP TABLE IF EXISTS commercial_mutations_types CASCADE;
            DROP TABLE IF EXISTS gl_accounts CASCADE;
            DROP TABLE IF EXISTS value_types CASCADE;
            DROP SEQUENCE IF EXISTS pnl_id_seq CASCADE;
            DROP SEQUENCE IF EXISTS period_id_seq CASCADE;
            DROP SEQUENCE IF EXISTS value_type_id_seq CASCADE;
            DROP SEQUENCE IF EXISTS commercial_mutations_types_id_seq CASCADE;
            DROP SEQUENCE IF EXISTS commercial_mutations_id_seq CASCADE;
        """)

    def create_tables(self) -> None:
        print("Creating tables...")

        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS gl_accounts (
                id INTEGER PRIMARY KEY,
                name VARCHAR NOT NULL,
                parent_gl INTEGER
            );

            CREATE SEQUENCE IF NOT EXISTS value_type_id_seq START 1;
            CREATE TABLE IF NOT EXISTS value_types (
                id INTEGER PRIMARY KEY DEFAULT nextval('value_type_id_seq'),
                name VARCHAR NOT NULL CHECK (name IN ('actuals', 'budget'))
            );

            CREATE SEQUENCE IF NOT EXISTS period_id_seq START 1;
            CREATE TABLE IF NOT EXISTS periods (
                id INTEGER PRIMARY KEY DEFAULT nextval('period_id_seq'),
                period INTEGER NOT NULL
            );

            CREATE SEQUENCE IF NOT EXISTS commercial_mutations_types_id_seq START 1;
            CREATE TABLE IF NOT EXISTS commercial_mutations_types (
                id INTEGER PRIMARY KEY DEFAULT nextval('commercial_mutations_types_id_seq'),
                name VARCHAR NOT NULL CHECK (name IN ('new_booking', 'upsell', 'downsell', 'churn'))
            );

            CREATE SEQUENCE IF NOT EXISTS pnl_id_seq START 1;
            CREATE TABLE IF NOT EXISTS pnl (
                id INTEGER PRIMARY KEY DEFAULT nextval('pnl_id_seq'),
                gl_account_id INTEGER NOT NULL,
                value_type_id INTEGER NOT NULL,
                period_id INTEGER NOT NULL,
                amount DOUBLE NOT NULL,
                FOREIGN KEY (gl_account_id) REFERENCES gl_accounts(id),
                FOREIGN KEY (value_type_id) REFERENCES value_types(id),
                FOREIGN KEY (period_id) REFERENCES periods(id),
                UNIQUE (gl_account_id, period_id, value_type_id)
            );

            CREATE SEQUENCE IF NOT EXISTS commercial_mutations_id_seq START 1;
            CREATE TABLE IF NOT EXISTS commercial_mutations (
                id INTEGER PRIMARY KEY DEFAULT nextval('commercial_mutations_id_seq'),
                period_id INTEGER NOT NULL,
                commercial_mutation_type_id INTEGER NOT NULL,
                nr_of_customers INTEGER NOT NULL,
                mrr_per_customer DOUBLE,
                value_type_id INTEGER NOT NULL,
                FOREIGN KEY (period_id) REFERENCES periods(id),
                FOREIGN KEY (value_type_id) REFERENCES value_types(id),
                FOREIGN KEY (commercial_mutation_type_id) REFERENCES commercial_mutations_types(id)
            );
        """)

    def insert_data(self, df: pl.DataFrame, table: str) -> None:
        cols = ", ".join(df.columns)
        self.conn.execute(
            f"""
            INSERT INTO {table} ({cols}) SELECT * FROM df
            """
        )
