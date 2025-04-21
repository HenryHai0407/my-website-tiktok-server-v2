from sqlmodel import Session
from models.order_model import OrderModel, OrderDTO, OrderDTOCreate
from models.order_item_model import OrderItemModel
from models.product_model import ProductModel
from repositories.order_repository import OrderRepository
from exceptions.custom_exception import AppException, ExceptionType
import uuid
from typing import List


class OrderService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = OrderRepository(db)

    def create(self, dto: OrderDTOCreate) -> OrderDTO:
        order = OrderModel(
            order_number=str(uuid.uuid4()),
            status="ORDERED",
            customer_id=dto.customer_id,
            description=dto.description,
        )

        order_items = []
        for item in dto.items:
            product = self.db.get(ProductModel, item.product_id)
            if not product:
                raise AppException(ExceptionType.NOT_FOUND,f"Product {item.product_id} not found.")

            # Check stock availability
            if product.quantity < item.quantity:
                raise AppException(
                    ExceptionType.BAD_REQUEST,
                    f"Not enough stock for {product.name}. Available {product.quantity}, Requested: {item.quantity}"
                )
            
            # Deduct stock
            product.quantity -= item.quantity

            # Create order item
            order_items.append(OrderItemModel(
                product_id=product.id,
                quantity=item.quantity,
                unit_price=product.price,
                description=item.description
            ))
        self.repo.create(order, order_items)

        # Commit the transaction to persist product quantity changes too
        self.db.commit()

        return OrderDTO.model_validate(order)

    def get_list(self) -> List[OrderDTO]:
        models = self.repo.get_list()
        return [OrderDTO.model_validate(model) for model in models]

    def get_by_id(self, id: int) -> OrderDTO:
        model = self.repo.get_by_id(id)
        return OrderDTO.model_validate(model)
