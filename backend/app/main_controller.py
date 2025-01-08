from .services.ai_model import AIModel
from .services.database_utility import DatabaseUtility
import logging
import pickle

logger = logging.getLogger(__name__)
 
 
class MainController:
    def __init__(self, app):
        # Keep track of whether routes have been set up
        self._is_routes_set_up = False
 
        self._app = app
        self._ai_model = AIModel()
 
        # Initialize other attributes to None, they'll be set up later
        self._database_utility = DatabaseUtility(self._app)
        self._db = self._database_utility.db

        self._prediction_history_service = None
        self._User_service = None

    @property
    def db(self):
        return self._db
 
    @property
    def database_utility(self):
        return self._database_utility

    def _setup_routes(self):
        """
        Configure and register API routes for the Flask application.
 
        The method uses Flask's add_url_rule to register these routes, utilizing MethodView
        classes for handling the requests.
 
        Note:
        - This method should be called after the AI model and prediction history service have been initialized.
        - The controllers are imported within this method to avoid circular imports.
 
        Raises:
            ImportError: If the required controllers cannot be imported.
        """
        # Check if routes are already set up
        if self._is_routes_set_up:
            logger.info("Warning: Routes are already set up. Skipping.")
            return
        
        # ------------------------------------------------
        # Register the routes  
        # ------------------------------------------------
        from .controllers.default_controller import DefaultController
        DefaultController.register(self._app)
    

        from .controllers.User_controller import User_Controller
        User_Controller.register(self._app,self._User_service)

        # Register the Prediction History Routes
        from .controllers.prediction_history_controller import (
            PredictionHistoryController,
        )
 
        PredictionHistoryController.register(
            self._app, self._ai_model, self._prediction_history_service
        )

        # Register the AI Model Routes
        from .controllers.ai_model_controller import AIModelController
        AIModelController.register(self._app, self._ai_model)
 
        # Mark routes as set up
        self._is_routes_set_up = True
 
    def run(self):
        # Register the blueprint.
        # The AI Model is a very important part of the application.
        # If the AI model is not loaded, the application will not function properly,
        # And the return statement ensures that the application will not start.
 
        try:
            logger.info("Trying to Load AI Model")
            self._ai_model.load()
            logger.info("Ai Model Loaded!")
        except FileNotFoundError as e:
            logger.error(f"AI model file not found: {str(e)}")
            return
        except pickle.UnpicklingError as e:
            logger.error(f"Error unpickling AI model: {str(e)}")
            return
        except Exception as e:
            logger.error(f"Unexpected error loading AI model: {str(e)}")
            return
        
        self._database_utility.init(self._app)

        # Set up the prediction history service.
        from .services.prediction_history_service import PredictionHistoryService
        from .services.User_service import UserService
        self._User_service = UserService(self._database_utility)
        self._prediction_history_service = PredictionHistoryService(
            self._database_utility
        )

        self._setup_routes()
        logger.info("Routes are Setup!")

