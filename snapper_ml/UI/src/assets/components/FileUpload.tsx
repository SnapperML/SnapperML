// FileUpload.tsx
import React, { useState, useRef } from "react";
import YamlEditor from "./YamlEditor";
import "bootstrap/dist/css/bootstrap.min.css"; // Ensure Bootstrap is imported

const FileUpload: React.FC = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      const fileExtension = file.name.split(".").pop()?.toLowerCase();
      if (fileExtension === "yaml" || fileExtension === "yml") {
        setSelectedFile(file);
      } else {
        console.error(
          "Formato de archivo no soportado. Por favor sube un archivo .yaml o .yml"
        );
        setSelectedFile(null);
      }
    }
  };

  const handleButtonClick = () => {
    fileInputRef.current?.click();
  };

  return (
    <div className="container mt-4">
      <div className="header-section mb-4 text-center">
        <h1 className="header-title">SnapperML</h1>
        <p className="header-subtitle">Make your experiments reproducible</p>
      </div>

      <div className="d-flex justify-content-center">
        <div className="text-center">
          <button
            type="button"
            className="btn btn-primary btn-lg upload-button"
            onClick={handleButtonClick}
          >
            Upload YAML File
          </button>
          <input
            type="file"
            accept=".yaml, .yml"
            ref={fileInputRef}
            onChange={handleFileUpload}
            className="hidden-file-input"
          />
        </div>
      </div>

      {/* Render YAML editor */}
      {selectedFile && <YamlEditor file={selectedFile} />}
    </div>
  );
};

export default FileUpload;
