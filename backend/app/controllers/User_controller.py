from flask.views import MethodView
from flask import jsonify
from flask import request
from typing import Optional
from sqlalchemy.exc import SQLAlchemyError
import logging
 
logger = logging.getLogger(__name__)
 
 
class User_Controller(MethodView):
 
    def __init__(self, user_service):
        self._User_service = user_service
 
    def get_all_user(self):
        logger.info("Handling GET > get all prediction history")
 
        try:
            entries = self._User_service.get_all()
            return jsonify(entries), 200
        except SQLAlchemyError as e:
            logger.error(
                f"Database error while retrieving prediction history: {str(e)}"
            )
            return jsonify({"error": "Database error occurred"}), 500
        except Exception as e:
            logger.error(
                f"Unexpected error while retrieving prediction history: {str(e)}"
            )
            return jsonify({"error": "An unexpected error occurred"}), 500
 
    def add_user(self):
        logger.info("Handling POST > add")
        data = request.get_json()

        # Extract and validate data from the request JSON
        try:
            first_name = str(data["first_name"])
            last_name = str(data["last_name"])
            username = str(data["username"])
            password = str(data["password"])
            
        except KeyError as e:
            logger.error(f"Missing required field: {str(e)}")
            return (
                jsonify(
                    {"success": False, "message": f"Missing required field: {str(e)}"}
                ),
                400,
            )
        except ValueError as e:
            logger.error(f"Invalid input: {str(e)}")
            return (
                jsonify({"success": False, "message": f"Invalid input: {str(e)}"}),
                400,
            )

        try:
            # Create a new history entry in the database
            logger.info("Inserting prediction into database")
            db_result = self._User_service.insert(
                first_name, last_name, username, password
            )

            # Return JSON object response
            if db_result is not None:
                logger.info(f"Successfully created entry with id: {db_result}")
                return jsonify({"success": True, "id": db_result}), 201
            else:
                logger.error("Failed to create entry")
                return (
                    jsonify({"success": False, "message": "Failed to create entry"}),
                    400,
                )
        except ValueError as e:
            logger.error(f"Error creating entry: {str(e)}")
            return jsonify({"success": False, "message": str(e)}), 400
        except SQLAlchemyError as e:
            logger.error(f"Database error while creating entry: {str(e)}")
            return jsonify({"error": "Database error occurred"}), 500
        except Exception as e:
            logger.error(f"Unexpected error while adding prediction history: {str(e)}")
            return jsonify({"error": "An unexpected error occurred"}), 500
    

    @classmethod
    def register(cls, app, user_service):
        logger.info("register routes")
 
        # get all prediction history records
        app.add_url_rule(
            "/api/user",
            view_func=cls(user_service).get_all_user,
            methods=["GET"],
        )

        # add a prediction history record
        app.add_url_rule(
            "/api/user",
            view_func=cls(user_service).add_user,
            methods=["POST"],
        )