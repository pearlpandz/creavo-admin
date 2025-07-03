import { useEffect, useRef } from "react";
import { Transformer } from "react-konva";

// Reusable Transformer Component
const TransformerComponent = ({ shapeRef, isSelected, element }) => {
    const transformerRef = useRef();
    useEffect(() => {
        if (isSelected) {
            transformerRef.current.nodes([shapeRef.current]);
            transformerRef.current.getLayer().batchDraw();
        }
    }, [isSelected, shapeRef, element]);

    return isSelected ? <Transformer ref={transformerRef}
        boundBoxFunc={(oldBox, newBox) => {
            // limit resize
            if (newBox.width < 5 || newBox.height < 5) {
                return oldBox;
            }
            return newBox;
        }}
    /> : null;
};

export default TransformerComponent; 