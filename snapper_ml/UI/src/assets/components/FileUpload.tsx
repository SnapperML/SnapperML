import React, { useState, useRef } from "react";
import YamlEditor from "./YamlEditor";
import "bootstrap/dist/css/bootstrap.min.css";

const FileUpload: React.FC = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [error, setError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      const fileExtension = file.name.split(".").pop()?.toLowerCase();
      if (fileExtension === "yaml" || fileExtension === "yml") {
        setSelectedFile(file);
        setError(null); // Clear any previous error
      } else {
        setError(
          "Unsupported file format. Please upload a .yaml or .yml file."
        );
        setSelectedFile(null);
      }
    }
  };

  const handleButtonClick = () => {
    fileInputRef.current?.click();
  };

  return (
    <main className="container mt-4">
      <header className="mb-4 text-center">
        <h1 className="header-title">SnapperML</h1>
        <p className="header-subtitle">Make your experiments reproducible</p>
      </header>

      <div className="d-flex justify-content-center">
        <div className="text-center">
          <button
            type="button"
            className="btn btn-primary btn-lg upload-button"
            onClick={handleButtonClick}
            aria-label="Upload YAML File"
          >
            Upload YAML File
          </button>
          <input
            type="file"
            accept=".yaml, .yml"
            ref={fileInputRef}
            onChange={handleFileUpload}
            className="d-none"
          />
          {error && <p className="text-danger mt-2">{error}</p>}
        </div>
      </div>

      {selectedFile && <YamlEditor file={selectedFile} />}
    </main>
  );
};

export default FileUpload;
