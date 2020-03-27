import sqlite3
from db import db


class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel')

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {'name': self.name, 'price': self.price}

    @classmethod
    def find_by_name(cls, name):
        return ItemModel.query.filter_by(name = name).first() #SELECT * FROM __tablename__ WHERE name=name we can add couple of .filter_by().filter_by etc..
                                                                # also we can do filter_by(name = name, id = 1)
    def save_to_db(self):# this method is usefull for both update and insert
        db.session.add(self) # session is collection of objects that we're going to write into the database
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
