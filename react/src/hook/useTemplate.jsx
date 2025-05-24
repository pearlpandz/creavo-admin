import {
    useQuery,
    QueryClient,
    useMutation
} from '@tanstack/react-query'
import { SETTINGS } from '../constants'
import { toast } from 'react-toastify'
import { useNavigate } from 'react-router'

// Create a client
const queryClient = new QueryClient()

const fetchTemplates = async () => {
    const response = await fetch(`${SETTINGS.api_endpoint}/api/frame/list`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    if (!response.ok) {
        throw new Error('Network response was not ok')
    }
    const data = await response.json()
    return data
}

export const useTemplate = () => {
    const { data: templates, isLoading, refetch } = useQuery({
        queryKey: ['templates'],
        queryFn: fetchTemplates
    })
    return {
        templates,
        isLoading,
        refetch,
    }
}

export const useTemplateById = (templateId) => {
    const { data: template, isLoading } = useQuery({
        queryKey: ['template', templateId],
        queryFn: async () => {
            const response = await fetch(`${SETTINGS.api_endpoint}/api/frame/${templateId}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                }
            })
            if (!response.ok) {
                throw new Error('Network response was not ok')
            }
            const data = await response.json()
            return data
        },
        enabled: !!templateId,
    })
    return {
        template,
        isLoading,
    }
}

const patchTemplate = async ({ payload, id }) => {
    const response = await fetch(`${SETTINGS.api_endpoint}/api/frame/${id}`, {
        method: 'PATCH',
        body: payload,
    });

    if (!response.ok) {
        throw new Error('Failed to update user');
    }

    return response.json();
}

export const usePatchTemplate = () => {
    const navigate = useNavigate();
    // Mutations
    const mutation = useMutation({
        mutationFn: patchTemplate,
        onSuccess: (data, variables) => {
            queryClient.setQueryData(['template', variables._id], data);
            toast.success('Template updated successfully!', {
                position: "bottom-right",
                autoClose: 1000,
            });
            navigate('/');
        },
        onError: (error) => {
            toast.error(`Error updating template: ${error.message}`, {
                position: "bottom-right",
                autoClose: 3000,
            });
        },
    })

    return mutation;
}

const createTemplate = async ({ payload }) => {
    const response = await fetch(`${SETTINGS.api_endpoint}/api/frame/create`, {
        method: 'POST',
        body: payload,
    });

    if (!response.ok) {
        throw new Error('Failed to update user');
    }

    return response.json();
}

export const useCreateTemplate = () => {
    const navigate = useNavigate();
    // Mutations
    const mutation = useMutation({
        mutationFn: createTemplate,
        onSuccess: (data, variables) => {
            console.log(variables, data)
            queryClient.setQueryData(['template', variables._id], data);
            toast.success('Template updated successfully!', {
                position: "bottom-right",
                autoClose: 1000,
            });
            navigate('/');
        },
        onError: (error) => {
            toast.error(`Error updating template: ${error.message}`, {
                position: "bottom-right",
                autoClose: 3000,
            });
        },
    })

    return mutation;
}