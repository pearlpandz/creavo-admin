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