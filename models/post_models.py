from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    date = db.Column(db.String(20), nullable=False)     # You can also use db.Date
    time = db.Column(db.String(20), nullable=False)
    items = db.Column(db.Text, nullable=False)           # Comma-separated items
    contact = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    donor_username = db.Column(db.String(100), nullable=False)  # Who posted it

    def __repr__(self):
        return f"<Post {self.title}>"
