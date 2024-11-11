import React from "react";

interface YamlAttributesProps {
  yamlData: Record<string, any>; // Use Record for more flexibility with values
}

const YamlAttributes: React.FC<YamlAttributesProps> = ({ yamlData }) => {
  // Recursive function to render nested attributes
  const renderAttributes = (
    data: Record<string, any>,
    prefix = "",
    level = 0
  ) => {
    const indentationStyle = { paddingLeft: `${level * 20}px` }; // Indent based on the level

    return Object.entries(data).map(([key, value]) => {
      const fieldKey = prefix ? `${prefix}.${key}` : key; // Create a prefixed key for nested attributes
      const inputId = `input-${fieldKey.replace(/\./g, "-")}`; // Generate a unique ID for each input

      // Skip rendering of top-level keys in the nested rendering
      if (["name", "kind", "num_trials", "sampler"].includes(key)) {
        return null; // Skip rendering these top-level keys
      }

      if (
        typeof value === "object" &&
        value !== null &&
        !Array.isArray(value)
      ) {
        // If the value is an object, render it recursively
        return (
          <div key={fieldKey} className="form-group nested-attributes">
            <label className="bold" htmlFor={inputId}>
              {key}
            </label>
            <div>{renderAttributes(value, fieldKey, level + 1)}</div>
          </div>
        );
      } else {
        // Render input for non-object values
        return (
          <div key={fieldKey} className="form-group" style={indentationStyle}>
            <label className="regular" htmlFor={inputId}>
              {key}
            </label>
            <input
              type="text"
              id={inputId} // Set the id for the input
              className="form-control custom-input"
              readOnly
              value={
                typeof value === "string"
                  ? value.replace(/(^"|"$)/g, "")
                  : String(value)
              }
            />
          </div>
        );
      }
    });
  };

  const renderTopLevelAttributes = () => {
    const topLevelKeys = ["name", "kind", "num_trials", "sampler"]; // List of top-level keys to display inline
    return (
      <div className="top-level-attributes">
        {topLevelKeys.map((key) => {
          const inputId = `input-${key}`; // Generate a unique ID for each top-level input
          return (
            <div key={key} className="form-group">
              <label className="bold" htmlFor={inputId}>
                {key}
              </label>
              <input
                type="text"
                id={inputId} // Set the id for the input
                className={`form-control custom-input ${
                  key === "name" || key === "kind" ? "name-kind" : "num-sampler"
                }`} // Use custom class
                readOnly
                value={
                  typeof yamlData[key] === "string"
                    ? yamlData[key].replace(/(^"|"$)/g, "")
                    : String(yamlData[key])
                }
              />
            </div>
          );
        })}
      </div>
    );
  };

  return (
    <div>
      {renderTopLevelAttributes()} {/* Render top-level attributes inline */}
      {renderAttributes(yamlData, "", 1)}{" "}
      {/* Render other attributes with indentation */}
    </div>
  );
};

export default YamlAttributes;
