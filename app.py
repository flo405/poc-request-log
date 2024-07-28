from flask import Flask, request, jsonify, send_from_directory
import json
import os

app = Flask(__name__)

# Directory to save request logs
LOG_DIR = "data"
LOG_FILE = os.path.join(LOG_DIR, "requests.log")

# Ensure the log directory exists
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

@app.before_request
def log_request():
    if request.endpoint != 'admin' and request.endpoint != 'index_html':
        # Record the request data
        token = request.headers.get('Authorization')  # Get the token from the Authorization header
        req_data = {
            'method': request.method,
            'path': request.path,
            'headers': dict(request.headers),
            'args': request.args.to_dict(),
            'form': request.form.to_dict(),
            'json': request.get_json() if request.is_json else None,
            'token': token  # Log the token
        }
        # Append the request data to the log file
        with open(LOG_FILE, 'a') as f:
            f.write(json.dumps(req_data) + '\n')

@app.route('/admin', methods=['GET'])
def admin():
    # Read the request logs
    logs = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r') as f:
            logs = [json.loads(line) for line in f]
    return jsonify(logs)

@app.route('/')
def index_html():
    return send_from_directory('', 'index.html')

@app.route('/example')
def example():
    return "This is an example endpoint. Your request is being recorded."

if __name__ == '__main__':
    app.run(debug=True)
