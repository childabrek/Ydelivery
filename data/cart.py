import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Cart(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'cart'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    price = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    count = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)
    sum = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)


