import React from "react";
import CanvasEditor from "../CanvasComponents/CanvasEditor";
import { useParams } from "react-router";
import { useTemplateById } from "../hook/useTemplate";

const EditPage = () => {
    const { templateId } = useParams();
    const {template, isLoading} = useTemplateById(templateId);

   if(isLoading) {
        return <div>Loading...</div>
    }

    return (
        <CanvasEditor template={template} mode='edit' />
    );
};

export default EditPage;
