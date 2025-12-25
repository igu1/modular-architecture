from modules.base.views.auth import auth, add_product

url = [
    ('/', 'GET', auth),
    ('/add_product', 'POST', add_product)
]