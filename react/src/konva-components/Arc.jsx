
import React from "react";
import { Arc as KonvaArc } from "react-konva";
import { getFill } from "../utils";

const Arc = (props) => {
  const fillProps = getFill(props);
  return (
    <KonvaArc
      {...props}
      {...fillProps}
      angle={props.angle}
      innerRadius={props.innerRadius}
      outerRadius={props.outerRadius}
    />
  );
};

export default Arc;
