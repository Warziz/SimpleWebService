from flask import jsonify

def register_error_handlers(app):
    @app.errorhandler(ValueError)
    def handle_value_error(error):
        response = jsonify({
            "result": "error",
            "message": str(error)
        })
        response.status_code = 400
        return response

    @app.errorhandler(500)
    def handle_internal_error(error):
        response = jsonify({
            "result": "error",
            "message": "Une erreur interne est survenue. Veuillez réessayer plus tard."
        })
        response.status_code = 500
        return response

    @app.errorhandler(Exception)
    def handle_unexpected_exception(error):
        response = jsonify({
            "result": "error",
            "message": str(error)
        })
        response.status_code = 500
        return response
