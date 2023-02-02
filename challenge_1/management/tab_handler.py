from menu import products


def calculate_tab(bills: list):
    total = sum(
        product["price"] * table["amount"]
        for product in products
        for table in bills
        if product["_id"] == table["_id"]
    )

    bills.append({"subtotal": f'${round(total, 2)}'})

    return bills[-1]
