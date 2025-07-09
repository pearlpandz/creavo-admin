// get dynamic placeholder image based resized width and height
export function updateImageUrl(url, newWidth, newHeight) {
  return url
    .replace(/w=\d+/, `w=${newWidth}`)
    .replace(/h=\d+/, `h=${newHeight}`);
}

export function dataURLtoFile(dataUrl, filename) {
  const arr = dataUrl.split(",");
  const mime = arr[0].match(/:(.*?);/)[1];
  const bstr = atob(arr[1]); // decode base64
  let n = bstr.length;
  const u8arr = new Uint8Array(n);

  while (n--) {
    u8arr[n] = bstr.charCodeAt(n);
  }

  return new File([u8arr], filename, { type: mime });
}

export const getRelativePointerPosition = (node) => {
  const transform = node.getAbsoluteTransform().copy();
  transform.invert();

  const pos = node.getStage().getPointerPosition();
  if (!pos) return;
  return transform.point(pos);
};

export const getNumericVal = (val) => val || 0;

export const getFill = (element) => {
  if (element.fillType === "linear-gradient") {
    let startPoint = { ...element.fillLinearGradientStartPoint }; // Create copies
    let endPoint = { ...element.fillLinearGradientEndPoint };     // Create copies

    // Adjust gradient points for Circle and RegularPolygon
    // The gradient points are defined relative to a 0,0 top-left origin (like for a rect)
    // Konva Circle/Polygon expects gradient points relative to their center (0,0 in their local coord system)
    // So, we need to shift the points by -width/2 and -height/2
    if (element.type === "circle" || element.type === "polygon") {
      const offsetX = element.width / 2;
      const offsetY = element.height / 2;

      startPoint.x -= offsetX;
      startPoint.y -= offsetY;
      endPoint.x -= offsetX;
      endPoint.y -= offsetY;
    }

    return {
      fill: undefined, // Explicitly set fill to undefined for gradients
      fillLinearGradientStartPoint: startPoint,
      fillLinearGradientEndPoint: endPoint,
      fillLinearGradientColorStops: element.fillLinearGradientColorStops,
    };
  } else {
    return { fill: element.fill };
  }
};

export const roundProps = (obj, propsToRound) => {
  const newObj = { ...obj };
  propsToRound.forEach(prop => {
    if (typeof newObj[prop] === 'number') {
      newObj[prop] = Math.round(newObj[prop]);
    }
  });
  return newObj;
};