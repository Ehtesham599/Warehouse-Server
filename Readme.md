# Warehouse App

> A flask-RESTful server that helps manage and view an inventory of products in respective warehouses and get a balance report.

## Database

The application uses a MySQL database with the following tables and schema:

- Products (product_id)
- Locations (location_id)
- Productmovement (movement_id, from_location, to_location, product_id, qty)
- Balance (product_id, location_id, qty)

## Resources

The app has the following resources and their respective Add/Edit/View views implemented.

## Product Resource

### View products

To view products in the Products database, user must make a `GET` request at the `/products` endpoint.
Expected result would be :

```
{
    "status": 200,
    "message": "Success",
    "data": [
        "PRODUCT_ID_1",
        "PRODUCT_ID_2",
        ...
    ]
}
```

### Add a product

To add a product to the Products database, user must make a `POST` request at the `/products` endpoint with the following JSON body:

```
{
    "product_id" : "YOUR_PRODUCT_ID"
}
```

Note: The `product_id` must be of type string.

### Edit a product

To edit a product in the Products database, user must make a `PUT` request at the `/products/PRODUCT_ID` endpoint with the following JSON body:

```
{
    "product_id" : "YOUR_PRODUCT_ID"
}
```

Note: The `product_id` must be of type string.

## Location Resource

### View locations

To view warehpuse locations in the Locations database, user must make a `GET` request at the `/locations` endpoint.
Expected result would be :

```
{
    "status": 200,
    "message": "Success",
    "data": [
        "LOCATION_ID_1",
        "LOCATION_ID_2",
        ...
    ]
}
```

### Add a location

To add a location to the Locations database, user must make a `POST` request at the `/locations` endpoint with the following JSON body:

```
{
    "location_id" : "YOUR_LOCATION_ID"
}
```

Note: The `location_id` must be of type string.

### Edit a location

To edit a location in the Locations database, user must make a `PUT` request at the `/locations/LOCATION_ID` endpoint with the following JSON body:

```
{
    "location_id" : "YOUR_LOCATION_ID"
}
```

Note: The `location_id` must be of type string.

## ProductMovement Resource

### View product movements

To view product movements from the Productmovement database, user must make a `GET` request at the `/productmovement` endpoint.
Expected result would be :

```
{
    "status": 200,
    "message": "Success",
    "data": [
        {
            "movement_id": "YOUR_MOVEMENT_ID",
            "timestamp": "ISO_8601_TIMESTAMP",
            "from_location": "SOURCE_LOCATION_ID",
            "to_location": "DESTINATION_LOCATION_ID",
            "product_id": "PRODUCT_ID",
            "qty": some_quantity
        },
        ...
    ]
}
```

### Add a product movement

To add a product movement, user must make a `POST` request at the `/productmovement` endpoint with the following JSON body :

```
{
    "movement_id": "YOUR_MOVEMENT_ID",
    "from_location": "SOURCE_LOCATION",
    "to_location": "DESTINATION_LOCATION",
    "product_id": "PRODUCT_ID",
    "qty": some_quantity
}
```

Any one, or both of `from_location` and `to_location` can be filled. If you want to move things into
a location, `from_location` will be blank, if you want to move things out, then `to_location` will be
blank.

Note: The `movement_id`, `from_location`, `to_location` and `product_id` must be of type string. The `qty` must be of type integer.

## Balance Resource

### View balance report

The home page returns the balance report with a grid view of three columns: Product, Warehouse and Quantity.
