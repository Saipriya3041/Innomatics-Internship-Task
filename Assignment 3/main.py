from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from typing import Optional
from fastapi import Query

app = FastAPI()

# Pydantic model for new product request
class NewProduct(BaseModel):
    name: str
    price: int
    category: str
    in_stock: bool = True


# Initial product list (already exists in the file)
products = [
    {"id": 1, "name": "Wireless Mouse", "price": 499, "category": "Electronics", "in_stock": True},
    {"id": 2, "name": "Keyboard", "price": 99, "category": "Electronics", "in_stock": True},
    {"id": 3, "name": "USB Hub", "price": 699, "category": "Electronics", "in_stock": False},
    {'id': 4, 'name': 'Pen Set',        'price':  49, 'category': 'Stationery',  'in_stock': True},
    {"id":5,"name":"Notebook","price":120,"category":"Stationery","in_stock":False},
    
]
#GET/Products/audit
@app.get("/products/audit")
def product_audit():
    # Products currently in stock
    in_stock_list = [p for p in products if p['in_stock']]
    
    # Products currently out of stock
    out_stock_list = [p for p in products if not p['in_stock']]
    
    # Total stock value (price × 10 units each for in-stock products)
    total_stock_value = sum(p['price'] * 10 for p in in_stock_list)
    
    # Most expensive product
    priciest = max(products, key=lambda p: p['price'])
    
    return {
        "total_products": len(products),
        "in_stock_count": len(in_stock_list),
        "out_of_stock_names": [p['name'] for p in out_stock_list],
        "total_stock_value": total_stock_value,
        "most_expensive": {
            "name": priciest['name'],
            "price": priciest['price']
        }
    }
#PUT/products/discounts-bulk discount
@app.put("/products/discount")
def bulk_discount(
    category: str = Query(..., description="Category to discount"),
    discount_percent: int = Query(..., ge=1, le=99, description="% off")
):
    updated = []

    for p in products:
        if p['category'].lower() == category.lower():  # case-insensitive match
            p['price'] = int(p['price'] * (1 - discount_percent / 100))
            updated.append({"id": p["id"], "name": p["name"], "new_price": p["price"]})

    if not updated:
        return {"message": f"No products found in category: {category}"}

    return {
        "message": f"{discount_percent}% discount applied to {category}",
        "updated_count": len(updated),
        "updated_products": updated
    }


# GET all products
@app.get("/products")
def get_products():
    return products
# GET single product
@app.get("/products/{product_id}")
def get_product(product_id: int):

    for product in products:
        if product["id"] == product_id:
            return product

    raise HTTPException(status_code=404, detail="Product not found")



# POST add new product
@app.post("/products", status_code=201)
def add_product(product: NewProduct):

    # Check duplicate name
    for p in products:
        if p["name"].lower() == product.name.lower():
            raise HTTPException(
                status_code=400,
                detail="Product with this name already exists"
            )

    # Auto-generate ID
    new_id = len(products) + 1

    new_product = {
        "id": new_id,
        "name": product.name,
        "price": product.price,
        "category": product.category,
        "in_stock": product.in_stock
    }

    products.append(new_product)

    return {
        "message": "Product added",
        "product": new_product
    }

# PUT update product
@app.put("/products/{product_id}")
def update_product(
    product_id: int,
    price: Optional[int] = None,
    in_stock: Optional[bool] = None
):

    for product in products:

        if product["id"] == product_id:

            if price is not None:
                product["price"] = price

            if in_stock is not None:
                product["in_stock"] = in_stock

            return {
                "message": "Product updated",
                "product": product
            }
        

    raise HTTPException(status_code=404, detail="Product not found")
#delete product
@app.delete('/products/{product_id}')
def delete_product(product_id: int):
    # Step 1: find the product
    product = next((p for p in products if p["id"] == product_id), None)

    # Step 2: if not found, return 404
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Step 3: remove from list
    products.remove(product)

    return {"message": f"Product '{product['name']}' deleted"}
