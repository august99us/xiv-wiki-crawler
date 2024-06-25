import json

class DynamoFacade():

    def __init__(self):
        print("Initializing dynamo facade object")

    def Table(self, table_name):
        return DynamoTableFacade(table_name)

class DynamoTableFacade():

    def __init__(self, table_name):
        print("Creating dynamo table object with table name: " + table_name)

    def get_item(self, Key):
        print("Received a get request for item with id " + json.dumps(Key))
        # returning this should effectively be a 404, item not found
        return {'emptyobject': 'iamempty'}

    def put_item(self, Item):
        print("Received a put request for an item with id " + json.dumps(Item))
