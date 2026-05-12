export interface Producto {
  id_producto: number;
  nombre_producto: string;
  descripcion: string | null;
  precio: number;
  stock: number;
  categoria: string | null;
  fecha_creacion: string;
}

export interface ProductoCreate {
  nombre_producto: string;
  descripcion?: string;
  precio: number;
  stock: number;
  categoria?: string;
}

export interface ProductoUpdate {
  nombre_producto?: string;
  descripcion?: string;
  precio?: number;
  stock?: number;
  categoria?: string;
}
