from datetime import datetime
from typing import Optional
from .. import app_factory

db = app_factory.main_controller.db

# Define the CustomerRecord model
class PredictionHistory(db.Model):
    """
    Represents a record of customer shopping data.
    """

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_ID: int = db.Column(db.Integer, nullable=False)
    shopping_pt: int = db.Column(db.Integer, nullable=False)
    record_type: int = db.Column(db.Integer, nullable=False)
    day: int = db.Column(db.Integer, nullable=False)
    state: int = db.Column(db.Integer, nullable=False)
    location: int = db.Column(db.Integer, nullable=False)
    group_size: int = db.Column(db.Integer, nullable=False)
    homeowner: int = db.Column(db.Integer, nullable=False)
    car_age: int = db.Column(db.Integer, nullable=False)
    car_value: int = db.Column(db.Integer, nullable=False)
    risk_factor: int = db.Column(db.Integer, nullable=False)
    age_oldest: int = db.Column(db.Integer, nullable=False)
    age_youngest: int = db.Column(db.Integer, nullable=False)
    married_couple: int = db.Column(db.Integer, nullable=False)
    C_previous: int = db.Column(db.Integer, nullable=False)
    duration_previous: int = db.Column(db.Integer, nullable=False)
    A: int = db.Column(db.Integer, nullable=False)
    B: int = db.Column(db.Integer, nullable=False)
    C: int = db.Column(db.Integer, nullable=False)
    D: int = db.Column(db.Integer, nullable=False)
    E: int = db.Column(db.Integer, nullable=False)
    F: int = db.Column(db.Integer, nullable=False)
    G: int = db.Column(db.Integer, nullable=False)
    hours: int = db.Column(db.Integer, nullable=False)
    minutes: int = db.Column(db.Integer, nullable=False)
    prediction: int = db.Column(db.Integer, nullable=False)
    predicted_on: datetime = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow
    )

    def to_dict(self):
        return {
            "id": self.id,
            "customer_ID": self.customer_ID,
            "shopping_pt": self.shopping_pt,
            "record_type": self.record_type,
            "day": self.day,
            "state": self.state,
            "location": self.location,
            "group_size": self.group_size,
            "homeowner": self.homeowner,
            "car_age": self.car_age,
            "car_value": self.car_value,
            "risk_factor": self.risk_factor,
            "age_oldest": self.age_oldest,
            "age_youngest": self.age_youngest,
            "married_couple": self.married_couple,
            "C_previous": self.C_previous,
            "duration_previous": self.duration_previous,
            "A": self.A,
            "B": self.B,
            "C": self.C,
            "D": self.D,
            "E": self.E,
            "F": self.F,
            "G": self.G,
            "hours": self.hours,
            "minutes": self.minutes,
            "prediction": self.prediction,
            "predicted_on": self.predicted_on,
        }

    def __repr__(self) -> str:
        return f"<CustomerRecord(id={self.id}, customer_ID={self.customer_ID}, created_on={self.predicted_on})>"