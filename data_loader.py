import pandas as pd

products_df = pd.read_csv("product_inventory.csv")
orders_df = pd.read_csv("orders.csv")

with open("policy.txt", "r") as f:
    policy_text = f.read()