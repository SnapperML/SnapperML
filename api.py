from flask import Flask, request, jsonify, Response, stream_with_context
from flask_cors import CORS
import subprocess
import logging
import os
import select
import threading
import uuid

app = Flask(__name__)

CORS(app, allow_headers=["Content-Type", "Authorization"],
          methods=["POST", "OPTIONS"])

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Dictionary to store the running processes keyed by a unique ID
processes = {}

# Mutex lock to prevent race conditions
process_lock = threading.Lock()

# Set the desired terminal size
os.environ["COLUMNS"] = "134"
os.environ["LINES"] = "24"

# Endpoint to execute a generic command
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
        logging.error(f"Error executing command: {e}")
        return jsonify({"output": str(e), "logs": str(e)}), 500

# Endpoint to execute snapper-ml within the virtual environment
@app.route('/execute_snapper_ml', methods=['POST'])
def execute_snapper_ml():
    try:
        # Set the desired terminal size
        os.environ["COLUMNS"] = "110"
        os.environ["LINES"] = "24"

        # Use 'stdbuf' to disable output buffering for the command
        command = "source .venv/bin/activate && unbuffer snapper-ml --config_file examples/experiments/svm.yaml"

        # Set text=True (universal_newlines=True) for real-time line-by-line output
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
                                   executable="/bin/bash", env=os.environ)

        # Store the process in the global dictionary with a unique ID
        process_id = request.remote_addr  # Use the client IP address as a unique identifier
        with process_lock:
            processes[process_id] = process

        def generate():
            while True:
                reads = [process.stdout, process.stderr]
                readable, _, _ = select.select(reads, [], [])

                for stream in readable:
                    output = stream.readline()
                    yield output
                if process.poll() is not None:
                    break

            # Clean up the process when done
            process.stdout.close()
            process.stderr.close()
            with process_lock:
                processes.pop(process_id, None)  # Remove the process from the global dictionary

        # Stream the output using Flask's Response
        return Response(stream_with_context(generate()), content_type='text/plain', mimetype='text/event-stream')

    except Exception as e:
        logging.error(f"Error executing snapper-ml: {e}")
        return jsonify({"output": str(e), "logs": str(e)}), 500

@app.route('/cancel_snapper_ml', methods=['POST'])
def cancel_snapper_ml():
    try:
        process_id = request.remote_addr  # Use the client IP address to identify the process
        with process_lock:
            process = processes.get(process_id)

        if process and process.poll() is None:  # Check if the process is running
            process.terminate() 
            with process_lock:
                processes.pop(process_id, None) 
            return jsonify({"status": "Process terminated successfully"}), 200
        else:
            return jsonify({"status": "No running process found"}), 404

    except Exception as e:
        return jsonify({"output": str(e), "logs": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=8000)
