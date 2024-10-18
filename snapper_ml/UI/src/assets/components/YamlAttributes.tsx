import React from "react";

interface YamlAttributesProps {
  yamlData: object;
  onAttributeChange: (updatedYaml: object) => void;
}

const YamlAttributes: React.FC<YamlAttributesProps> = ({
  yamlData,
  onAttributeChange,
}) => {
  const handleInputChange = (key: string, value: string) => {
    const updatedYaml = { ...yamlData, [key]: value };
    onAttributeChange(updatedYaml);
  };

  return (
    <div>
      {Object.entries(yamlData).map(([key, value]) => (
        <div key={key} className="form-group">
          <label>{key}</label>
          <input
            type="text"
            className="form-control"
            value={String(value)}
            onChange={(e) => handleInputChange(key, e.target.value)}
          />
        </div>
      ))}
    </div>
  );
};

export default YamlAttributes;
