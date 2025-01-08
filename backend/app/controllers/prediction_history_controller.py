from flask.views import MethodView
from flask import jsonify
from flask import request
from typing import Optional
from sqlalchemy.exc import SQLAlchemyError
import logging
 
logger = logging.getLogger(__name__)
 
 
class PredictionHistoryController(MethodView):
 
    def __init__(self, ai_model, prediction_history_service):
        self._ai_model = ai_model
        self._prediction_history_service = prediction_history_service
 
    def get_all(self):
        logger.info("Handling GET > get all prediction history")
 
        try:
            entries = self._prediction_history_service.get_all()
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
 
    def add(self):
        logger.info("Handling POST > add")
        data = request.get_json()

        # Extract and validate data from the request JSON
        try:
            customer_ID = int(data["customer_ID"])
            shopping_pt = int(data["shopping_pt"])
            record_type = int(data["record_type"])
            day = int(data["day"])
            state = int(data["state"])
            location = int(data["location"])
            group_size = int(data["group_size"])
            homeowner = int(data["homeowner"])
            car_age = int(data["car_age"])
            car_value = int(data["car_value"])
            risk_factor = int(data["risk_factor"])
            age_oldest = int(data["age_oldest"])
            age_youngest = int(data["age_youngest"])
            married_couple = int(data["married_couple"])
            C_previous = int(data["C_previous"])
            duration_previous = int(data["duration_previous"])            
            A = int(data["A"])
            B = int(data["B"])
            C = int(data["C"])
            D = int(data["D"])
            E = int(data["E"])
            F = int(data["F"])
            G = int(data["G"]) 
            hours = int(data["hours"])  
            minutes =  int(data["minutes"])
            
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

        # Make a prediction using the AI model
        # Additional validation checks
        if any(x < 0 for x in [customer_ID, shopping_pt, record_type, day, state, location, car_value, married_couple, C_previous, duration_previous, A,B,C,D,E,F,G,hours,minutes,group_size, homeowner, car_age, age_oldest, age_youngest, risk_factor]):
            logger.error("All measurements must be positive")

            return (
                jsonify(
                    {"success": False, "message": "All measurements must be positive"}
                ),
                400,
            )

        X = [[customer_ID, shopping_pt, record_type, day, state, location, car_value, married_couple, C_previous, duration_previous, A,B,C,D,E,F,G,hours,minutes,group_size, homeowner, car_age, age_oldest, age_youngest, risk_factor]]

        logger.info(f"Making prediction for input: {X}")
        prediction_results = self._ai_model.predict(X)
        logger.info(f"Prediction Result: {prediction_results}")

        # Check if prediction_results is None
        if prediction_results is None:
            logger.error("Prediction failed")
            return jsonify({"success": False, "message": "Prediction failed"}), 500

        prediction: int = int(prediction_results[0])
        logger.info(f"Prediction result: {prediction}")

        try:
            # Create a new history entry in the database
            logger.info("Inserting prediction into database")
            db_result = self._prediction_history_service.insert(
                customer_ID, shopping_pt, record_type, day, state, location, car_value, married_couple, C_previous, duration_previous, A,B,C,D,E,F,G,hours,minutes,group_size, homeowner, car_age, age_oldest, age_youngest, risk_factor, prediction
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
    
    def delete_by_id(self, id):
            logger.info("Handling DELETE > delete by some id")
    
            try:
                result = self._prediction_history_service.delete_by_id(id)
                if result:
                    return (
                        jsonify(
                            {
                                "success": True,
                                "message": f"Entry with id {id} deleted successfully",
                            }
                        ),
                        200,
                    )
                else:
                    return (
                        jsonify(
                            {"success": False, "message": f"No entry found with id {id}"}
                        ),
                        404,
                    )
            except ValueError as e:
                logger.error(f"Invalid input: {str(e)}")
                return jsonify({"success": False, "message": str(e)}), 400
            except SQLAlchemyError as e:
                logger.error(f"Database error while deleting entry: {str(e)}")
                return (
                    jsonify({"success": False, "message": "A database error occurred"}),
                    500,
                )
            except Exception as e:
                logger.error(f"Error deleting entry: {str(e)}")
                return (
                    jsonify(
                        {
                            "success": False,
                            "message": "An error occurred while deleting the entry",
                        }
                    ),
                    500,
                )
            
    def delete_all(self):
            logger.info("Handling DELETE > delete all")
            try:
                num_deleted = self._prediction_history_service.delete_all()
    
                return (
                    jsonify({"success": True, "message": f"Deleted {num_deleted} entries"}),
                    200,
                )
            except SQLAlchemyError as e:
                logger.error(f"Database error while deleting all entries: {str(e)}")
                return (
                    jsonify({"success": False, "message": "A database error occurred"}),
                    500,
                )
            except Exception as e:
                logger.error(f"Unexpected error while deleting all entries: {str(e)}")
                return (
                    jsonify({"success": False, "message": "An unexpected error occurred"}),
                    500,
                )


    @classmethod
    def register(cls, app, ai_model, prediction_history_service):
        logger.info("register routes")
 
        # get all prediction history records
        app.add_url_rule(
            "/api/prediction-history",
            view_func=cls(ai_model, prediction_history_service).get_all,
            methods=["GET"],
        )

        # add a prediction history record
        app.add_url_rule(
            "/api/prediction-history",
            view_func=cls(ai_model, prediction_history_service).add,
            methods=["POST"],
        )

        
       # delete a prediction history record by id
        app.add_url_rule(
            "/api/prediction-history/<int:id>",
            view_func=cls(None, prediction_history_service).delete_by_id,
            methods=["DELETE"],
        )

    
        # delete all prediction history records
        app.add_url_rule(
            "/api/prediction-history",
            view_func=cls(None, prediction_history_service).delete_all,
            methods=["DELETE"],
        )