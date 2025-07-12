from flask import jsonify

def register_error_handlers(app):
    """
    Register error handlers for the application
    """
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "error": "Bad Request",
            "message": str(error.description) if hasattr(error, 'description') else "Invalid request data"
        }), 400
    
    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            "error": "Unauthorized",
            "message": str(error.description) if hasattr(error, 'description') else "Authentication required"
        }), 401
    
    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
            "error": "Forbidden",
            "message": str(error.description) if hasattr(error, 'description') else "You don't have permission to access this resource"
        }), 403
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "error": "Not Found",
            "message": str(error.description) if hasattr(error, 'description') else "Resource not found"
        }), 404
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "error": "Method Not Allowed",
            "message": str(error.description) if hasattr(error, 'description') else "The method is not allowed for the requested URL"
        }), 405
    
    @app.errorhandler(429)
    def too_many_requests(error):
        return jsonify({
            "error": "Too Many Requests",
            "message": str(error.description) if hasattr(error, 'description') else "Rate limit exceeded"
        }), 429
    
    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "error": "Internal Server Error",
            "message": str(error.description) if hasattr(error, 'description') else "An unexpected error occurred"
        }), 500