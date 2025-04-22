from sqlmodel import Session, text
from models.product_model import ProductModel
from typing import List, Optional


class ProductRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_list(self, hot_flg: Optional[int] = None, recommend_flg: Optional[int] = None) -> List[ProductModel]:
        # query = text("SELECT * FROM products")
        # condition = ""
        # if hot_flg and recommend_flg:
        #     condition = "hot_flg = 1 and recommend_flg = 1"
        # elif hot_flg:
        #     condition = "hot_flg = 1"
        # elif recommend_flg:
        #     condition = "recommend_flg = 1"
        
        # if condition:
        #     query = text(f"SELECT * FROM products WHERE {condition}")
        # result = self.db.execute(query)
        # return [ProductModel(**dict(row._mapping)) for row in result]

        # Second solution:
        query = "SELECT * FROM products WHERE 1=1"
        params = {}

        if hot_flg:
            query += " AND hot_flg = :hot_flg"
            params["hot_flg"] = hot_flg

        if recommend_flg:
            query += " AND recommend_flg = :recommend_flg"
            params["recommend_flg"] = recommend_flg

        result = self.db.execute(text(query), params)
        return [ProductModel(**dict(row._mapping)) for row in result]

    def get_by_id(self, id: int) -> ProductModel:
        query = text("SELECT * FROM products WHERE id = :id")
        result = self.db.execute(query, {"id": id}).first()
        return ProductModel(**dict(result._mapping)) if result else None

    def create(self, model: ProductModel):
        query = text("""
            INSERT INTO products (
                name, summary, price, quantity, description, category_id
            ) VALUES (
                :name, :summary, :price, :quantity, :description, :category_id
            )
        """)
        self.db.execute(query, model.model_dump())
        self.db.commit()

        result = self.db.execute(text("SELECT LAST_INSERT_ID()")).scalar()
        return result

    def update(self, model: ProductModel):
        query = text("""
            UPDATE products
            SET name = :name,
                summary = :summary,
                price = :price,
                quantity = :quantity,
                description = :description,
                category_id = :category_id  
            WHERE id = :id
        """)
        values = model.model_dump(exclude_unset=True)

        self.db.execute(query, values)
        self.db.commit()

    def delete(self, model: ProductModel) -> None:
        query = text("DELETE FROM products WHERE id = :id")
        self.db.execute(query, {"id": model.id})
        self.db.commit()

    def search_by_name_or_summary(self, query: str) -> List[ProductModel]:
        # return self.db.query(ProductModel).filter(
        #     (ProductModel.name.ilike(f"%{query}%")) |
        # (ProductModel.summary.ilike(f"%{query}%"))
        # ).all()
    
        # Second solution:
        query = text("SELECT * FROM products WHERE name LIKE :query OR summary LIKE :query")
        result = self.db.execute(query, {"query":f"%{query}%"})
        return [ProductModel(**dict(row.__mapping)) for row in result]

    def get_by_hot_product(self) -> List[ProductModel]:
        query = text("SELECT * FROM products WHERE hot_flg IS NULL")
        result = self.db.execute(query)
        return [ProductModel(**dict(row._mapping)) for row in result]