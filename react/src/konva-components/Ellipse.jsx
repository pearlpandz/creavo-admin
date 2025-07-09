
import React from "react";
import { Ellipse as KonvaEllipse } from "react-konva";
import { getFill } from "../utils";

const Ellipse = (props) => {
  const fillProps = getFill(props);
  return (
    <KonvaEllipse
      {...props}
      {...fillProps}
      radiusX={props.radiusX}
      radiusY={props.radiusY}
    />
  );
};

export default Ellipse;
