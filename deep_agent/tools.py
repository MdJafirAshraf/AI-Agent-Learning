import json
from langchain_core.tools import tool


@tool
def get_customer(customer_id: int) -> dict:
    """Get customer information using the customer ID."""

    with open("customers.json", "r", encoding="utf-8") as file:
        customers = json.load(file)

    for customer in customers:
        if customer["id"] == customer_id:
            return {
                "id": customer["id"],
                "name": customer["name"],
                "email": customer["email"],
                "status": customer["status"],
                "city": customer["city"],
            }

    return {
        "error": f"Customer {customer_id} not found"
    }


@tool
def get_customer_orders(customer_id: int) -> list:
    """Get all orders belonging to a customer."""

    with open("customers.json", "r", encoding="utf-8") as file:
        customers = json.load(file)

    for customer in customers:
        if customer["id"] == customer_id:
            return customer["orders"]

    return [
        {
            "error": f"Customer {customer_id} not found"
        }
    ]


@tool
def get_order(customer_id: int, order_id: int) -> dict:
    """Get a specific order belonging to a customer."""

    with open("customers.json", "r", encoding="utf-8") as file:
        customers = json.load(file)

    for customer in customers:
        if customer["id"] == customer_id:

            for order in customer["orders"]:
                if order["order_id"] == order_id:
                    return order

            return {
                "error": f"Order {order_id} not found"
            }

    return {
        "error": f"Customer {customer_id} not found"
    }


@tool
def get_customers_by_city(city: str) -> list:
    """Find all customers who live in a specific city."""

    with open("customers.json", "r", encoding="utf-8") as file:
        customers = json.load(file)

    results = []
    for customer in customers:
        if customer["city"].lower() == city.lower():
            results.append({
                "id": customer["id"],
                "name": customer["name"],
                "email": customer["email"],
                "status": customer["status"],
                "city": customer["city"],
            })

    return results