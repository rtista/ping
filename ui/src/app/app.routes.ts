import { Routes } from '@angular/router';
import { AuthGuard } from './login/guards/auth.guard';

export const routes: Routes = [
    { path: '', pathMatch: 'full', redirectTo: '' },
    { 
        path: 'home',
        loadChildren: './home/home.module#HomeModule',
        canActivate: [AuthGuard]
    },
    {
        path: 'login',
        loadChildren: './login/login.module#LoginModule'
    }
];