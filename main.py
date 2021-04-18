from flask import Flask, request
from flask_restful import Api, Resource
from datetime import datetime
from db_connect import *

cursor = db.cursor()  # cursor to execute sql queries


def getISOtimestamp() -> str:
    """ A function that generates ISO 8601 timestamp """
    date = datetime.now()
    return date.isoformat()


def generate400response(error: str) -> dict:
    """ A function that generates a '400-Bad Request' message """
    return {
        "status": 400,
        "message": "Bad Request",
        "error": error
    }


def generate500response(error: str) -> dict:
    """ A function that generates a '500-Internal Server Error' message """
    return {
        "status": 500,
        "message": "Internal Server Error",
        "error": error
    }


def productExists(product_id: str) -> bool:
    """ A function that checks if a product exists in the database """
    cursor.execute(
        f"SELECT * from Products where product_id = '{product_id}'")
    row = cursor.fetchone()
    if row is not None:
        return True
    else:
        return False


def locationExists(location_id: str) -> bool:
    """ A function that checks if a location exists in the database """
    cursor.execute(
        f"SELECT * from Locations where location_id = '{location_id}'")
    row = cursor.fetchone()
    if row is not None:
        return True
    else:
        return False


class Product(Resource):
    """Resource for managing products on the server"""

    def get(self, product_id: str = None):
        """ RESTful GET method """
        try:
            if product_id:
                cursor.execute(
                    f"SELECT * from Products where product_id = '{product_id}'")
                row = cursor.fetchone()
                if row is not None:
                    data = row[0]
                else:
                    response = generate400response(
                        f"Product id : {product_id} does not exist!")
                    return response, 400
            else:
                cursor.execute(f"SELECT * from Products")
                rows = [res[0] for res in cursor.fetchall()]
                if rows is not None:
                    data = rows
                else:
                    data = "Empty set!"

        except Exception as error:
            response = generate500response(f"database query failed - {error}")
            return response, 500

        return {
            "status": 200,
            "message": "Success",
            "data": data
        }, 200

    def post(self):
        """ RESTful POST method """
        data = request.get_json()

        try:
            product_id: str = data['product_id']
        except KeyError as key:
            response = generate400response(f"{key} is required!")
            return response, 400

        if not isinstance(product_id, str):
            response = generate400response("'product_id' must be a str")
            return response, 400

        try:
            cursor.execute(
                f"INSERT INTO Products (product_id) VALUES('{product_id}')")
            db.commit()

        except Exception as error:
            response = generate500response(f"database query failed - {error}")
            return response, 500

        return {
            "status": 201,
            "message": "Success"
        }, 201


class Location(Resource):
    """Resource for managing warehouse locations on the server"""

    def get(self, location_id: str = None):
        """ RESTful GET handler """
        try:
            if location_id:
                cursor.execute(
                    f"SELECT * from Locations where location_id = '{location_id}'")
                row = cursor.fetchone()
                if row is not None:
                    data = row[0]
                else:
                    response = generate400response(
                        f"Location id : {location_id} does not exist!")
                    return response, 400
            else:
                cursor.execute(f"SELECT * from Locations")
                rows = [res[0] for res in cursor.fetchall()]
                if rows is not None:
                    data = rows
                else:
                    data = "Empty set!"

        except Exception as error:
            response = generate500response(f"database query failed - {error}")
            return response, 500

        return {
            "status": 200,
            "message": "Success",
            "data": data
        }, 200

    def post(self):
        """ RESTful POST method """
        data = request.get_json()

        try:
            location_id: str = data['location_id']
        except KeyError as key:
            response = generate400response(f"{key} is required!")
            return response, 400

        if not isinstance(location_id, str):
            response = generate400response("'location_id' must be a str")
            return response, 400

        try:
            cursor.execute(
                f"INSERT INTO Locations (location_id) VALUES('{location_id}')")
            db.commit()

        except Exception as error:
            response = generate500response(f"database query failed - {error}")
            return response, 500

        return {
            "status": 201,
            "message": "Success"
        }, 201

    def put(self, location_id: str):
        """ RESTful PUT method """
        data = request.get_json()

        try:
            new_location_id: str = data['new_location_id']
        except KeyError as key:
            response = generate400response(f"{key} is required!")
            return response, 400

        if not isinstance(new_location_id, str):
            response = generate400response(
                "'new_location_id' must be a str")
            return response, 400

        try:
            if locationExists(location_id):
                cursor.execute(
                    f"UPDATE Locations SET location_id = '{new_location_id}' WHERE location_id = '{location_id}'")
                db.commit()
            else:
                response = generate400response(
                    f"Location id : {location_id} does not exist!")
                return response, 400

        except Exception as error:
            response = generate500response(
                f"database query failed - {error}")
            return response, 500

        return {
            "status": 201,
            "message": "Success",
            "location_id": f"{location_id} replaced with {new_location_id}"
        }, 201


class ProductMovement(Resource):
    """Resource for managing product movement on the server"""

    def get(self):
        """ RESTful GET handler """
        data = request.get_json()
        return {
            "status": 200,
            "data": data
        }, 200


app = Flask(__name__)
api = Api(app)

api.add_resource(Product, '/products', '/products/',
                 '/products/<string:product_id>')

api.add_resource(Location, '/locations', '/locations/',
                 '/locations/<string:location_id>')

if __name__ == "__main__":
    app.run(debug=True)  # test environment
