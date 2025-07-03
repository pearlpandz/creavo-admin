import React, { useState } from 'react';
import './Layers.css';
import { DndContext, closestCenter } from '@dnd-kit/core';
import { SortableContext, useSortable, arrayMove, verticalListSortingStrategy } from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';
import { FaGripVertical } from 'react-icons/fa';

const SortableItem = ({ id, element, selectedIds, onSelect, onContextMenu }) => {
  const { attributes, listeners, setNodeRef, transform, transition } = useSortable({ id });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
    display: 'flex',
    alignItems: 'center',
    padding: '8px 12px',
    margin: '4px 0',
    backgroundColor: selectedIds.includes(id) ? '#e6f7ff' : '#fff',
    border: `1px solid ${selectedIds.includes(id) ? '#91d5ff' : '#d9d9d9'}`,
    borderRadius: '4px',
    cursor: 'pointer',
  };

  return (
    <div
      ref={setNodeRef}
      style={style}
      {...attributes}
      onClick={(e) => {
        if (e.button === 0) {
          onSelect(id, e.shiftKey || e.ctrlKey);
        }
      }}
      onContextMenu={(e) => onContextMenu(e, element)}
    >
      <span {...listeners} style={{ cursor: 'grab', marginRight: '10px' }}><FaGripVertical /></span>
      {element.slug || element.type}
    </div>
  );
};

const Layers = ({ elements, onSelect, selectedIds, onDelete, onReorder }) => {
  const [menuPosition, setMenuPosition] = useState({ x: 0, y: 0 });
  const [showMenu, setShowMenu] = useState(false);
  const [selectedLayer, setSelectedLayer] = useState(null);

  const handleContextMenu = (e, element) => {
    e.preventDefault();
    setSelectedLayer(element);
    setMenuPosition({ x: e.clientX, y: e.clientY });
    setShowMenu(true);
  };

  const handleDelete = () => {
    onDelete(selectedLayer.id);
    setShowMenu(false);
  };

  const handleDragEnd = (event) => {
    const { active, over } = event;
    if (active.id !== over.id) {
      const oldIndex = elements.findIndex((el) => el.id === active.id);
      const newIndex = elements.findIndex((el) => el.id === over.id);
      onReorder(oldIndex, newIndex);
    }
  };

  return (
    <div className="layers-panel" style={{ padding: '10px', backgroundColor: '#f0f2f5', height: '100%' }}>
      <h4 style={{ marginTop: 0, marginBottom: '10px' }}>Layers</h4>
      <DndContext collisionDetection={closestCenter} onDragEnd={handleDragEnd}>
        <SortableContext items={elements.map(el => el.id)} strategy={verticalListSortingStrategy}>
          {elements.map(element => (
            <SortableItem
              key={element.id}
              id={element.id}
              element={element}
              selectedIds={selectedIds}
              onSelect={onSelect}
              onContextMenu={handleContextMenu}
            />
          ))}
        </SortableContext>
      </DndContext>
      {showMenu && (
        <div
          style={{
            position: 'absolute',
            top: menuPosition.y,
            left: menuPosition.x,
            backgroundColor: 'white',
            boxShadow: '0 0 5px grey',
            borderRadius: '3px',
            zIndex: 10,
          }}
          onClick={(e) => e.stopPropagation()}
        >
          <button onClick={handleDelete} style={{ border: 'none', background: 'none', padding: '8px 12px', cursor: 'pointer' }}>Delete</button>
        </div>
      )}
    </div>
  );
};

export default Layers;