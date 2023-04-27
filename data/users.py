import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase

class User(SqlAlchemyBase):
    __tablename__ = 'users'
    uid = sqlalchemy.Column(sqlalchemy.String, primary_key=True, index=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    links = orm.relationship("Links", back_populates='user')

    def __repr__(self):
        st = f"banned for: {self.banned_for}" if self.is_banned else "status: not banned"
        return f"uid: {self.uid} | name: {self.name} | notify: {self.notify} | {st} | date: {self.created_date} | last active: {self.last_active}"
