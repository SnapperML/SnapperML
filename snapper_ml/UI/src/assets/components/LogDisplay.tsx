import React from "react";

interface LogDisplayProps {
  output: string;
  logs: string;
}

const LogDisplay: React.FC<LogDisplayProps> = ({ output, logs }) => {
  return (
    <div className="mt-4">
      <h5>Command Output:</h5>
      <pre>{output}</pre>

      <h5>Logs:</h5>
      <pre>{logs}</pre>
    </div>
  );
};

export default LogDisplay;
