from ninja import NinjaAPI
from .api import router 
from ninja_simple_jwt.auth.views.api import web_auth_router # Import the web_auth_router from ninja_simple_jwt

api = NinjaAPI()

api.add_router('/user', router)
api.add_router("/auth/", web_auth_router)

