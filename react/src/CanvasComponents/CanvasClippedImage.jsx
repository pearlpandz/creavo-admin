import { Image, Group } from "react-konva";
import { useRef } from "react";
import useImage from "use-image";
import TransformerComponent from "./TransformerComponent";

const CanvasClippedImage = ({ element, isSelected, onSelect, onChange, isEditable = true }) => {
    const [image] = useImage(element.src, 'anonymous');
    const shapeRef = useRef();

    const handleDragMove = (e) => {
        const node = e.target;
        onChange({
            ...element,
            x: node.x(),
            y: node.y(),
        })
    }

    const handleTransformEnd = () => {
        const node = shapeRef.current;
        const scaleX = node.scaleX();
        const scaleY = node.scaleY();

        const newWidth = node.width() * scaleX;
        const newHeight = node.height() * scaleY;

        let newClip = element.clip;

        // Example: if polygon, scale points
        if (newClip?.type === 'polygon') {
            newClip = {
                ...newClip,
                points: newClip.points.map((val, i) => val * (i % 2 === 0 ? scaleX : scaleY)),
            };
        }

        // we will reset it back
        node.scaleX(1);
        node.scaleY(1);
        onChange({
            ...element,
            x: node.x(),
            y: node.y(),
            // set minimal value
            width: newWidth,
            height: newHeight,
            clip: newClip,
        });
    };

    // If clip is present, use its region relative to the image for all shape types
    let groupX = element.x;
    let groupY = element.y;
    let groupWidth = element.width;
    let groupHeight = element.height;
    let cropProps = {};
    let imageWidth = groupWidth;
    let imageHeight = groupHeight;
    let clipShapeProps = {};
    if (image && element.clip) {
        // Calculate scale between displayed image and natural image size
        const scaleX = image.width / element.width;
        const scaleY = image.height / element.height;
        cropProps = {
            x: element.clip.x * scaleX,
            y: element.clip.y * scaleY,
            width: element.clip.width * scaleX,
            height: element.clip.height * scaleY,
        };
        groupX = element.x + element.clip.x;
        groupY = element.y + element.clip.y;
        groupWidth = element.clip.width;
        groupHeight = element.clip.height;
        imageWidth = element.clip.width;
        imageHeight = element.clip.height;
        clipShapeProps = {
            ...element.clip,
            width: groupWidth,
            height: groupHeight,
        };
    } else if (image) {
        // Fallback: crop to the group (element) size, as before
        const imageAspectRatio = image.width / image.height;
        const groupAspectRatio = groupWidth / groupHeight;
        if (imageAspectRatio > groupAspectRatio) {
            const cropWidth = image.height * groupAspectRatio;
            cropProps = {
                x: (image.width - cropWidth) / 2,
                y: 0,
                width: cropWidth,
                height: image.height,
            };
        } else {
            const cropHeight = image.width / groupAspectRatio;
            cropProps = {
                x: 0,
                y: (image.height - cropHeight) / 2,
                width: image.width,
                height: cropHeight,
            };
        }
        clipShapeProps = { type: 'rectangle', width: groupWidth, height: groupHeight };
    }

    return (
        <>
            <Group
                ref={shapeRef}
                x={groupX}
                y={groupY}
                width={groupWidth}
                height={groupHeight}
                clipFunc={(ctx) => clipShape(ctx, clipShapeProps)}
                onClick={isEditable ? (e) => { if (e.evt.button === 0) onSelect(e.evt.shiftKey || e.evt.ctrlKey); } : null}
                onTap={isEditable ? (e) => { if (e.evt.button === 0) onSelect(e.evt.shiftKey || e.evt.ctrlKey); } : null}
                draggable={isEditable}
                onDragMove={isEditable ? handleDragMove : null}
                onTransformEnd={isEditable ? handleTransformEnd : null}
                opacity={element.opacity}
            >
                <Image
                    opacity={element.opacity}
                    fill={element.color}
                    image={image}
                    x={0}
                    y={0}
                    width={imageWidth}
                    height={imageHeight}
                    crop={cropProps}
                />
            </Group>
            <TransformerComponent shapeRef={shapeRef} isSelected={isSelected} element={element} />
        </>
    );
};

// Clip Shape Function
const clipShape = (ctx, shape) => {
    const { width, height, type, radius = 0, sides, angle, rotation } = shape;
    ctx.beginPath();
    if (type === 'rectangle') {
        ctx.rect(0, 0, width, height);
    } else if (type === 'circle') {
        ctx.arc(width / 2, height / 2, Math.min(width, height) / 2, 0, Math.PI * 2);
    } else if (type === 'wedge') {
        const a = (angle ?? 90) * Math.PI / 180;
        const rot = (rotation ?? 0) * Math.PI / 180;
        const r = Math.min(width, height) / 2;
        const cx = width / 2;
        const cy = height / 2;
        ctx.moveTo(cx, cy);
        ctx.arc(cx, cy, r, rot, rot + a, false);
        ctx.closePath();
    } else if (type === 'polygon' || type === 'triangle') {
        const n = sides || (type === 'triangle' ? 3 : 5);
        const rot = (rotation ?? 0) * Math.PI / 180;
        const centerX = width / 2;
        const centerY = height / 2;
        const r = Math.min(width, height) / 2;
        ctx.moveTo(centerX + r * Math.cos(rot), centerY + r * Math.sin(rot));
        for (let i = 1; i <= n; i++) {
            const ang = (i / n) * 2 * Math.PI + rot;
            ctx.lineTo(centerX + r * Math.cos(ang), centerY + r * Math.sin(ang));
        }
        ctx.closePath();
    } else {
        // fallback: rounded rectangle
        ctx.moveTo(radius, 0);
        ctx.lineTo(width - radius, 0);
        ctx.arcTo(width, 0, width, radius, radius);
        ctx.lineTo(width, height - radius);
        ctx.arcTo(width, height, width - radius, height, radius);
        ctx.lineTo(radius, height);
        ctx.arcTo(0, height, 0, height - radius, radius);
        ctx.lineTo(0, radius);
        ctx.arcTo(0, 0, radius, 0, radius);
        ctx.closePath();
    }
};

export default CanvasClippedImage;