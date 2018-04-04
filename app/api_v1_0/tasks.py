###########################################
# File: tasks.py
# Desc: definition of all endpoints
# Apr 2018
###########################################

from flask import jsonify, request, g, abort, url_for, current_app, Response
from .. import db
from ..models import Task
from . import api

"""
tasks: Return all tasks, pagination every 4 items.
"""
@api.route('/tasks/')
def get_tasks():
    """Endpoint returning all tasks
    ---
    parameters:
    definitions:
      Palette:
        type: object
        properties:
          palette_name:
            type: array
            items:
              $ref: '#/definitions/Color'
      Color:
        type: string
    responses:
      201:
        description: A list of tasks
        schema:
          $ref: '#/definitions/Palette'
    """
    page = request.args.get('page', 1, type=int)
    pagination = Task.query.paginate(
        page, per_page = current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    tasks = pagination.items
    prev = None

    if pagination.has_prev:
        prev = url_for('api.get_tasks', page = page - 1, _external=True)
    next = None
    if pagination.has_next:
        next = url_for('api.get_tasks', page = page + 1, _external=True)

    return jsonify({
        'tasks': [task.to_json() for task in tasks], 'prev': prev,
        'next': next,
        'count': pagination.total
    })


"""
tasks/{id}: Returns a specific task by id.
"""
@api.route('/tasks/<int:id>')
def get_task(id):
    """Example endpoint returning a task by id
    ---
    parameters:
      - id: id of task
    definitions:
      Palette:
        type: object
        properties:
          palette_name:
            type: array
            items:
              $ref: '#/definitions/Color'
      Color:
        type: string
    responses:
      201:
        description: A simple task
        schema:
          $ref: '#/definitions/Palette'
        examples:
          {
              "description": "nothing",
              "duration": 0,
              "status": "PENDING",
              "time_to_complete": -1,
              "ts": 1522816804,
              "url": "http://127.0.0.1:5000/api/v1.0/tasks/?id=1"
        }
    """
    task = Task.query.get_or_404(id)
    return jsonify(task.to_json(), 201)

"""
tasks: Create a new task.
"""
@api.route('/tasks/', methods=['POST'])
def new_task():
    """Endpoint returning a new tasks
    ---
    parameters:
        - description: a briefly title
        - duration: a number of minutes
    definitions:
      Palette:
        type: object
        properties:
          palette_name:
            type: array
            items:
              $ref: '#/definitions/Color'
      Color:
        type: string
    responses:
      201:
        description: A new task
        schema:
          $ref: '#/definitions/Palette'
    """
    task = Task.from_json(request.json)
    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_json()), 201, \
        {'Location': url_for('api.get_task', id = task.task_id, _external=True)}

"""
tasks: Modify an existing task by id.
"""
@api.route('/tasks/<int:id>', methods=['PUT'])
def edit_task(id):
    """Endpoint returning a edited task by id
    ---
    parameters:
        - description: a briefly title
        - status: completed
    definitions:
      Palette:
        type: object
        properties:
          palette_name:
            type: array
            items:
              $ref: '#/definitions/Color'
      Color:
        type: string
    responses:
      201:
        description: A modified task
        schema:
          $ref: '#/definitions/Palette'
    """
    task = Task.query.get_or_404(id)

    # only modified if current status is pending
    if task.status == "PENDING":
        task.description = request.json.get('description', task.description)
        task.status = request.json.get('status', task.status)
        task.time_to_complete = time.duration - task.ts
        db.session.add(task)
        return jsonify(task.to_json())
    return jsonify('is not possible modify this task', 201)

"""
tasks: Delete an existing task by id.
"""
@api.route('/tasks/<int:id>', methods=['DELETE'])
def del_task(id):
    """Endpoint that deletes a task by id
    ---
    parameters:
      - id: id of task
    definitions:
      Palette:
        type: object
        properties:
          palette_name:
            type: array
            items:
              $ref: '#/definitions/Color'
      Color:
        type: string
    responses:
      201:
        description: delete a simple task by id
        schema:
          $ref: '#/definitions/Palette'
    """
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return jsonify('ok', 201)

"""
tasks: Search a list of tasks by description or status.
"""
@api.route('/tasks/search/')
def get_tasks_by():
    """Endpoint that retrieve a task by status or word
    ---
    parameters:
      - q: some word
      -status: COMPLETED or PENDING
    definitions:
      Palette:
        type: object
        properties:
          palette_name:
            type: array
            items:
              $ref: '#/definitions/Color'
      Color:
        type: string
    responses:
      201:
        description: retrieves a list of tasks
        schema:
          $ref: '#/definitions/Palette'
    """
    q = request.args.get('q')
    status = request.args.get('status')

    if status:
        tasks = Task.query.filter_by(status = status).all()
    elif q:
        tasks = Task.query.filter(Task.description.like("%{}%".format(q))).all()

    return jsonify({
        'tasks': [task.to_json() for task in tasks]
    }, 201)
