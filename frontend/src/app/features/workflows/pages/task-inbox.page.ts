import { AsyncPipe, DatePipe, TitleCasePipe } from '@angular/common';
import { ChangeDetectionStrategy, Component, inject } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { BehaviorSubject, switchMap } from 'rxjs';

import { PlatformApiService } from '../../../core/api/platform-api.service';

@Component({
  standalone: true,
  imports: [AsyncPipe, DatePipe, MatButtonModule, MatCardModule, TitleCasePipe],
  template: `
    <header class="page-heading"><div><span>Workflow automation</span><h2>Approval Inbox</h2><p>Review assigned decisions before SLA thresholds are reached.</p></div></header>
    <section class="task-list">
      @for (task of (tasks$ | async) ?? []; track task.id) {
        <mat-card>
          <div><span class="chip">{{ task.status | titlecase }}</span><h3>{{ task.title }}</h3>
            <p>{{ task.due_at ? 'Due ' + (task.due_at | date:'medium') : 'No SLA deadline assigned' }}</p></div>
          @if (task.status === 'pending') {
            <div class="actions"><button mat-stroked-button (click)="act(task.id, 'reject')">Reject</button>
              <button mat-flat-button color="primary" (click)="act(task.id, 'approve')">Approve</button></div>
          }
        </mat-card>
      } @empty { <mat-card><p>Your approval queue is clear.</p></mat-card> }
    </section>
  `,
  styles: `
    .task-list { display: grid; gap: 12px; } mat-card { display: flex; justify-content: space-between;
      align-items: center; padding: 18px; border: 1px solid #e0e6ec; box-shadow: none; }
    h3 { margin: 10px 0 4px; color: #243e55; } p { margin: 0; color: #718395; }
    .chip { color: #27628b; background: #e6f1f8; padding: 4px 9px; border-radius: 12px; font-size: 12px; }
    .actions { display: flex; gap: 10px; }
  `,
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class TaskInboxPage {
  private readonly api = inject(PlatformApiService);
  private readonly refresh = new BehaviorSubject<void>(undefined);
  readonly tasks$ = this.refresh.pipe(switchMap(() => this.api.workflowTasks()));

  act(taskId: string, action: 'approve' | 'reject'): void {
    this.api.actionTask(taskId, action).subscribe(() => this.refresh.next());
  }
}
