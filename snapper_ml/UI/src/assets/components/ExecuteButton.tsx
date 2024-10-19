import React, { useState } from "react";
import axios, { AxiosError } from "axios";
import TerminalComponent from "./Terminal";

interface ExecuteResponse {
  command: string; // Add command to interface to capture the executed command
  output: string; // The command output
  logs: string; // The command logs
}

interface ExecuteButtonProps {
  yamlContent: string | null;
}

const ExecuteButton: React.FC<ExecuteButtonProps> = ({ yamlContent }) => {
  const [loading, setLoading] = useState(false);
  const [output, setOutput] = useState<string>("");
  const [command, setCommand] = useState<string>("");

  const handleExecute = async () => {
    setLoading(true);
    setOutput("");

    try {
      // Call the backend API to execute the command
      const response = await axios.post<ExecuteResponse>(
        "http://localhost:5000/execute_snapper_ml"
      );
      // Set the command and output from the backend response
      setCommand(response.data.command);
      setOutput(response.data.output);
    } catch (error) {
      const axiosError = error as AxiosError;
      console.error("Error executing command:", axiosError);
      setOutput("Execution failed!");
    } finally {
      setLoading(false);
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
      <br></br>
      <br></br>
      <TerminalComponent command={command} output={output} />
      <br></br>
    </div>
  );
};

export default ExecuteButton;
