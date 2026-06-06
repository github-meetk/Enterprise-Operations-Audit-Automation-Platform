import { Routes } from '@angular/router';

import { authGuard } from './core/guards/auth.guard';
import { AppShellComponent } from './core/layout/app-shell.component';

export const routes: Routes = [
  {
    path: 'login',
    loadComponent: () =>
      import('./features/auth/pages/login.page').then((module) => module.LoginPage),
  },
  {
    path: '',
    component: AppShellComponent,
    canActivate: [authGuard],
    children: [
      {
        path: 'dashboard',
        loadComponent: () =>
          import('./features/analytics/pages/dashboard.page').then((module) => module.DashboardPage),
      },
      {
        path: 'audits',
        loadComponent: () =>
          import('./features/audits/pages/audit-list.page').then((module) => module.AuditListPage),
      },
      {
        path: 'approvals',
        loadComponent: () =>
          import('./features/workflows/pages/task-inbox.page').then((module) => module.TaskInboxPage),
      },
      {
        path: 'operations',
        loadComponent: () =>
          import('./features/operations/pages/operations.page').then((module) => module.OperationsPage),
      },
      { path: '', pathMatch: 'full', redirectTo: 'dashboard' },
    ],
  },
  { path: '**', redirectTo: '' },
];
