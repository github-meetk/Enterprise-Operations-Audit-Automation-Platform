import { ChangeDetectionStrategy, Component, inject } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { Store } from '@ngrx/store';

import { AuthActions } from '../../../store/auth/auth.actions';

@Component({
  standalone: true,
  imports: [MatButtonModule, MatCardModule, MatFormFieldModule, MatInputModule, ReactiveFormsModule],
  template: `
    <section class="login-shell">
      <div class="login-context">
        <span>Enterprise Operations</span>
        <h1>Governance, audit, and internal workflows in one workspace.</h1>
        <p>Secure access for employees, managers, auditors, and compliance teams.</p>
      </div>
      <mat-card class="login-card">
        <mat-card-header><mat-card-title>Sign in</mat-card-title></mat-card-header>
        <mat-card-content>
          <form [formGroup]="form" (ngSubmit)="submit()">
            <mat-form-field appearance="outline">
              <mat-label>Work email</mat-label><input matInput formControlName="email" />
            </mat-form-field>
            <mat-form-field appearance="outline">
              <mat-label>Password</mat-label><input matInput type="password" formControlName="password" />
            </mat-form-field>
            <button mat-flat-button color="primary" type="submit" [disabled]="form.invalid">
              Continue securely
            </button>
          </form>
        </mat-card-content>
      </mat-card>
    </section>
  `,
  styles: `
    .login-shell { min-height: 100vh; display: grid; grid-template-columns: 1.2fr .8fr; align-items: center;
      gap: 70px; padding: 8vw; background: linear-gradient(120deg, #10263d 0 58%, #edf2f6 58%); }
    .login-context { color: white; max-width: 650px; }
    .login-context span { color: #8cc5f0; text-transform: uppercase; letter-spacing: .14em; font-size: 12px; }
    h1 { font-size: 44px; line-height: 1.14; margin: 18px 0; }
    p { color: #b7cadb; font-size: 17px; }
    .login-card { padding: 18px; }
    form, mat-form-field { display: block; width: 100%; }
    form { padding-top: 20px; }
    button { width: 100%; height: 44px; }
  `,
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class LoginPage {
  private readonly builder = inject(FormBuilder);
  private readonly store = inject(Store);
  readonly form = this.builder.nonNullable.group({
    email: ['admin@example.com', [Validators.required, Validators.email]],
    password: ['ChangeMe123!', [Validators.required, Validators.minLength(8)]],
  });

  submit(): void {
    if (this.form.valid) this.store.dispatch(AuthActions.loginSubmitted(this.form.getRawValue()));
  }
}
