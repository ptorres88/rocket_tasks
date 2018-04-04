###########################################
# File: models.py
# Desc: definition of the task class
# Apr 2018
###########################################

from app import db
from flask import current_app, request, url_for
from app.exceptions import ValidationError
import time

class Task(db.Model):
    """
    Inserts the current timestamp for calculate the elapsed time.
    """
    __tablename__ = 'task'
    task_id = db.Column(db.Integer, primary_key = True)
    description = db.Column(db.String(128))
    duration = db.Column(db.Integer, default = 0)
    ts = db.Column(db.Integer, default = int(time.time()))
    time_to_complete = db.Column(db.Integer, default = -1)
    status = db.Column(db.Enum("PENDING", "COMPLETED", name='status'), default="PENDING")

    # Convert to json the task object
    def to_json(self):
        json_post = {
            'url': url_for('api.get_tasks', id = self.task_id, _external=True),
            'description': self.description,
            'duration': self.duration,
            'ts': self.ts,
            'time_to_complete' : self.time_to_complete,
            'status' : self.status
        }
        return json_post

    # Get all info from parameters and try to create a task
    @staticmethod
    def from_json(json_post):
        description = json_post.get('description')
        duration = int(json_post.get('duration'))
        status = json_post.get('status')

        if description is None or description == '':
            raise ValidationError('task does not have a description')
        if duration <= 0:
            raise ValidationError('task does not have a valid duration')
        if status is None or status == '':
            status = "PENDING"

        return Task(description = description, duration = duration, status = status)
