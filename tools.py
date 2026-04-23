from data_loader import products_df, orders_df
from datetime import datetime
import pandas as pd
import ast
from datetime import datetime

def search_products(max_price=None, size=None, tags=None, is_sale=None):
    df = products_df.copy()
    df.columns = df.columns.str.strip() 

    # Safety: Ensure columns exist before logic starts
    if "is_sale" not in df.columns:
        df["is_sale"] = False
    if "bestseller_score" not in df.columns:
        df["bestseller_score"] = 0

    # ... [Keep your existing filtering logic here] ...

    # NEW SAFE SORTING LOGIC
    if not df.empty:
        # Create a list of keys that are actually present in the dataframe
        available_cols = [col for col in ["is_sale", "bestseller_score"] if col in df.columns]
        
        if available_cols:
            df = df.sort_values(
                by=available_cols,
                ascending=[False] * len(available_cols)
            )
    else:
        # Return empty list immediately if no products match
        return []

    return df.head(5).to_dict(orient="records")

def get_product(product_id: int):
    row = products_df[products_df["product_id"] == product_id]
    if row.empty:
        return {"error": "Product not found"}
    return row.iloc[0].to_dict()


def get_order(order_id):
    order = orders_df[orders_df["order_id"] == order_id]

    if order.empty:
        return {"error": "Order not found"}

    return order.iloc[0].to_dict()


def evaluate_return(order_id):
    order = get_order(order_id)

    if "error" in order:
        return {"decision": "رفض", "reason": "Order not found"}

    # Get product info
    product = get_product(order["product_id"])

    if "error" in product:
        return {"decision": "رفض", "reason": "Product not found"}

    # Parse dates
    # order_date = datetime.strptime(order["order_date"], "%d-%m-%Y")
    order_date = datetime.strptime(order["order_date"], "%Y-%m-%d")
    today = datetime.now()

    days_passed = (today - order_date).days

    # Rules

    #  Clearance → no return
    if str(product["is_clearance"]).upper() == "TRUE":
        return {
            "decision": "NO",
            "reason": "Clearance items are not returnable"
        }

    #  Return window check
    if days_passed > 7:
        return {
            "decision": "NO",
            "reason": f"Return window expired ({days_passed} days)"
        }

    #  Sale item
    if str(product["is_sale"]).upper() == "TRUE":
        return {
            "decision": "PARTIAL",
            "reason": "Sale item – only exchange allowed"
        }

    #  Normal return
    return {
        "decision": "YES",
        "reason": "Eligible for return within 7 days"
    }