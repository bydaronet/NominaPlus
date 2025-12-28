// API Configuration
const API_BASE_URL = window.location.origin + '/api';

// Helper function for API calls
async function apiCall(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
        },
    };

    const config = { ...defaultOptions, ...options };

    if (config.body && typeof config.body === 'object') {
        config.body = JSON.stringify(config.body);
    }

    try {
        const response = await fetch(url, config);
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Error en la petición');
        }

        return data;
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// Employees API
const employeesAPI = {
    getAll: (isActive = null) => {
        const params = isActive !== null ? `?is_active=${isActive}` : '';
        return apiCall(`/employees${params}`);
    },
    getById: (id) => apiCall(`/employees/${id}`),
    create: (data) => apiCall('/employees', {
        method: 'POST',
        body: data,
    }),
    update: (id, data) => apiCall(`/employees/${id}`, {
        method: 'PUT',
        body: data,
    }),
    delete: (id) => apiCall(`/employees/${id}`, {
        method: 'DELETE',
    }),
};

// Attendances API
const attendancesAPI = {
    getAll: (filters = {}) => {
        const params = new URLSearchParams();
        if (filters.employee_id) params.append('employee_id', filters.employee_id);
        if (filters.start_date) params.append('start_date', filters.start_date);
        if (filters.end_date) params.append('end_date', filters.end_date);
        const queryString = params.toString();
        return apiCall(`/attendances${queryString ? '?' + queryString : ''}`);
    },
    getById: (id) => apiCall(`/attendances/${id}`),
    create: (data) => apiCall('/attendances', {
        method: 'POST',
        body: data,
    }),
    update: (id, data) => apiCall(`/attendances/${id}`, {
        method: 'PUT',
        body: data,
    }),
    delete: (id) => apiCall(`/attendances/${id}`, {
        method: 'DELETE',
    }),
};

// Payrolls API
const payrollsAPI = {
    getAll: (filters = {}) => {
        const params = new URLSearchParams();
        if (filters.employee_id) params.append('employee_id', filters.employee_id);
        if (filters.period) params.append('period', filters.period);
        if (filters.status) params.append('status', filters.status);
        const queryString = params.toString();
        return apiCall(`/payrolls${queryString ? '?' + queryString : ''}`);
    },
    getById: (id) => apiCall(`/payrolls/${id}`),
    create: (data) => apiCall('/payrolls', {
        method: 'POST',
        body: data,
    }),
    update: (id, data) => apiCall(`/payrolls/${id}`, {
        method: 'PUT',
        body: data,
    }),
    delete: (id) => apiCall(`/payrolls/${id}`, {
        method: 'DELETE',
    }),
    calculate: (data) => apiCall('/payrolls/calculate', {
        method: 'POST',
        body: data,
    }),
};

// Reports API
const reportsAPI = {
    getSummary: (period = null) => {
        const params = period ? `?period=${period}` : '';
        return apiCall(`/reports/summary${params}`);
    },
};

// Export APIs
window.employeesAPI = employeesAPI;
window.attendancesAPI = attendancesAPI;
window.payrollsAPI = payrollsAPI;
window.reportsAPI = reportsAPI;

