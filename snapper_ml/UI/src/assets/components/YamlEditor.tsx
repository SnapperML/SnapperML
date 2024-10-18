import React, { useState, useEffect } from "react";
import * as yaml from "js-yaml";
import Editor from "react-simple-code-editor";
import Prism from "prismjs";
import "prismjs/components/prism-yaml";
import "prismjs/themes/prism.css"; // Optional: Choose a theme for the editor
import YamlAttributes from "./YamlAttributes";
import ExecuteButton from "./ExecuteButton";

interface YamlEditorProps {
  file: File | null;
}

const YamlEditor: React.FC<YamlEditorProps> = ({ file }) => {
  const [yamlContent, setYamlContent] = useState<string | null>(null);
  const [parsedYaml, setParsedYaml] = useState<object | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        const text = e.target?.result as string;
        setYamlContent(text);
        try {
          const parsed = yaml.load(text) as object;
          setParsedYaml(parsed);
        } catch (err) {
          setError("Error al parsear el archivo YAML.");
          setParsedYaml(null);
        }
      };
      reader.readAsText(file);
    }
  }, [file]);

  const handleYamlChange = (updatedYaml: string) => {
    setYamlContent(updatedYaml);

    try {
      const parsed = yaml.load(updatedYaml) as object;
      setParsedYaml(parsed);
      setError(null);
    } catch (err) {
      setError("Error al parsear el archivo YAML.");
      setParsedYaml(null);
    }
  };

  // Function to highlight YAML syntax
  const highlightWithPrism = (code: string) =>
    Prism.highlight(code, Prism.languages.yaml, "yaml");

  return (
    <div className="container mt-4">
      <div className="row">
        {/* Left side - YAML editor with syntax highlighting */}
        <div className="col-md-6">
          <h5>YAML Editor:</h5>
          <Editor
            value={yamlContent || ""}
            onValueChange={handleYamlChange}
            highlight={highlightWithPrism}
            padding={10}
            style={{
              fontFamily: '"Fira code", "Fira Mono", monospace',
              minHeight: "400px",
              backgroundColor: "#f5f5f5",
              borderRadius: "4px",
              overflow: "auto",
            }}
          />
        </div>

        {/* Right side - Editable YAML attributes */}
        <div className="col-md-6">
          <h5>Preview atributes:</h5>
          {parsedYaml && <YamlAttributes yamlData={parsedYaml} />}
        </div>
      </div>
      <ExecuteButton yamlContent={yamlContent} />

      {/* Error Alert */}
      {error && (
        <div className="alert alert-danger mt-3" role="alert">
          {error}
        </div>
      )}
    </div>
  );
};

export default YamlEditor;
