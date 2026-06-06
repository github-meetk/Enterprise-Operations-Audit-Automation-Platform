import { inject, Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { Actions, createEffect, ofType } from '@ngrx/effects';
import { catchError, map, of, switchMap, tap } from 'rxjs';

import { AuthService } from '../../core/auth/auth.service';
import { TokenStorageService } from '../../core/auth/token-storage.service';
import { AuthActions } from './auth.actions';

@Injectable()
export class AuthEffects {
  private readonly actions = inject(Actions);
  private readonly auth = inject(AuthService);
  private readonly storage = inject(TokenStorageService);
  private readonly router = inject(Router);

  readonly login = createEffect(() =>
    this.actions.pipe(
      ofType(AuthActions.loginSubmitted),
      switchMap(({ email, password }) =>
        this.auth.login(email, password).pipe(
          map((tokens) => AuthActions.loginSucceeded({ tokens })),
          catchError(() => of(AuthActions.loginFailed({ error: 'Unable to sign in.' }))),
        ),
      ),
    ),
  );

  readonly loginSucceeded = createEffect(() =>
    this.actions.pipe(
      ofType(AuthActions.loginSucceeded),
      tap(({ tokens }) => this.storage.setTokens(tokens.access_token, tokens.refresh_token)),
      tap(() => void this.router.navigate(['/dashboard'])),
      map(() => AuthActions.loadCurrentUser()),
    ),
  );

  readonly loadCurrentUser = createEffect(() =>
    this.actions.pipe(
      ofType(AuthActions.loadCurrentUser),
      switchMap(() => this.auth.me().pipe(map((user) => AuthActions.currentUserLoaded({ user })))),
    ),
  );
}
