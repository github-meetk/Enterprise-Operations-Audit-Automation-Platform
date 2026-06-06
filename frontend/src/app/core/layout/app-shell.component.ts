import { ChangeDetectionStrategy, Component } from '@angular/core';
import { MatIconModule } from '@angular/material/icon';
import { MatListModule } from '@angular/material/list';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatToolbarModule } from '@angular/material/toolbar';
import { RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-shell',
  standalone: true,
  imports: [
    MatIconModule,
    MatListModule,
    MatSidenavModule,
    MatToolbarModule,
    RouterLink,
    RouterLinkActive,
    RouterOutlet,
  ],
  template: `
    <mat-sidenav-container class="shell">
      <mat-sidenav mode="side" opened class="sidebar">
        <div class="brand">
          <div class="brand-mark">EO</div>
          <div><strong>Enterprise Ops</strong><span>Governance Platform</span></div>
        </div>
        <mat-nav-list>
          @for (item of navigation; track item.path) {
            <a mat-list-item [routerLink]="item.path" routerLinkActive="active">
              <mat-icon matListItemIcon>{{ item.icon }}</mat-icon>
              <span matListItemTitle>{{ item.label }}</span>
            </a>
          }
        </mat-nav-list>
        <div class="sidebar-footer">Internal systems workspace</div>
      </mat-sidenav>
      <mat-sidenav-content>
        <mat-toolbar class="topbar">
          <div>
            <span class="eyebrow">Operations control center</span>
            <h1>Enterprise Operations & Audit</h1>
          </div>
          <div class="topbar-actions">
            <mat-icon>notifications_none</mat-icon>
            <span class="avatar">PA</span>
          </div>
        </mat-toolbar>
        <main class="page"><router-outlet /></main>
      </mat-sidenav-content>
    </mat-sidenav-container>
  `,
  styles: `
    .shell { min-height: 100vh; background: #f4f6f8; }
    .sidebar { width: 252px; background: #11263d; color: #eef5fb; padding: 18px 12px; }
    .brand { display: flex; gap: 10px; align-items: center; padding: 4px 8px 22px; }
    .brand-mark { display: grid; place-items: center; width: 38px; height: 38px; border-radius: 8px;
      background: #2e75b6; font-weight: 700; }
    .brand span, .eyebrow { display: block; color: #8fa4b8; font-size: 11px; letter-spacing: .08em;
      text-transform: uppercase; }
    a { color: #c7d5e2 !important; border-radius: 6px; margin: 4px 0; }
    a.active { background: #1d3b58 !important; color: white !important; }
    .sidebar-footer { position: absolute; bottom: 18px; left: 20px; color: #8295a8; font-size: 12px; }
    .topbar { min-height: 76px; height: 76px; display: flex; justify-content: space-between;
      background: white; border-bottom: 1px solid #dce3ea; padding: 0 28px; }
    h1 { margin: 2px 0 0; color: #1b2d40; font-size: 19px; font-weight: 600; }
    .topbar-actions { display: flex; align-items: center; gap: 20px; color: #486177; }
    .avatar { display: grid; place-items: center; width: 34px; height: 34px; border-radius: 50%;
      background: #d9e8f5; color: #1e5c92; font-size: 12px; font-weight: 700; }
    .page { padding: 28px; }
  `,
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class AppShellComponent {
  readonly navigation = [
    { path: '/dashboard', label: 'Dashboard', icon: 'space_dashboard' },
    { path: '/audits', label: 'Audits & Compliance', icon: 'fact_check' },
    { path: '/approvals', label: 'Approval Inbox', icon: 'approval' },
    { path: '/operations', label: 'Employee Operations', icon: 'business_center' },
  ];
}
