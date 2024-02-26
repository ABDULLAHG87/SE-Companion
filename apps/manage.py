from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from secompanion.app import app, db
from secompanion.models import User

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Initialize Flask-Script
manager = Manager(app)
manager.add_command('db', MigrateCommand)

@manager.command
def create_tables():
    """Create all database tables."""
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    manager.run()
