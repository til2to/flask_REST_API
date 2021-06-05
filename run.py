from app import app
from db import db


db.init_app(app)

@app.before_first_request #Before the first request runs, the function below runs
def create_tables():
  db.create_all()
  db.session.commit()