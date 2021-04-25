import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Blank(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'posts'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    structure = sqlalchemy.Column(sqlalchemy.String)
    street = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    house = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    flat = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    phone = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
