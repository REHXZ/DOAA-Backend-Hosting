from flask.views import MethodView
from flask import jsonify
import logging
 
logger = logging.getLogger(__name__)
 
 
class DefaultController(MethodView):
 
    def __init__(self):
        pass
 
    def health(self):
        logger.info("Handling GET > health")
        return jsonify({"status": "OK YONG BONG HONG BIN"}), 200
 
    @classmethod
    def register(cls, app):
        logger.info("register routes")
 
        app.add_url_rule(
            "/api/health",
            view_func=cls().health,
            methods=["GET"],
        )
 