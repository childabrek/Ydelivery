import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Pizza(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'pizza'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    photo = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    price = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    in_stock = sqlalchemy.Column(sqlalchemy.Boolean, default=False)

    def __repr__(self):
        return f'{self.id} {self.title} {self.photo} {self.content} {self.price} {self.in_stock}'
