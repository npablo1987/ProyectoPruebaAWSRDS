import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ProductoService } from '../../services/producto.service';
import { Producto, ProductoCreate, ProductoUpdate } from '../../models/producto.model';

@Component({
  selector: 'app-producto-list',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './producto-list.component.html',
  styleUrls: ['./producto-list.component.css']
})
export class ProductoListComponent implements OnInit {
  productos: Producto[] = [];
  loading = false;
  error: string | null = null;
  success: string | null = null;
  
  showForm = false;
  isEditing = false;
  currentProductoId: number | null = null;
  
  formData: ProductoCreate = {
    nombre_producto: '',
    descripcion: '',
    precio: 0,
    stock: 0,
    categoria: ''
  };

  constructor(private productoService: ProductoService) {}

  ngOnInit(): void {
    this.loadProductos();
  }

  loadProductos(): void {
    this.loading = true;
    this.error = null;
    
    this.productoService.getProductos().subscribe({
      next: (data) => {
        this.productos = data;
        this.loading = false;
      },
      error: (err) => {
        this.error = 'Error al cargar los productos: ' + err.message;
        this.loading = false;
      }
    });
  }

  openCreateForm(): void {
    this.showForm = true;
    this.isEditing = false;
    this.currentProductoId = null;
    this.resetForm();
  }

  openEditForm(producto: Producto): void {
    this.showForm = true;
    this.isEditing = true;
    this.currentProductoId = producto.id_producto;
    this.formData = {
      nombre_producto: producto.nombre_producto,
      descripcion: producto.descripcion || '',
      precio: producto.precio,
      stock: producto.stock,
      categoria: producto.categoria || ''
    };
  }

  closeForm(): void {
    this.showForm = false;
    this.resetForm();
  }

  resetForm(): void {
    this.formData = {
      nombre_producto: '',
      descripcion: '',
      precio: 0,
      stock: 0,
      categoria: ''
    };
    this.error = null;
    this.success = null;
  }

  onSubmit(): void {
    if (this.isEditing && this.currentProductoId) {
      this.updateProducto();
    } else {
      this.createProducto();
    }
  }

  createProducto(): void {
    this.loading = true;
    this.error = null;
    
    this.productoService.createProducto(this.formData).subscribe({
      next: (producto) => {
        this.success = 'Producto creado exitosamente';
        this.loadProductos();
        this.closeForm();
        setTimeout(() => this.success = null, 3000);
      },
      error: (err) => {
        this.error = 'Error al crear el producto: ' + err.message;
        this.loading = false;
      }
    });
  }

  updateProducto(): void {
    if (!this.currentProductoId) return;
    
    this.loading = true;
    this.error = null;
    
    const updateData: ProductoUpdate = { ...this.formData };
    
    this.productoService.updateProducto(this.currentProductoId, updateData).subscribe({
      next: (producto) => {
        this.success = 'Producto actualizado exitosamente';
        this.loadProductos();
        this.closeForm();
        setTimeout(() => this.success = null, 3000);
      },
      error: (err) => {
        this.error = 'Error al actualizar el producto: ' + err.message;
        this.loading = false;
      }
    });
  }

  deleteProducto(id: number): void {
    if (!confirm('¿Estás seguro de que deseas eliminar este producto?')) {
      return;
    }
    
    this.loading = true;
    this.error = null;
    
    this.productoService.deleteProducto(id).subscribe({
      next: () => {
        this.success = 'Producto eliminado exitosamente';
        this.loadProductos();
        setTimeout(() => this.success = null, 3000);
      },
      error: (err) => {
        this.error = 'Error al eliminar el producto: ' + err.message;
        this.loading = false;
      }
    });
  }

  formatDate(dateString: string): string {
    const date = new Date(dateString);
    return date.toLocaleDateString('es-ES', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  }

  formatPrice(price: number): string {
    return new Intl.NumberFormat('es-ES', {
      style: 'currency',
      currency: 'EUR'
    }).format(price);
  }
}
