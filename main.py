from flask import Flask, request, render_template, make_response
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


def movementExists(movement_id: str) -> bool:
    """ A function that checks if a product movement exists in the database """
    cursor.execute(
        f"SELECT * from Productmovement where movement_id = '{movement_id}'")
    row = cursor.fetchone()
    if row is not None:
        return True
    else:
        return False


def productExistsAtLocation(product_id: str, location_id: str) -> bool:
    """ A function that checks if a specific product and its location exists in the database """
    cursor.execute(
        f"SELECT id from Balance WHERE product_id='{product_id}' AND location_id='{location_id}'")
    row = cursor.fetchone()
    if row is not None:
        return True
    else:
        return False


def getQtyFromBalance(product_id: str, location_id: str) -> int:
    """ A function that returns the quantity present in balance for a specific product and location """

    cursor.execute(
        f"SELECT qty from Balance WHERE product_id='{product_id}' AND location_id='{location_id}'")
    row = cursor.fetchone()
    if row is not None:
        return row[0]
    else:
        return 0


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

        if productExists(product_id):
            response = generate400response(f"'{product_id}' already exists!")
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

    def put(self, product_id: str):
        """ RESTful PUT method """
        data = request.get_json()

        try:
            new_product_id: str = data['new_product_id']
        except KeyError as key:
            response = generate400response(f"{key} is required!")
            return response, 400

        if not isinstance(new_product_id, str):
            response = generate400response(
                "'new_product_id' must be a str")
            return response, 400

        if productExists(product_id):
            try:
                cursor.execute(
                    f"UPDATE Products SET product_id = '{new_product_id}' WHERE product_id = '{product_id}'")
                db.commit()
            except Exception as error:
                response = generate500response(
                    f"database query failed - {error}")
                return response, 500
        else:
            response = generate400response(
                f"Product id : {product_id} does not exist!")
            return response, 400

        return {
            "status": 201,
            "message": "Success",
            "product_id": f"{product_id} replaced with {new_product_id}"
        }, 201


class Location(Resource):
    """Resource for managing warehouse locations on the server"""

    def get(self, location_id: str = None):
        """ RESTful GET method """
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

        if locationExists(location_id):
            response = generate400response(f"'{location_id}' already exists!")
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

        if locationExists(location_id):
            try:
                cursor.execute(
                    f"UPDATE Locations SET location_id = '{new_location_id}' WHERE location_id = '{location_id}'")
                db.commit()
            except Exception as error:
                response = generate500response(
                    f"database query failed - {error}")
                return response, 500
        else:
            response = generate400response(
                f"Location id : {location_id} does not exist!")
            return response, 400

        return {
            "status": 201,
            "message": "Success",
            "location_id": f"{location_id} replaced with {new_location_id}"
        }, 201


class ProductMovement(Resource):
    """Resource for managing product movement on the server"""

    def get(self, movement_id: str = None):
        """ RESTful GET method """
        try:
            if movement_id:
                cursor.execute(
                    f"SELECT * from Productmovement where movement_id = '{movement_id}'")
                row = cursor.fetchall()
                if len(row) > 0:
                    if row is not None:
                        data = row[0]
                        result = {
                            "movement_id": data[0],
                            "timestamp": data[1],
                            "from_location": data[2],
                            "to_location": data[3],
                            "product_id": data[4],
                            "qty": data[5]
                        }
                else:
                    response = generate400response(
                        f"Movement id : {movement_id} does not exist!")
                    return response, 400
            else:
                cursor.execute(f"SELECT * from Productmovement")
                rows = cursor.fetchall()
                if len(rows) > 0:
                    result = []
                    for row in rows:
                        singleResult = {
                            "movement_id": row[0],
                            "timestamp": row[1],
                            "from_location": row[2],
                            "to_location": row[3],
                            "product_id": row[4],
                            "qty": row[5]
                        }
                        result.append(singleResult.copy())
                else:
                    result = "Empty set!"

        except Exception as error:
            response = generate500response(f"database query failed - {error}")
            return response, 500

        return {
            "status": 200,
            "message": "Success",
            "data": result
        }, 200

    def post(self):
        """ RESTful POST method """
        data = request.get_json()

        try:
            movement_id: str = data['movement_id']
            from_location: str = data['from_location']
            to_location: str = data['to_location']
            product_id: str = data['product_id']
            qty: int = data['qty']

        except KeyError as key:
            response = generate400response(f"{key} is required!")
            return response, 400

        if not isinstance(movement_id, str):
            response = generate400response("'movement_id' must be a str")
            return response, 400

        if movementExists(movement_id):
            response = generate400response(f"'{movement_id}' already exists")
            return response, 400

        if not from_location and not to_location:
            response = generate400response("'Both locations cannot be empty")
            return response, 400

        if from_location:
            if not isinstance(from_location, str):
                response = generate400response("'from_location' must be a str")
                return response, 400

            if not locationExists(from_location):
                response = generate400response(
                    "'from_location' does not exist! Please register the location")
                return response, 400

        if to_location:
            if not isinstance(to_location, str):
                response = generate400response("'to_location' must be a str")
                return response, 400

            if not locationExists(to_location):
                response = generate400response(
                    "'to_location' does not exist! Please register the location")
                return response, 400

        if not productExists(product_id):
            response = generate400response(
                f"{product_id} is not resgistered! Please add product")
            return response, 400

        if not isinstance(product_id, str):
            response = generate400response("'product_id' must be a str")
            return response, 400

        if not isinstance(qty, int):
            response = generate400response("'qty' must be an int")
            return response, 400

        try:
            if not from_location and to_location:
                if productExistsAtLocation(product_id, to_location):
                    cursor.execute(
                        f"UPDATE Balance SET qty = qty+{qty} WHERE product_id='{product_id}' and location_id='{to_location}'")
                    db.commit()
                else:
                    cursor.execute(
                        f"INSERT INTO Balance (product_id, location_id, qty) VALUES('{product_id}', '{to_location}', '{qty}')")
                    db.commit()

            if from_location and not to_location:
                cursor.execute(
                    f"UPDATE Balance SET qty = qty-{qty} WHERE product_id='{product_id}' and location_id='{from_location}'")
                db.commit()

            if from_location and to_location:

                if getQtyFromBalance(product_id, from_location) >= qty:
                    cursor.execute(
                        f"UPDATE Balance SET qty = qty-{qty} WHERE product_id='{product_id}' and location_id='{from_location}'")
                    db.commit()

                    if productExistsAtLocation(product_id, to_location):
                        cursor.execute(
                            f"UPDATE Balance SET qty = qty+{qty} WHERE product_id='{product_id}' and location_id='{to_location}'")
                        db.commit()

                    else:
                        cursor.execute(
                            f"INSERT INTO Balance (product_id, location_id, qty) VALUES('{product_id}', '{to_location}', '{qty}')")

                else:
                    response = generate400response(
                        "Not enough quantity at 'from_location'")
                    return response, 400

            cursor.execute(
                f"INSERT INTO Productmovement (movement_id, timestamp, from_location, to_location, product_id, qty) VALUES('{movement_id}','{getISOtimestamp()}','{from_location}', '{to_location}', '{product_id}', '{qty}')")
            db.commit()

        except Exception as error:
            response = generate500response(f"database query failed - {error}")
            return response, 500

        return {
            "status": 201,
            "message": "Success"
        }, 201


class BalanceReport(Resource):
    def get(self):
        """ A RESTful GET method """

        headers = {'Content-Type': 'text/html'}

        try:
            cursor.execute(f"SELECT * from Balance")
            rows = cursor.fetchall()
            if len(rows) > 0:
                result = rows
            else:
                return make_response(render_template("no_data.html"), 200, headers)

        except Exception as error:
            response = generate500response(f"database query failed - {error}")
            return response, 500

        return make_response(render_template("balance.html", rows=result, mimetype='text/html'), 200, headers)


app = Flask(__name__)
api = Api(app)

api.add_resource(BalanceReport, '/')

api.add_resource(Product, '/products', '/products/',
                 '/products/<string:product_id>')

api.add_resource(Location, '/locations', '/locations/',
                 '/locations/<string:location_id>')

api.add_resource(ProductMovement, '/productmovement', '/productmovement/',
                 '/productmovement/<string:movement_id>')

if __name__ == "__main__":
    app.run(debug=True)  # test environment
