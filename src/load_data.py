import os
import pandas as pd
import psycopg2
from dotenv import load_dotenv


load_dotenv()


DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD")
}


def get_connection():
    """Create and return a connection to PostgreSQL."""
    return psycopg2.connect(**DB_CONFIG)


def load_table(connection, csv_file, table_name):
    """Load a CSV file into a PostgreSQL table."""

    df = pd.read_csv(csv_file)

    print(f"Loading {len(df)} rows into {table_name}...")

    cursor = connection.cursor()

    # Insert each row into PostgreSQL
    columns = list(df.columns)

    column_names = ", ".join(columns)
    placeholders = ", ".join(["%s"] * len(columns))

    query = f"""
        INSERT INTO {table_name} ({column_names})
        VALUES ({placeholders})
    """

    for row in df.itertuples(index=False, name=None):
        cursor.execute(query, row)

    connection.commit()
    cursor.close()

    print(f"Loaded {len(df)} rows into {table_name}.")

def clear_tables(connection):
    cursor = connection.cursor()

    print("Clearing existing tables...")

    cursor.execute("""
        TRUNCATE TABLE
            order_items,
            orders,
            products,
            customers
        RESTART IDENTITY CASCADE;
    """)

    connection.commit()
    cursor.close()

    print("Existing data cleared.")


def main():
    connection = get_connection()

    try:
        clear_tables(connection)

        load_table(connection, "data/customers.csv", "customers")
        load_table(connection, "data/products.csv", "products")
        load_table(connection, "data/orders.csv", "orders")
        load_table(connection, "data/order_items.csv", "order_items")

        print("\nAll data loaded successfully!")

    except Exception as e:
        connection.rollback()
        print(f"\nError loading data: {e}")
        raise

    finally:
        connection.close()

if __name__ == "__main__":
    main()
