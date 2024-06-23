from app import app
from app import create_app, db
from flask_migrate import Migrate

app = create_app()

#@app.before_first_request
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
