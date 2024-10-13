from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin


metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

#customer model
class Customer(db.Model, SerializerMixin):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    # Establishes a relationship with the Review model
    reviews = db.relationship('Review', back_populates='customer')

    # Association proxy to get items for this customer through reviews
    items = association_proxy('reviews', 'item')

    # Serialization rule to avoid recursion with reviews -> customer
    serialize_rules = ('-reviews.customer',)


    def __repr__(self):
        return f'<Customer {self.id}, {self.name}>'

#item model
class Item(db.Model, SerializerMixin):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)

    #establishes a relationship with the review model
    reviews = db.relationship('Review', back_populates='item')

    # Serialization rule to avoid recursion with reviews -> item
    serialize_rules = ('-reviews.item',)

    def __repr__(self):
        return f'<Item {self.id}, {self.name}, {self.price}>'

# Review model
class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String)

    # Foreign key to the 'customers' table
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))

    # Foreign key to the 'items' table
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))

   # Establishes a relationship with the Customer model
    customer = db.relationship('Customer', back_populates='reviews')

    # Establishes a relationship with the Item model
    item = db.relationship('Item', back_populates='reviews')

    # Serialization rule to avoid recursion with customer -> reviews and item -> reviews
    serialize_rules = ('-customer.reviews', '-item.reviews')

    def __repr__(self):
        return f'<Review {self.id}, {self.comment}, Customer {self.customer_id}, Item {self.item_id}>'