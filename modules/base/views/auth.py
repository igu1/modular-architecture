from helper import WSGIHelpers
from modules.base.models import Product


def auth(environ, start_response):
    return WSGIHelpers.response(start_response, "Auth")


def add_product(environ, start_response):
    body = WSGIHelpers.get_body(environ)
    if not body:
        return WSGIHelpers.error_response(start_response, "Invalid JSON body", 400)
    
    # Django-like create method
    product = Product.create(
        name=body.get("name"),
        price=body.get("price")
    )
    
    return WSGIHelpers.json_response(start_response, product.to_dict())