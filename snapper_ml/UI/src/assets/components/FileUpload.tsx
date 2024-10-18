import React, { useState } from "react";
import YamlEditor from "./YamlEditor";

const FileUpload: React.FC = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

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

  return (
    <div className="container mt-4">
      <form>
        <div className="form-group">
          <label htmlFor="fileUpload">Subir archivo (.yaml, .yml):</label>
          <input
            type="file"
            className="form-control-file"
            id="fileUpload"
            accept=".yaml, .yml"
            onChange={handleFileUpload}
          />
        </div>
      </form>

      {/* Render YAML editor */}
      {selectedFile && <YamlEditor file={selectedFile} />}
    </div>
  );
};

export default FileUpload;
