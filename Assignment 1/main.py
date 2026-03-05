from fastapi import FastAPI

app = FastAPI()

# Sample product database
products = [
    {"id": 1, "name": "Wireless Mouse", "category": "Electronics", "price": 599, "in_stock": True},
    {"id": 2, "name": "Mechanical Keyboard", "category": "Electronics", "price": 2499, "in_stock": True},
    {"id": 3, "name": "Notebook", "category": "Stationery", "price": 99, "in_stock": True},
    {"id": 4, "name": "Pen Set", "category": "Stationery", "price": 49, "in_stock": True},
    {"id": 5, "name": "Laptop Stand", "category": "Electronics", "price": 899, "in_stock": False},
    {"id": 6, "name": "Water Bottle", "category": "Accessories", "price": 199, "in_stock": True},
    {"id": 7, "name": "Backpack", "category": "Accessories", "price": 1299, "in_stock": True}
]

# Q1 - Get all products
@app.get("/products")
def get_products():
    return {
        "products": products,
        "total": len(products)
    }

# Q2 - Get products by category
@app.get("/products/category/{category}")
def get_by_category(category: str):
    results = [p for p in products if p["category"].lower() == category.lower()]
    return {
        "category": category,
        "products": results,
        "total": len(results)
    }

# Q3 - Get in-stock products
@app.get("/products/instock")
def get_instock_products():
    results = [p for p in products if p["in_stock"]]
    return {
        "products": results,
        "total": len(results)
    }

# Q4 - Store summary
@app.get("/store/summary")
def store_summary():
    total_products = len(products)
    total_instock = len([p for p in products if p["in_stock"]])
    categories = list(set(p["category"] for p in products))

    return {
        "total_products": total_products,
        "products_in_stock": total_instock,
        "categories": categories
    }

# Q5 - Search products by keyword (case insensitive)
@app.get("/products/search/{keyword}")
def search_products(keyword: str):
    results = [
        p for p in products
        if keyword.lower() in p["name"].lower()
    ]

    if not results:
        return {"message": "No products matched your search"}

    return {
        "keyword": keyword,
        "results": results,
        "total_matches": len(results)
    }

# ⭐ Bonus - Cheapest and most expensive products
@app.get("/products/deals")
def get_deals():
    cheapest = min(products, key=lambda p: p["price"])
    expensive = max(products, key=lambda p: p["price"])

    return {
        "best_deal": cheapest,
        "premium_pick": expensive
    }