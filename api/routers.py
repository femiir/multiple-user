from ninja import NinjaAPI
from .api import router as user_router

api = NinjaAPI()

api.add_router('/user', user_router)

