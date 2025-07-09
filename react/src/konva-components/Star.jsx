
import React from "react";
import { Star as KonvaStar } from "react-konva";
import { getFill } from "../utils";

const Star = (props) => {
  const fillProps = getFill(props);
  return (
    <KonvaStar
      {...props}
      {...fillProps}
      sides={props.numPoints}
      innerRadius={props.innerRadius}
      outerRadius={props.outerRadius}
    />
  );
};

export default Star;
