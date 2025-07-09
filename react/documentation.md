# Creavo Design Tool Documentation

This document provides a comprehensive guide to using the Creavo Design Tool, covering its various features, tools, and functionalities.

## 1. Core Tools and Shape Creation

The toolbar provides a variety of tools to create and manipulate elements on the canvas.

### 1.1. Basic Shapes

You can add the following basic shapes to your canvas:

*   **Rectangle:** Adds a rectangular shape.
*   **Square:** Adds a square shape.
*   **Circle:** Adds a circular shape.
*   **Line:** Adds a straight line.
*   **Polygon:** Adds a multi-sided polygon.
*   **Star:** Adds a star shape.
*   **Arc:** Adds an arc segment.
*   **Ellipse:** Adds an elliptical shape.

**How to Add Shapes:**
1.  Click on the desired shape icon in the toolbar.
2.  The shape will be added to the canvas with default properties.
3.  Select the shape to adjust its properties in the Properties Panel.

### 1.2. Pen Tool

The Pen tool allows you to draw custom paths and shapes.

**How to Use the Pen Tool:**
1.  Click on the Pen tool icon in the toolbar.
2.  Click on the canvas to add points.
3.  To create a curved line, drag the mouse while adding a point.
4.  To close the path, click on the first point.
5.  You can adjust `lineCap`, `lineJoin`, and `tension` properties in the Properties Panel.
    *   **Line Cap:** Defines the appearance of the ends of open lines (Butt, Round, Square).
    *   **Line Join:** Defines the appearance of corners where two lines meet (Bevel, Round, Miter).
    *   **Tension:** Controls the curvature of the line segments. A higher tension creates smoother curves, while a lower tension (closer to 0) results in sharper corners.

### 1.3. Text Tool

The Text tool allows you to add and format text on the canvas.

**How to Use the Text Tool:**
1.  Click on the Text tool icon in the toolbar.
2.  A default text element will be added to the canvas.
3.  Select the text element to modify its content, font, size, color, alignment, and other properties in the Properties Panel.

### 1.4. Image Tool

The Image tool allows you to add images to your canvas.

**How to Use the Image Tool:**
1.  Click on the Image tool icon in the toolbar.
2.  A placeholder image will be added to the canvas.
3.  Select the image element. In the Properties Panel, you can upload your own image or remove the existing one.

## 2. Media Elements (Future Scope)

The following media elements are planned for future integration:

### 2.1. GIF

The GIF tool will allow you to add animated GIF images to your canvas.

### 2.2. Video

The Video tool will allow you to embed video content into your designs.

## 3. Clipping Mask

The Clipping Mask feature allows you to use one shape to mask or clip another element, revealing only the portion of the masked element that overlaps with the masking shape.

**Working Behavior:**
*   When a clipping mask is applied, a new group is created.
*   The selected elements (the object to be clipped and the mask) are moved into this new group.
*   The properties of the elements themselves are not changed.
*   The initial width and height of the group are taken from the masking object (the "shape").
*   When the group is selected and moved, all child elements (the clipped object and the mask) move along with the group.
*   The clipped elements retain their original x, y coordinates relative to the canvas; they do not move from their initial positions when the mask is applied.

**How to Perform a Clipping Mask:**
1.  Select two elements on the canvas that you wish to use for the clipping mask (one will be the shape, and the other will be the content to be clipped).
2.  Right-click on one of the selected elements to open the context menu.
3.  Click on "Apply Clipping Mask".
4.  The two selected elements will be grouped, and the content element will be clipped by the shape element.

**How to Release a Clipping Mask:**
1.  Select the grouped element that has a clipping mask applied.
2.  Right-click on the grouped element to open the context menu.
3.  Click on "Release Clipping Mask".
4.  The elements will be ungrouped, and the clipping mask will be removed.

## 4. Other Features

### 4.1. Download PNG

Exports the current canvas as a PNG image.

### 4.2. Toggle Layers Panel

Shows or hides the Layers Panel, which allows you to manage the order and visibility of elements on your canvas.

### 4.3. Save and Update Template

Templates can be saved and updated using the buttons in the navigation bar. When you are in 'edit' mode, the button will display 'Update Template'; otherwise, it will display 'Save Template'. Clicking this button will trigger the saving or updating of your current design.

### 4.4. Load Template

Templates are loaded automatically when you navigate to the 'Edit' page. When a user clicks the 'Edit' button for a specific template on the homepage, the `templateId` is passed through the URL. The 'Edit' page then uses this `templateId` to fetch and display the saved template elements on the canvas.

## 5. Color and Fill Options

The Properties Panel allows you to customize the fill and stroke colors of selected elements. You can choose between solid colors and linear gradients.

### 5.1. Solid Color

To apply a solid color fill or stroke:
1. Select an element on the canvas.
2. In the Properties Panel, locate the 'FILL TYPE' dropdown.
3. Select 'Solid'.
4. Click on the color swatch next to 'FILL COLOR' (or 'STROKE' for stroke color). A native color picker will appear.
5. Choose your desired color.

### 5.2. Linear Gradient

Linear gradients blend two colors along a straight line.

**Properties:**
*   **GRADIENT COLOR 1:** The starting color of the gradient.
*   **GRADIENT COLOR 2:** The ending color of the gradient.
*   **START X, START Y:** Coordinates for the starting point of the gradient line.
*   **END X, END Y:** Coordinates for the ending point of the gradient line.

**How to Apply a Linear Gradient:**
1. Select an element on the canvas.
2. In the Properties Panel, set 'FILL TYPE' to 'Linear Gradient'.
3. Use the color pickers to choose 'GRADIENT COLOR 1' and 'GRADIENT COLOR 2'.
4. Adjust 'START X', 'START Y', 'END X', and 'END Y' to control the direction of the gradient, or use the 'PRESET' dropdown for common directions:
    *   **Left to Right:** `START X: 0`, `START Y: 0`, `END X: [element_width]`, `END Y: 0`
    *   **Right to Left:** `START X: [element_width]`, `START Y: 0`, `END X: 0`, `END Y: 0`
    *   **Top to Bottom:** `START X: 0`, `START Y: 0`, `END X: 0`, `END Y: [element_height]`
    *   **Bottom to Top:** `START X: 0`, `START Y: [element_height]`, `END X: 0`, `END Y: 0`
    *   *(Note: `[element_width]` and `[element_height]` refer to the width and height of your selected element. You may need to experiment with these values to achieve the desired effect.)*

