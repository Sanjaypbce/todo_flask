from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson import ObjectId
from flask_cors import CORS

app = Flask(__name__)

# MongoDB configuration

client = MongoClient('mongodb+srv://wwwsanjayijk07:xaZYk6xBacA4LabQ@cluster0.ek565j8.mongodb.net/')
db = client['test']  # Replace with your database name



# Define your collection
todos_collection = db['to_do']  # Replace with your collection name


cors_config = {
    "origins": ["*"],  # List your front-end URLs here
    "methods": ["GET", "POST", "PUT", "DELETE"],  # HTTP methods to allow
    "allow_headers": ["Content-Type", "Authorization"],  # Headers to allow
}

CORS(app, resources={
    r"/*": cors_config
})





# Sample Todo model (optional)
class Todo:
    def __init__(self, name, description, complete=False):
        self.name = name
        self.description = description
        self.complete = complete
        
    def json(self):
        return {
            'name': self.name,
            'description': self.description,
            'complete': self.complete
        }

    @staticmethod
    def from_json(json_data):
        return Task(
            name=json_data.get('name', ''),
            description=json_data.get('description', ''),
            complete=json_data.get('complete', False)
        )

    def to_dict(self):
        return {
            'name': self.name,
            'description': self.description,
            'complete': self.complete
        }

    @staticmethod
    def from_dict(data):
        return Task(
            name=data.get('name', ''),
            description=data.get('description', ''),
            complete=data.get('complete', False)
        )
# Routes...
# Get all todos
@app.route('/todos', methods=['GET'])
def get_todos():
    todos = []
    for todo in todos_collection.find():
        todos.append({
            'id': str(todo['_id']),
            'name': todo['name'],
            'description': todo['description'],
            'complete': todo['complete']
        })
    return jsonify(todos)

# Add a new todo
@app.route('/todos', methods=['POST'])
def add_todo():
    data = request.json
    name = data.get('name', '')
    description = data.get('description','')
    complete = data.get('complete', False)
    
    new_todo = {'name': name, 'description': description,"complete":complete}
    result = todos_collection.insert_one(new_todo)
    
    return jsonify({'id': str(result.inserted_id), 'name': name, 'complete': complete}), 201

# Update a todo by ID
@app.route('/todos/<string:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    data = request.json
    updated_todo = {
        'complete': data.get('complete', True)
    }
    
    result = todos_collection.update_one({'_id': ObjectId(todo_id)}, {'$set': updated_todo})
    
    if result.modified_count > 0:
        return jsonify({'message': 'Todo updated successfully'})
    else:
        return jsonify({'error': 'Todo not found'}), 404

# Delete a todo by ID
@app.route('/todos/<string:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    result = todos_collection.delete_one({'_id': ObjectId(todo_id)})
    
    if result.deleted_count > 0:
        return '', 204
    else:
        return jsonify({'error': 'Todo not found'}), 404


if __name__ == '__main__':
    app.run(debug=True)
