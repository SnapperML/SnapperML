from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import logging

app = Flask(__name__)

CORS(app, allow_headers=["Content-Type", "Authorization"],
          methods=["POST", "OPTIONS"])

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Endpoint to execute a command
@app.route('/execute', methods=['POST'])
def execute_command():
    try:
        # Get the command from the request JSON
        data = request.get_json() or {}
        command = data.get("command", "")

        if not command:
            return jsonify({"output": "", "logs": "No command provided"}), 200

        # Run the provided command

        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        # Check if there is an error in stderr
        if stderr:
            logging.info(f"output {stderr}")
            return jsonify({"command": command, "output": stderr.decode("utf-8"), "logs": stderr.decode("utf-8")}), 200

        # Return the output and logs (for this example, logs will be empty)
        return jsonify({"command": command, "output": stdout.decode("utf-8"), "logs": ""}), 200
    except Exception as e:
        return jsonify({"output": str(e), "logs": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
