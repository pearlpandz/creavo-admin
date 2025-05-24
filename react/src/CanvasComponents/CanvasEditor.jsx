import { Stage, Layer, Transformer } from "react-konva";
import { useState, useRef, useEffect, useMemo, useCallback, use } from "react";
import { useUndoRedo } from "../hook/useUndoRedo";
import CanvasImage from "./CanvasImage";
import CanvasText from "./CanvasText";
import CanvasRectangleWithText from "./CanvasRectangleWithText";
import CanvasRectangle from "./CanvasRectangle";
import CanvasCircle from "./CanvasCircle";
import CanvasElementForm from "./CanvasElementForm";
import CanvasClippedImage from "./CanvasClippedImage";
import {
  dataURLtoFile,
  getNumericVal,
  getRelativePointerPosition,
} from "../utils";
import { useCreateTemplate, usePatchTemplate } from "../hook/useTemplate";
import { MdOutlineFormatShapes } from "react-icons/md";
import {
  CgShapeCircle,
  CgShapeHexagon,
  CgShapeSquare,
  CgShapeTriangle,
} from "react-icons/cg";
import { BiCircleHalf } from "react-icons/bi";
import { TbShape } from "react-icons/tb";
import { FaUndo, FaRedo } from "react-icons/fa";
import { Tooltip } from "react-tooltip";
import { FaImage } from "react-icons/fa6";
import Navigation from "../components/Navigation";
import CanvasPolygon from "./CanvasPolygon";
import CanvasWedge from "./CanvasWedge";
import { v4 as uuidv4 } from "uuid";
import MultiPointLine from "./CanvasMultiPointLine";
import { toast } from "react-toastify";


// Canvas Editor
const CanvasEditor = ({ template, mode = "edit" }) => {
  const [elements, setElements, undo, redo] = useUndoRedo([]);
  const [selectedId, setSelectedId] = useState(null);
  const [templateName, setTemplateName] = useState("");
  const stageRef = useRef();
  const [templateCategory, setTemplateCategory] = useState("regular");
  const { mutate: patchMutate } = usePatchTemplate();
  const { mutate: createMutate } = useCreateTemplate();
  const [show, setShow] = useState(false);
  const [menuPosition, setMenuPosition] = useState({ x: 0, y: 0 });
  const [showMenu, setShowMenu] = useState(false);

  const [drawAction, setDrawAction] = useState(null);
  const [currentlyDrawnShape, setCurrentlyDrawnShape] = useState({});
  const numMultiPointRef = useRef(0);
  const isPaintRef = useRef(false);
  const transformerRef = useRef(null);

  const mutate = mode === "edit" ? patchMutate : createMutate;

  const dimensions = useMemo(() => {
    if (templateCategory === "product") {
      return { width: 500, height: 700 };
    } else {
      return { width: 600, height: 600 };
    }
  }, [templateCategory]);

  useEffect(() => {
    // Load initial elements from template prop
    if (template?.elements) {
      setElements(template.elements);
      setTemplateName(template.name);
      setTemplateCategory(template.category);
    } else {
      setElements([]);
    }
  }, [template]);

  // Create and cleanup context menu
  useEffect(() => {
    // Hide menu on window click
    const handleWindowClick = () => {
      setShowMenu(false);
    };
    window.addEventListener("click", handleWindowClick);

    return () => {
      window.removeEventListener("click", handleWindowClick);
    };
  }, []);

  const handleSelect = (id) => setSelectedId(id);

  const handleChange = (newAttrs) => {
    setElements(
      elements.map((el) =>
        el.id === newAttrs.id ? { ...el, ...newAttrs } : el
      )
    );
  };

  const deSelect = useCallback(() => {
    setSelectedId(null);
    transformerRef?.current?.nodes([]);
  }, []);

  const checkDeselect = useCallback(
    (e) => {
      const clickedOnEmpty = e.target === stageRef?.current;
      if (clickedOnEmpty) {
        deSelect();
      }
    },
    [stageRef, deSelect]
  );

  const handleStageClick = (e) => {
    // Deselect if clicking on empty space
    if (e.target === e.target.getStage()) {
      checkDeselect(e);
    }

    // only for MultiPointLine
    const stage = stageRef?.current;
    if (e.evt.button !== 0 || !stage) return;
    const id = uuidv4();

    const pos = getRelativePointerPosition(stage);
    const x = getNumericVal(pos?.x);
    const y = getNumericVal(pos?.y);

    if (drawAction === "MultiPointLine") {
      if (numMultiPointRef.current === 0) {
        setCurrentlyDrawnShape({
          id,
          points: [x, y],
          type: "MultiPointLine",
          strokeColor: "#444000",
          bgColor: "#ff0000",
          slug: "{{MultiPointLine}}",
          strokeWidth: 2,
        });
        numMultiPointRef.current += 1;
      } else {
        if (
          numMultiPointRef.current >= 3 &&
          currentlyDrawnShape?.points?.[0] ===
          currentlyDrawnShape?.points?.at(-2) &&
          currentlyDrawnShape?.points?.[1] ===
          currentlyDrawnShape?.points?.at(-1)
        ) {
          if (currentlyDrawnShape) {
            setElements([...elements, currentlyDrawnShape]);
            setCurrentlyDrawnShape({});
            numMultiPointRef.current = 0;
            setDrawAction(null);
          }
        } else {
          numMultiPointRef.current += 1;
        }
      }
      return;
    }

    isPaintRef.current = true;
  };

  const handleStageMouseUp = () => {
    if (numMultiPointRef.current) return;
    isPaintRef.current = false;
    numMultiPointRef.current = 0;
    setDrawAction(null);

    if (currentlyDrawnShape) setElements([...elements, currentlyDrawnShape]);
    setCurrentlyDrawnShape({});
  };

  const handleStageMouseMove = (e) => {
    const stage = stageRef?.current;
    if (e.evt.button !== 0 || !stage) return;

    const pos = getRelativePointerPosition(stage);
    const x = getNumericVal(pos?.x);
    const y = getNumericVal(pos?.y);

    if (numMultiPointRef.current && drawAction === "MultiPointLine") {
      setCurrentlyDrawnShape((prevLine) => {
        const prevPoints = [...(prevLine?.points || [])];
        const pointsLength = numMultiPointRef.current;

        if (
          Math.abs(prevPoints?.[0] - x) < 7 &&
          Math.abs(prevPoints?.[1] - y) < 7
        ) {
          prevPoints[pointsLength * 2] = prevPoints?.[0];
          prevPoints[pointsLength * 2 + 1] = prevPoints?.[1];
        } else {
          prevPoints[pointsLength * 2] = x;
          prevPoints[pointsLength * 2 + 1] = y;
        }

        return { ...prevLine, points: prevPoints };
      });

      return;
    }

    if (!isPaintRef.current) return;
  };

  const bringToFront = () => {
    if (selectedId) {
      const updatedElements = elements.filter((el) => el.id !== selectedId);
      const selectedElement = elements.find((el) => el.id === selectedId);
      updatedElements.push(selectedElement);
      setElements(updatedElements);
    }
  };

  const sendToBack = () => {
    if (selectedId) {
      const updatedElements = elements.filter((el) => el.id !== selectedId);
      const selectedElement = elements.find((el) => el.id === selectedId);
      updatedElements.unshift(selectedElement);
      setElements(updatedElements);
    }
  };

  const addTextElement = () => {
    setElements([
      ...elements,
      {
        id: `text-${Date.now()}`,
        type: "text",
        content: "New Text",
        x: 50,
        y: 50,
        fontSize: 14,
        textColor: "black",
        textAlign: "center",
        slug: "{{text}}",
      },
    ]);
  };

  const addTextBoxElement = () => {
    deSelect();
    const id = uuidv4();
    const newTextBoxElement = {
      id,
      type: "text-box", // ✅ New type for linked Text & Rectangle
      content: "New Text Box",
      x: 50,
      y: 50,
      width: 150,
      height: 50,
      radius: [0, 0, 0, 0],
      fontSize: 20,
      align: "left",
      padding: 0,
      bgColor: "#ffffff", // ✅ Background color of rectangle
      opacity: 50,
      strokeWidth: 0,
      strokeColor: "#FF0000",
      textColor: "#000000", // ✅ Text color
      slug: "{{text-box}}",
    };
    setElements([...elements, newTextBoxElement]);
    setSelectedId(id); // Select the new element
  };

  const addImageElement = () => {
    setElements([
      ...elements,
      {
        id: `image-${Date.now()}`,
        type: "image",
        src: "https://frame-service.creavo.in/uploads/placeholder-image.jpg",
        x: 100,
        y: 100,
        width: 150,
        height: 150,
        slug: "{{image}}",
      },
    ]);
  };

  const addRectangle = () => {
    deSelect();
    const id = uuidv4();
    const newRectangleElement = {
      id,
      type: "rectangle",
      x: 150,
      y: 150,
      width: 100,
      height: 100,
      radius: [0, 0, 0, 0],
      bgColor: "#444000",
      opacity: 50,
      strokeWidth: 0,
      strokeColor: "#FF0000",
      slug: "{{rect}}",
    };
    setElements([...elements, newRectangleElement]);
    setSelectedId(id);
  };

  const addPolygon = (type = "polygon", sides = 6) => {
    deSelect();
    const id = uuidv4();
    const newPolygonElement = {
      id,
      type: type,
      x: 150,
      y: 150,
      width: 100,
      height: 100,
      bgColor: "#444000",
      opacity: 50,
      strokeWidth: 0,
      strokeColor: "#FF0000",
      sides,
      slug: `{{${type}}}`,
    };
    setElements([...elements, newPolygonElement]);
    setSelectedId(id);
  };

  const addWedge = () => {
    deSelect();
    const id = uuidv4();
    const newWedgeElement = {
      id,
      type: "wedge",
      x: 150,
      y: 150,
      width: 100,
      height: 100,
      bgColor: "#444000",
      opacity: 50,
      strokeWidth: 0,
      strokeColor: "#FF0000",
      angle: 180,
      slug: `{{wedge}}`,
    };
    setElements([...elements, newWedgeElement]);
    setSelectedId(id);
  };

  const addTriangle = () => {
    deSelect();
    const id = uuidv4();
    const newTriangleElement = {
      id,
      type: "triangle",
      x: 150,
      y: 150,
      width: 100,
      height: 100,
      bgColor: "#444000",
      opacity: 50,
      strokeWidth: 0,
      strokeColor: "#FF0000",
      sides: 3,
      lineJoin: "bevel",
      slug: "{{triangle}}",
    };
    setElements([...elements, newTriangleElement]);
    setSelectedId(id);
  };

  const addCircle = () => {
    deSelect();
    const id = uuidv4();
    const newCircleElement = {
      id,
      type: "circle",
      x: 200,
      y: 200,
      width: 100,
      height: 100,
      bgColor: "#444",
      opacity: 50,
      strokeWidth: 0,
      strokeColor: "#FF0000",
      slug: "{{circle}}",
    };
    setElements([...elements, newCircleElement]);
    setSelectedId(id);
  };

  const addClipImage = () => {
    deSelect();
    const id = uuidv4();
    const newClipImageElement = {
      id,
      x: 100,
      y: 100,
      width: 200,
      height: 200,
      src: "https://frame-service.creavo.in/uploads/placeholder-image.jpg",
      radius: 0,
      opacity: 100,
      type: "clip-image",
      slug: "{{clip-image}}",
      bgColor: "#444",
    };
    setElements([...elements, newClipImageElement]);
    setSelectedId(id);
  };

  const saveTemplate = async () => {
    const dataURL = stageRef.current.toDataURL({
      pixelRatio: 0.5, // double resolution
    });
    const file = dataURLtoFile(dataURL, `${templateName}.png`);
    const formdata = new FormData();
    formdata.append("name", templateName);
    formdata.append("frame", file);
    formdata.append(
      "elements",
      JSON.stringify(elements?.filter((a) => Object.keys(a).length > 0))
    );
    formdata.append("category", templateCategory);
    mutate({
      payload: formdata
    });
  };

  const updateTemplate = async () => {
    const dataURL = stageRef.current.toDataURL({
      pixelRatio: 1, // double resolution
    });
    const file = dataURLtoFile(dataURL, `${templateName}.png`);
    const formdata = new FormData();
    formdata.append("name", templateName);
    formdata.append("frame", file);
    formdata.append("elements", JSON.stringify(elements));
    formdata.append("category", templateCategory);
    mutate({
      payload: formdata,
      id: template._id
    });
  };

  const handleImageChange = (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = () => {
      setElements(
        elements.map((el) =>
          el.id === selectedId ? { ...el, src: reader.result } : el
        )
      );
    };
    reader.readAsDataURL(file);
  };

  const handleCategoryChange = (e) => {
    setTemplateCategory(e.target.value);
  };

  const onShapeClick = (e) => {
    const node = e.currentTarget;
    handleSelect(node.attrs.id);
    transformerRef.current?.nodes([node]);
  };

  const shapeProps = {
    onClick: onShapeClick,
    draggable: true,
  };

  // Handle context menu for circles
  const handleContextMenu = (e) => {
    e.evt.preventDefault();
    if (e.target === e.target.getStage()) {
      return;
    }

    const stage = e.target.getStage();
    const containerRect = stage.container().getBoundingClientRect();
    const pointerPosition = stage.getPointerPosition();

    setMenuPosition({
      x: containerRect.left + pointerPosition.x + 4,
      y: containerRect.top + pointerPosition.y + 4,
    });

    setShowMenu(true);
    // setSelectedId(e.target.id());
    e.cancelBubble = true;
  };

  // Handle delete element by context menu
  const handleDelete = () => {
    const newCircles = elements.filter((circle) => circle.id !== selectedId);
    setElements(newCircles);
    setShowMenu(false);
  };

  // Handle duplicate to create a new element as similar to the selected element
  const handleDuplicate = () => {
    const index = elements?.findIndex((a) => a.id === selectedId);
    const isExist = index !== -1;
    if (!isExist) return;
    let selectedElement = { ...elements[index] };
    selectedElement["id"] = uuidv4(); // generate new id
    selectedElement["x"] = selectedElement["x"] + 10;
    selectedElement["y"] = selectedElement["y"] + 10;
    selectedElement["slug"] = "";
    setElements([...elements, selectedElement]);
    setSelectedId(selectedElement.id);
    setShowMenu(false);
  };

  return (
    <>
      <Navigation
        onClick={mode === "edit" ? updateTemplate : saveTemplate}
        mode={mode}
      />

      <div className="layout">
        <div className="toolbar">
          <button
            data-tooltip-id="add-textbox"
            data-tooltip-content="Add Textbox"
            onClick={addTextBoxElement}
          >
            <MdOutlineFormatShapes />
          </button>
          <Tooltip id="add-textbox" />

          {/* Text Alignments - wil move to properties*/}

          {/* Shapes */}
          <button
            onClick={addRectangle}
            data-tooltip-id="add-rectangle"
            data-tooltip-content="Add Rectangle"
          >
            <CgShapeSquare />
          </button>
          <Tooltip id="add-rectangle" />

          <button
            data-tooltip-id="add-circle"
            data-tooltip-content="Add Circle"
            onClick={addCircle}
          >
            <CgShapeCircle />
          </button>
          <Tooltip id="add-circle" />

          <button
            data-tooltip-id="add-rectangle"
            data-tooltip-content="Add Rectangle"
            onClick={addTriangle}
          >
            <CgShapeTriangle />
          </button>
          <Tooltip id="add-rectangle" />

          <button
            data-tooltip-id="add-polygon"
            data-tooltip-content="Add Polygon"
            onClick={() => addPolygon()}
          >
            <CgShapeHexagon />
          </button>
          <Tooltip id="add-polygon" />

          <button
            data-tooltip-id="add-wedge"
            data-tooltip-content="Add Wedge"
            onClick={() => addWedge()}
          >
            <BiCircleHalf />
          </button>
          <Tooltip id="add-wedge" />

          <button
            data-tooltip-id="add-pen"
            data-tooltip-content="Add Pen"
            onClick={() => setDrawAction("MultiPointLine")}
          >
            <TbShape />
          </button>
          <Tooltip id="add-pen" />

          {/* Image */}
          <button
            data-tooltip-id="add-image"
            data-tooltip-content="Add Image"
            onClick={addClipImage}
          >
            <FaImage />
          </button>
          <Tooltip id="add-image" />

          <button
            data-tooltip-id="undo"
            data-tooltip-content="Undo"
            onClick={undo}
          >
            <FaUndo />
          </button>
          <Tooltip id="undo" />

          <button
            data-tooltip-id="redo"
            data-tooltip-content="Redo"
            onClick={redo}
          >
            <FaRedo />
          </button>
          <Tooltip id="redo" />
        </div>

        <div className="canvas-container">
          <Stage
            ref={stageRef}
            width={dimensions.width}
            height={dimensions.height}
            onMouseUp={handleStageMouseUp}
            onMouseDown={handleStageClick} // 👈 Click anywhere to deselect
            onMouseMove={handleStageMouseMove}
            onTouchStart={handleStageClick} // 👈 Works on touch devices too
            onContextMenu={handleContextMenu}
          >
            <Layer>
              {[...elements, currentlyDrawnShape].map((el) => {
                if (el.type === "image") {
                  return (
                    <CanvasImage
                      key={el.id}
                      element={el}
                      isSelected={el.id === selectedId}
                      onSelect={() => handleSelect(el.id)}
                      onChange={handleChange}
                    />
                  );
                } else if (el.type === "text") {
                  return (
                    <CanvasText
                      key={el.id}
                      element={el}
                      isSelected={el.id === selectedId}
                      onSelect={() => handleSelect(el.id)}
                      onChange={handleChange}
                    />
                  );
                } else if (el.type === "text-box") {
                  return (
                    <CanvasRectangleWithText
                      key={el.id}
                      element={el}
                      isSelected={el.id === selectedId}
                      onSelect={() => handleSelect(el.id)}
                      onChange={handleChange}
                    />
                  );
                } else if (el.type === "rectangle") {
                  return (
                    <CanvasRectangle
                      key={el.id}
                      element={el}
                      isSelected={el.id === selectedId}
                      onSelect={() => handleSelect(el.id)}
                      onChange={handleChange}
                    />
                  );
                } else if (el.type === "circle") {
                  return (
                    <CanvasCircle
                      key={el.id}
                      element={el}
                      isSelected={el.id === selectedId}
                      onSelect={() => handleSelect(el.id)}
                      onChange={handleChange}
                    />
                  );
                } else if (el.type === "clip-image") {
                  return (
                    <CanvasClippedImage
                      key={el.id}
                      element={el}
                      isSelected={el.id === selectedId}
                      onSelect={() => handleSelect(el.id)}
                      onChange={handleChange}
                    />
                  );
                } else if (el.type === "polygon") {
                  return (
                    <CanvasPolygon
                      key={el.id}
                      element={el}
                      isSelected={el.id === selectedId}
                      onSelect={() => handleSelect(el.id)}
                      onChange={handleChange}
                    />
                  );
                } else if (el.type === "triangle") {
                  return (
                    <CanvasPolygon
                      key={el.id}
                      element={el}
                      isSelected={el.id === selectedId}
                      onSelect={() => handleSelect(el.id)}
                      onChange={handleChange}
                    />
                  );
                } else if (el.type === "wedge") {
                  return (
                    <CanvasWedge
                      key={el.id}
                      element={el}
                      isSelected={el.id === selectedId}
                      onSelect={() => handleSelect(el.id)}
                      onChange={handleChange}
                    />
                  );
                } else if (el.type === "MultiPointLine") {
                  // move to different component and implement properties
                  return (
                    <>
                      <MultiPointLine
                        {...el}
                        closed={el?.id !== currentlyDrawnShape?.id}
                        activatePoints={
                          el?.id === currentlyDrawnShape?.id ||
                          el?.id === selectedId
                        }
                        isSelected={el?.id === selectedId}
                        onPointDrag={(newPoints) => {
                          setElements(
                            elements.map((drawing) => {
                              if (drawing.id === selectedId) {
                                return { ...drawing, points: newPoints };
                              } else return drawing;
                            })
                          );
                        }}
                        onChange={handleChange}
                        {...shapeProps}
                      />

                      <Transformer ref={transformerRef} rotateEnabled={false} />
                    </>
                  );
                }
                return null;
              })}
            </Layer>
          </Stage>
        </div>

        <div className="form-container">
          <CanvasElementForm
            element={elements?.find((el) => el.id === selectedId)}
            onChange={handleChange}
            templateCategory={templateCategory}
            handleCategoryChange={handleCategoryChange}
            templateName={templateName || template?.name}
            setTemplateName={setTemplateName}
          />
        </div>
      </div>

      {/* Context Menu */}
      {showMenu && (
        <div
          style={{
            position: "absolute",
            top: menuPosition.y,
            left: menuPosition.x,
            width: "120px",
            backgroundColor: "white",
            boxShadow: "0 0 5px grey",
            borderRadius: "3px",
            zIndex: 10,
          }}
          onClick={(e) => e.stopPropagation()}
        >
          <button
            style={{
              width: "100%",
              backgroundColor: "white",
              border: "none",
              margin: 0,
              padding: "10px",
              cursor: "pointer",
            }}
            onMouseOver={(e) => (e.target.style.backgroundColor = "lightgray")}
            onMouseOut={(e) => (e.target.style.backgroundColor = "white")}
            onClick={handleDuplicate}
          >
            Duplicate
          </button>
          <button
            style={{
              width: "100%",
              backgroundColor: "white",
              border: "none",
              margin: 0,
              padding: "10px",
              cursor: "pointer",
            }}
            onMouseOver={(e) => (e.target.style.backgroundColor = "lightgray")}
            onMouseOut={(e) => (e.target.style.backgroundColor = "white")}
            onClick={handleDelete}
          >
            Delete
          </button>
        </div>
      )}
    </>
  );
};

export default CanvasEditor;
