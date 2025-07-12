from flask import Flask, render_template, jsonify, request, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__, static_folder='../frontend/build', static_url_path='/')
CORS(app)

# Add other imports and configurations here

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

# Add your API routes here
@app.route('/api/health')
def health_check():
    return jsonify({"status": "ok"})

# Catch-all route to handle frontend routing
@app.errorhandler(404)
def not_found(e):
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')