from fastapi import FastAPI, Query
from typing import List
from typing import Optional
from pydantic import BaseModel, Field

app = FastAPI()

products = [
    {"id": 1, "name": "Wireless Mouse", "category": "Electronics", "price": 499, "in_stock": True},
    {"id": 2, "name": "Notebook", "category": "Stationery", "price": 99, "in_stock": True},
    {"id": 3, "name": "USB Hub", "category": "Electronics", "price": 799, "in_stock": False},
]

@app.get("/products/filter")
def filter_products(
    category: str = Query(None, description="Filter by category"),
    max_price: int = Query(None, description="Maximum price"),
    min_price: int = Query(None, description="Minimum price")   # ✅ new parameter
):
    result = products

    if category:
        result = [p for p in result if p["category"] == category]

    if max_price:
        result = [p for p in result if p["price"] <= max_price]

    if min_price:   # ✅ new filter condition
        result = [p for p in result if p["price"] >= min_price]

    return result
#only the name and price for a given product ID
@app.get("/products/{product_id}/price")
def get_product_price(product_id: int):
    for product in products:
        if product["id"] == product_id:
            return {
                "name": product["name"],
                "price": product["price"]
            }

    return {"error": "Product not found"}
#Pydantic Model + POST Endpoint
# Store feedback
feedback = []

# Pydantic Model
class CustomerFeedback(BaseModel):
    customer_name: str = Field(..., min_length=2, max_length=100)
    product_id: int = Field(..., gt=0)
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = Field(None, max_length=300)


# POST endpoint
@app.post("/feedback")
def submit_feedback(data: CustomerFeedback):
    feedback.append(data.dict())

    return {
        "message": "Feedback submitted successfully",
        "feedback": data.dict(),
        "total_feedback": len(feedback)
    }
#GET + Query + Business Logic
@app.get("/products/summary")
def product_summary():

    if not products:
        return {"error": "No products available"}

    in_stock = [p for p in products if p.get("in_stock")]
    out_stock = [p for p in products if not p.get("in_stock")]

    expensive = max(products, key=lambda p: p["price"])
    cheapest = min(products, key=lambda p: p["price"])

    categories = list(set(p["category"] for p in products))

    return {
        "total_products": len(products),
        "in_stock_count": len(in_stock),
        "out_of_stock_count": len(out_stock),
        "most_expensive": {"name": expensive["name"], "price": expensive["price"]},
        "cheapest": {"name": cheapest["name"], "price": cheapest["price"]},
        "categories": categories
    }
#Pydantic Models + Bulk Order Endpoint
class CustomerFeedback(BaseModel):
    customer_name: str = Field(..., min_length=2, max_length=100)
    product_id: int = Field(..., gt=0)
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = Field(None, max_length=300)


class OrderItem(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0, le=50)


class BulkOrder(BaseModel):
    company_name: str = Field(..., min_length=2)
    contact_email: str = Field(..., min_length=5)
    items: List[OrderItem] = Field(..., min_items=1)
@app.post("/orders/bulk")
def place_bulk_order(order: BulkOrder):
    confirmed = []
    failed = []
    grand_total = 0

    for item in order.items:
        product = next((p for p in products if p["id"] == item.product_id), None)

        if not product:
            failed.append({"product_id": item.product_id, "reason": "Product not found"})
        elif not product.get("in_stock", False):
            failed.append({"product_id": item.product_id, "reason": f"{product['name']} is out of stock"})
        else:
            subtotal = product["price"] * item.quantity
            grand_total += subtotal
            confirmed.append({"product": product["name"], "qty": item.quantity, "subtotal": subtotal})

    return {
        "company": order.company_name,
        "confirmed": confirmed,
        "failed": failed,
        "grand_total": grand_total
    }
#POST + GET + Order Tracking
class OrderRequest(BaseModel):
    customer_name: str = Field(..., min_length=2)
    delivery_address: str = Field(..., min_length=5)
    items: List[OrderItem] = Field(..., min_items=1)
orders = []
order_counter = 1

@app.post("/orders")
def place_order(order: OrderRequest):
    global order_counter
    new_order = {
        "order_id": order_counter,
        "customer_name": order.customer_name,
        "items": [item.dict() for item in order.items],
        "status": "pending"  # <-- start as pending
    }
    orders.append(new_order)
    order_counter += 1
    return {"message": "Order placed", "order": new_order}
@app.get("/orders/{order_id}")
def get_order(order_id: int):
    for order in orders:
        if order["order_id"] == order_id:
            return {"order": order}
    return {"error": "Order not found"}
@app.patch("/orders/{order_id}/confirm")
def confirm_order(order_id: int):
    for order in orders:
        if order["order_id"] == order_id:
            if order["status"] == "pending":
                order["status"] = "confirmed"
            return {"message": "Order confirmed", "order": order}
    return {"error": "Order not found"}


