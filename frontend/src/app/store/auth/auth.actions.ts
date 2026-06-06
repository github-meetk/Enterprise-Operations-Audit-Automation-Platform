import { createActionGroup, emptyProps, props } from '@ngrx/store';

import { CurrentUser, TokenResponse } from '../../core/auth/auth.models';

export const AuthActions = createActionGroup({
  source: 'Auth',
  events: {
    'Login Submitted': props<{ email: string; password: string }>(),
    'Login Succeeded': props<{ tokens: TokenResponse }>(),
    'Login Failed': props<{ error: string }>(),
    'Load Current User': emptyProps(),
    'Current User Loaded': props<{ user: CurrentUser }>(),
    Logout: emptyProps(),
  },
});
