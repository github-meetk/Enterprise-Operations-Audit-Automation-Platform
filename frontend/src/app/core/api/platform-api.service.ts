import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

import { environment } from '../../../environments/environment';

export interface DashboardSummary {
  total_audits: number;
  open_audits: number;
  high_risk_audits: number;
  pending_workflow_tasks: number;
  submitted_leave_requests: number;
  submitted_expense_requests: number;
  audit_statuses: Record<string, number>;
}

export interface Audit {
  id: string;
  reference: string;
  title: string;
  audit_type: string;
  status: string;
  risk_level: string;
  risk_score: number;
  department_id: string;
  lead_auditor_id: string | null;
  planned_end_at: string | null;
}

export interface WorkflowTask {
  id: string;
  instance_id: string;
  title: string;
  status: string;
  due_at: string | null;
}

export interface LeaveRequest {
  id: string;
  requester_id: string;
  department_id: string;
  leave_type: string;
  start_date: string;
  end_date: string;
  status: string;
}

@Injectable({ providedIn: 'root' })
export class PlatformApiService {
  constructor(private readonly http: HttpClient) {}

  dashboard(): Observable<DashboardSummary> {
    return this.http.get<DashboardSummary>(`${environment.apiUrl}/analytics/dashboard`);
  }

  audits(status = ''): Observable<Audit[]> {
    const params = status ? new HttpParams().set('status', status) : undefined;
    return this.http.get<Audit[]>(`${environment.apiUrl}/audits`, { params });
  }

  workflowTasks(): Observable<WorkflowTask[]> {
    return this.http.get<WorkflowTask[]>(`${environment.apiUrl}/workflow-tasks/mine`);
  }

  actionTask(taskId: string, action: 'approve' | 'reject'): Observable<WorkflowTask> {
    return this.http.post<WorkflowTask>(`${environment.apiUrl}/workflow-tasks/${taskId}/actions`, {
      action,
    });
  }

  leaveRequests(): Observable<LeaveRequest[]> {
    return this.http.get<LeaveRequest[]>(`${environment.apiUrl}/operations/leave-requests/mine`);
  }

  createLeaveRequest(payload: {
    department_id: string;
    leave_type: string;
    start_date: string;
    end_date: string;
    reason: string;
  }): Observable<LeaveRequest> {
    return this.http.post<LeaveRequest>(`${environment.apiUrl}/operations/leave-requests`, payload);
  }
}
