# Configuración del Application Load Balancer (ALB)

## Problema Actual

El ALB está enviando `/productos` a Angular en lugar de FastAPI, por eso recibes HTML en lugar de JSON.

## Solución: Configurar Reglas de Enrutamiento

### 1. Ir a la Consola de AWS EC2 → Load Balancers

1. Busca tu Load Balancer: `lbs-pvpv2-1330869850`
2. Ve a la pestaña **"Listeners"**
3. Selecciona el listener HTTP:80 (o HTTPS:443)
4. Click en **"View/edit rules"**

### 2. Configurar las Reglas en este Orden

**Regla 1: API Routes (Prioridad 1)**
- **Condición:** Path is `/api/*`
- **Acción:** Forward to → Target Group de FastAPI (`tg-fastapi`)

**Regla 2: Health Checks (Prioridad 2)**
- **Condición:** Path is `/health*`
- **Acción:** Forward to → Target Group de FastAPI (`tg-fastapi`)

**Regla 3: Docs (Prioridad 3)**
- **Condición:** Path is `/docs` OR Path is `/redoc` OR Path is `/openapi.json`
- **Acción:** Forward to → Target Group de FastAPI (`tg-fastapi`)

**Regla 4: Default (Prioridad última)**
- **Condición:** Default (todas las demás rutas)
- **Acción:** Forward to → Target Group de Angular

### 3. Resultado Esperado

Después de configurar:

- ✅ `http://tu-alb.com/api/productos` → FastAPI (JSON)
- ✅ `http://tu-alb.com/health` → FastAPI (JSON)
- ✅ `http://tu-alb.com/api/docs` → FastAPI Swagger UI
- ✅ `http://tu-alb.com/` → Angular (HTML)
- ✅ `http://tu-alb.com/productos` → Angular (HTML - para la UI)

## Endpoints de la API

### FastAPI (Backend)
- `GET /api/productos` - Listar productos
- `POST /api/productos` - Crear producto
- `GET /api/productos/{id}` - Obtener producto
- `PUT /api/productos/{id}` - Actualizar producto
- `DELETE /api/productos/{id}` - Eliminar producto
- `GET /health` - Health check
- `GET /api/docs` - Documentación Swagger

### Angular (Frontend)
- `/*` - Todas las demás rutas (UI de Angular)

## Verificación

Después de configurar, prueba:

```bash
# Debe devolver JSON de FastAPI
curl http://lbs-pvpv2-1330869850.us-east-2.elb.amazonaws.com/api/productos

# Debe devolver HTML de Angular
curl http://lbs-pvpv2-1330869850.us-east-2.elb.amazonaws.com/
```

## Alternativa: Si no puedes modificar el ALB

Si no puedes modificar las reglas del ALB, asegúrate de que Angular **siempre** use la URL completa con `/api`:

```typescript
private apiUrl = 'http://lbs-pvpv2-1330869850.us-east-2.elb.amazonaws.com/api/productos';
```

Y **nunca** accedas directamente a `/productos` sin el prefijo `/api`.
