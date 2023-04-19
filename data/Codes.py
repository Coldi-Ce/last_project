import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Codes(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'codes'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    information = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    script = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.Date,
                                     default=datetime.date.today())
    is_private = sqlalchemy.Column(sqlalchemy.Boolean, default=True)

    mark = sqlalchemy.Column(sqlalchemy.Integer, default=5)

    count = sqlalchemy.Column(sqlalchemy.Integer, default=1)

    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    user = orm.relationship('User')
    topic = orm.relationship("Topic",
                                  secondary="association",
                                  backref="codes")