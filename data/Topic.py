import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


association_table = sqlalchemy.Table(
    'association',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('codes', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('codes.id')),
    sqlalchemy.Column('topics', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('topics.id'))
)


class Topic(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'topics'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True,
                           autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)