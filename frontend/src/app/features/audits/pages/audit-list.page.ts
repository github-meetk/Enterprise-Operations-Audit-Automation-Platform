import { AsyncPipe, DatePipe, TitleCasePipe } from '@angular/common';
import { ChangeDetectionStrategy, Component, inject, signal } from '@angular/core';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatSelectModule } from '@angular/material/select';
import { MatTableModule } from '@angular/material/table';
import { switchMap } from 'rxjs';
import { toObservable } from '@angular/core/rxjs-interop';

import { PlatformApiService } from '../../../core/api/platform-api.service';

@Component({
  standalone: true,
  imports: [AsyncPipe, DatePipe, MatCardModule, MatFormFieldModule, MatSelectModule, MatTableModule, TitleCasePipe],
  template: `
    <header class="page-heading">
      <div><span>Audit & compliance</span><h2>Audit Portfolio</h2><p>Track lifecycle, ownership, and risk exposure.</p></div>
      <mat-form-field appearance="outline"><mat-label>Status</mat-label>
        <mat-select [value]="status()" (valueChange)="status.set($event)">
          <mat-option value="">All statuses</mat-option>
          @for (option of statuses; track option) { <mat-option [value]="option">{{ option | titlecase }}</mat-option> }
        </mat-select>
      </mat-form-field>
    </header>
    <mat-card>
      <table mat-table [dataSource]="(audits$ | async) ?? []">
        <ng-container matColumnDef="reference"><th mat-header-cell *matHeaderCellDef>Reference</th><td mat-cell *matCellDef="let row">{{ row.reference }}</td></ng-container>
        <ng-container matColumnDef="title"><th mat-header-cell *matHeaderCellDef>Audit</th><td mat-cell *matCellDef="let row"><strong>{{ row.title }}</strong><small>{{ row.audit_type | titlecase }}</small></td></ng-container>
        <ng-container matColumnDef="risk"><th mat-header-cell *matHeaderCellDef>Risk</th><td mat-cell *matCellDef="let row"><span class="chip" [class.danger]="row.risk_level === 'high' || row.risk_level === 'critical'">{{ row.risk_level | titlecase }}</span></td></ng-container>
        <ng-container matColumnDef="status"><th mat-header-cell *matHeaderCellDef>Status</th><td mat-cell *matCellDef="let row">{{ row.status | titlecase }}</td></ng-container>
        <ng-container matColumnDef="due"><th mat-header-cell *matHeaderCellDef>Planned end</th><td mat-cell *matCellDef="let row">{{ row.planned_end_at ? (row.planned_end_at | date) : 'Not scheduled' }}</td></ng-container>
        <tr mat-header-row *matHeaderRowDef="columns"></tr><tr mat-row *matRowDef="let row; columns: columns"></tr>
      </table>
    </mat-card>
  `,
  styles: `
    mat-card { border: 1px solid #e0e6ec; box-shadow: none; overflow: hidden; } table { width: 100%; }
    td, th { color: #40566a; } td small { display: block; color: #7d8d9c; margin-top: 4px; }
    .chip { padding: 4px 9px; border-radius: 12px; background: #e8f2f8; color: #286385; font-size: 12px; }
    .danger { background: #fbe7e7; color: #a33434; }
  `,
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class AuditListPage {
  private readonly api = inject(PlatformApiService);
  readonly status = signal('');
  readonly audits$ = toObservable(this.status).pipe(switchMap((status) => this.api.audits(status)));
  readonly statuses = ['draft', 'planned', 'in_progress', 'under_review', 'approved', 'closed'];
  readonly columns = ['reference', 'title', 'risk', 'status', 'due'];
}
