import { useState, useRef, useEffect } from "react";
import { useUndoRedo } from "../hook/useUndoRedo";
import { dataURLtoFile } from "../utils";
import { useCreateTemplate, usePatchTemplate } from "../hook/useTemplate";
import Navigation from "../components/Navigation";
import KonvaBuilder from "../konva-components/KonvaBuilder";

// Canvas Editor
const CanvasEditor = ({ template, mode = "edit" }) => {
  const stageRef = useRef();
  const [elements, setElements] = useUndoRedo([]);
  const [templateObj, setTemplateObj] = useState({});
  const { mutate: patchMutate } = usePatchTemplate();
  const { mutate: createMutate } = useCreateTemplate();
  const mutate = mode === "edit" ? patchMutate : createMutate;

  useEffect(() => {
    // Load initial elements from template prop
    if (template?.elements) {
      setElements(template.elements);
      setTemplateObj({
        name: template.name,
        category: template.category,
        state: template.state || "draft",
      });
    } else {
      setElements([]);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [template]);

  const saveTemplate = async () => {
    const dataURL = stageRef.current.toDataURL({
      pixelRatio: 0.4, // 40% resolution of actual canvas size
    });
    const file = dataURLtoFile(dataURL, `${templateObj.name}.png`);
    const formdata = new FormData();
    formdata.append("name", templateObj.name);
    formdata.append("frame", file);
    formdata.append(
      "elements",
      JSON.stringify(elements?.filter((a) => Object.keys(a).length > 0))
    );
    formdata.append("category", templateObj.category || "regular");
    formdata.append("state", templateObj.state || "draft");
    mutate({
      payload: formdata
    });
  };

  const updateTemplate = async () => {
    const dataURL = stageRef.current.toDataURL({
      pixelRatio: 0.4, // 40% resolution of actual canvas size
    });
    const file = dataURLtoFile(dataURL, `${templateObj.name}.png`);
    const formdata = new FormData();
    formdata.append("name", templateObj.name);
    formdata.append("frame", file);
    formdata.append("elements", JSON.stringify(elements));
    formdata.append("category", templateObj.category || "regular");
    formdata.append("state", templateObj.state || "draft");
    mutate({
      payload: formdata,
      id: template._id
    });
  };

  return (
    <>
      <Navigation
        onClick={mode === "edit" ? updateTemplate : saveTemplate}
        mode={mode}
      />

      <KonvaBuilder
        elements={elements}
        setElements={setElements}
        templateObj={templateObj}
        setTemplateObj={setTemplateObj}
        mode="edit"
        stageRef={stageRef}
      />
    </>
  );
};

export default CanvasEditor;
