import requests
import json

BASE_URL = "http://localhost:8000"

def test_crear_producto():
    print("\n=== TEST: Crear Producto ===")
    producto = {
        "nombre_producto": "Laptop Dell XPS 15",
        "descripcion": "Laptop de alto rendimiento",
        "precio": 1299.99,
        "stock": 10,
        "categoria": "Electrónica"
    }
    
    response = requests.post(f"{BASE_URL}/productos", json=producto)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    return response.json()

def test_listar_productos():
    print("\n=== TEST: Listar Productos ===")
    response = requests.get(f"{BASE_URL}/productos")
    print(f"Status: {response.status_code}")
    print(f"Total productos: {len(response.json())}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    return response.json()

def test_obtener_producto(id_producto):
    print(f"\n=== TEST: Obtener Producto {id_producto} ===")
    response = requests.get(f"{BASE_URL}/productos/{id_producto}")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    return response.json()

def test_actualizar_producto(id_producto):
    print(f"\n=== TEST: Actualizar Producto {id_producto} ===")
    actualizacion = {
        "precio": 1199.99,
        "stock": 15
    }
    
    response = requests.put(f"{BASE_URL}/productos/{id_producto}", json=actualizacion)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    return response.json()

def test_eliminar_producto(id_producto):
    print(f"\n=== TEST: Eliminar Producto {id_producto} ===")
    response = requests.delete(f"{BASE_URL}/productos/{id_producto}")
    print(f"Status: {response.status_code}")
    print("Producto eliminado exitosamente" if response.status_code == 204 else "Error al eliminar")

if __name__ == "__main__":
    try:
        print("Iniciando pruebas del CRUD de Productos...")
        
        producto_creado = test_crear_producto()
        id_producto = producto_creado["id_producto"]
        
        test_listar_productos()
        
        test_obtener_producto(id_producto)
        
        test_actualizar_producto(id_producto)
        
        test_obtener_producto(id_producto)
        
        test_eliminar_producto(id_producto)
        
        test_listar_productos()
        
        print("\n✅ Todas las pruebas completadas!")
        
    except Exception as e:
        print(f"\n❌ Error en las pruebas: {str(e)}")
