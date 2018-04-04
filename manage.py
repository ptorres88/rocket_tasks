#!/usr/bin/env python

###########################################
# File: manage.py
# Desc: Starting point of the application
# Apr 2018
###########################################

import os
from app import create_app, db
from app.models import Task
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from flasgger import Swagger

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

# Swagger initialization for the documentation
swagger = Swagger(app)

# The script tool for running commands
manager = Manager(app)

# For the new changes to the db
migrate = Migrate(app, db)

def make_shell_context():
    return dict(app = app, db = db, Task = Task)

manager.add_command('shell', Shell(make_context = make_shell_context))
manager.add_command('db', MigrateCommand)

# usage: python manager.py test
# desc: run the unit tests for all files within tests dir.
@manager.command
def test():
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity = 2).run(tests)

# usage: python manager.py test_data
# desc: create 50 random and completed tasks
@manager.command
def test_data():
    from random_words import RandomWords
    rw = RandomWords()
    for i in range(50):
        word = rw.random_word()
        task = Task.from_json({'description' : word, 'duration' : 10})
        db.session.add(task)
    db.session.commit()

if __name__ == '__main__':
    manager.run()
