from datetime import datetime
from typing import Optional
from .. import app_factory

db = app_factory.main_controller.db

# Define the UserAccount model
class UserAccount(db.Model):
    """
    Represents a user account in the system.
    """

    id : int = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Primary key
    first_name : str = db.Column(db.String(100), nullable=False)  # First name
    last_name : str= db.Column(db.String(100), nullable=False)    # Last name
    username : str = db.Column(db.String(50), unique=True, nullable=False)  # Unique username
    password : str = db.Column(db.String(255), nullable=False)  # Password (hashed)
    created_on : datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # Account creation date

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "username": self.username,
            "password": self.password,
            "created_on": self.created_on
        }

    def __repr__(self) -> str:
        return f"<User Account(id={self.id}, username={self.username}, created_on={self.created_on})>"