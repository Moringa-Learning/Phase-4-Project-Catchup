from app import create_app, db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app.models import User

app = create_app()

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

@manager.command
def make_shell_context():
    return dict(app=app, db=db, user=User)

if __name__ == '__main__':
    manager.run()