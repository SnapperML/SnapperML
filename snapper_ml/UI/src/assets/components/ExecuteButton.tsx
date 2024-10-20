import React, { useState, useRef } from "react";
import TerminalComponent from "./Terminal";

interface ExecuteButtonProps {
  yamlContent: string | null;
}

const ExecuteButton: React.FC<ExecuteButtonProps> = ({ yamlContent }) => {
  const [loading, setLoading] = useState(false);
  const [controller, setController] = useState<AbortController | null>(null);

  const terminalRef = useRef<any>(null);

  const handleExecute = async () => {
    if (loading) return;

    const cmd = "snapper-ml --config_file examples/experiments/svm.yaml";
    setLoading(true);

    terminalRef.current?.writeCommand(cmd);

    const newController = new AbortController();
    setController(newController);

    try {
      const response = await fetch("http://localhost:8000/execute_snapper_ml", {
        method: "POST",
        signal: newController.signal,
      });

      if (!response.ok) {
        throw new Error("Failed to execute the command.");
      }

      const reader = response.body?.getReader();
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
    } catch (error) {
      const typedError = error as Error;
      console.error("Error executing command:", typedError);

      // Only write the execution error if it's not an AbortError
      if (typedError.name !== "AbortError") {
        terminalRef.current?.writeOutput("Execution error!\n", false);
      }
    } finally {
      handleMlflowClick();
      setLoading(false);
      setController(null);
    }
  };

  const handleCancel = async () => {
    if (controller) {
      terminalRef.current?.writeOutput("Execution canceled!\n", false);
      try {
        // Call the cancel_snapper_ml API to terminate the ongoing process
        await fetch("http://localhost:8000/cancel_snapper_ml", {
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

export default ExecuteButton;
