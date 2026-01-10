from budget_vs_actuals.data.main import create_db_and_insert_sample_data


def main() -> None:
    """
    Set up the database schema for assets and its data.
    """
    try:
        print("Starting process...")
        create_db_and_insert_sample_data()
        print("Process finished successfully")
    except Exception as e:
        print(f"Failure setting up db schema and filling it in with sample data: {e}")
        raise


if __name__ == "__main__":
    main()
