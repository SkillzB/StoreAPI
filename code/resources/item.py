import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required


class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument(
        'price',
        type=float,
        required=True,
        help="This field cannot be leave blank."
    )

    @jwt_required()
    def get(self, name):
        item = self.find_by_name(name)
        if item:
            return item
        return {'message': 'Item not found'}, 404

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        results = cursor.execute(query, (name,))
        row = results.fetchone()
        connection.close()

        if row:
            return {'item': {'name': row[0], 'price': row[1]}}

    def post(self, name):
        # force=True to force the data to be accepted as JSON, but not recommended
        if self.find_by_name(name):
            return {'message': "An items with name '{}' already exists".format(name)}, 400

        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}
        try:
            self.insert(item)
        except:
            return {'message': 'An error occured inserting the item.'}, 500
        # Status code for created
        return item, 201

    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        insert_query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(insert_query, (item['name'], item['price']))

        connection.commit()
        connection.close()

    @classmethod
    def update(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        update_query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(update_query, (item['price'], item['name']))

        connection.commit()
        connection.close()

    def put(self, name):
        data = Item.parser.parse_args()

        item = self.find_by_name(name)
        updated_item = {'name': name, 'price': data['price']}
        if item:
            # try:
            self.update(updated_item)
            return updated_item, 200
            # except:
            # return {'message': 'An error occurred updating the item.'}, 500
        else:
            # try:
            self.insert(updated_item)
            return updated_item, 201
            # except:
            #    return {'message': 'An error occurred inserting the item.'}, 500

    def delete(self, name):
        item = self.find_by_name(name)
        if item:
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()

            query = "DELETE FROM items WHERE name=?"
            cursor.execute(query, (name,))
            connection.commit()
            connection.close()
            return {'message': 'Item deleted.'}
        return {'message': 'Item not found'}, 404


class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        results = cursor.execute(query)
        #rows = cursor.fetchall()
        items = []
        for row in results:
            print(row)
            item = {'name': row[0], 'price': row[1]}
            items.append(item)
        connection.close()

        if items:
            return {'items': items}  # or use {'items', items}
        return {'items': None}, 404
