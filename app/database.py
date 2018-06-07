# coding=utf-8

from .compat import string_types

from sqlalchemy.orm import backref, aliased
from sqlalchemy.ext.declarative import as_declarative, declared_attr

# Alias common SQLAlchemy names
# from . import db
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

Column = db.Column
relationship = db.relationship


class CRUDMixin(object):
    """Mixin that adds convenience methods for CRUD (create, read, update, delete) operations."""

    @classmethod
    def create(cls, **kwargs):
        """Create a new record and save it the database."""
        instance = cls(**kwargs)
        return instance.save()

    def update(self, commit=True, **kwargs):
        """Update specific fields of a record."""
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        """Save the record."""
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit=True):
        """Remove the record from the database."""
        db.session.delete(self)
        return commit and db.session.commit()

    @classmethod
    def get_or_create(cls, q=None, **kwargs):
        """
        以指定参数进行查询，如果查询到则返回该对象
        如果没有查询到，则创建一个对象并返回

        example:
        ```
        cls.get_or_create(q={"username":"admin"}, password="admin")
        cls.get_or_create(username="admin")
        ```

        """

        instance = None

        # 以指定参数进行查询
        if q:
            instance = cls.query.filter_by(**q).first()
        else:
            attr_list = [{attr: val} for attr, val in kwargs.items()]
            # 以 kwargs 排第一的参数进行查询
            # 因为Python3.5以前字典是无序，所以可能拿到的不是传参的第一个参数
            if len(attr_list) > 0:
                # print("attr_list", attr_list)
                q = attr_list[0]
                instance = cls.query.filter_by(**q).first()

        if not instance:
            if not q:
                q = {}
            q.update(kwargs)
            # print("q", q)
            instance = cls.create(**q)
            # print("create a " + str(instance))

        return instance


class Model(CRUDMixin, db.Model):
    """Base model class that includes CRUD convenience methods."""
    __abstract__ = True

    # def __init__(*args, **kwargs):
    #     pass


# From Mike Bayer's "Building the app" talk
# https://speakerdeck.com/zzzeek/building-the-app
class SurrogatePK(object):
    """A mixin that adds a surrogate integer 'primary key' column named ``id`` to any declarative-mapped class."""
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)

    @classmethod
    def get_by_id(cls, record_id):
        """Get record by ID."""
        if any((isinstance(record_id, string_types) and record_id.isdigit(),
                isinstance(record_id, (int, float))), ):
            return cls.query.get(int(record_id))
        return None


def reference_col(tablename, nullable=False, pk_name='id', **kwargs):
    """Column that adds primary key foreign key reference.
    Usage: ::
        category_id = reference_col('category')
        category = relationship('Category', backref='categories')
    """
    return db.Column(
        db.ForeignKey('{0}.{1}'.format(tablename, pk_name)),
        nullable=nullable,
        **kwargs)
