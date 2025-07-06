import { useState, useRef, useEffect } from "react";
import { useUndoRedo } from "../hook/useUndoRedo";
import { dataURLtoFile } from "../utils";
import { useCreateTemplate, usePatchTemplate } from "../hook/useTemplate";
import Navigation from "../components/Navigation";
import KonvaBuilder from "../konva-components/KonvaBuilder";

// Canvas Editor
const CanvasEditor = ({ template, mode = "edit" }) => {
  const [elements, setElements] = useUndoRedo([]);
  const [templateName, setTemplateName] = useState("");
  const stageRef = useRef();
  const [templateCategory, setTemplateCategory] = useState();
  const { mutate: patchMutate } = usePatchTemplate();
  const { mutate: createMutate } = useCreateTemplate();
  const mutate = mode === "edit" ? patchMutate : createMutate;

  useEffect(() => {
    // Load initial elements from template prop
    if (template?.elements) {
      setElements(template.elements);
      setTemplateName(template.name);
      setTemplateCategory(template.category);
    } else {
      setElements([]);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [template]);

  const saveTemplate = async () => {
    const dataURL = stageRef.current.toDataURL({
      pixelRatio: 0.4, // 40% resolution of actual canvas size
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
      pixelRatio: 0.4, // 40% resolution of actual canvas size
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

  return (
    <>
      <Navigation
        onClick={mode === "edit" ? updateTemplate : saveTemplate}
        mode={mode}
      />

      <KonvaBuilder
        elements={elements}
        setElements={setElements}
        mode="edit"
      />
    </>
  );
};

export default CanvasEditor;
