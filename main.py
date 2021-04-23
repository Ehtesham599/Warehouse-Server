from flask import Flask, request, render_template, make_response, redirect, flash
from flask_restful import Api, Resource
from datetime import datetime
from db_connect import *

cursor = db.cursor()  # cursor to execute sql queries


def getISOtimestamp() -> str:
    """ A function that generates ISO 8601 timestamp """
    date = datetime.now()
    return date.isoformat()


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

        headers = {'Content-Type': 'text/html'}
        data = []
        response = None

        try:
            if product_id:
                cursor.execute(
                    f"SELECT * from Products where product_id = '{product_id}'")
                row = cursor.fetchone()
                if row is not None:
                    data = row[0]
                else:
                    response = f"Product id : {product_id} does not exist!"
            else:
                cursor.execute(f"SELECT * from Products")
                rows = [res[0] for res in cursor.fetchall()]
                if rows is not None:
                    data = rows
                else:
                    data = "Empty set!"

        except Exception as error:
            response = f"database query failed - {error}"

        return make_response(render_template("product.html", rows=data, errorResponse=response, mimetype='text/html'), 200, headers)

    def post(self):
        """ RESTful POST method """
        product_id = request.form.get("productId")

        response = None

        try:
            cursor.execute(
                f"INSERT INTO Products (product_id) VALUES('{product_id}')")
            db.commit()

        except Exception as error:
            response = f"database query failed - {error}"

        if response:
            print(response)

        return redirect("/products")


class Location(Resource):
    """Resource for managing warehouse locations on the server"""

    def get(self, location_id: str = None):
        """ RESTful GET method """

        headers = {'Content-Type': 'text/html'}
        data = []
        response = None

        try:
            if location_id:
                cursor.execute(
                    f"SELECT * from Locations where location_id = '{location_id}'")
                row = cursor.fetchone()
                if row is not None:
                    data = row[0]
                else:
                    response = f"Location id : {location_id} does not exist!"

            else:
                cursor.execute(f"SELECT * from Locations")
                rows = [res[0] for res in cursor.fetchall()]
                if rows is not None:
                    data = rows
                else:
                    data = "Empty set!"

        except Exception as error:
            response = f"database query failed - {error}"

        return make_response(render_template("location.html", rows=data, errorResponse=response, mimetype='text/html'), 200, headers)

    def post(self):
        """ RESTful POST method """
        location_id = request.form.get("locationId")

        try:
            cursor.execute(
                f"INSERT INTO Locations (location_id) VALUES('{location_id}')")
            db.commit()

        except Exception as error:
            response = f"database query failed - {error}"

        if response:
            print(response)

        return redirect("/locations")


class ProductMovement(Resource):
    """Resource for managing product movement on the server"""

    def get(self, movement_id: str = None):
        """ RESTful GET method """

        headers = {'Content-Type': 'text/html'}
        result = []
        products = []
        locations = []
        cursor.execute(f"SELECT * from Products")
        products = [res[0] for res in cursor.fetchall()]
        cursor.execute(f"SELECT * from Locations")
        locations = [res[0] for res in cursor.fetchall()]
        response = None

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
                    response = f"Movement id : {movement_id} does not exist!"
            else:
                cursor.execute(f"SELECT * from Productmovement")
                rows = cursor.fetchall()
                if len(rows) > 0:
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
                    response = "Empty set!"

        except Exception as error:
            response = f"database query failed - {error}"

        return make_response(render_template("product_movement.html", result=result, products=products, locations=locations, errorResponse=response, mimetype='text/html'), 200, headers)

    def post(self):
        """ RESTful POST method """

        movement_id = request.form.get("movementId")
        from_location = request.form.get("fromLocation")
        to_location = request.form.get("toLocation")
        product_id = request.form.get("productId")
        qty = int(request.form.get("qty"))

        if from_location == "Select":
            from_location = None

        if to_location == "Select":
            to_location = None

        if movementExists(movement_id):
            response = f"'{movement_id}' already exists"

        if not from_location and not to_location:
            response = "'Both locations cannot be empty"

        if not isinstance(qty, int):
            response = "'qty' must be an int"

        try:

            if not productExists(product_id):
                response = f"{product_id} is not resgistered! Please add product"

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
                    response = "Not enough quantity at 'from_location'"
                    flash(response)

            cursor.execute(
                f"INSERT INTO Productmovement (movement_id, timestamp, from_location, to_location, product_id, qty) VALUES('{movement_id}','{getISOtimestamp()}','{from_location}', '{to_location}', '{product_id}', '{qty}')")
            db.commit()

        except Exception as error:
            response = f"database query failed - {error}"

        if response:
            print(response)

        return redirect("/productmovement")


class BalanceReport(Resource):
    def get(self):
        """ A RESTful GET method """

        headers = {'Content-Type': 'text/html'}
        response = None
        result = []

        try:
            cursor.execute(f"SELECT * from Balance")
            rows = cursor.fetchall()
            if len(rows) > 0:
                result = rows
            else:
                response = "Empty Set"

        except Exception as error:
            response = f"database query failed - {error}"

        return make_response(render_template("index.html", rows=result, errorResponse=response, mimetype='text/html'), 200, headers)


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
