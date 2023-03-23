from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

# Add models here
class Restaurant(db.Model, SerializerMixin):
    __tablename__ = "restaurants"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)

    restaurant_pizzas = db.relationship('RestaurantPizza', backref='restaurant')

    serialize_rules = ('-restaurant_pizzas.restaurant', '-pizzas.restaurants')

    pizzas = association_proxy('restaurant_pizzas', 'pizza')

    def __repr__(self):
        return f'<restaurant name:{self.name}, address:{self.address}, >'


class Pizza(db.Model, SerializerMixin):
    __tablename__ = "pizzas"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ingredients = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())


    restaurant_pizzas = db.relationship('RestaurantPizza', backref='pizza')

    restaurants = association_proxy('restaurant_pizzas', 'restaurant')


    serialize_rules = ('-restaurant_pizzas.pizza', '-restaurants.pizzas')


    def __repr__(self):
        return f'<pizza name:{self.name}, ingredients:{self.ingredients}, >'


class RestaurantPizza(db.Model, SerializerMixin):
    __tablename__ = "restaurant_pizzas"

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'))
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'))

    serialize_rules = ('-restaurant.pizzas', '-pizza.restaurants', '-restaurant.restaurant_pizzas', 'pizza.restaurant_pizzas','-created_at', '-updated_at')


    @validates('price')
    def validate_age(self, key, price):
        if price < 2 or price > 29:
            raise ValueError('price must be between 1 and 30 years old')
        return price

