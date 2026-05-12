from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import pyodbc

app = FastAPI()

DB_CONFIG = {
    "server": "database-2.cza4ek4s8hav.us-east-2.rds.amazonaws.com,1433",
    "username": "admin",
    "password": "admin1234",
    "database": "Productos"
}

class ProductoCreate(BaseModel):
    nombre_producto: str = Field(..., max_length=100)
    descripcion: Optional[str] = Field(None, max_length=255)
    precio: float = Field(..., gt=0)
    stock: int = Field(..., ge=0)
    categoria: Optional[str] = Field(None, max_length=50)

class ProductoUpdate(BaseModel):
    nombre_producto: Optional[str] = Field(None, max_length=100)
    descripcion: Optional[str] = Field(None, max_length=255)
    precio: Optional[float] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)
    categoria: Optional[str] = Field(None, max_length=50)

class ProductoResponse(BaseModel):
    id_producto: int
    nombre_producto: str
    descripcion: Optional[str]
    precio: float
    stock: int
    categoria: Optional[str]
    fecha_creacion: datetime

def get_db_connection():
    connection_string = (
        f"DRIVER={{ODBC Driver 18 for SQL Server}};"
        f"SERVER={DB_CONFIG['server']};"
        f"DATABASE={DB_CONFIG['database']};"
        f"UID={DB_CONFIG['username']};"
        f"PWD={DB_CONFIG['password']};"
        f"TrustServerCertificate=yes;"
        f"Encrypt=yes;"
    )
    return pyodbc.connect(connection_string, timeout=10)

@app.get("/health")
def health():
    return {"status": "ok"}
def inicio():

@app.get("/")
    return {"message": "¡Hola, Mundo! FastApi"}

@app.get("/health/db")
def check_db_connection():
    import time
    start_time = time.time()
    
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT @@VERSION;")
        version = cursor.fetchone()[0]
        cursor.execute("SELECT DB_NAME(), SYSTEM_USER;")
        db_info = cursor.fetchone()
        cursor.close()
        connection.close()
        
        elapsed_time = time.time() - start_time
        
        return {
            "status": "success",
            "message": "Conexión a AWS RDS SQL Server exitosa",
            "database": db_info[0] if db_info[0] else "master",
            "user": db_info[1],
            "version": version.split('\n')[0],
            "region": "us-east-2",
            "connection_time_seconds": round(elapsed_time, 2)
        }
    except pyodbc.Error as e:
        elapsed_time = time.time() - start_time
        error_msg = str(e)
        
        if "timeout" in error_msg.lower() or "timed out" in error_msg.lower():
            diagnosis = "Timeout de conexión - Posibles causas: Security Group bloqueando puerto 1433, Network ACL, o Route Table sin IGW"
        elif "login failed" in error_msg.lower() or "authentication" in error_msg.lower():
            diagnosis = "Error de autenticación - Verificar usuario/contraseña"
        elif "could not translate" in error_msg.lower() or "name or service not known" in error_msg.lower():
            diagnosis = "Error DNS - No se puede resolver el hostname"
        else:
            diagnosis = "Error de conexión general"
        
        return {
            "status": "error",
            "message": f"Error al conectar a la base de datos: {error_msg}",
            "diagnosis": diagnosis,
            "connection_time_seconds": round(elapsed_time, 2)
        }
    except Exception as e:
        elapsed_time = time.time() - start_time
        return {
            "status": "error",
            "message": f"Error inesperado: {str(e)}",
            "connection_time_seconds": round(elapsed_time, 2)
        }

@app.post("/productos", response_model=ProductoResponse, status_code=201)
def crear_producto(producto: ProductoCreate):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        query = """
        INSERT INTO Producto (nombre_producto, descripcion, precio, stock, categoria)
        OUTPUT INSERTED.id_producto, INSERTED.nombre_producto, INSERTED.descripcion, 
               INSERTED.precio, INSERTED.stock, INSERTED.categoria, INSERTED.fecha_creacion
        VALUES (?, ?, ?, ?, ?)
        """
        
        cursor.execute(query, (
            producto.nombre_producto,
            producto.descripcion,
            producto.precio,
            producto.stock,
            producto.categoria
        ))
        
        row = cursor.fetchone()
        connection.commit()
        cursor.close()
        connection.close()
        
        return ProductoResponse(
            id_producto=row[0],
            nombre_producto=row[1],
            descripcion=row[2],
            precio=float(row[3]),
            stock=row[4],
            categoria=row[5],
            fecha_creacion=row[6]
        )
    except pyodbc.Error as e:
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

@app.get("/productos", response_model=List[ProductoResponse])
def listar_productos():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        query = """
        SELECT id_producto, nombre_producto, descripcion, precio, stock, categoria, fecha_creacion
        FROM Producto
        ORDER BY id_producto DESC
        """
        
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        
        productos = [
            ProductoResponse(
                id_producto=row[0],
                nombre_producto=row[1],
                descripcion=row[2],
                precio=float(row[3]),
                stock=row[4],
                categoria=row[5],
                fecha_creacion=row[6]
            )
            for row in rows
        ]
        
        return productos
    except pyodbc.Error as e:
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

@app.get("/productos/{id_producto}", response_model=ProductoResponse)
def obtener_producto(id_producto: int):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        query = """
        SELECT id_producto, nombre_producto, descripcion, precio, stock, categoria, fecha_creacion
        FROM Producto
        WHERE id_producto = ?
        """
        
        cursor.execute(query, (id_producto,))
        row = cursor.fetchone()
        cursor.close()
        connection.close()
        
        if not row:
            raise HTTPException(status_code=404, detail=f"Producto con id {id_producto} no encontrado")
        
        return ProductoResponse(
            id_producto=row[0],
            nombre_producto=row[1],
            descripcion=row[2],
            precio=float(row[3]),
            stock=row[4],
            categoria=row[5],
            fecha_creacion=row[6]
        )
    except HTTPException:
        raise
    except pyodbc.Error as e:
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

@app.put("/productos/{id_producto}", response_model=ProductoResponse)
def actualizar_producto(id_producto: int, producto: ProductoUpdate):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        cursor.execute("SELECT id_producto FROM Producto WHERE id_producto = ?", (id_producto,))
        if not cursor.fetchone():
            cursor.close()
            connection.close()
            raise HTTPException(status_code=404, detail=f"Producto con id {id_producto} no encontrado")
        
        update_fields = []
        params = []
        
        if producto.nombre_producto is not None:
            update_fields.append("nombre_producto = ?")
            params.append(producto.nombre_producto)
        if producto.descripcion is not None:
            update_fields.append("descripcion = ?")
            params.append(producto.descripcion)
        if producto.precio is not None:
            update_fields.append("precio = ?")
            params.append(producto.precio)
        if producto.stock is not None:
            update_fields.append("stock = ?")
            params.append(producto.stock)
        if producto.categoria is not None:
            update_fields.append("categoria = ?")
            params.append(producto.categoria)
        
        if not update_fields:
            cursor.close()
            connection.close()
            raise HTTPException(status_code=400, detail="No se proporcionaron campos para actualizar")
        
        params.append(id_producto)
        
        query = f"""
        UPDATE Producto
        SET {', '.join(update_fields)}
        WHERE id_producto = ?
        """
        
        cursor.execute(query, params)
        connection.commit()
        
        cursor.execute("""
            SELECT id_producto, nombre_producto, descripcion, precio, stock, categoria, fecha_creacion
            FROM Producto
            WHERE id_producto = ?
        """, (id_producto,))
        
        row = cursor.fetchone()
        cursor.close()
        connection.close()
        
        return ProductoResponse(
            id_producto=row[0],
            nombre_producto=row[1],
            descripcion=row[2],
            precio=float(row[3]),
            stock=row[4],
            categoria=row[5],
            fecha_creacion=row[6]
        )
    except HTTPException:
        raise
    except pyodbc.Error as e:
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

@app.delete("/productos/{id_producto}", status_code=204)
def eliminar_producto(id_producto: int):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        cursor.execute("SELECT id_producto FROM Producto WHERE id_producto = ?", (id_producto,))
        if not cursor.fetchone():
            cursor.close()
            connection.close()
            raise HTTPException(status_code=404, detail=f"Producto con id {id_producto} no encontrado")
        
        cursor.execute("DELETE FROM Producto WHERE id_producto = ?", (id_producto,))
        connection.commit()
        cursor.close()
        connection.close()
        
        return None
    except HTTPException:
        raise
    except pyodbc.Error as e:
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")


