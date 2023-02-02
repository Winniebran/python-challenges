from menu import products
import math
import statistics


def get_product_by_id(id):
    if type(id) != int:
        raise TypeError('product id must be an int')

    for element in products:
        if element["_id"] == id:
            return element
    return {}


def get_products_by_type(type_product):
    if type(type_product) != str:
        raise TypeError('product type must be a str')

    return [product for product in products if product["type"] == type_product]


def add_product(menu: list, **kwargs):
    if menu == []:
        kwargs["_id"] = 1
    else:
        kwargs["_id"] = max(elem["_id"] for elem in menu) + 1

    menu.append(kwargs)
    return kwargs


def menu_report():
    product_count = len(products)

    media_price = math.fsum([product["price"] for product in products]) / product_count

    most_common_type = statistics.mode([product["type"] for product in products])

    return f'Products Count: {product_count} - Average Price: ${round(media_price, 2)} - Most Common Type: {most_common_type}'


def add_product_extra(menu: list, *args, **kwargs):
    for key in args:
        if not kwargs.get(key):
            raise KeyError(f'field {key} is required')

    diferents_keys = [key for key in kwargs.keys() if key not in list(args)]
    for key in diferents_keys:
        del kwargs[key]

    if menu == []:
        kwargs["_id"] = 1
    else:
        kwargs["_id"] = max(elem["_id"] for elem in menu) + 1

    menu.append(kwargs)
    return kwargs
