# ```
import datetime
from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

TODOS = {
    'todo1': {'task': 'build an API'},
    'todo2': {'task': '?????'},
    'todo3': {'task': 'profit!'},
}


def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in TODOS:
        abort(404, message="Todo {} doesn't exist".format(todo_id))


parser = reqparse.RequestParser()
parser.add_argument('task')
parser.add_argument('due date')
parser.add_argument('completed')
parser.add_argument('date completed')


# Todo
# shows a single todo item and lets you delete a todo item
class Todo(Resource):
    def get(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        return TODOS[todo_id]

    def delete(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        del TODOS[todo_id]
        return '', 204

    def put(self, todo_id):
        args = parser.parse_args()
        task = {'task title': args['task']}
        due_date = {'due date': args['due date']}
        last_updated = {'last upated': str(datetime.datetime.now())}
        completed = {'completed': args['completed']}
        completed_date = {'date completed': args['date completed']}
        if completed and not completed_date:
            completed_date = {'completed date': str(datetime.datetime.now())}
        TODOS[todo_id] = task, last_updated, due_date, completed
        return task, due_date, completed, 201


# TodoList
# shows a list of all todos, and lets you POST to add new tasks
class TodoList(Resource):
    def get(self):
        return TODOS

    def post(self):
        args = parser.parse_args()
        todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
        todo_id = 'todo%i' % todo_id
        # creation_date = {'creation date': str(datetime.datetime.now())}
        TODOS[todo_id] = {'task': args['task'], 'creation_date': str(datetime.datetime.now()), 'completed': args['completed'], 'due date': args['due date']}
        return TODOS[todo_id], 201


## Actually setup the Api resource routing here
api.add_resource(TodoList, '/todos')
api.add_resource(Todo, '/todos/<todo_id>')


if __name__ == '__main__':
    app.run(debug=True)
# ```