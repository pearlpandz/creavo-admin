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
  if (element.fillType !== "linear-gradient") {
    return { fill: element.fill };
  }

  if (
    !element.fillLinearGradientStartPoint ||
    !element.fillLinearGradientEndPoint ||
    !element.fillLinearGradientColorStops
  ) {
    return { fill: element.fill || "transparent" };
  }

  let startPoint = { ...element.fillLinearGradientStartPoint };
  let endPoint = { ...element.fillLinearGradientEndPoint };

  if (element.type === "pen") {
    // Special handling for pen tool
    if (!element.points || element.points.length < 2) {
      return { fill: element.fill || "transparent" };
    }

    let minX = Infinity,
      minY = Infinity,
      maxX = -Infinity,
      maxY = -Infinity;
    for (let i = 0; i < element.points.length; i += 2) {
      if (
        element.points[i + 1] === undefined ||
        !isFinite(element.points[i]) ||
        !isFinite(element.points[i + 1])
      )
        continue;
      minX = Math.min(minX, element.points[i]);
      minY = Math.min(minY, element.points[i + 1]);
      maxX = Math.max(maxX, element.points[i]);
      maxY = Math.max(maxY, element.points[i + 1]);
    }

    if (!isFinite(minX)) {
      // Only need to check one, they'll all be Infinity if points are bad
      return { fill: element.fill || "transparent" };
    }

    const hasFiniteGradientPoints =
      isFinite(startPoint.x) &&
      isFinite(startPoint.y) &&
      isFinite(endPoint.x) &&
      isFinite(endPoint.y);

    if (!hasFiniteGradientPoints) {
      // Preset calculation failed, create a default gradient geometry
      const width = maxX - minX;
      const height = maxY - minY;
      startPoint = { x: 0, y: height / 2 }; // Default to left-to-right
      endPoint = { x: width, y: height / 2 };
    }

    // Offset the gradient to the bounding box origin
    startPoint.x += minX;
    startPoint.y += minY;
    endPoint.x += minX;
    endPoint.y += minY;
  } else {
    // Common logic for all other shapes
    if (
      !isFinite(startPoint.x) ||
      !isFinite(startPoint.y) ||
      !isFinite(endPoint.x) ||
      !isFinite(endPoint.y)
    ) {
      return { fill: element.fill || "transparent" };
    }

    if (element.type === "circle" || element.type === "polygon") {
      const offsetX = element.width / 2;
      const offsetY = element.height / 2;
      startPoint.x -= offsetX;
      startPoint.y -= offsetY;
      endPoint.x -= offsetX;
      endPoint.y -= offsetY;
    } else if (element.type === "star") {
      const scaleX = element.scaleX !== undefined ? element.scaleX : 1;
      const scaleY = element.scaleY !== undefined ? element.scaleY : 1;
      const offsetX = element.outerRadius * scaleX;
      const offsetY = element.outerRadius * scaleY;
      startPoint.x -= offsetX;
      startPoint.y -= offsetY;
      endPoint.x -= offsetX;
      endPoint.y -= offsetY;
    }
    // For other shapes like 'rect', no adjustment is needed as their origin is top-left.
  }

  return {
    fill: undefined,
    fillLinearGradientStartPoint: startPoint,
    fillLinearGradientEndPoint: endPoint,
    fillLinearGradientColorStops: element.fillLinearGradientColorStops,
  };
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