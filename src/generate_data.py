from faker import Faker
import pandas as pd
import random

fake = Faker()

# Number of records to generate
NUM_CUSTOMERS = 1000
NUM_PRODUCTS = 200
NUM_ORDERS = 5000

# Make results reproducible
random.seed(42)
Faker.seed(42)


def generate_customers():
    customers = []

    for customer_id in range(1, NUM_CUSTOMERS + 1):
        customers.append({
            "customer_id": customer_id,
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": fake.unique.email(),
            "city": fake.city(),
            "state": fake.state_abbr(),
            "created_at": fake.date_time_between(
                start_date="-2y",
                end_date="now"
            )
        })

    return pd.DataFrame(customers)


def generate_products():
    product_names = [
        "Laptop",
        "Wireless Mouse",
        "Mechanical Keyboard",
        "USB-C Cable",
        "Monitor",
        "Webcam",
        "Headphones",
        "Bluetooth Speaker",
        "External SSD",
        "Phone Charger",
        "Desk Lamp",
        "Office Chair",
        "Laptop Stand",
        "Tablet",
        "Smartphone"
    ]

    categories = {
        "Laptop": "Electronics",
        "Wireless Mouse": "Electronics",
        "Mechanical Keyboard": "Electronics",
        "USB-C Cable": "Accessories",
        "Monitor": "Electronics",
        "Webcam": "Electronics",
        "Headphones": "Audio",
        "Bluetooth Speaker": "Audio",
        "External SSD": "Storage",
        "Phone Charger": "Accessories",
        "Desk Lamp": "Home Office",
        "Office Chair": "Furniture",
        "Laptop Stand": "Accessories",
        "Tablet": "Electronics",
        "Smartphone": "Electronics"
    }

    products = []

    for product_id in range(1, NUM_PRODUCTS + 1):
        name = random.choice(product_names)

        products.append({
            "product_id": product_id,
            "product_name": name,
            "category": categories[name],
            "price": round(random.uniform(10, 2000), 2),
            "created_at": fake.date_time_between(
                start_date="-2y",
                end_date="now"
            )
        })

    return pd.DataFrame(products)


def generate_orders():
    orders = []

    statuses = [
        "completed",
        "completed",
        "completed",
        "shipped",
        "processing",
        "cancelled"
    ]

    for order_id in range(1, NUM_ORDERS + 1):
        orders.append({
            "order_id": order_id,
            "customer_id": random.randint(1, NUM_CUSTOMERS),
            "order_date": fake.date_time_between(
                start_date="-1y",
                end_date="now"
            ),
            "status": random.choice(statuses)
        })

    return pd.DataFrame(orders)


def generate_order_items(orders, products):
    order_items = []

    order_item_id = 1

    for _, order in orders.iterrows():

        # Each order contains between 1 and 5 products
        num_items = random.randint(1, 5)

        selected_products = random.sample(
            list(products["product_id"]),
            num_items
        )

        for product_id in selected_products:

            product = products[
                products["product_id"] == product_id
            ].iloc[0]

            order_items.append({
                "order_item_id": order_item_id,
                "order_id": order["order_id"],
                "product_id": product_id,
                "quantity": random.randint(1, 3),
                "unit_price": product["price"]
            })

            order_item_id += 1

    return pd.DataFrame(order_items)


if __name__ == "__main__":

    print("Generating customers...")
    customers = generate_customers()

    print("Generating products...")
    products = generate_products()

    print("Generating orders...")
    orders = generate_orders()

    print("Generating order items...")
    order_items = generate_order_items(
        orders,
        products
    )

    # Save everything to CSV
    customers.to_csv(
        "data/customers.csv",
        index=False
    )

    products.to_csv(
        "data/products.csv",
        index=False
    )

    orders.to_csv(
        "data/orders.csv",
        index=False
    )

    order_items.to_csv(
        "data/order_items.csv",
        index=False
    )

    print()
    print("Data generation complete!")
    print(f"Customers: {len(customers)}")
    print(f"Products: {len(products)}")
    print(f"Orders: {len(orders)}")
    print(f"Order items: {len(order_items)}")