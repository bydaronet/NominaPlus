# Frontend NominaPlus

Este proyecto incluye dos frontends diferentes:

## 1. Frontend Administrativo

**Ruta:** `/` (raíz)

Interfaz completa para administradores del sistema con las siguientes funcionalidades:

### Características:
- **Dashboard**: Resumen general con estadísticas de empleados, nóminas y asistencias
- **Gestión de Empleados**: CRUD completo de empleados
- **Control de Asistencias**: Registro y gestión de asistencias
- **Gestión de Nóminas**: Creación, edición y cálculo automático de nóminas
- **Cálculo Automático**: Cálculo de nóminas basado en asistencias registradas

### Tecnologías:
- HTML5
- CSS3 (diseño responsivo con CSS Grid y Flexbox)
- JavaScript Vanilla (sin frameworks)
- Font Awesome para iconos

### Archivos:
- `frontend/index.html` - Página principal
- `frontend/static/css/style.css` - Estilos
- `frontend/static/js/api.js` - Cliente API
- `frontend/static/js/app.js` - Lógica de la aplicación

## 2. Frontend Público (Usuarios Finales)

**Ruta:** `/public`

Interfaz para que los empleados consulten sus pagos, recibos y asistencias.

### Características:
- **Acceso Seguro**: Login con DNI y código de acceso
- **Consulta de Nóminas**: Visualización de todas las nóminas del empleado
- **Detalle de Nóminas**: Desglose completo de cada nómina
- **Consulta de Asistencias**: Historial de asistencias con filtros por mes
- **Estadísticas Personales**: Resumen de nóminas y totales ganados

### Tecnologías:
- HTML5
- CSS3 (diseño moderno y responsivo)
- JavaScript Vanilla

### Archivos:
- `frontend_public/index.html` - Página principal
- `frontend_public/static/css/public.css` - Estilos
- `frontend_public/static/js/public.js` - Lógica de la aplicación

## Acceso

### Frontend Administrativo
```
http://localhost:5000/
```

### Frontend Público
```
http://localhost:5000/public
```

## Autenticación del Frontend Público

**Nota:** Actualmente el frontend público usa un sistema de autenticación simple para demostración:
- **DNI**: Número de identificación del empleado
- **Código de Acceso**: Últimos 4 dígitos del DNI (o "demo" para pruebas)

**⚠️ IMPORTANTE:** En producción, se debe implementar un sistema de autenticación seguro con:
- Tokens JWT
- Encriptación de contraseñas
- Sesiones seguras
- Rate limiting

## Diseño Responsivo

Ambos frontends están completamente optimizados para:
- 📱 Móviles (320px+)
- 📱 Tablets (768px+)
- 💻 Desktop (1024px+)

## Estructura de Carpetas

```
NominaPlus/
├── frontend/              # Frontend administrativo
│   ├── index.html
│   └── static/
│       ├── css/
│       │   └── style.css
│       └── js/
│           ├── api.js
│           └── app.js
│
└── frontend_public/       # Frontend público
    ├── index.html
    └── static/
        ├── css/
        │   └── public.css
        └── js/
            └── public.js
```

## Próximos Pasos

1. **Autenticación Real**: Implementar sistema de autenticación seguro
2. **Exportación de Recibos**: Permitir descargar recibos en PDF
3. **Notificaciones**: Sistema de notificaciones para empleados
4. **Gráficos**: Agregar gráficos y visualizaciones en el dashboard
5. **Búsqueda Avanzada**: Mejorar filtros y búsquedas
6. **Temas**: Sistema de temas claro/oscuro

## Desarrollo

Para desarrollar o modificar los frontends:

1. Los archivos estáticos se sirven automáticamente desde las carpetas `static/`
2. Los cambios en HTML/CSS/JS se reflejan inmediatamente (en modo debug)
3. La API está disponible en `/api/*`

## Notas

- Los frontends consumen la API REST disponible en `/api`
- Todos los endpoints de la API devuelven JSON
- El diseño es moderno y sigue las mejores prácticas de UX/UI
- Compatible con todos los navegadores modernos

