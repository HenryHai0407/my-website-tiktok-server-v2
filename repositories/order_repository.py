from sqlmodel import Session, select
from models.order_model import OrderModel
from models.order_item_model import OrderItemModel
from typing import List


class OrderRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, order: OrderModel, order_items: OrderItemModel) -> OrderModel:
        self.db.add(order)
        self.db.flush()

        for item in order_items:
            item.order_id = order.id
            self.db.add(item)

        self.db.commit()
        self.db.refresh(order)
        return order

    def get_list(self) -> List[OrderModel]:
        statement = select(OrderModel)
        result = self.db.exec(statement)
        return result.all()

    def get_by_id(self, id: int) -> OrderModel:
        model = self.db.get(OrderModel, id)
        self.db.refresh(model)
        return model
