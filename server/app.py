#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Restaurant, RestaurantPizza, Pizza

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

@app.route('/')
def index():
    return '<h1>Code challenge</h1>'

# @app.route('/restaurants')
# def restaurants():

#     pass

#GET /restaurants
class Restaurants(Resource):
    def get(self):

        restaurant_list = [restaurant.to_dict() for restaurant in Restaurant.query.all()]

        response = make_response(restaurant_list, 200)

        return response

api.add_resource(Restaurants, '/restaurants')

#GET /restaurants/:id

class RestaurantById(Resource):
    def get(self, id):

        restaurant = Restaurant.query.filter(Restaurant.id == id).first().to_dict()

        response = make_response(restaurant, 200)

        return response

#DELETE /restaurants/:id

    def delete_restaurant(self, id):
        restaurant = Restaurant.query.filter_by(id = id).first()

        if restaurant:

            db.session.delete(restaurant)
            db.session.commit()

            response = make_response(
                "",
                204

            )

        else:

            response = make_response(
                {"error": "Restaurant not found"},
                404
            )

        return response

api.add_resource(RestaurantById, '/restaurants/<int:id>')


#GET /pizzas
class Pizzas(Resource):
    def get(self):

        pizza_list = [pizza.to_dict() for pizza in Pizza.query.all()]

        response = make_response(pizza_list, 200)

        return response

api.add_resource(Pizzas, '/pizzas')

#POST /restaurant_pizzas
class RestaurantPizzas(Resource):
    def post(self):
        
        #####typo here...i had Pizzas and it should be Pizza#########
        try:
            new_restaurant_pizza = RestaurantPizza(
                price = request.get_json()('price'),
                restaurant_id = request.get_json()('restaurant_id'),
                pizza_id = request.get_json()('pizza_id')
            )

            db.session.add(new_restaurant_pizza)
            db.session.commit()

            pizza = Pizza.query.filter(Pizza.id == new_restaurant_pizza.pizza_id).first()
            pizza_dict = pizza.to_dict()

            response = make_response(pizza_dict, 201)

            return response
        
        except ValueError:
            response = make_response({"errors": ["validation errors"]}, 400)

            return response
                
    
api.add_resource(RestaurantPizzas, '/restaurant_pizzas')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
