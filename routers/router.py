from fastapi import APIRouter
from controllers import (
    product_controller,
    category_controller,
    user_controller,
    auth_controller,
    order_controller,
)

routes = APIRouter(
    prefix="/api/v1"
)

routes.include_router(product_controller.router)
routes.include_router(category_controller.router)
routes.include_router(user_controller.router)
routes.include_router(auth_controller.router)
routes.include_router(order_controller.router)
