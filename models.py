"""Models for Cupcake app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

DEFAULT_IMG = "https://tinyurl.com/demo-cupcake"

class Cupcake(db.Model):
    """Cupcake Class"""
    __tablename__ = "cupcakes"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    flavor = db.Column(db.String,
                       nullable=False)
    size = db.Column(db.String,
                     nullable=False)
    rating = db.Column(db.Float, 
                     nullable=False)
    image  = db.Column(db.String, 
                       default= DEFAULT_IMG,
                       nullable=False)

    def serialize(self):
        """Returns dictionary with my attributes
        mapped to keys and values."""

        return {
            "id": self.id,
            "flavor": self.flavor,
            "size": self.size,
            "rating": self.rating,
            "image": self.image
        }

    
