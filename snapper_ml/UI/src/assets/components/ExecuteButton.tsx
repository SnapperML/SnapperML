import React, { useState } from "react";
import TerminalComponent from "./Terminal";

interface ExecuteButtonProps {
  yamlContent: string | null;
}

const ExecuteButton: React.FC<ExecuteButtonProps> = ({ yamlContent }) => {
  const [loading, setLoading] = useState(false);
  const [output, setOutput] = useState<string>("");
  const [command, setCommand] = useState<string>("");
  const [controller, setController] = useState<AbortController | null>(null); // Track abort controller

  const handleExecute = async () => {
    if (loading) return; // If already loading, prevent execution
    setCommand("snapper-ml --config_file examples/experiments/svm.yaml");
    setOutput("");
    setLoading(true);

    const newController = new AbortController(); // Create a new AbortController for this execution
    setController(newController); // Store the controller in state
    const timeoutId = setTimeout(() => {
      newController.abort(); // Abort if it exceeds 20 seconds
    }, 20000);

    try {
      const response = await fetch("http://localhost:5000/execute_snapper_ml", {
        method: "POST",
        signal: newController.signal, // Use the new controller's signal
      });

      clearTimeout(timeoutId);
      if (!response.ok) {
        throw new Error("Failed to execute the command.");
      }

      // Read the response stream
      const reader = response.body?.getReader();
      const decoder = new TextDecoder("utf-8");

      if (reader) {
        let done = false;
        while (!done) {
          const { value, done: doneReading } = await reader.read();
          done = doneReading;
          const chunk = decoder.decode(value);
          setOutput(chunk);
        }
      }
    } catch (error) {
      const typedError = error as Error; // Type the caught error

      console.error("Error executing command:", typedError);
      if (typedError.name === "AbortError") {
        setOutput("Execution canceled!"); // Specific message for abort errors
      } else {
        setOutput("Execution error!");
      }
    } finally {
      setLoading(false);
      setController(null); // Reset the controller
    }
  };

  const handleCancel = () => {
    if (controller) {
      controller.abort(); // Abort the fetch request
      setLoading(false); // Set loading to false
      setController(null); // Reset the controller
      setCommand("^C");
      setOutput("Execution canceled!"); // Update output message
    }
  };

  return (
    <div className="text-center mt-4">
      <button
        className="btn btn-primary"
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
        className="btn btn-danger ml-2"
        onClick={handleCancel}
        disabled={!loading} // Enable only if loading
      >
        Cancel
      </button>
      <br />
      <br />
      <TerminalComponent
        command={command}
        output={output}
        dataStream={loading}
      />
      <br />
    </div>
  );
};

export default ExecuteButton;
