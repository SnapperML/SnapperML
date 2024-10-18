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
          <div key={fieldKey} className="form-group" style={indentationStyle}>
            <label style={{ fontWeight: "bold" }}>{key}</label>{" "}
            <div className="nested-attributes">
              {renderAttributes(value, fieldKey, level + 1)}{" "}
              {/* Pass the prefix and increment level */}
            </div>
          </div>
        );
      } else {
        // Render input for non-object values
        return (
          <div key={fieldKey} className="form-group" style={indentationStyle}>
            <label>{key}</label> {/* Regular font weight for child labels */}
            <input
              type="text"
              className="form-control"
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
      <div style={{ display: "flex", gap: "10px", marginBottom: "10px" }}>
        {topLevelKeys.map((key) => (
          <div key={key} className="form-group">
            <label style={{ fontWeight: "bold" }}>{key}</label>
            <input
              type="text"
              className="form-control"
              style={{
                width: key === "name" || key === "kind" ? "200px" : "100px", // Increase width for name and kind
              }}
              value={
                typeof yamlData[key] === "string"
                  ? yamlData[key].replace(/(^"|"$)/g, "")
                  : String(yamlData[key])
              } // Remove outer quotes for display
            />
          </div>
        ))}
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
