from flask import Flask, request, jsonify, Response, stream_with_context
from flask_cors import CORS
import subprocess
import logging
import os
import glob
import select
import threading

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

@app.route('/save_experiment_file', methods=['POST'])
def save_experiment_file():
    try:
        data = request.get_json()
        folder = data.get('folder')
        experiment_name = data.get('experiment_name')
        yaml_content = data.get('yamlContent')
        dataset = data.get('dataset')

        train_files = []
        for file_pattern in dataset['files']:
            glob_pattern = os.path.join(dataset['folder'], file_pattern)
            matched_files = glob.glob(glob_pattern)
            train_files.extend(matched_files)

        if not yaml_content or not experiment_name:
            return "Invalid data", 400

        # Ensure the directory exists
        os.makedirs(folder, exist_ok=True)

        # Save the YAML content
        file_path = os.path.join(folder, f'{experiment_name}.yaml')
        with open(file_path, 'w') as f:
            f.write(yaml_content)

        # Save the dataset content
        data_path = os.path.join(folder, 'datasets.txt')
        with open(data_path, 'w') as f:
            f.write(str(train_files))

        # Create soft symlinks for each train file with absolute paths
        for file_path in train_files:
            file_name = os.path.basename(file_path)
            symlink_path = os.path.join(folder, file_name)
            if not os.path.exists(symlink_path):
                os.symlink(os.path.abspath(file_path), symlink_path)

        return {"message": "YAML file created successfully", "file_path": file_path}, 200

    except Exception as e:
        return str(e), 500

# Endpoint to execute commands within the virtual environment
@app.route('/execute', methods=['POST'])
def execute():
    try:
        data = request.get_json()
        cmd = data.get('cmd')  # Get the cmd from the request body

        if not cmd:
            return "Invalid command", 400

        # Change the working directory to the parent of the parent directory
        parent_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        os.chdir(parent_directory)

        # Append "unbuffer" to the command received from the client
        command = f"unbuffer {cmd}"

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
                    if output:
                        yield output.decode()  # Decode output to a string
                if process.poll() is not None:  # Check if the process has completed
                    break

            # Clean up the process when done
            process.stdout.close()
            process.stderr.close()
            with process_lock:
                processes.pop(process_id, None)  # Remove the process from the global dictionary

            # Check if the process finished successfully
            exit_code = process.returncode
            success = exit_code == 0
            yield f"\nPROCESS_STATUS: {success}\n"

        # Stream the output using Flask's Response
        return Response(stream_with_context(generate()), content_type='text/plain', mimetype='text/event-stream')

    except Exception as e:
        logging.error(f"Error executing {cmd}: {e}")
        return jsonify({"output": str(e), "logs": str(e)}), 500
    

@app.route('/cancel', methods=['POST'])
def cancel():
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
