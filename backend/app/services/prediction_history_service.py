from datetime import datetime
from typing import Optional
from .models import PredictionHistory
from .ai_model import AIModel
import logging
 
logger = logging.getLogger(__name__)
 
 
class PredictionHistoryService:
 
    def __init__(self, database_utility):
        self._database_utility = database_utility
 
    def get_all(self):
        """
        Retrieve all prediction history entries from the database.
        """
        with self._database_utility.session_scope() as session:
            # entries = Entry.query.all() # version 2
            entries = (
                session.execute(
                    self._database_utility.db.select(PredictionHistory).order_by(
                        PredictionHistory.id
                    )
                )
                .scalars()
                .all()
            )
 
            # Convert to list of dictionaries within the session scope
            entries_dict = [entry.to_dict() for entry in entries]
 
            logger.info(f"Retrieved {len(entries)} prediction history entries")
  
            return entries_dict
        
    def insert(
        self,
        customer_ID: int,
        shopping_pt: int,
        record_type: int,
        day: int,
        state: int,
        location: int,
        group_size: int,
        homeowner: int,
        car_age: int,
        car_value: int,
        risk_factor: int,
        age_oldest: int,
        age_youngest: int,
        married_couple: int,
        C_previous: int,
        duration_previous: int,
        A: int,
        B: int,
        C: int,
        D: int,
        E: int,
        F: int,
        G: int,
        hours: int,
        minutes: int,
        prediction: int,
    ) -> Optional[int]:
        """
        Create a new history entry for a prediction.

        This function creates a new PredictionHistory object with the provided
        parameters, then adds it to the database.

        Args:
            customer_ID (int): The ID of the customer.
            shopping_pt (int): The shopping point.
            record_type (int): The type of record.
            day (int): The day of the record.
            state (int): The state value.
            location (int): The location value.
            group_size (int): The size of the group.
            homeowner (int): Whether the customer is a homeowner.
            car_age (int): The age of the car.
            car_value (int): The value of the car.
            risk_factor (int): The risk factor.
            age_oldest (int): The age of the oldest person in the group.
            age_youngest (int): The age of the youngest person in the group.
            married_couple (int): Whether the customer is a married couple.
            C_previous (int): Previous value of C.
            duration_previous (int): Duration of previous interaction.
            A (int): Value of A.
            B (int): Value of B.
            C (int): Value of C.
            D (int): Value of D.
            E (int): Value of E.
            F (int): Value of F.
            G (int): Value of G.
            hours (int): The hour of the interaction.
            minutes (int): The minutes of the interaction.
            prediction (int): The predicted class.

        Returns:
            int or None: The ID of the newly created history entry if successful,
                          None if an error occurred during the database operation.

        Raises:
            Exception: If there's an error during the database operation.
                        The error is caught, printed, and None is returned.
        """
        # Ensures that all the provided inputs are numeric values
        if not all(
            isinstance(x, (int))
            for x in [
                customer_ID, shopping_pt, record_type, day, state,
                location, group_size, homeowner, car_age, car_value,
                risk_factor, age_oldest, age_youngest, married_couple,
                C_previous, duration_previous, A, B, C, D, E, F, G,
                hours, minutes, prediction
            ]
        ):
            logger.error("Invalid input: All inputs must be numeric values")
            raise ValueError("All inputs must be numeric values")

        # Ensures all provided inputs are positive values
        if not all(
            x >= 0 for x in [
                customer_ID, shopping_pt, record_type, day, state,
                location, group_size, homeowner, car_age, car_value,
                risk_factor, age_oldest, age_youngest, married_couple,
                C_previous, duration_previous, A, B, C, D, E, F, G,
                hours, minutes, prediction
            ]
        ):
            logger.error("Invalid input: All inputs must be positive values")
            raise ValueError("All inputs must be positive values")

        # The above checks are performed before creating a new history entry in the database to maintain data integrity.
        from .models import PredictionHistory

        new_entry = PredictionHistory(
            customer_ID=customer_ID,
            shopping_pt=shopping_pt,
            record_type=record_type,
            day=day,
            state=state,
            location=location,
            group_size=group_size,
            homeowner=homeowner,
            car_age=car_age,
            car_value=car_value,
            risk_factor=risk_factor,
            age_oldest=age_oldest,
            age_youngest=age_youngest,
            married_couple=married_couple,
            C_previous=C_previous,
            duration_previous=duration_previous,
            A=A,
            B=B,
            C=C,
            D=D,
            E=E,
            F=F,
            G=G,
            hours=hours,
            minutes=minutes,
            prediction=prediction,
            predicted_on=datetime.utcnow(),
        )

        with self._database_utility.session_scope() as session:
            session.add(new_entry)

            # This will populate the id of the new entry
            session.flush()

            logger.info(
                f"Added new history entry with ID {new_entry.id} , with Prediction : {new_entry.prediction}"
            )

            return new_entry.id

        return None

    def delete_by_id(self, id: int) -> bool:
        """
        Delete a history entry by its ID.
        """
        # Ensures that the provided id is a valid positive integer
        if not isinstance(id, int) or id <= 0:
            logger.error("Invalid input: ID must be a positive integer")
            raise ValueError("ID must be a positive integer")

        with self._database_utility.session_scope() as session:
            entry = session.get(PredictionHistory, id)
            if entry:
                session.delete(entry)
                logger.info(f"Deleted history entry with ID {id}")
                return True
            else:
                logger.warning(f"No history entry found with ID {id}")
                return False
            
    def delete_all(self) -> int:
        """
        Delete all history entries.
        """
        with self._database_utility.session_scope() as session:
            num_deleted = session.query(PredictionHistory).delete()
            logger.info(f"Deleted {num_deleted} history entries")
            return num_deleted