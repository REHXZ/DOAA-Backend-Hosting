from datetime import datetime
from typing import Optional
from .user import UserAccount
import logging
 
logger = logging.getLogger(__name__)
 
 
class UserService:
 
    def __init__(self, database_utility):
        self._database_utility = database_utility
 
    def get_all(self):
        """
        Retrieve all prediction history entries from the database.
        """
        with self._database_utility.session_scope() as session:
            entries = (
                session.execute(
                    self._database_utility.db.select(UserAccount).order_by(
                        UserAccount.id
                    )
                )
                .scalars()
                .all()
            )
 
            # Convert to list of dictionaries within the session scope
            entries_dict = [entry.to_dict() for entry in entries]
 
            logger.info(f"Retrieved {len(entries)} prediction history entries")
  
            return entries_dict
        return None
    
    def insert(
        self,
        first_name : str,
        last_name : str,
        username : str,
        password : str,
    ) -> Optional[int]:

        # Ensures that all the provided inputs are numeric values
        if not all( isinstance(x, (str)) for x in [first_name, last_name, username, password]):

            logger.error("Invalid input: All inputs must be numeric values")
            raise ValueError("All inputs must be numeric values")

        # The above checks are performed before creating a new history entry in the database to maintain data integrity.
        from .user import UserAccount

        new_entry = UserAccount(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
            created_on=datetime.utcnow(),
        )

        with self._database_utility.session_scope() as session:
            session.add(new_entry)

            # This will populate the id of the new entry
            session.flush()

            logger.info(
                f"Added new User entry with ID {new_entry.id}."
            )

            return new_entry.id

        return None
            