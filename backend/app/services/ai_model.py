from typing import Optional
import pickle
import logging
import os

logger = logging.getLogger(__name__)

class AIModel:
    def __init__(self):
        # /backend/app/services
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # /backend/app
        parent_dir = os.path.dirname(current_dir)

        # /backend
        grandparent_dir = os.path.dirname(parent_dir)

        model_path = os.path.join(grandparent_dir, "ai_model", "joblib_Model.pkl")

        self._model_path: str = model_path
        self._model = None

    def load(self) -> None:
        """
        Load the AI model from the specified file path.

        Raises:
            FileNotFoundError: If the model file is not found.
            pickle.UnpicklingError: If there's an error unpickling the model file.
            MemoryError: If the file is too large to load into memory.
            Exception: For any other unexpected errors during loading.
        """
        try:
            with open(self._model_path, 'rb') as file:
                self._model = pickle.load(file)
                logger.info("AI model loaded successfully")

        except FileNotFoundError:
            logger.error(f"The file {self._model_path} was not found.")
            raise FileNotFoundError(f"The file {self._model_path} was not found.")

        except pickle.UnpicklingError:
            logger.error(f"The file {self._model_path} could not be unpickled.")
            raise pickle.UnpicklingError(
                f"The file {self._model_path} could not be unpickled."
            )

        except MemoryError:
            logger.error(f"The file {self._model_path} is too large to load into memory.")
            raise MemoryError(
                f"The file {self._model_path} is too large to load into memory."
            )

        except Exception as e:
            logger.error(
                f"An unexpected error occurred while loading the AI model: {str(e)}"
            )
            raise Exception(
                f"An unexpected error occurred while loading the AI model: {str(e)}"
            )

    def predict(self, data):
        """
        Make predictions using the loaded AI model.

        Args:
            data: Input data for prediction.

        Returns:
            Prediction results if successful, None otherwise.
        """
        if self._model is not None:
            try:
                logger.info("Model is loaded. Making prediction.")
                return self._model.predict(data)
            except Exception as e:
                logger.error(f"Error during prediction: {str(e)}")
                return None
        else:
            logger.warning("Model is not loaded. Cannot make predictions.")
            return None

    def __repr__(self) -> str:
        """
        Return a string representation of the AIModel instance.

        Returns:
            str: A string describing the AIModel instance.
        """
        return f"AIModel(model_path='{self._model_path}', model_loaded={self._model is not None})"