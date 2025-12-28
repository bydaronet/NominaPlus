// App State
const appState = {
    currentPage: 'dashboard',
    employees: [],
    attendances: [],
    payrolls: [],
    locales: {}, // Cache de traducciones por país
    currentLocale: null, // Locale actual (para el contexto)
};

// Localization System
const i18n = {
    translations: {},
    currency: { code: 'GTQ', symbol: 'Q', locale: 'es-GT' },
    
    async loadLocale(countryCode = 'GT') {
        try {
            // Verificar cache
            if (appState.locales[countryCode]) {
                this.translations = appState.locales[countryCode].translations;
                this.currency = appState.locales[countryCode].currency;
                return;
            }
            
            // Cargar desde API
            const response = await localeAPI.getLocale(countryCode);
            if (response.success) {
                this.translations = response.data.translations;
                this.currency = response.data.currency;
                appState.locales[countryCode] = response.data;
            }
        } catch (error) {
            console.error('Error loading locale:', error);
            // Fallback a GT
            if (countryCode !== 'GT') {
                await this.loadLocale('GT');
            }
        }
    },
    
    t(key, defaultValue = null) {
        return this.translations[key] || defaultValue || key;
    },
    
    getCurrencyInfo() {
        return this.currency;
    }
};

// Utility Functions
function formatCurrency(amount, countryCode = null) {
    if (!amount && amount !== 0) return '-';
    
    // Si se especifica un país, usar su moneda
    if (countryCode && appState.locales[countryCode]) {
        const currency = appState.locales[countryCode].currency;
        return new Intl.NumberFormat(currency.locale, {
            style: 'currency',
            currency: currency.code,
            minimumFractionDigits: 2,
        }).format(amount);
    }
    
    // Usar locale actual
    const currency = i18n.getCurrencyInfo();
    return new Intl.NumberFormat(currency.locale, {
        style: 'currency',
        currency: currency.code,
        minimumFractionDigits: 2,
    }).format(amount);
}

function formatDate(dateString) {
    if (!dateString) return '-';
    const date = new Date(dateString);
    return date.toLocaleDateString('es-GT', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
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
    // Simple notification - can be enhanced with a toast library
    alert(message);
}

// Navigation
function initNavigation() {
    const navItems = document.querySelectorAll('.nav-item');
    const menuToggle = document.getElementById('menuToggle');
    const sidebar = document.querySelector('.sidebar');

    navItems.forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            const page = item.getAttribute('data-page');
            switchPage(page);
            
            navItems.forEach(nav => nav.classList.remove('active'));
            item.classList.add('active');
        });
    });

    menuToggle?.addEventListener('click', () => {
        sidebar.classList.toggle('active');
    });

    // Close sidebar when clicking outside on mobile
    document.addEventListener('click', (e) => {
        if (window.innerWidth <= 768) {
            if (!sidebar.contains(e.target) && !menuToggle.contains(e.target)) {
                sidebar.classList.remove('active');
            }
        }
    });
}

function switchPage(page) {
    // Hide all pages
    document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
    
    // Show selected page
    const targetPage = document.getElementById(page);
    if (targetPage) {
        targetPage.classList.add('active');
        appState.currentPage = page;
        
        // Update page title (usará traducciones después de cargar)
        updatePageTitle(page);
        
        // Load page data
        loadPageData(page);
    }
}

async function updatePageTitle(page) {
    // Cargar locale por defecto si no hay uno cargado
    if (!i18n.translations || Object.keys(i18n.translations).length === 0) {
        await i18n.loadLocale('GT');
    }
    
    const titles = {
        dashboard: 'Dashboard',
        employees: i18n.t('employees', 'Empleados'),
        attendances: i18n.t('attendances', 'Asistencias'),
        payrolls: i18n.t('payrolls', 'Nóminas'),
    };
    document.getElementById('pageTitle').textContent = titles[page] || 'Dashboard';
    
    // Actualizar todos los textos de la interfaz
    updateUITexts();
}

function updateUITexts() {
    const t = i18n.translations;
    
    // Navegación
    const navPayrolls = document.getElementById('navPayrolls');
    if (navPayrolls) navPayrolls.textContent = t.payrolls || 'Nóminas';
    
    // Dashboard stats
    const statPayrollsLabel = document.getElementById('statPayrollsLabel');
    if (statPayrollsLabel) statPayrollsLabel.textContent = `${t.payrolls || 'Nóminas'} del Mes`;
    
    // Página de nóminas
    const payrollsPageTitle = document.getElementById('payrollsPageTitle');
    if (payrollsPageTitle) payrollsPageTitle.textContent = `Gestión de ${t.payrolls || 'Nóminas'}`;
    
    const addPayrollBtnText = document.getElementById('addPayrollBtnText');
    if (addPayrollBtnText) addPayrollBtnText.textContent = `Nueva ${t.payroll || 'Nómina'}`;
    
    const loadingPayrolls = document.getElementById('loadingPayrolls');
    if (loadingPayrolls) loadingPayrolls.textContent = `Cargando ${t.payrolls || 'nóminas'}...`;
}

function loadPageData(page) {
    switch (page) {
        case 'dashboard':
            loadDashboard();
            break;
        case 'employees':
            loadEmployees();
            break;
        case 'attendances':
            loadAttendances();
            break;
        case 'payrolls':
            loadPayrolls();
            break;
    }
}

// Dashboard
async function loadDashboard() {
    try {
        showLoading();
        const summary = await reportsAPI.getSummary();
        
        if (summary.success) {
            const data = summary.data;
            document.getElementById('totalEmployees').textContent = data.employees.total_active || 0;
            document.getElementById('totalPayrolls').textContent = data.payrolls.total || 0;
            document.getElementById('totalPaid').textContent = formatCurrency(data.payrolls.total_paid || 0);
            document.getElementById('totalAttendances').textContent = data.attendances.total || 0;
        }
        
        // Load recent activity
        await loadRecentActivity();
    } catch (error) {
        showNotification('Error al cargar el dashboard: ' + error.message, 'error');
    } finally {
        hideLoading();
    }
}

async function loadRecentActivity() {
    try {
        const [employeesRes, payrollsRes] = await Promise.all([
            employeesAPI.getAll(true),
            payrollsAPI.getAll(),
        ]);
        
        const activityList = document.getElementById('recentActivity');
        const activities = [];
        
        if (payrollsRes.success && payrollsRes.data.length > 0) {
            // Cargar locale si no está cargado
            if (!i18n.translations || Object.keys(i18n.translations).length === 0) {
                await i18n.loadLocale('GT');
            }
            const t = i18n.translations;
            
            const recentPayrolls = payrollsRes.data.slice(0, 5);
            recentPayrolls.forEach(payroll => {
                activities.push({
                    type: 'payroll',
                    message: `${t.payroll || 'Nómina'} de ${payroll.employee_name} - ${payroll.period}`,
                    date: payroll.created_at,
                });
            });
        }
        
        if (activities.length === 0) {
            activityList.innerHTML = '<p class="text-center">No hay actividad reciente</p>';
        } else {
            activityList.innerHTML = activities.map(activity => `
                <div class="activity-item">
                    <p>${activity.message}</p>
                    <small>${formatDate(activity.date)}</small>
                </div>
            `).join('');
        }
    } catch (error) {
        document.getElementById('recentActivity').innerHTML = 
            '<p class="text-center">Error al cargar actividad</p>';
    }
}

// Employees
async function loadEmployees() {
    try {
        showLoading();
        const response = await employeesAPI.getAll();
        
        if (response.success) {
            appState.employees = response.data;
            renderEmployeesTable(response.data);
            populateEmployeeSelects();
        }
    } catch (error) {
        showNotification('Error al cargar empleados: ' + error.message, 'error');
    } finally {
        hideLoading();
    }
}

function renderEmployeesTable(employees) {
    const tbody = document.getElementById('employeesTableBody');
    
    if (employees.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" class="text-center">No hay empleados registrados</td></tr>';
        return;
    }
    
    tbody.innerHTML = employees.map(async (emp) => {
        // Cargar locale del empleado si no está en cache
        if (!appState.locales[emp.country_code]) {
            await i18n.loadLocale(emp.country_code || 'GT');
        }
        const currency = appState.locales[emp.country_code]?.currency || i18n.getCurrencyInfo();
        
        return `
        <tr>
            <td>${emp.id}</td>
            <td>${emp.name}</td>
            <td>${emp.dni}${emp.cuil ? ` / ${emp.cuil}` : ''}</td>
            <td>${emp.position}</td>
            <td>${formatCurrency(emp.hourly_rate, emp.country_code)}</td>
            <td>
                <span class="badge ${emp.is_active ? 'badge-success' : 'badge-danger'}">
                    ${emp.is_active ? 'Activo' : 'Inactivo'}
                </span>
            </td>
            <td>
                <button class="btn btn-sm btn-primary" onclick="editEmployee(${emp.id})">
                    <i class="fas fa-edit"></i>
                </button>
                <button class="btn btn-sm btn-danger" onclick="deleteEmployee(${emp.id})">
                    <i class="fas fa-trash"></i>
                </button>
            </td>
        </tr>
    `;
    }).join('');
    
    // Cargar locales en paralelo
    Promise.all(employees.map(emp => 
        appState.locales[emp.country_code] ? Promise.resolve() : i18n.loadLocale(emp.country_code || 'GT')
    )).then(() => {
        // Re-renderizar con las traducciones cargadas
        tbody.innerHTML = employees.map(emp => {
            const currency = appState.locales[emp.country_code]?.currency || i18n.getCurrencyInfo();
            return `
            <tr>
                <td>${emp.id}</td>
                <td>${emp.name}</td>
                <td>${emp.dni}${emp.cuil ? ` / ${emp.cuil}` : ''}</td>
                <td>${emp.position}</td>
                <td>${formatCurrency(emp.hourly_rate, emp.country_code)}</td>
                <td>
                    <span class="badge ${emp.is_active ? 'badge-success' : 'badge-danger'}">
                        ${emp.is_active ? 'Activo' : 'Inactivo'}
                    </span>
                </td>
                <td>
                    <button class="btn btn-sm btn-primary" onclick="editEmployee(${emp.id})">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button class="btn btn-sm btn-danger" onclick="deleteEmployee(${emp.id})">
                        <i class="fas fa-trash"></i>
                    </button>
                </td>
            </tr>
        `;
        }).join('');
    });
}

function populateEmployeeSelects() {
    const selects = [
        document.getElementById('attendanceEmployeeId'),
        document.getElementById('payrollEmployeeId'),
        document.getElementById('attendanceEmployeeFilter'),
        document.getElementById('payrollEmployeeFilter'),
    ];
    
    selects.forEach(select => {
        if (select) {
            const currentValue = select.value;
            select.innerHTML = '<option value="">Seleccionar empleado</option>' +
                appState.employees
                    .filter(emp => emp.is_active)
                    .map(emp => 
                        `<option value="${emp.id}">${emp.name}</option>`
                    ).join('');
            if (currentValue) select.value = currentValue;
        }
    });
}

// Employee Modal
function initEmployeeModal() {
    const modal = document.getElementById('employeeModal');
    const form = document.getElementById('employeeForm');
    const addBtn = document.getElementById('addEmployeeBtn');
    const closeBtn = document.getElementById('closeEmployeeModal');
    const cancelBtn = document.getElementById('cancelEmployeeBtn');
    
    addBtn?.addEventListener('click', () => openEmployeeModal());
    closeBtn?.addEventListener('click', () => closeEmployeeModal());
    cancelBtn?.addEventListener('click', () => closeEmployeeModal());
    
    form?.addEventListener('submit', async (e) => {
        e.preventDefault();
        await saveEmployee();
    });
    
    // Close modal on outside click
    modal?.addEventListener('click', (e) => {
        if (e.target === modal) closeEmployeeModal();
    });
}

async function openEmployeeModal(employeeId = null) {
    const modal = document.getElementById('employeeModal');
    const form = document.getElementById('employeeForm');
    const title = document.getElementById('employeeModalTitle');
    
    form.reset();
    document.getElementById('employeeId').value = '';
    document.getElementById('employeeCountryCode').value = 'GT';
    
    // Cargar locale por defecto
    await i18n.loadLocale('GT');
    updateEmployeeFormLabels('GT');
    
    // Listener para cambiar país (remover listeners anteriores si existen)
    const countrySelect = document.getElementById('employeeCountryCode');
    const newCountrySelect = countrySelect.cloneNode(true);
    countrySelect.parentNode.replaceChild(newCountrySelect, countrySelect);
    
    newCountrySelect.addEventListener('change', async (e) => {
        const countryCode = e.target.value;
        await i18n.loadLocale(countryCode);
        await updateEmployeeFormLabels(countryCode);
    });
    
    if (employeeId) {
        title.textContent = 'Editar Empleado';
        await loadEmployeeData(employeeId);
    } else {
        title.textContent = 'Nuevo Empleado';
    }
    
    modal.classList.add('active');
}

async function updateEmployeeFormLabels(countryCode) {
    // Cargar locale si no está en cache
    if (!appState.locales[countryCode]) {
        await i18n.loadLocale(countryCode);
    }
    
    if (!appState.locales[countryCode]) return;
    
    const locale = appState.locales[countryCode];
    const t = locale.translations;
    const currency = locale.currency;
    
    // Actualizar etiquetas
    document.getElementById('labelDni').textContent = `${t.dni || 'DNI'} *`;
    document.getElementById('labelCuil').textContent = t.cuil || 'CUIL';
    document.getElementById('labelHourlyRate').textContent = `${t.hourly_rate || 'Tarifa por Hora'} (${currency.symbol}) *`;
    
    // Mostrar/ocultar CUIL según el país
    const cuilGroup = document.getElementById('cuilGroup');
    if (countryCode === 'AR') {
        cuilGroup.style.display = 'block';
    } else {
        cuilGroup.style.display = 'none';
    }
    
    // Actualizar textos de la interfaz principal si es necesario
    // (opcional: solo si quieres que toda la UI cambie cuando editas un empleado)
}

function closeEmployeeModal() {
    document.getElementById('employeeModal').classList.remove('active');
}

async function loadEmployeeData(id) {
    try {
        showLoading();
        const response = await employeesAPI.getById(id);
        
        if (response.success) {
            const emp = response.data;
            
            // Cargar locale del empleado
            await i18n.loadLocale(emp.country_code || 'GT');
            updateEmployeeFormLabels(emp.country_code || 'GT');
            
            document.getElementById('employeeId').value = emp.id;
            document.getElementById('employeeName').value = emp.name || '';
            document.getElementById('employeeDni').value = emp.dni || '';
            document.getElementById('employeeCuil').value = emp.cuil || '';
            document.getElementById('employeeNit').value = emp.nit || '';
            document.getElementById('employeeCountryCode').value = emp.country_code || 'GT';
            document.getElementById('employeePosition').value = emp.position || '';
            document.getElementById('employeeHourlyRate').value = emp.hourly_rate || '';
            document.getElementById('employeePhone').value = emp.phone || '';
            document.getElementById('employeeEmail').value = emp.email || '';
            document.getElementById('employeeAddress').value = emp.address || '';
            document.getElementById('employeeBankAccount').value = emp.bank_account || '';
            document.getElementById('employeeIsActive').checked = emp.is_active !== false;
        }
    } catch (error) {
        showNotification('Error al cargar empleado: ' + error.message, 'error');
    } finally {
        hideLoading();
    }
}

async function saveEmployee() {
    try {
        showLoading();
        const id = document.getElementById('employeeId').value;
        const countryCode = document.getElementById('employeeCountryCode').value;
        const data = {
            name: document.getElementById('employeeName').value,
            dni: document.getElementById('employeeDni').value,
            cuil: document.getElementById('employeeCuil').value || null,
            nit: document.getElementById('employeeNit').value || null,
            country_code: countryCode,
            position: document.getElementById('employeePosition').value,
            hourly_rate: parseFloat(document.getElementById('employeeHourlyRate').value),
            phone: document.getElementById('employeePhone').value,
            email: document.getElementById('employeeEmail').value,
            address: document.getElementById('employeeAddress').value,
            bank_account: document.getElementById('employeeBankAccount').value,
            is_active: document.getElementById('employeeIsActive').checked,
        };
        
        let response;
        if (id) {
            response = await employeesAPI.update(id, data);
        } else {
            response = await employeesAPI.create(data);
        }
        
        if (response.success) {
            showNotification(response.message || 'Empleado guardado exitosamente', 'success');
            closeEmployeeModal();
            loadEmployees();
        }
    } catch (error) {
        showNotification('Error al guardar empleado: ' + error.message, 'error');
    } finally {
        hideLoading();
    }
}

async function editEmployee(id) {
    openEmployeeModal(id);
}

async function deleteEmployee(id) {
    if (!confirm('¿Está seguro de desactivar este empleado?')) return;
    
    try {
        showLoading();
        const response = await employeesAPI.delete(id);
        
        if (response.success) {
            showNotification('Empleado desactivado exitosamente', 'success');
            loadEmployees();
        }
    } catch (error) {
        showNotification('Error al desactivar empleado: ' + error.message, 'error');
    } finally {
        hideLoading();
    }
}

// Employee Search and Filter
function initEmployeeFilters() {
    const searchInput = document.getElementById('employeeSearch');
    const filterSelect = document.getElementById('employeeFilter');
    
    searchInput?.addEventListener('input', filterEmployees);
    filterSelect?.addEventListener('change', filterEmployees);
}

function filterEmployees() {
    const searchTerm = document.getElementById('employeeSearch').value.toLowerCase();
    const filterValue = document.getElementById('employeeFilter').value;
    
    let filtered = appState.employees;
    
    if (filterValue !== '') {
        filtered = filtered.filter(emp => emp.is_active === (filterValue === 'true'));
    }
    
    if (searchTerm) {
        filtered = filtered.filter(emp => 
            emp.name.toLowerCase().includes(searchTerm) ||
            emp.dni.toLowerCase().includes(searchTerm) ||
            emp.position.toLowerCase().includes(searchTerm)
        );
    }
    
    renderEmployeesTable(filtered);
}

// Attendances
async function loadAttendances() {
    try {
        showLoading();
        const filters = {
            employee_id: document.getElementById('attendanceEmployeeFilter')?.value || null,
            start_date: document.getElementById('attendanceStartDate')?.value || null,
            end_date: document.getElementById('attendanceEndDate')?.value || null,
        };
        
        const response = await attendancesAPI.getAll(filters);
        
        if (response.success) {
            appState.attendances = response.data;
            renderAttendancesTable(response.data);
        }
    } catch (error) {
        showNotification('Error al cargar asistencias: ' + error.message, 'error');
    } finally {
        hideLoading();
    }
}

function renderAttendancesTable(attendances) {
    const tbody = document.getElementById('attendancesTableBody');
    
    if (attendances.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" class="text-center">No hay asistencias registradas</td></tr>';
        return;
    }
    
    tbody.innerHTML = attendances.map(att => `
        <tr>
            <td>${att.employee_name || 'N/A'}</td>
            <td>${formatDate(att.date)}</td>
            <td>${formatTime(att.in_time)}</td>
            <td>${formatTime(att.out_time)}</td>
            <td>${att.hours_worked ? att.hours_worked.toFixed(2) + 'h' : '-'}</td>
            <td>
                <button class="btn btn-sm btn-primary" onclick="editAttendance(${att.id})">
                    <i class="fas fa-edit"></i>
                </button>
                <button class="btn btn-sm btn-danger" onclick="deleteAttendance(${att.id})">
                    <i class="fas fa-trash"></i>
                </button>
            </td>
        </tr>
    `).join('');
}

// Attendance Modal
function initAttendanceModal() {
    const modal = document.getElementById('attendanceModal');
    const form = document.getElementById('attendanceForm');
    const addBtn = document.getElementById('addAttendanceBtn');
    const closeBtn = document.getElementById('closeAttendanceModal');
    const cancelBtn = document.getElementById('cancelAttendanceBtn');
    
    addBtn?.addEventListener('click', () => openAttendanceModal());
    closeBtn?.addEventListener('click', () => closeAttendanceModal());
    cancelBtn?.addEventListener('click', () => closeAttendanceModal());
    
    form?.addEventListener('submit', async (e) => {
        e.preventDefault();
        await saveAttendance();
    });
    
    modal?.addEventListener('click', (e) => {
        if (e.target === modal) closeAttendanceModal();
    });
}

function openAttendanceModal(attendanceId = null) {
    const modal = document.getElementById('attendanceModal');
    const form = document.getElementById('attendanceForm');
    const title = document.getElementById('attendanceModalTitle');
    
    form.reset();
    document.getElementById('attendanceId').value = '';
    document.getElementById('attendanceDate').value = new Date().toISOString().split('T')[0];
    
    if (attendanceId) {
        title.textContent = 'Editar Asistencia';
        loadAttendanceData(attendanceId);
    } else {
        title.textContent = 'Registrar Asistencia';
    }
    
    modal.classList.add('active');
}

function closeAttendanceModal() {
    document.getElementById('attendanceModal').classList.remove('active');
}

async function loadAttendanceData(id) {
    try {
        showLoading();
        const response = await attendancesAPI.getById(id);
        
        if (response.success) {
            const att = response.data;
            document.getElementById('attendanceId').value = att.id;
            document.getElementById('attendanceEmployeeId').value = att.employee_id;
            document.getElementById('attendanceDate').value = att.date;
            document.getElementById('attendanceInTime').value = att.in_time?.substring(0, 5) || '';
            document.getElementById('attendanceOutTime').value = att.out_time?.substring(0, 5) || '';
            document.getElementById('attendanceIsHoliday').checked = att.is_holiday || false;
            document.getElementById('attendanceIsVacation').checked = att.is_vacation || false;
            document.getElementById('attendanceNotes').value = att.notes || '';
        }
    } catch (error) {
        showNotification('Error al cargar asistencia: ' + error.message, 'error');
    } finally {
        hideLoading();
    }
}

async function saveAttendance() {
    try {
        showLoading();
        const id = document.getElementById('attendanceId').value;
        const date = document.getElementById('attendanceDate').value;
        const inTime = document.getElementById('attendanceInTime').value;
        const outTime = document.getElementById('attendanceOutTime').value;
        
        const data = {
            employee_id: parseInt(document.getElementById('attendanceEmployeeId').value),
            date: date,
            in_time: inTime + ':00',
            out_time: outTime ? outTime + ':00' : null,
            is_holiday: document.getElementById('attendanceIsHoliday').checked,
            is_vacation: document.getElementById('attendanceIsVacation').checked,
            notes: document.getElementById('attendanceNotes').value,
        };
        
        let response;
        if (id) {
            response = await attendancesAPI.update(id, data);
        } else {
            response = await attendancesAPI.create(data);
        }
        
        if (response.success) {
            showNotification(response.message || 'Asistencia guardada exitosamente', 'success');
            closeAttendanceModal();
            loadAttendances();
        }
    } catch (error) {
        showNotification('Error al guardar asistencia: ' + error.message, 'error');
    } finally {
        hideLoading();
    }
}

async function editAttendance(id) {
    openAttendanceModal(id);
}

async function deleteAttendance(id) {
    if (!confirm('¿Está seguro de eliminar esta asistencia?')) return;
    
    try {
        showLoading();
        const response = await attendancesAPI.delete(id);
        
        if (response.success) {
            showNotification('Asistencia eliminada exitosamente', 'success');
            loadAttendances();
        }
    } catch (error) {
        showNotification('Error al eliminar asistencia: ' + error.message, 'error');
    } finally {
        hideLoading();
    }
}

// Payrolls
async function loadPayrolls() {
    try {
        showLoading();
        const filters = {
            employee_id: document.getElementById('payrollEmployeeFilter')?.value || null,
            period: document.getElementById('payrollPeriod')?.value || null,
            status: document.getElementById('payrollStatusFilter')?.value || null,
        };
        
        const response = await payrollsAPI.getAll(filters);
        
        if (response.success) {
            appState.payrolls = response.data;
            await renderPayrollsTable(response.data);
        }
    } catch (error) {
        showNotification('Error al cargar nóminas: ' + error.message, 'error');
    } finally {
        hideLoading();
    }
}

async function renderPayrollsTable(payrolls) {
    const tbody = document.getElementById('payrollsTableBody');
    
    if (payrolls.length === 0) {
        await i18n.loadLocale('GT');
        const t = i18n.translations;
        tbody.innerHTML = `<tr><td colspan="7" class="text-center">No hay ${t.payrolls || 'nóminas'} registradas</td></tr>`;
        return;
    }
    
    // Cargar locales de todos los empleados
    const employeeIds = [...new Set(payrolls.map(p => p.employee_id))];
    const employees = appState.employees.filter(e => employeeIds.includes(e.id));
    
    await Promise.all(employees.map(emp => 
        appState.locales[emp.country_code] ? Promise.resolve() : i18n.loadLocale(emp.country_code || 'GT')
    ));
    
    // Crear mapa de empleado a país
    const employeeCountryMap = {};
    employees.forEach(emp => {
        employeeCountryMap[emp.id] = emp.country_code || 'GT';
    });
    
    tbody.innerHTML = payrolls.map(payroll => {
        const countryCode = employeeCountryMap[payroll.employee_id] || 'GT';
        const locale = appState.locales[countryCode];
        const t = locale?.translations || {};
        const statusBadges = {
            pending: 'badge-warning',
            confirmed: 'badge-info',
            paid: 'badge-success',
        };
        const statusLabels = {
            pending: t.status_pending || 'Pendiente',
            confirmed: t.status_confirmed || 'Confirmado',
            paid: t.status_paid || 'Pagado',
        };
        
        return `
            <tr>
                <td>${payroll.employee_name || 'N/A'}</td>
                <td>${payroll.period}</td>
                <td>${payroll.hours_worked ? payroll.hours_worked.toFixed(2) + 'h' : '-'}</td>
                <td>${formatCurrency(payroll.base_salary || 0, countryCode)}</td>
                <td><strong>${formatCurrency(payroll.total_amount || 0, countryCode)}</strong></td>
                <td>
                    <span class="badge ${statusBadges[payroll.status] || 'badge-secondary'}">
                        ${statusLabels[payroll.status] || payroll.status}
                    </span>
                </td>
                <td>
                    <button class="btn btn-sm btn-primary" onclick="editPayroll(${payroll.id})">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button class="btn btn-sm btn-danger" onclick="deletePayroll(${payroll.id})">
                        <i class="fas fa-trash"></i>
                    </button>
                </td>
            </tr>
        `;
    }).join('');
}

// Payroll Modal
function initPayrollModal() {
    const modal = document.getElementById('payrollModal');
    const form = document.getElementById('payrollForm');
    const addBtn = document.getElementById('addPayrollBtn');
    const closeBtn = document.getElementById('closePayrollModal');
    const cancelBtn = document.getElementById('cancelPayrollBtn');
    const calculateBtn = document.getElementById('calculatePayrollBtn');
    
    addBtn?.addEventListener('click', () => openPayrollModal());
    closeBtn?.addEventListener('click', () => closePayrollModal());
    cancelBtn?.addEventListener('click', () => closePayrollModal());
    calculateBtn?.addEventListener('click', () => calculatePayroll());
    
    form?.addEventListener('submit', async (e) => {
        e.preventDefault();
        await savePayroll();
    });
    
    modal?.addEventListener('click', (e) => {
        if (e.target === modal) closePayrollModal();
    });
}

async function openPayrollModal(payrollId = null) {
    const modal = document.getElementById('payrollModal');
    const form = document.getElementById('payrollForm');
    const title = document.getElementById('payrollModalTitle');
    
    // Cargar locale si no está cargado
    if (!i18n.translations || Object.keys(i18n.translations).length === 0) {
        await i18n.loadLocale('GT');
    }
    const t = i18n.translations;
    
    form.reset();
    document.getElementById('payrollId').value = '';
    
    const today = new Date();
    document.getElementById('payrollPeriodInput').value = 
        `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, '0')}`;
    
    if (payrollId) {
        title.textContent = `Editar ${t.payroll || 'Nómina'}`;
        await loadPayrollData(payrollId);
    } else {
        title.textContent = `Nueva ${t.payroll || 'Nómina'}`;
    }
    
    modal.classList.add('active');
}

function closePayrollModal() {
    document.getElementById('payrollModal').classList.remove('active');
}

async function loadPayrollData(id) {
    try {
        showLoading();
        const response = await payrollsAPI.getById(id);
        
        if (response.success) {
            const payroll = response.data;
            document.getElementById('payrollId').value = payroll.id;
            document.getElementById('payrollEmployeeId').value = payroll.employee_id;
            document.getElementById('payrollPeriodInput').value = payroll.period + '-01';
            document.getElementById('payrollHoursWorked').value = payroll.hours_worked || 0;
            document.getElementById('payrollOvertimeHours').value = payroll.overtime_hours || 0;
            document.getElementById('payrollBaseSalary').value = payroll.base_salary || 0;
            document.getElementById('payrollBonuses').value = payroll.bonuses || 0;
            document.getElementById('payrollDeductions').value = payroll.deductions || 0;
            document.getElementById('payrollStatus').value = payroll.status || 'pending';
            document.getElementById('payrollPaymentDate').value = payroll.payment_date || '';
            document.getElementById('payrollBankTransferId').value = payroll.bank_transfer_id || '';
            document.getElementById('payrollNotes').value = payroll.notes || '';
        }
    } catch (error) {
        showNotification('Error al cargar nómina: ' + error.message, 'error');
    } finally {
        hideLoading();
    }
}

async function calculatePayroll() {
    const employeeId = document.getElementById('payrollEmployeeId').value;
    const period = document.getElementById('payrollPeriodInput').value;
    
    if (!employeeId || !period) {
        showNotification('Por favor seleccione empleado y período', 'warning');
        return;
    }
    
    try {
        showLoading();
        const periodFormatted = period.substring(0, 7); // YYYY-MM
        const response = await payrollsAPI.calculate({
            employee_id: parseInt(employeeId),
            period: periodFormatted,
            bonuses: parseFloat(document.getElementById('payrollBonuses').value) || 0,
            deductions: parseFloat(document.getElementById('payrollDeductions').value) || 0,
        });
        
        if (response.success) {
            const data = response.data;
            document.getElementById('payrollHoursWorked').value = data.hours_worked || 0;
            document.getElementById('payrollOvertimeHours').value = data.overtime_hours || 0;
            document.getElementById('payrollBaseSalary').value = data.base_salary || 0;
            document.getElementById('payrollBonuses').value = data.bonuses || 0;
            document.getElementById('payrollDeductions').value = data.deductions || 0;
            
            if (response.summary) {
                showNotification(
                    `Cálculo completado: ${response.summary.regular_hours}h regulares, ` +
                    `${response.summary.overtime_hours}h extras`,
                    'success'
                );
            }
        }
    } catch (error) {
        showNotification('Error al calcular nómina: ' + error.message, 'error');
    } finally {
        hideLoading();
    }
}

async function savePayroll() {
    try {
        showLoading();
        const id = document.getElementById('payrollId').value;
        const period = document.getElementById('payrollPeriodInput').value;
        const periodFormatted = period.substring(0, 7); // YYYY-MM
        
        const data = {
            employee_id: parseInt(document.getElementById('payrollEmployeeId').value),
            period: periodFormatted,
            hours_worked: parseFloat(document.getElementById('payrollHoursWorked').value) || 0,
            overtime_hours: parseFloat(document.getElementById('payrollOvertimeHours').value) || 0,
            base_salary: parseFloat(document.getElementById('payrollBaseSalary').value) || 0,
            bonuses: parseFloat(document.getElementById('payrollBonuses').value) || 0,
            deductions: parseFloat(document.getElementById('payrollDeductions').value) || 0,
            status: document.getElementById('payrollStatus').value,
            payment_date: document.getElementById('payrollPaymentDate').value || null,
            bank_transfer_id: document.getElementById('payrollBankTransferId').value || null,
            notes: document.getElementById('payrollNotes').value || null,
        };
        
        let response;
        if (id) {
            response = await payrollsAPI.update(id, data);
        } else {
            response = await payrollsAPI.create(data);
        }
        
        if (response.success) {
            const t = i18n.translations;
            showNotification(response.message || `${t.payroll || 'Nómina'} guardada exitosamente`, 'success');
            closePayrollModal();
            loadPayrolls();
        }
    } catch (error) {
        showNotification('Error al guardar nómina: ' + error.message, 'error');
    } finally {
        hideLoading();
    }
}

async function editPayroll(id) {
    openPayrollModal(id);
}

async function deletePayroll(id) {
    // Cargar locale si no está cargado
    if (!i18n.translations || Object.keys(i18n.translations).length === 0) {
        await i18n.loadLocale('GT');
    }
    const t = i18n.translations;
    
    if (!confirm(`¿Está seguro de eliminar esta ${t.payroll || 'nómina'}?`)) return;
    
    try {
        showLoading();
        const response = await payrollsAPI.delete(id);
        
        if (response.success) {
            showNotification(`${t.payroll || 'Nómina'} eliminada exitosamente`, 'success');
            loadPayrolls();
        }
    } catch (error) {
        showNotification(`Error al eliminar ${t.payroll || 'nómina'}: ` + error.message, 'error');
    } finally {
        hideLoading();
    }
}

// Filter buttons
function initFilters() {
    document.getElementById('filterAttendancesBtn')?.addEventListener('click', loadAttendances);
    document.getElementById('filterPayrollsBtn')?.addEventListener('click', loadPayrolls);
}

// Initialize App
document.addEventListener('DOMContentLoaded', async () => {
    // Cargar locale por defecto
    await i18n.loadLocale('GT');
    
    // Actualizar textos de la interfaz
    updateUITexts();
    
    initNavigation();
    initEmployeeModal();
    initEmployeeFilters();
    initAttendanceModal();
    initPayrollModal();
    initFilters();
    
    // Load initial page
    loadPageData('dashboard');
});

// Make functions globally available
window.editEmployee = editEmployee;
window.deleteEmployee = deleteEmployee;
window.editAttendance = editAttendance;
window.deleteAttendance = deleteAttendance;
window.editPayroll = editPayroll;
window.deletePayroll = deletePayroll;

