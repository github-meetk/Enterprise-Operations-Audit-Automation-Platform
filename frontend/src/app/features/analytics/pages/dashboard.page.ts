import { AsyncPipe, TitleCasePipe } from '@angular/common';
import { ChangeDetectionStrategy, Component, inject } from '@angular/core';
import { MatCardModule } from '@angular/material/card';
import { MatProgressBarModule } from '@angular/material/progress-bar';

import { PlatformApiService } from '../../../core/api/platform-api.service';

@Component({
  standalone: true,
  imports: [AsyncPipe, MatCardModule, MatProgressBarModule, TitleCasePipe],
  template: `
    <header class="page-heading"><div><span>Executive overview</span><h2>Operational Dashboard</h2></div></header>
    @if (summary$ | async; as summary) {
      <section class="metrics">
        @for (metric of metrics(summary); track metric.label) {
          <mat-card><span>{{ metric.label }}</span><strong>{{ metric.value }}</strong><small>{{ metric.note }}</small></mat-card>
        }
      </section>
      <section class="dashboard-grid">
        <mat-card class="panel">
          <h3>Audit Portfolio</h3><p>Lifecycle distribution across active compliance programs.</p>
          @for (status of entries(summary.audit_statuses); track status[0]) {
            <div class="status-row"><span>{{ status[0] | titlecase }}</span><b>{{ status[1] }}</b></div>
            <mat-progress-bar mode="determinate" [value]="summary.total_audits ? status[1] / summary.total_audits * 100 : 0" />
          }
        </mat-card>
        <mat-card class="panel">
          <h3>Operations Watchlist</h3><p>Queues requiring management attention.</p>
          <div class="watch"><span>Pending approval tasks</span><b>{{ summary.pending_workflow_tasks }}</b></div>
          <div class="watch"><span>Leave requests submitted</span><b>{{ summary.submitted_leave_requests }}</b></div>
          <div class="watch"><span>Expense claims submitted</span><b>{{ summary.submitted_expense_requests }}</b></div>
        </mat-card>
      </section>
    }
  `,
  styles: `
    .metrics { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin: 18px 0 24px; }
    mat-card { padding: 18px; border: 1px solid #e0e6ec; box-shadow: none; }
    mat-card span, small { color: #687d90; } strong { display: block; margin: 12px 0 4px; font-size: 30px; color: #173652; }
    .dashboard-grid { display: grid; grid-template-columns: 1.2fr .8fr; gap: 18px; }
    .panel h3 { margin: 0; }.panel p { color: #718395; }
    .status-row, .watch { display: flex; justify-content: space-between; padding: 12px 0 7px; }
    .watch { border-bottom: 1px solid #e6eaee; }
  `,
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class DashboardPage {
  private readonly api = inject(PlatformApiService);
  readonly summary$ = this.api.dashboard();
  readonly entries = Object.entries;
  metrics(summary: { total_audits: number; open_audits: number; high_risk_audits: number; pending_workflow_tasks: number }) {
    return [
      { label: 'Total audits', value: summary.total_audits, note: 'Portfolio coverage' },
      { label: 'Open audits', value: summary.open_audits, note: 'Active lifecycle items' },
      { label: 'High risk audits', value: summary.high_risk_audits, note: 'Priority remediation' },
      { label: 'Pending approvals', value: summary.pending_workflow_tasks, note: 'Workflow task queue' },
    ];
  }
}
