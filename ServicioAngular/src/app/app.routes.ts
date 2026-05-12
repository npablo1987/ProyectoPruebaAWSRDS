import { Routes } from '@angular/router';
import { ProductoListComponent } from './components/producto-list/producto-list.component';

export const routes: Routes = [
  { path: '', component: ProductoListComponent },
  { path: '**', redirectTo: '' }
];
