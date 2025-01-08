from flask.views import MethodView
from flask import jsonify
from flask import request
import logging

logger = logging.getLogger(__name__)

class AIModelController(MethodView):
    
    def __init__(self, ai_model):
        self._ai_model = ai_model

    def predict(self):
        """
        This endpoint accepts relevant features and returns a regression prediction.

        Request JSON:
        {
            "group_size": int,
            "homeowner": int,
            "car_age": int,
            "age_oldest": int,
            "age_youngest": int,
            "risk_factor": float
        }

        Returns:
        JSON object with fields:
            - success: boolean indicating if the operation was successful
            - prediction: float, the predicted value
            - message: string, error message (if not successful)

        Response Codes:
            - 200: Prediction successful
            - 400: Bad request (input validation failed)
            - 500: Prediction failed
        """
        data = request.get_json()
        logger.info(f"Raw request data: {data}")
        logger.info("Handling POST > predict")

        if data is None:
            logger.info("Data is Transformed to Object.")
            return jsonify({"success": False, "message": "No JSON data received or JSON is malformed."}), 400
        
        logger.info(f"Received data: {data}")
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
        X = [[customer_ID, shopping_pt, record_type, day, state, location, car_value, married_couple, C_previous, duration_previous, A,B,C,D,E,F,G,hours,minutes,group_size, homeowner, car_age, age_oldest, age_youngest, risk_factor]]

        logger.info(f"Making prediction for input: {X}")
        prediction_results = self._ai_model.predict(X)

        # Check if prediction_results is None
        if prediction_results is None:
            logger.error("Prediction failed")
            return jsonify({"success": False, "message": "Prediction failed"}), 500

        prediction: float = float(prediction_results[0])  # Assuming regression returns a float

        logger.info(f"Prediction result: {prediction}")

        return jsonify({"success": True, "prediction": prediction})

    @classmethod
    def register(cls, app, ai_model):
        logger.info("Registering routes")

        # Predict based on input features
        app.add_url_rule(
            "/api/model/predict",
            view_func=cls(ai_model).predict,
            methods=["POST"],
        )