from modules.auth.views.auth import *

url = [
    ('/auth/login', 'POST', login),
    ('/auth/logout', 'POST', logout),
    ('/auth/register', 'POST', register),
    ('/auth/profile', 'GET', profile),
    ('/auth/check', 'GET', check_auth),
    ('/auth/<id>/users', 'GET', get_user)
]
