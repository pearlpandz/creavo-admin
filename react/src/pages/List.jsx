import React from 'react'
import { useNavigate } from 'react-router';
import { useTemplate } from '../hook/useTemplate';
import { AiOutlineDelete, AiOutlinePlus, AiOutlineEye } from "react-icons/ai";
import { FiEdit } from "react-icons/fi";
import { Tooltip } from 'react-tooltip';
import { format } from 'date-fns';
import { toast } from 'react-toastify';

import './List.css'
import { SETTINGS } from '../constants';

function ListPage() {
    const { templates, isLoading, refetch } = useTemplate()
    const navigate = useNavigate();

    const handleTemplateEdit = (templateId) => {
        navigate(`/edit/${templateId}`);
    }

    const handleTemplateDelete = async (templateId) => {
        console.log(`Delete template with ID: ${templateId}`);
        try {
            const response = await fetch(`${SETTINGS.api_endpoint}/api/frame/${templateId}`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                },
            });

            if (response.ok) {
                console.log('Template deleted successfully');
                toast.success('Template deleted successfully!', {
                    position: "bottom-right",
                    autoClose: 3000,
                });
                refetch();
            } else {
                console.error('Failed to delete template');
                toast.error('Failed to delete template.', {
                    position: "bottom-right",
                    autoClose: 3000,
                });
            }
        } catch (error) {
            console.error('Error deleting template:', error);
            toast.error('Error deleting template.', {
                position: "bottom-right",
                autoClose: 3000,
            });
        }
    }

    const handleCreateTemplate = () => {
        navigate('/create');
    }

    const handlePreviewTemplate = (template) => {
        const previewImage = document.getElementById('preview-image');
        if (previewImage) {
            previewImage.src = template.image;
            previewImage.style.display = 'block';
        }
    };

    const handleHidePreview = () => {
        const previewImage = document.getElementById('preview-image');
        if (previewImage) {
            previewImage.style.display = 'none';
        }
    };

    if (isLoading) {
        return <div className="loading">Loading...</div>
    }

    return (
        <div className='template-list-page'>
            <div className='header-row'>
                <div>
                    <h1 className='page-title'>List of Templates</h1>
                    <p className='page-description'>Here you can see the list of templates.</p>
                </div>
                <button
                    className='create-button'
                    onClick={handleCreateTemplate}
                    title="Create Template"
                >
                    <AiOutlinePlus /> Create Template
                </button>
            </div>
            <div className='template-list'>
                <table className='template-table'>
                    <thead>
                        <tr>
                            <th>Template Name</th>
                            <th>Category</th>
                            <th>Created At</th>
                            <th>Updated At</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {
                            templates.map(template => (
                                <tr key={template._id} className='template-row'>
                                    <td>{template.name}</td>
                                    <td className='category'>{template.category}</td>
                                    <td>{format(new Date(template.createdAt), 'MMM dd yyyy, hh:mm a')}</td>
                                    <td>{format(new Date(template.updatedAt), 'MMM dd yyyy, hh:mm a')}</td>
                                    <td>
                                        <button
                                            className='action-button preview-button'
                                            onMouseOver={() => handlePreviewTemplate(template)}
                                            onMouseOut={handleHidePreview}
                                            title="Preview Template"
                                            data-tooltip-id="preview-tooltip"
                                            data-tooltip-content="Preview Template"
                                        >
                                            <AiOutlineEye />
                                        </button>
                                        <button
                                            className='action-button edit-button'
                                            onClick={() => handleTemplateEdit(template._id)}
                                            title="Edit Template"
                                            data-tooltip-id="edit-tooltip"
                                            data-tooltip-content="Edit Template"
                                        >
                                            <FiEdit />
                                        </button>
                                        <button
                                            className='action-button delete-button'
                                            onClick={() => handleTemplateDelete(template._id)}
                                            title="Delete Template"
                                            data-tooltip-id="delete-tooltip"
                                            data-tooltip-content="Delete Template"
                                        >
                                            <AiOutlineDelete />
                                        </button>
                                    </td>
                                </tr>
                            ))
                        }
                    </tbody>
                </table>
                <Tooltip id="preview-tooltip" />
                <Tooltip id="edit-tooltip" />
                <Tooltip id="delete-tooltip" />
            </div>
            <img id="preview-image" className="preview-image" alt="Template Preview" />
        </div>
    )
}

export default ListPage