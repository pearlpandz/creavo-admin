import { CiText, CiTextAlignCenter, CiTextAlignJustify, CiTextAlignLeft, CiTextAlignRight, CiImageOn, CiUndo, CiRedo } from "react-icons/ci";
import { CgShapeCircle, CgShapeSquare } from "react-icons/cg";
import { RiBringForward, RiBringToFront, RiSendBackward, RiSendToBack } from "react-icons/ri";

// Form Component for Element Properties
const CanvasElementForm = ({ element, onChange, templateCategory, handleCategoryChange, templateName, setTemplateName }) => {

  const updateValue = (field, value) => {
    onChange({ ...element, [field]: value });
  };

  const updateRadius = (field, value) => {
    let updatedValue = element.radius
    switch (field) {
      case 'topleft':
        updatedValue[0] = value;
        onChange({ ...element, radius: updatedValue });
        break;

      case 'topright':
        updatedValue[1] = value;
        onChange({ ...element, radius: updatedValue });
        break;

      case 'bottomleft':
        updatedValue[3] = value;
        onChange({ ...element, radius: updatedValue });
        break;

      case 'bottomright':
        updatedValue[2] = value;
        onChange({ ...element, radius: updatedValue });
        break;

      default:
        break;
    }
  }

  return (
    <div style={{
      display: "flex",
      flexDirection: "column",
      gap: "10px",
      height: "100%",
      overflowY: "auto"
    }}>
      <div className="template-properties">
        <h6>template properties</h6>

        <label>
          <span>template name</span>
          <input
            value={templateName}
            onChange={(e) => setTemplateName(e.target.value)}
          />
        </label>

        <label>
          <span>cateogry</span>
          <select name="category" id="category" value={templateCategory} onChange={handleCategoryChange}>
            <option value="regular">Regular</option>
            <option value="product">Product</option>
            <option value="political">Political</option>
          </select>
        </label>
      </div>

      {/* section 1 */}
      <div className="appearance">
        <div className="element-positions flex">
          <button className='icon-btn'><RiBringToFront /></button>
          <button className='icon-btn'><RiBringForward /></button>
          <button className='icon-btn'><RiSendBackward /></button>
          <button className='icon-btn'><RiSendToBack /></button>
        </div>
        {element?.type === "text-box" && (
          <div className="text-alignments flex">
            <button onClick={() => updateValue('align', 'center')} className={`icon-btn ${element?.align === 'center' && 'active'}`}><CiTextAlignCenter /></button>
            <button onClick={() => updateValue('align', 'justify')} className={`icon-btn ${element?.align === 'justify' && 'active'}`}><CiTextAlignJustify /></button>
            <button onClick={() => updateValue('align', 'left')} className={`icon-btn ${element?.align === 'left' && 'active'}`}><CiTextAlignLeft /></button>
            <button onClick={() => updateValue('align', 'right')} className={`icon-btn ${element?.align === 'right' && 'active'}`}><CiTextAlignRight /></button>
          </div>
        )}
      </div>

      {/* section 2 */}
      <div className="placement">
        <h6>transform</h6>
        <div className="element-placement" >
          {!["MultiPointLine"].includes(element?.type) && (
            <div className="element-size">
              <label>
                <span>W</span>
                <input
                  type="number"
                  value={Math.ceil(element?.width || 100)}
                  onChange={(e) => updateValue("width", parseInt(e.target.value))}
                />
              </label>

              <label>
                <span>H</span>
                <input
                  type="number"
                  value={Math.ceil(element?.height || 100)}
                  onChange={(e) => updateValue("height", parseInt(e.target.value))}
                />
              </label>
            </div>
          )}
          <div className="element-axis">
            <label>
              <span>X</span>
              <input
                type="number"
                value={Math.ceil(element?.x || 0)}
                onChange={(e) => updateValue("x", parseInt(e.target.value))}
              />
            </label>

            <label>
              <span>Y</span>
              <input
                type="number"
                value={Math.ceil(element?.y || 0)}
                onChange={(e) => updateValue("y", parseInt(e.target.value))}
              />
            </label>
          </div>
        </div>
      </div>

      {/* section 3 */}
      <div className="style-properties">
        <h6>appearance</h6>
        {
          element?.type === 'text-box' &&
          <>
            <label>
              <span>font size</span>
              <input
                type="number"
                value={element?.fontSize}
                min="12"
                onChange={(e) => updateValue("fontSize", parseInt(e.target.value))}
              />
            </label>
            <label>
              <span>padding</span>
              <input
                type="number"
                value={element?.padding}
                min="12"
                onChange={(e) => updateValue("padding", parseInt(e.target.value))}
              />
            </label>
          </>
        }

        {element?.type !== 'clip-image' && <label>
          <span>fill</span>
          <input
            type="color"
            value={element?.bgColor}
            onChange={(e) => updateValue("bgColor", e.target.value)}
          />
        </label>}

        {element?.type !== 'clip-image' && <label>
          <span>stroke</span>
          <input
            type="color"
            value={element?.strokeColor}
            onChange={(e) => updateValue("strokeColor", e.target.value)}
          />
          <input
            type="number"
            value={element?.strokeWidth}
            onChange={(e) => updateValue("strokeWidth", parseInt(e.target.value))}
            style={{ marginLeft: 10 }}
          />
        </label>}

        {element?.type === 'polygon' && <label>
          <span>sides</span>
          <input
            type="number"
            value={element?.sides}
            onChange={(e) => updateValue("sides", parseInt(e.target.value))}
            style={{ marginLeft: 10 }}
          />
        </label>}

        {element?.type === 'triangle' && <label>
          <span>Line Join</span>
          <select name="triangleType" id="triangleType" value={element.lineJoin} onChange={(e) => updateValue("lineJoin", e.target.value)}>
            <option value="miter">miter</option>
            <option value="bevel">bevel</option>
            <option value="round">round</option>
          </select>
        </label>}

        {element?.type === 'text-box' && <label>
          <span>color</span>
          <input
            type="color"
            value={element?.textColor}
            onChange={(e) => updateValue("textColor", e.target.value)}
          />
        </label>}



        {['rectangle', 'text-box'].includes(element?.type) && (
          <>
            <label>
              <span>radius</span>
            </label>
            <div className="element-placement" >
              <div className="element-size">
                <label>
                  <span>TL</span>
                  <input
                    type="number"
                    value={element?.radius[0]}
                    onChange={(e) => updateRadius("topleft", parseInt(e.target.value))}
                  />
                </label>
                <label>
                  <span>BL</span>
                  <input
                    type="number"
                    value={element?.radius[3]}
                    onChange={(e) => updateRadius("bottomleft", parseInt(e.target.value))}
                  />
                </label>

              </div>
              <div className="element-axis">
                <label>
                  <span>TR</span>
                  <input
                    type="number"
                    value={element?.radius[1]}
                    onChange={(e) => updateRadius("topright", parseInt(e.target.value))}
                  />
                </label>


                <label>
                  <span>BR</span>
                  <input
                    type="number"
                    value={element?.radius[2]}
                    onChange={(e) => updateRadius("bottomright", parseInt(e.target.value))}
                  />
                </label>
              </div>
            </div>
          </>
        )}

        {['wedge'].includes(element?.type) && (
          <label>
            <span>angle</span>
            <input
              type="number"
              value={element?.angle}
              onChange={(e) => updateValue("angle", parseInt(e.target.value))}
              style={{ marginLeft: 10 }}
            />
            <input
              type="range"
              value={element?.angle}
              min={0}
              max={360}
              onChange={(e) => updateValue("angle", parseInt(e.target.value))}
            />

          </label>
        )}

        {!["MultiPointLine"].includes(element?.type) && <label>
          <span>opacity</span>
          <input
            type="range"
            value={element?.opacity}
            min={0}
            max={100}
            onChange={(e) => updateValue("opacity", parseInt(e.target.value))}
          />
        </label>}
      </div>

      {element && <div className="style-properties attributes">
        <h6>attributes</h6>

        {element?.type === 'text-box' && <label>
          <span>content</span>
          <input
            value={element?.content}
            onChange={(e) => updateValue("content", e.target.value)}
          />
        </label>}

        <label>
          <span>slug</span>
          <input
            value={element?.slug}
            onChange={(e) => updateValue("slug", e.target.value)}
          />
        </label>
      </div>}
    </div>
  );
};

export default CanvasElementForm;