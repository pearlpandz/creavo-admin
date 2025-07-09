import React from "react";
import {
  FaBold,
  FaItalic,
  FaUnderline,
  FaStrikethrough,
  FaAlignLeft,
  FaAlignCenter,
  FaAlignRight,
  FaAlignJustify,
} from "react-icons/fa";

const fontFamilies = [
  "Arial",
  "Verdana",
  "Helvetica",
  "Tahoma",
  "Trebuchet MS",
  "Times New Roman",
  "Georgia",
  "Courier New",
  "Lucida Console",
  "Impact",
  "Comic Sans MS",
];

const sliderStyle = { width: "100px", marginLeft: "10px" };
const sectionTitleStyle = {
  fontWeight: "bold",
  fontSize: "14px" /* Increased font size */,
  letterSpacing: "1px",
  margin: "20px 0 10px 0" /* Adjusted margin for more space */,
  border: "none",
  background: "none",
  padding: 0,
  color: "#222",
};

const rowStyle = {
  display: "flex",
  alignItems: "center",
  marginBottom: "8px" /* Increased bottom margin for more vertical space */,
  gap: "10px" /* Increased gap for more horizontal space */,
};

const labelStyle = {
  minWidth: "40px" /* Adjusted min-width for better alignment */,
  fontSize: "13px" /* Increased font size */,
  color: "#444",
};

const inputStyle = {
  width: "50px" /* Slightly increased width */,
  fontSize: "13px" /* Increased font size */,
  padding: "4px 6px" /* Increased padding */,
  border: "1px solid #ccc",
  borderRadius: "4px",
};

const PropertiesPanel = ({
  selectedElement,
  updateElement,
  // canvasBackgroundColor,
  // setCanvasBackgroundColor,
  templateObj,
  setTemplateObj,
  mode,
}) => {
  const handleChange = (e) => {
    if (mode === "view") return;
    const { name, value, type } = e.target;

    if (name === "fillType") {
      let newProperties = { [name]: value };
      if (value === "linear-gradient") {
        newProperties = {
          ...newProperties,
          fillLinearGradientColorStops: [0, "#ff0000", 1, "#0000ff"],
          fillLinearGradientStartPoint: { x: 0, y: 0 },
          fillLinearGradientEndPoint: { x: 100, y: 100 },
        };
      } else if (value === "radial-gradient") {
        newProperties = {
          ...newProperties,
          fillRadialGradientColorStops: [0, "#ff0000", 1, "#0000ff"],
          fillRadialGradientStartPoint: { x: 0, y: 0 },
          fillRadialGradientEndPoint: { x: 50, y: 50 },
          fillRadialGradientStartRadius: 0,
          fillRadialGradientEndRadius: 50,
        };
      } else if (value === "solid") {
        newProperties = {
          ...newProperties,
          fill: "#000000", // Default solid color
        };
      }
      updateElement(selectedElement.id, newProperties);
    } else if (type === "number") {
      updateElement(selectedElement.id, {
        [name]: e?.target?.valueAsNumber ?? Number(value),
      });
    } else {
      updateElement(selectedElement.id, { [name]: value });
    }
  };

  const handleColorChange = (color, name) => {
    if (mode === "view") return;
    updateElement(selectedElement.id, { [name]: color });
  };

  const handleTemplateChange = (e) => {
    if (mode === "view") return;
    const { name, value } = e.target;
    setTemplateObj((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  return (
    <div
      className="properties-panel"
      style={{
        fontFamily: "inherit",
        fontSize: "13px" /* Adjusted font size */,
        padding: "12px 10px" /* Adjusted padding */,
        borderRight: "1px solid #ddd",
        height: "100%",
        overflowY: "auto",
      }}
    >
      {/* TEMPLATE PROPERTIES SECTION */}
      <div style={sectionTitleStyle}>TEMPLATE PROPERTIES</div>
      <div style={rowStyle}>
        <span style={{ ...labelStyle, minWidth: '100px' }}>TEMPLATE NAME</span>
        <input
          type="text"
          name="name"
          value={templateObj?.name}
          onChange={handleTemplateChange}
          style={{ ...inputStyle, width: "120px" }}
        />
      </div>
      <div style={rowStyle}>
        <span style={{ ...labelStyle, minWidth: '100px' }}>CATEGORY</span>
        <select
          name="category"
          value={templateObj?.category}
          onChange={handleTemplateChange}
          style={{ ...inputStyle, width: "120px" }}
        >
          <option value="regular">Regular</option>
          <option value="political">Political</option>
          <option value="product">Product</option>
        </select>
      </div>
      <div style={rowStyle}>
        <span style={{ ...labelStyle, minWidth: '100px' }}>STATE</span>
        <select
          name="state"
          value={templateObj?.state}
          onChange={handleTemplateChange}
          style={{ ...inputStyle, width: "120px" }}
        >
          <option value="draft">Draft</option>
          <option value="production">Production</option>
        </select>
      </div>

      {selectedElement && (
        <>
          {/* TRANSFORM SECTION */}
          <div style={sectionTitleStyle}>TRANSFORM</div>
          <div style={{ ...rowStyle, marginBottom: "2px" }}>
            <span style={labelStyle}>W</span>
            <input
              type="number"
              name="width"
              value={selectedElement.width}
              onChange={handleChange}
              style={inputStyle}
            />
            <span style={labelStyle}>X</span>
            <input
              type="number"
              name="x"
              value={selectedElement.x}
              onChange={handleChange}
              style={inputStyle}
            />
          </div>
          <div style={rowStyle}>
            <span style={labelStyle}>H</span>
            <input
              type="number"
              name="height"
              value={selectedElement.height}
              onChange={handleChange}
              style={inputStyle}
            />
            <span style={labelStyle}>Y</span>
            <input
              type="number"
              name="y"
              value={selectedElement.y}
              onChange={handleChange}
              style={inputStyle}
            />
          </div>
          <div style={rowStyle}>
            <span style={labelStyle}>ROTATION</span>
            <input
              type="number"
              name="rotation"
              value={selectedElement.rotation || 0}
              onChange={handleChange}
              style={inputStyle}
            />
          </div>

          {/* APPEARANCE SECTION */}
          <div style={sectionTitleStyle}>APPEARANCE</div>
          {selectedElement.type === "text" && (
            <>
              <div style={rowStyle}>
                <span style={labelStyle}>FONT SIZE</span>
                <input
                  type="number"
                  name="fontSize"
                  value={selectedElement.fontSize}
                  onChange={handleChange}
                  style={inputStyle}
                />
              </div>
              <div style={rowStyle}>
                <span style={labelStyle}>PADDING</span>
                <input
                  type="number"
                  name="padding"
                  value={selectedElement.padding}
                  onChange={handleChange}
                  style={inputStyle}
                />
              </div>
              <div style={rowStyle}>
                <span style={labelStyle}>FONT FAMILY</span>
                <select
                  name="fontFamily"
                  value={selectedElement.fontFamily}
                  onChange={handleChange}
                  style={{ ...inputStyle, width: "120px" }}
                >
                  {fontFamilies.map((font) => (
                    <option key={font} value={font}>
                      {font}
                    </option>
                  ))}
                </select>
              </div>
              <div style={rowStyle}>
                <span style={labelStyle}>LINE HEIGHT</span>
                <input
                  type="number"
                  name="lineHeight"
                  value={selectedElement.lineHeight}
                  onChange={handleChange}
                  style={inputStyle}
                  step="0.1"
                />
              </div>
              <div style={rowStyle}>
                <span style={labelStyle}>TEXT STYLE</span>
                <div style={{ display: "flex", gap: "4px" }}>
                  <button
                    style={{
                      ...inputStyle,
                      width: "auto",
                      padding: "4px 8px",
                      cursor: "pointer",
                      backgroundColor:
                        selectedElement.fontWeight === "bold" ? "#eee" : "#fff",
                    }}
                    onClick={() =>
                      updateElement(selectedElement.id, {
                        fontWeight:
                          selectedElement.fontWeight === "bold"
                            ? "normal"
                            : "bold",
                      })
                    }
                  >
                    <FaBold />
                  </button>
                  <button
                    style={{
                      ...inputStyle,
                      width: "auto",
                      padding: "4px 8px",
                      cursor: "pointer",
                      backgroundColor:
                        selectedElement.fontStyle === "italic"
                          ? "#eee"
                          : "#fff",
                    }}
                    onClick={() =>
                      updateElement(selectedElement.id, {
                        fontStyle:
                          selectedElement.fontStyle === "italic"
                            ? "normal"
                            : "italic",
                      })
                    }
                  >
                    <FaItalic />
                  </button>
                  <button
                    style={{
                      ...inputStyle,
                      width: "auto",
                      padding: "4px 8px",
                      cursor: "pointer",
                      backgroundColor:
                        selectedElement.textDecoration === "underline"
                          ? "#eee"
                          : "#fff",
                    }}
                    onClick={() =>
                      updateElement(selectedElement.id, {
                        textDecoration:
                          selectedElement.textDecoration === "underline"
                            ? "none"
                            : "underline",
                      })
                    }
                  >
                    <FaUnderline />
                  </button>
                  <button
                    style={{
                      ...inputStyle,
                      width: "auto",
                      padding: "4px 8px",
                      cursor: "pointer",
                      backgroundColor:
                        selectedElement.textDecoration === "line-through"
                          ? "#eee"
                          : "#fff",
                    }}
                    onClick={() =>
                      updateElement(selectedElement.id, {
                        textDecoration:
                          selectedElement.textDecoration === "line-through"
                            ? "none"
                            : "line-through",
                      })
                    }
                  >
                    <FaStrikethrough />
                  </button>
                </div>
              </div>
              <div style={rowStyle}>
                <span style={labelStyle}>ALIGNMENT</span>
                <div style={{ display: "flex", gap: "4px" }}>
                  <button
                    style={{
                      ...inputStyle,
                      width: "auto",
                      padding: "4px 8px",
                      cursor: "pointer",
                      backgroundColor:
                        selectedElement.textAlign === "left" ? "#eee" : "#fff",
                    }}
                    onClick={() =>
                      updateElement(selectedElement.id, { textAlign: "left" })
                    }
                  >
                    <FaAlignLeft />
                  </button>
                  <button
                    style={{
                      ...inputStyle,
                      width: "auto",
                      padding: "4px 8px",
                      cursor: "pointer",
                      backgroundColor:
                        selectedElement.textAlign === "center"
                          ? "#eee"
                          : "#fff",
                    }}
                    onClick={() =>
                      updateElement(selectedElement.id, { textAlign: "center" })
                    }
                  >
                    <FaAlignCenter />
                  </button>
                  <button
                    style={{
                      ...inputStyle,
                      width: "auto",
                      padding: "4px 8px",
                      cursor: "pointer",
                      backgroundColor:
                        selectedElement.textAlign === "right" ? "#eee" : "#fff",
                    }}
                    onClick={() =>
                      updateElement(selectedElement.id, { textAlign: "right" })
                    }
                  >
                    <FaAlignRight />
                  </button>
                  <button
                    style={{
                      ...inputStyle,
                      width: "auto",
                      padding: "4px 8px",
                      cursor: "pointer",
                      backgroundColor:
                        selectedElement.textAlign === "justify"
                          ? "#eee"
                          : "#fff",
                    }}
                    onClick={() =>
                      updateElement(selectedElement.id, {
                        textAlign: "justify",
                      })
                    }
                  >
                    <FaAlignJustify />
                  </button>
                </div>
              </div>
            </>
          )}
          <div style={rowStyle}>
            <span style={labelStyle}>FILL TYPE</span>
            <select
              name="fillType"
              value={selectedElement.fillType || "solid"}
              onChange={handleChange}
              style={{ ...inputStyle, width: "120px" }}
            >
              <option value="solid">Solid</option>
              <option value="linear-gradient">Linear Gradient</option>
              <option value="radial-gradient">Radial Gradient</option>
            </select>
          </div>
          {(selectedElement.fillType === "solid" || !selectedElement.fillType) && (
            <div style={rowStyle}>
              <span style={labelStyle}>FILL COLOR</span>
              <input
                type="color"
                value={selectedElement.fill}
                onChange={(e) => handleColorChange(e.target.value, "fill")}
              />
            </div>
          )}
          {selectedElement.fillType === "linear-gradient" && (
            <>
              <div style={rowStyle}>
                <span style={labelStyle}>GRADIENT COLOR 1</span>
                <input
                  type="color"
                  value={selectedElement.fillLinearGradientColorStops[1]}
                  onChange={(e) => {
                    const newStops = [
                      selectedElement.fillLinearGradientColorStops[0],
                      e.target.value,
                      selectedElement.fillLinearGradientColorStops[2],
                      selectedElement.fillLinearGradientColorStops[3],
                    ];
                    updateElement(selectedElement.id, {
                      fillLinearGradientColorStops: newStops,
                    });
                  }}
                />
              </div>
              <div style={rowStyle}>
                <span style={labelStyle}>GRADIENT COLOR 2</span>
                <input
                  type="color"
                  value={selectedElement.fillLinearGradientColorStops[3]}
                  onChange={(e) => {
                    const newStops = [
                      selectedElement.fillLinearGradientColorStops[0],
                      selectedElement.fillLinearGradientColorStops[1],
                      selectedElement.fillLinearGradientColorStops[2],
                      e.target.value,
                    ];
                    updateElement(selectedElement.id, {
                      fillLinearGradientColorStops: newStops,
                    });
                  }}
                />
              </div>
              <div style={rowStyle}>
                <span style={labelStyle}>START X</span>
                <input
                  type="number"
                  name="fillLinearGradientStartPoint.x"
                  value={selectedElement.fillLinearGradientStartPoint.x}
                  onChange={(e) =>
                    updateElement(selectedElement.id, {
                      fillLinearGradientStartPoint: {
                        ...selectedElement.fillLinearGradientStartPoint,
                        x: e.target.valueAsNumber,
                      },
                    })
                  }
                  style={inputStyle}
                />
                <span style={labelStyle}>START Y</span>
                <input
                  type="number"
                  name="fillLinearGradientStartPoint.y"
                  value={selectedElement.fillLinearGradientStartPoint.y}
                  onChange={(e) =>
                    updateElement(selectedElement.id, {
                      fillLinearGradientStartPoint: {
                        ...selectedElement.fillLinearGradientStartPoint,
                        y: e.target.valueAsNumber,
                      },
                    })
                  }
                  style={inputStyle}
                />
              </div>
              <div style={rowStyle}>
                <span style={labelStyle}>END X</span>
                <input
                  type="number"
                  name="fillLinearGradientEndPoint.x"
                  value={selectedElement.fillLinearGradientEndPoint.x}
                  onChange={(e) =>
                    updateElement(selectedElement.id, {
                      fillLinearGradientEndPoint: {
                        ...selectedElement.fillLinearGradientEndPoint,
                        x: e.target.valueAsNumber,
                      },
                    })
                  }
                  style={inputStyle}
                />
                <span style={labelStyle}>END Y</span>
                <input
                  type="number"
                  name="fillLinearGradientEndPoint.y"
                  value={selectedElement.fillLinearGradientEndPoint.y}
                  onChange={(e) =>
                    updateElement(selectedElement.id, {
                      fillLinearGradientEndPoint: {
                        ...selectedElement.fillLinearGradientEndPoint,
                        y: e.target.valueAsNumber,
                      },
                    })
                  }
                  style={inputStyle}
                />
              </div>
            </>
          )}
          {selectedElement.fillType === "radial-gradient" && (
            <>
              <div style={rowStyle}>
                <span style={labelStyle}>GRADIENT COLOR 1</span>
                <input
                  type="color"
                  value={selectedElement.fillRadialGradientColorStops[1]}
                  onChange={(e) => {
                    const newStops = [
                      selectedElement.fillRadialGradientColorStops[0],
                      e.target.value,
                      selectedElement.fillRadialGradientColorStops[2],
                      selectedElement.fillRadialGradientColorStops[3],
                    ];
                    updateElement(selectedElement.id, {
                      fillRadialGradientColorStops: newStops,
                    });
                  }}
                />
              </div>
              <div style={rowStyle}>
                <span style={labelStyle}>GRADIENT COLOR 2</span>
                <input
                  type="color"
                  value={selectedElement.fillRadialGradientColorStops[3]}
                  onChange={(e) => {
                    const newStops = [
                      selectedElement.fillRadialGradientColorStops[0],
                      selectedElement.fillRadialGradientColorStops[1],
                      selectedElement.fillRadialGradientColorStops[2],
                      e.target.value,
                    ];
                    updateElement(selectedElement.id, {
                      fillRadialGradientColorStops: newStops,
                    });
                  }}
                />
              </div>
              <div style={rowStyle}>
                <span style={labelStyle}>START X</span>
                <input
                  type="number"
                  name="fillRadialGradientStartPoint.x"
                  value={selectedElement.fillRadialGradientStartPoint.x}
                  onChange={(e) =>
                    updateElement(selectedElement.id, {
                      fillRadialGradientStartPoint: {
                        ...selectedElement.fillRadialGradientStartPoint,
                        x: e.target.valueAsNumber,
                      },
                    })
                  }
                  style={inputStyle}
                />
                <span style={labelStyle}>START Y</span>
                <input
                  type="number"
                  name="fillRadialGradientStartPoint.y"
                  value={selectedElement.fillRadialGradientStartPoint.y}
                  onChange={(e) =>
                    updateElement(selectedElement.id, {
                      fillRadialGradientStartPoint: {
                        ...selectedElement.fillRadialGradientStartPoint,
                        y: e.target.valueAsNumber,
                      },
                    })
                  }
                  style={inputStyle}
                />
              </div>
              <div style={rowStyle}>
                <span style={labelStyle}>END X</span>
                <input
                  type="number"
                  name="fillRadialGradientEndPoint.x"
                  value={selectedElement.fillRadialGradientEndPoint.x}
                  onChange={(e) =>
                    updateElement(selectedElement.id, {
                      fillRadialGradientEndPoint: {
                        ...selectedElement.fillRadialGradientEndPoint,
                        x: e.target.valueAsNumber,
                      },
                    })
                  }
                  style={inputStyle}
                />
                <span style={labelStyle}>END Y</span>
                <input
                  type="number"
                  name="fillRadialGradientEndPoint.y"
                  value={selectedElement.fillRadialGradientEndPoint.y}
                  onChange={(e) =>
                    updateElement(selectedElement.id, {
                      fillRadialGradientEndPoint: {
                        ...selectedElement.fillRadialGradientEndPoint,
                        y: e.target.valueAsNumber,
                      },
                    })
                  }
                  style={inputStyle}
                />
              </div>
              <div style={rowStyle}>
                <span style={labelStyle}>START RADIUS</span>
                <input
                  type="number"
                  name="fillRadialGradientStartRadius"
                  value={selectedElement.fillRadialGradientStartRadius}
                  onChange={handleChange}
                  style={inputStyle}
                />
              </div>
              <div style={rowStyle}>
                <span style={labelStyle}>END RADIUS</span>
                <input
                  type="number"
                  name="fillRadialGradientEndRadius"
                  value={selectedElement.fillRadialGradientEndRadius}
                  onChange={handleChange}
                  style={inputStyle}
                />
              </div>
            </>
          )}
          <div style={rowStyle}>
            <span style={labelStyle}>STROKE</span>
            <input
              type="color"
              value={selectedElement.stroke}
              onChange={(e) => handleColorChange(e.target.value, "stroke")}
            />
            <input
              type="number"
              name="strokeWidth"
              value={selectedElement.strokeWidth}
              onChange={handleChange}
              style={inputStyle}
            />
          </div>
          <div style={rowStyle}>
            <span style={labelStyle}>COLOR</span>
            <input
              type="color"
              value={selectedElement.color}
              onChange={(e) => handleColorChange(e.target.value, "color")}
            />
          </div>
          {(selectedElement.type === "rect" ||
            selectedElement.type === "square") && (
              <>
                <div style={rowStyle}>
                  <span style={labelStyle}>RADIUS</span>
                  <span
                    style={{
                      fontSize: "13px" /* Updated font size */,
                      color: "#888",
                      marginLeft: "8px",
                      flexShrink: 0,
                    }}
                  >
                    TL
                  </span>
                  <input
                    type="number"
                    name="cornerRadiusTopLeft"
                    value={selectedElement.cornerRadiusTopLeft || 0}
                    onChange={handleChange}
                    style={inputStyle}
                  />
                  <span
                    style={{
                      fontSize: "13px" /* Updated font size */,
                      color: "#888",
                      flexShrink: 0,
                    }}
                  >
                    TR
                  </span>
                  <input
                    type="number"
                    name="cornerRadiusTopRight"
                    value={selectedElement.cornerRadiusTopRight || 0}
                    onChange={handleChange}
                    style={inputStyle}
                  />
                </div>
                <div style={rowStyle}>
                  <span style={{ minWidth: "40px" }}></span>
                  <span
                    style={{
                      fontSize: "13px" /* Updated font size */,
                      color: "#888",
                      marginLeft: "8px",
                      flexShrink: 0,
                    }}
                  >
                    BL
                  </span>
                  <input
                    type="number"
                    name="cornerRadiusBottomLeft"
                    value={selectedElement.cornerRadiusBottomLeft || 0}
                    onChange={handleChange}
                    style={inputStyle}
                  />
                  <span
                    style={{
                      fontSize: "13px" /* Updated font size */,
                      color: "#888",
                      flexShrink: 0,
                    }}
                  >
                    BR
                  </span>
                  <input
                    type="number"
                    name="cornerRadiusBottomRight"
                    value={selectedElement.cornerRadiusBottomRight || 0}
                    onChange={handleChange}
                    style={inputStyle}
                  />
                </div>
              </>
            )}
          <div style={rowStyle}>
            <span style={labelStyle}>OPACITY</span>
            <input
              type="range"
              name="opacity"
              min="0"
              max="1"
              step="0.01"
              value={selectedElement.opacity}
              onChange={handleChange}
              style={sliderStyle}
            />
            <span
              style={{
                fontSize: "13px" /* Updated font size */,
                minWidth: "28px",
                textAlign: "right",
                flexShrink: 0,
              }}
            >
              {(selectedElement.opacity * 100).toFixed(0)}%
            </span>
          </div>

          {/* ATTRIBUTES SECTION */}
          <div style={sectionTitleStyle}>ATTRIBUTES</div>
          {selectedElement.type === "text" && (
            <>
              <div style={rowStyle}>
                <span style={labelStyle}>CONTENT</span>
                <input
                  type="text"
                  name="text"
                  value={selectedElement.text}
                  onChange={handleChange}
                  style={{ ...inputStyle, width: "120px" }}
                />
              </div>
            </>
          )}
          <div style={rowStyle}>
            <span style={labelStyle}>SLUG</span>
            <input
              type="text"
              name="slug"
              value={selectedElement.slug || ""}
              onChange={handleChange}
              style={{ ...inputStyle, width: "120px" }}
            />
          </div>

          {selectedElement.type === "image" && (
            <>
              <div style={rowStyle}>
                <span style={labelStyle}>IMAGE</span>
                <img
                  src={selectedElement.src}
                  alt="Selected"
                  style={{ width: "100px", height: "auto" }}
                />
              </div>
              <div style={rowStyle}>
                <input
                  type="file"
                  accept="image/*"
                  onChange={(e) => {
                    const file = e.target.files[0];
                    if (file) {
                      const reader = new FileReader();
                      reader.onloadend = () => {
                        updateElement(selectedElement.id, {
                          src: reader.result,
                        });
                      };
                      reader.readAsDataURL(file);
                    }
                  }}
                />
              </div>
              <div style={rowStyle}>
                <button
                  onClick={() =>
                    updateElement(selectedElement.id, {
                      src: "/assets/placeholder.webp",
                    })
                  }
                >
                  Remove Image
                </button>
              </div>
            </>
          )}

          {selectedElement.type === "star" && (
            <>
              <div style={sectionTitleStyle}>STAR PROPERTIES</div>
              <div style={rowStyle}>
                <span style={labelStyle}>SPIKES</span>
                <input
                  type="number"
                  name="numPoints"
                  value={selectedElement.numPoints}
                  onChange={handleChange}
                  style={inputStyle}
                />
              </div>
              <div style={rowStyle}>
                <span style={labelStyle}>INNER RADIUS</span>
                <input
                  type="number"
                  name="innerRadius"
                  value={selectedElement.innerRadius}
                  onChange={handleChange}
                  style={inputStyle}
                />
              </div>
              <div style={rowStyle}>
                <span style={labelStyle}>OUTER RADIUS</span>
                <input
                  type="number"
                  name="outerRadius"
                  value={selectedElement.outerRadius}
                  onChange={handleChange}
                  style={inputStyle}
                />
              </div>
            </>
          )}

          {selectedElement.type === "arc" && (
            <>
              <div style={sectionTitleStyle}>ARC PROPERTIES</div>
              <div style={rowStyle}>
                <span style={labelStyle}>ANGLE</span>
                <input
                  type="range"
                  name="angle"
                  min="0"
                  max="360"
                  step="1"
                  value={selectedElement.angle}
                  onChange={handleChange}
                  style={sliderStyle}
                />
                <span
                  style={{
                    fontSize: "13px",
                    minWidth: "28px",
                    textAlign: "right",
                    flexShrink: 0,
                  }}
                >
                  {selectedElement.angle}
                </span>
              </div>
              <div style={rowStyle}>
                <span style={labelStyle}>INNER RADIUS</span>
                <input
                  type="range"
                  name="innerRadius"
                  min="0"
                  max="200"
                  step="1"
                  value={selectedElement.innerRadius}
                  onChange={handleChange}
                  style={sliderStyle}
                />
                <span
                  style={{
                    fontSize: "13px",
                    minWidth: "28px",
                    textAlign: "right",
                    flexShrink: 0,
                  }}
                >
                  {selectedElement.innerRadius}
                </span>
              </div>
              <div style={rowStyle}>
                <span style={labelStyle}>OUTER RADIUS</span>
                <input
                  type="range"
                  name="outerRadius"
                  min="0"
                  max="200"
                  step="1"
                  value={selectedElement.outerRadius}
                  onChange={handleChange}
                  style={sliderStyle}
                />
                <span
                  style={{
                    fontSize: "13px",
                    minWidth: "28px",
                    textAlign: "right",
                    flexShrink: 0,
                  }}
                >
                  {selectedElement.outerRadius}
                </span>
              </div>
            </>
          )}

          {selectedElement.type === "ellipse" && (
            <>
              <div style={sectionTitleStyle}>ELLIPSE PROPERTIES</div>
              <div style={rowStyle}>
                <span style={labelStyle}>RADIUS X</span>
                <input
                  type="number"
                  name="radiusX"
                  value={selectedElement.radiusX}
                  onChange={handleChange}
                  style={inputStyle}
                />
              </div>
              <div style={rowStyle}>
                <span style={labelStyle}>RADIUS Y</span>
                <input
                  type="number"
                  name="radiusY"
                  value={selectedElement.radiusY}
                  onChange={handleChange}
                  style={inputStyle}
                />
              </div>
            </>
          )}

          {selectedElement.type === "polygon" && (
            <>
              <div style={sectionTitleStyle}>POLYGON PROPERTIES</div>
              <div style={rowStyle}>
                <span style={labelStyle}>SIDES</span>
                <input
                  type="number"
                  name="sides"
                  value={selectedElement.sides}
                  onChange={handleChange}
                  style={inputStyle}
                />
              </div>
              <div style={rowStyle}>
                <span style={labelStyle}>RADIUS</span>
                <input
                  type="number"
                  name="radius"
                  value={selectedElement.radius}
                  onChange={handleChange}
                  style={inputStyle}
                />
              </div>
            </>
          )}

          {selectedElement.type === "pen" && (
            <>
              <div style={sectionTitleStyle}>PEN PROPERTIES</div>
              <div style={rowStyle}>
                <span style={labelStyle}>CLOSED</span>
                <input
                  type="checkbox"
                  name="isClosed"
                  checked={selectedElement.isClosed || false}
                  onChange={(e) =>
                    updateElement(selectedElement.id, {
                      isClosed: e.target.checked,
                    })
                  }
                />
              </div>
              <div style={rowStyle}>
                <span style={labelStyle}>LINE CAP</span>
                <select
                  name="lineCap"
                  value={selectedElement.lineCap || "round"}
                  onChange={handleChange}
                  style={{ ...inputStyle, width: "120px" }}
                >
                  <option value="butt">Butt</option>
                  <option value="round">Round</option>
                  <option value="square">Square</option>
                </select>
              </div>
              <div style={rowStyle}>
                <span style={labelStyle}>LINE JOIN</span>
                <select
                  name="lineJoin"
                  value={selectedElement.lineJoin || "round"}
                  onChange={handleChange}
                  style={{ ...inputStyle, width: "120px" }}
                >
                  <option value="bevel">Bevel</option>
                  <option value="round">Round</option>
                  <option value="miter">Miter</option>
                </select>
              </div>
              <div style={rowStyle}>
                <span style={labelStyle}>TENSION</span>
                <input
                  type="range"
                  name="tension"
                  min="0"
                  max="1"
                  step="0.1"
                  value={selectedElement.tension ?? 0.5}
                  onChange={handleChange}
                  style={sliderStyle}
                />
                <span
                  style={{
                    fontSize: "13px",
                    minWidth: "28px",
                    textAlign: "right",
                    flexShrink: 0,
                  }}
                >
                  {selectedElement.tension ?? 0.5}
                </span>
              </div>
              {/* Bezier properties will go here */}
            </>
          )}
        </>
      )}
    </div>
  );
};

export default PropertiesPanel;