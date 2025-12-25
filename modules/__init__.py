from .product import Product
from .cart import Cart
from .checkout import Checkout

modules = {
    "product": Product,
    "cart": Cart,
    "checkout": Checkout
}

__all__ = ["modules"]