from app import create_app, db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app.models import User

import sys

app = create_app()

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

@manager.command
def make_shell_context():
    return dict(app=app, db=db, user=User)

if __name__ == '__main__':
    # Check if the "--debug" or "-d" option is provided
    if "--debug" in sys.argv or "-d" in sys.argv:
        app.debug = True  # Enable debug mode if the option is provided

    manager.run()