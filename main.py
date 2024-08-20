import pandas as pd
import json
import requests

url = "https://rest.iad-05.braze.com/users/track"
API_KEY = "Bearer api_key"

headers = {
    "Content-Type": "application/json",
    "Authorization": API_KEY
}

df = pd.read_csv("test purchase file.csv")
# print(df)

df.fillna("", inplace=True)
isna_rows = df[df.isna().values.any(axis=1)]
# print(isna_rows)

data = df.to_numpy()
# print(data)

columns = df.columns
# print(columns)

all_data = []
for x in data:
    dic = {}
    x[8] = x[8].replace(" ", "T") + ":00-04:00"
    for y in range(len(x)):
        dic[columns[y]] = x[y]

    all_data.append(dic)

# print(all_data)


def get_value(dic, key):
    return dic[key] if key in dic.keys() else ""


n = 0
for x in all_data[::]:
    n += 1
    purchase = {
        "purchases":
            [{
                "external_id": (get_value(x, "Email")).lower(),
                "product_id": get_value(x, "Product title"),
                "time": get_value(x, "Created at"),
                "quantity": get_value(x, "Quantity"),
                "currency": "USD",
                "price": get_value(x, "Price"),
                "properties": {
                    "sku": get_value(x, "SKU"),
                    "title": get_value(x, "Product title"),
                    "variant_id": get_value(x, "Variant id"),
                    "variant_title": get_value(x, "Variant title")
                }
            }]
    }

    track_purchase = json.dumps(purchase)
    # print(f"Row {n} - Purchase:", track_purchase)

    response = requests.post(url=url, data=track_purchase, headers=headers)
    print(f"Row {n}: {x['Email']} Purchase Response: ", response.json())

    order_created = {
        "events": [{
            "external_id": (get_value(x, "Email")).lower(),
            "name": "shopify_created_order",
            "time": get_value(x, "Created at"),
            "properties": {
                "line_items": [{
                    "price": get_value(x, "Price"),
                    "product_id": get_value(x, "Product id"),
                    "quantity": get_value(x, "Quantity"),
                    "sku": get_value(x, "SKU"),
                    "title": get_value(x, "Product title"),
                    "variant_id": get_value(x, "Variant id"),
                    "variant_title": get_value(x, "Variant title")
                }]
            }
        }]
    }

    track_order_created = json.dumps(order_created)
    # print(f"Row {n} - Order Created:", track_order_created)

    response = requests.post(url=url, data=track_order_created, headers=headers)
    print(f"Row {n}: {x['Email']} Order Created Response: ", response.json())





