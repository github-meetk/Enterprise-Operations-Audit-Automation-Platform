import { AsyncPipe, DatePipe, TitleCasePipe } from '@angular/common';
import { ChangeDetectionStrategy, Component, inject } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { BehaviorSubject, switchMap } from 'rxjs';

import { PlatformApiService } from '../../../core/api/platform-api.service';

@Component({
  standalone: true,
  imports: [AsyncPipe, DatePipe, MatButtonModule, MatCardModule, MatFormFieldModule, MatInputModule, MatSelectModule, ReactiveFormsModule, TitleCasePipe],
  template: `
    <header class="page-heading"><div><span>Employee operations</span><h2>Request Center</h2><p>Submit internal requests and monitor approvals from one workspace.</p></div></header>
    <section class="ops-grid">
      <mat-card><h3>New leave request</h3><form [formGroup]="form" (ngSubmit)="submit()">
        <mat-form-field appearance="outline"><mat-label>Department ID</mat-label><input matInput formControlName="department_id"></mat-form-field>
        <mat-form-field appearance="outline"><mat-label>Leave type</mat-label><mat-select formControlName="leave_type">
          @for (type of leaveTypes; track type) { <mat-option [value]="type">{{ type | titlecase }}</mat-option> }
        </mat-select></mat-form-field>
        <div class="date-grid"><mat-form-field appearance="outline"><mat-label>Start</mat-label><input matInput type="date" formControlName="start_date"></mat-form-field>
          <mat-form-field appearance="outline"><mat-label>End</mat-label><input matInput type="date" formControlName="end_date"></mat-form-field></div>
        <mat-form-field appearance="outline"><mat-label>Business context</mat-label><textarea matInput formControlName="reason"></textarea></mat-form-field>
        <button mat-flat-button color="primary" [disabled]="form.invalid">Submit request</button>
      </form></mat-card>
      <mat-card><h3>My leave requests</h3>
        @for (request of (requests$ | async) ?? []; track request.id) {
          <div class="request-row"><div><b>{{ request.leave_type | titlecase }} leave</b><span>{{ request.start_date | date }} - {{ request.end_date | date }}</span></div><small>{{ request.status | titlecase }}</small></div>
        } @empty { <p>No leave requests submitted.</p> }
      </mat-card>
    </section>
  `,
  styles: `
    .ops-grid { display: grid; grid-template-columns: .9fr 1.1fr; gap: 18px; } mat-card { padding: 18px; border: 1px solid #e0e6ec; box-shadow: none; }
    form, mat-form-field { display: block; width: 100%; } .date-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
    .request-row { display: flex; justify-content: space-between; padding: 15px 0; border-bottom: 1px solid #e6eaee; }
    .request-row span { display: block; color: #718395; margin-top: 5px; } small { color: #27628b; }
  `,
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class OperationsPage {
  private readonly builder = inject(FormBuilder);
  private readonly api = inject(PlatformApiService);
  private readonly refresh = new BehaviorSubject<void>(undefined);
  readonly requests$ = this.refresh.pipe(switchMap(() => this.api.leaveRequests()));
  readonly leaveTypes = ['annual', 'sick', 'personal', 'unpaid'];
  readonly form = this.builder.nonNullable.group({
    department_id: ['', Validators.required], leave_type: ['annual', Validators.required],
    start_date: ['', Validators.required], end_date: ['', Validators.required], reason: [''],
  });
  submit(): void {
    if (this.form.valid) this.api.createLeaveRequest(this.form.getRawValue()).subscribe(() => {
      this.form.patchValue({ start_date: '', end_date: '', reason: '' }); this.refresh.next();
    });
  }
}
