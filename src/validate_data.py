import os

import psycopg2

from dotenv import load_dotenv

load_dotenv()


def main():
    connection = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )

    try:
        cursor = connection.cursor()

        cursor.execute("SELECT COUNT(*) FROM customers")
        customers = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM products")
        products = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM orders")
        orders = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM order_items")
        order_items = cursor.fetchone()[0]

        print(f"Customers: {customers}")
        print(f"Products: {products}")
        print(f"Orders: {orders}")
        print(f"Order items: {order_items}")

        assert customers == 1000, "Unexpected customer count"
        assert products == 200, "Unexpected product count"
        assert orders == 5000, "Unexpected order count"
        assert order_items > 0, "No order items found"

        print("Data validation passed")

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    main()