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

// Utility Functions
function formatCurrency(amount) {
    return new Intl.NumberFormat('es-GT', {
        style: 'currency',
        currency: 'GTQ',
        minimumFractionDigits: 2,
    }).format(amount);
}

function formatDate(dateString) {
    if (!dateString) return '-';
    const date = new Date(dateString);
    return date.toLocaleDateString('es-GT', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
    });
}

function formatTime(timeString) {
    if (!timeString) return '-';
    return timeString.substring(0, 5);
}

function showLoading() {
    document.getElementById('loadingOverlay').classList.add('active');
}

function hideLoading() {
    document.getElementById('loadingOverlay').classList.remove('active');
}

function showNotification(message, type = 'info') {
    alert(message); // Simple notification - can be enhanced
}

// App State
let currentEmployee = null;

// Access Form
document.getElementById('accessForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    await handleAccess();
});

async function handleAccess() {
    const dni = document.getElementById('dni').value;
    const accessCode = document.getElementById('accessCode').value;

    // TODO: Implement proper authentication
    // For now, we'll search by DNI and use a simple access code
    // In production, implement proper authentication mechanism
    
    try {
        showLoading();
        
        // Get all employees and find by DNI
        const response = await apiCall('/employees');
        
        if (response.success) {
            const employee = response.data.find(emp => emp.dni === dni);
            
            if (!employee) {
                showNotification('DNI no encontrado', 'error');
                return;
            }
            
            // Simple access code validation (in production, use proper auth)
            // For demo: access code is last 4 digits of DNI
            const expectedCode = employee.dni.slice(-4);
            
            if (accessCode !== expectedCode && accessCode !== 'demo') {
                showNotification('Código de acceso incorrecto', 'error');
                return;
            }
            
            // Store employee and show dashboard
            currentEmployee = employee;
            showEmployeeDashboard(employee);
        }
    } catch (error) {
        showNotification('Error al acceder: ' + error.message, 'error');
    } finally {
        hideLoading();
    }
}

function showEmployeeDashboard(employee) {
    document.getElementById('accessSection').classList.add('hidden');
    document.getElementById('employeeDashboard').classList.remove('hidden');
    
    document.getElementById('employeeName').textContent = employee.name;
    document.getElementById('employeePosition').textContent = employee.position;
    
    loadEmployeeData(employee.id);
}

function logout() {
    currentEmployee = null;
    document.getElementById('accessSection').classList.remove('hidden');
    document.getElementById('employeeDashboard').classList.add('hidden');
    document.getElementById('accessForm').reset();
}

document.getElementById('logoutBtn').addEventListener('click', logout);

async function loadEmployeeData(employeeId) {
    await Promise.all([
        loadPayrolls(employeeId),
        loadAttendances(employeeId),
    ]);
}

async function loadPayrolls(employeeId) {
    try {
        showLoading();
        const response = await apiCall(`/payrolls?employee_id=${employeeId}`);
        
        if (response.success) {
            const payrolls = response.data;
            
            // Update stats
            document.getElementById('totalPayrollsCount').textContent = payrolls.length;
            
            const totalEarnings = payrolls.reduce((sum, p) => sum + (p.total_amount || 0), 0);
            document.getElementById('totalEarnings').textContent = formatCurrency(totalEarnings);
            
            // Render payrolls list
            renderPayrollsList(payrolls);
        }
    } catch (error) {
        showNotification('Error al cargar nóminas: ' + error.message, 'error');
    } finally {
        hideLoading();
    }
}

function renderPayrollsList(payrolls) {
    const container = document.getElementById('payrollsList');
    
    if (payrolls.length === 0) {
        container.innerHTML = '<p class="text-center">No hay nóminas disponibles</p>';
        return;
    }
    
    container.innerHTML = payrolls.map(payroll => {
        const statusBadges = {
            pending: 'badge-warning',
            confirmed: 'badge-info',
            paid: 'badge-success',
        };
        const statusLabels = {
            pending: 'Pendiente',
            confirmed: 'Confirmado',
            paid: 'Pagado',
        };
        
        return `
            <div class="payroll-item" onclick="showPayrollDetail(${payroll.id})">
                <div class="payroll-item-header">
                    <h4>Nómina - ${payroll.period}</h4>
                    <span class="amount">${formatCurrency(payroll.total_amount || 0)}</span>
                </div>
                <div class="payroll-item-details">
                    <div class="detail">
                        <label>Estado</label>
                        <span class="badge ${statusBadges[payroll.status] || 'badge-info'}">
                            ${statusLabels[payroll.status] || payroll.status}
                        </span>
                    </div>
                    <div class="detail">
                        <label>Horas Trabajadas</label>
                        <span>${payroll.hours_worked ? payroll.hours_worked.toFixed(2) + 'h' : '-'}</span>
                    </div>
                    <div class="detail">
                        <label>Salario Base</label>
                        <span>${formatCurrency(payroll.base_salary || 0)}</span>
                    </div>
                    ${payroll.payment_date ? `
                    <div class="detail">
                        <label>Fecha de Pago</label>
                        <span>${formatDate(payroll.payment_date)}</span>
                    </div>
                    ` : ''}
                </div>
            </div>
        `;
    }).join('');
}

async function loadAttendances(employeeId) {
    try {
        const month = document.getElementById('attendanceMonth').value;
        let url = `/attendances?employee_id=${employeeId}`;
        
        if (month) {
            const [year, monthNum] = month.split('-');
            const startDate = `${year}-${monthNum}-01`;
            const lastDay = new Date(year, monthNum, 0).getDate();
            const endDate = `${year}-${monthNum}-${lastDay}`;
            url += `&start_date=${startDate}&end_date=${endDate}`;
        }
        
        showLoading();
        const response = await apiCall(url);
        
        if (response.success) {
            renderAttendancesList(response.data);
        }
    } catch (error) {
        showNotification('Error al cargar asistencias: ' + error.message, 'error');
    } finally {
        hideLoading();
    }
}

function renderAttendancesList(attendances) {
    const container = document.getElementById('attendancesList');
    
    if (attendances.length === 0) {
        container.innerHTML = '<p class="text-center">No hay asistencias registradas</p>';
        return;
    }
    
    container.innerHTML = attendances.map(att => `
        <div class="attendance-item">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h4>${formatDate(att.date)}</h4>
                    <p style="color: var(--text-secondary); margin-top: 0.5rem;">
                        ${formatTime(att.in_time)} - ${formatTime(att.out_time)}
                    </p>
                </div>
                <div style="text-align: right;">
                    <strong>${att.hours_worked ? att.hours_worked.toFixed(2) + 'h' : '-'}</strong>
                    ${att.is_holiday ? '<span class="badge badge-info">Festivo</span>' : ''}
                    ${att.is_vacation ? '<span class="badge badge-warning">Vacaciones</span>' : ''}
                </div>
            </div>
        </div>
    `).join('');
}

// Payroll Detail Modal
async function showPayrollDetail(payrollId) {
    try {
        showLoading();
        const response = await apiCall(`/payrolls/${payrollId}`);
        
        if (response.success) {
            const payroll = response.data;
            const modal = document.getElementById('payrollModal');
            const detailContainer = document.getElementById('payrollDetail');
            
            detailContainer.innerHTML = `
                <div style="display: grid; gap: 1rem;">
                    <div>
                        <h4>Período: ${payroll.period}</h4>
                        <p style="color: var(--text-secondary);">${formatDate(payroll.created_at)}</p>
                    </div>
                    
                    <div style="background: var(--bg-color); padding: 1rem; border-radius: var(--radius);">
                        <h3 style="margin-bottom: 1rem;">Desglose</h3>
                        <div style="display: grid; gap: 0.75rem;">
                            <div style="display: flex; justify-content: space-between;">
                                <span>Horas Trabajadas:</span>
                                <strong>${payroll.hours_worked ? payroll.hours_worked.toFixed(2) + 'h' : '-'}</strong>
                            </div>
                            ${payroll.overtime_hours > 0 ? `
                            <div style="display: flex; justify-content: space-between;">
                                <span>Horas Extras:</span>
                                <strong>${payroll.overtime_hours.toFixed(2)}h</strong>
                            </div>
                            ` : ''}
                            <div style="display: flex; justify-content: space-between;">
                                <span>Salario Base:</span>
                                <strong>${formatCurrency(payroll.base_salary || 0)}</strong>
                            </div>
                            ${payroll.overtime_pay > 0 ? `
                            <div style="display: flex; justify-content: space-between;">
                                <span>Pago por Horas Extras:</span>
                                <strong>${formatCurrency(payroll.overtime_pay)}</strong>
                            </div>
                            ` : ''}
                            ${payroll.bonuses > 0 ? `
                            <div style="display: flex; justify-content: space-between;">
                                <span>Bonificaciones:</span>
                                <strong style="color: var(--success-color);">+${formatCurrency(payroll.bonuses)}</strong>
                            </div>
                            ` : ''}
                            ${payroll.deductions > 0 ? `
                            <div style="display: flex; justify-content: space-between;">
                                <span>Descuentos:</span>
                                <strong style="color: var(--danger-color);">-${formatCurrency(payroll.deductions)}</strong>
                            </div>
                            ` : ''}
                            <div style="border-top: 2px solid var(--border-color); padding-top: 0.75rem; margin-top: 0.75rem; display: flex; justify-content: space-between; font-size: 1.25rem;">
                                <strong>Total:</strong>
                                <strong style="color: var(--primary-color);">${formatCurrency(payroll.total_amount || 0)}</strong>
                            </div>
                        </div>
                    </div>
                    
                    ${payroll.payment_date ? `
                    <div>
                        <strong>Fecha de Pago:</strong> ${formatDate(payroll.payment_date)}
                    </div>
                    ` : ''}
                    
                    ${payroll.notes ? `
                    <div>
                        <strong>Notas:</strong>
                        <p style="margin-top: 0.5rem;">${payroll.notes}</p>
                    </div>
                    ` : ''}
                </div>
            `;
            
            modal.classList.add('active');
        }
    } catch (error) {
        showNotification('Error al cargar detalle: ' + error.message, 'error');
    } finally {
        hideLoading();
    }
}

// Close modal
document.getElementById('closePayrollModal').addEventListener('click', () => {
    document.getElementById('payrollModal').classList.remove('active');
});

// Filter attendances
document.getElementById('filterAttendancesBtn').addEventListener('click', () => {
    if (currentEmployee) {
        loadAttendances(currentEmployee.id);
    }
});

// Set current month as default
const today = new Date();
document.getElementById('attendanceMonth').value = 
    `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, '0')}`;

// Make functions globally available
window.showPayrollDetail = showPayrollDetail;

