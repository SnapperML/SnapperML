import React, { useState, useRef } from "react";
import TerminalComponent from "./Terminal";
import yaml from "js-yaml"; // Import js-yaml to parse YAML content

interface ExecuteProps {
  yamlContent: string | null;
}

// Define the interface for parsed YAML content
interface ParsedYaml {
  name?: string;
  num_trials?: number;
  run?: string[];
}

const Execute: React.FC<ExecuteProps> = ({ yamlContent }) => {
  const [loading, setLoading] = useState(false);
  const [controller, setController] = useState<AbortController | null>(null);

  const terminalRef = useRef<any>(null);
  const wasCanceledRef = useRef(false); // Ref to track if execution was canceled

  const handleExecute = async () => {
    if (loading) return;

    if (!yamlContent) {
      console.error("No YAML content to execute.");
      return;
    }

    let parsedYaml: ParsedYaml;
    try {
      // Parse the YAML content to extract the "name" attribute
      parsedYaml = yaml.load(yamlContent) as ParsedYaml;
    } catch (e) {
      console.error("Failed to parse YAML content:", e);
      return;
    }

    const nameAttribute = parsedYaml?.name || "default_name";
    const now = new Date();
    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, "0");
    const day = String(now.getDate()).padStart(2, "0");
    const hours = String(now.getHours()).padStart(2, "0");
    const minutes = String(now.getMinutes()).padStart(2, "0");
    const seconds = String(now.getSeconds()).padStart(2, "0");

    // Format: YYYY-MM-DD_HH-MM-SS
    const currentDateTime = `${year}-${month}-${day}_${hours}-${minutes}-${seconds}`;
    const filename = `${currentDateTime}_${nameAttribute}.yaml`;

    setLoading(true);

    const newController = new AbortController();
    setController(newController);

    wasCanceledRef.current = false;
    let executionCompleted = false;

    try {
      // Step 1: Create the YAML experiment file file on the server
      const saveExperimentResponse = await fetch(
        "http://localhost:8000/save_experiment_file",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ yamlContent, filename }),
        }
      );

      if (!saveExperimentResponse.ok) {
        throw new Error("Failed to create YAML file.");
      }

      // Step 2: Execute the command to run snapper-ml with the created YAML file
      const cmd = `snapper-ml --config_file artifacts/experiments_config/${filename}`;
      terminalRef.current?.writeCommand(cmd);

      const executeResponse = await fetch("http://localhost:8000/execute", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ cmd }), // pass the command to the execute API
        signal: newController.signal,
      });

      if (!executeResponse.ok) {
        throw new Error("Failed to execute the command.");
      }

      const reader = executeResponse.body?.getReader();
      const decoder = new TextDecoder("utf-8");

      if (reader) {
        let done = false;
        while (!done) {
          const { value, done: doneReading } = await reader.read();
          done = doneReading;
          const chunk = decoder.decode(value);

          terminalRef.current?.writeOutput(chunk, !done);
        }
      }

      executionCompleted = true;
    } catch (error) {
      const typedError = error as Error;
      console.error("Error executing command:", typedError);

      if (typedError.name !== "AbortError") {
        terminalRef.current?.writeOutput("Execution error!\n", false);
      }
    } finally {
      setLoading(false);
      setController(null);

      if (executionCompleted && !wasCanceledRef.current) {
        handleMlflowClick();
      }
    }
  };

  const handleCancel = async () => {
    if (controller) {
      wasCanceledRef.current = true; // Mark execution as canceled
      terminalRef.current?.writeOutput("Execution canceled!\n", false);
      try {
        // Call the cancel_snapper_ml API to terminate the ongoing process
        await fetch("http://localhost:8000/cancel", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
        });

        // Abort the fetch request
        controller.abort();
        setLoading(false);
        setController(null);
      } catch (error) {
        console.error("Error canceling the process:", error);
        terminalRef.current?.writeOutput("Error canceling process!\n", false);
      }
    }
  };

  const handleMlflowClick = () => {
    window.open("http://localhost:5000/#/experiments/1", "_blank"); // Open in new tab
  };

  return (
    <div className="text-center mt-4">
      <button
        className="btn btn-light ml-2 mlflowButton"
        onClick={handleMlflowClick}
      >
        <img src="MLflow-Logo.svg" alt="Mlflow" style={{ width: "50px" }} />
      </button>
      <button
        className="btn btn-primary executeButton"
        onClick={handleExecute}
        disabled={loading}
      >
        {loading ? (
          <span
            className="spinner-border spinner-border-sm"
            role="status"
            aria-hidden="true"
          ></span>
        ) : (
          "Execute"
        )}
      </button>
      <button
        className="btn btn-danger ml-2 cancelButton"
        onClick={handleCancel}
        disabled={!loading}
      >
        Cancel
      </button>
      <br />
      <br />
      <TerminalComponent ref={terminalRef} command="" output="" />
      <br />
    </div>
  );
};

export default Execute;
