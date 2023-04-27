import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Links(SqlAlchemyBase):
    __tablename__ = 'videos'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    link = sqlalchemy.Column(sqlalchemy.String)
    key = sqlalchemy.Column(sqlalchemy.String, index=True)
    asks = sqlalchemy.Column(sqlalchemy.Integer)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    user_uid = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.uid"))
    user = orm.relationship('User')
