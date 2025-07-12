from flask_cors import CORS

def configure_cors(app):
    """
    Configure CORS settings for the application
    """
    # Get CORS settings from config
    origins = app.config.get('CORS_ORIGINS', '*')
    
    # Setup CORS
    CORS(app, 
         resources={r"/api/*": {"origins": origins}},
         supports_credentials=True,
         allow_headers=[
             "Content-Type", 
             "Authorization", 
             "X-Requested-With",
             "Accept"
         ],
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    )