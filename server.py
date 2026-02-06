from flask import Flask, request, jsonify, send_from_directory
from uglier import execute_block, variables, functions, classes
import sys
import io
import traceback
import os

app = Flask(__name__, static_folder='.')

@app.route("/")
def index():
    return send_from_directory('.', 'index.html')

@app.route("/run", methods=["POST"])
def run_code():
    code = request.json.get("code", "")
    output = []
    
    # Capture stdout
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    
    try:
        # Split code into lines and execute
        lines = code.split('\n')
        execute_block(lines)
        
        # Get captured output
        output_text = sys.stdout.getvalue()
        
    except Exception as e:
        # Get detailed error information
        error_details = traceback.format_exc()
        output_text = f"Error: {str(e)}\n\n{error_details}"
    
    finally:
        # Restore stdout
        sys.stdout = old_stdout
    
    return jsonify({
        "output": output_text,
        "variables": {k: str(v) for k, v in variables.items()},
        "functions": list(functions.keys()),
        "classes": list(classes.keys())
    })

@app.route("/reset", methods=["POST"])
def reset():
    """Reset the interpreter state"""
    variables.clear()
    functions.clear()
    classes.clear()
    return jsonify({"status": "reset"})

@app.route("/state", methods=["GET"])
def get_state():
    """Get current interpreter state"""
    return jsonify({
        "variables": {k: str(v) for k, v in variables.items()},
        "functions": list(functions.keys()),
        "classes": list(classes.keys())
    })

@app.route("/health")
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy"})

if __name__ == "__main__":
    # Get port from environment variable (Railway sets this)
    port = int(os.environ.get("PORT", 5000))
    
    print(f"Starting Uglier web server on port {port}...")
    print(f"Server will be available at http://0.0.0.0:{port}")
    
    # Run with proper configuration for production
    app.run(
        host="0.0.0.0",
        port=port,
        debug=False,  # Disable debug mode in production
        threaded=True  # Enable threading for better performance
    )

