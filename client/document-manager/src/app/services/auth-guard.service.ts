import { inject } from '@angular/core';
import {
  ActivatedRouteSnapshot,
  RouterStateSnapshot,
  Router,
  CanActivateFn,
} from '@angular/router';
import { AuthService } from './auth.service';

export const AuthGuard: CanActivateFn = (
  route: ActivatedRouteSnapshot,
  state: RouterStateSnapshot
) => {
  const loginService = inject(AuthService);
  const router = inject(Router);

  const isLoggedIn = loginService.isLoggedIn();
  if (isLoggedIn) {
    return true;
  } else {
    router.navigate(['/auth/']);
    return false;
  }
};
