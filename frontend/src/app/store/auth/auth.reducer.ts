import { createReducer, on } from '@ngrx/store';

import { CurrentUser } from '../../core/auth/auth.models';
import { AuthActions } from './auth.actions';

export interface AuthState {
  user: CurrentUser | null;
  loading: boolean;
  error: string | null;
}

const initialState: AuthState = { user: null, loading: false, error: null };

export const authReducer = createReducer(
  initialState,
  on(AuthActions.loginSubmitted, (state) => ({ ...state, loading: true, error: null })),
  on(AuthActions.loginSucceeded, (state) => ({ ...state, loading: false })),
  on(AuthActions.loginFailed, (state, { error }) => ({ ...state, loading: false, error })),
  on(AuthActions.currentUserLoaded, (state, { user }) => ({ ...state, user })),
  on(AuthActions.logout, () => initialState),
);
