import { finalize, tap } from 'rxjs';

import { Injectable } from '@angular/core';
import {
  HttpErrorResponse,
  HttpHandler,
  HttpInterceptor,
  HttpRequest,
  HttpResponse,
} from '@angular/common/http';
import { Router } from '@angular/router';
import { AuthService } from './auth.service';
@Injectable()
export class TokenInterceptor implements HttpInterceptor {
  constructor(private router: Router, private auth: AuthService) {}

  intercept(req: HttpRequest<any>, next: HttpHandler) {
    let request = req;
    if (this.auth.getToken()) {
      request = req.clone({
        setHeaders: {
          Authorization: `Token ${this.auth.getToken()}`,
        },
      });
    }

    return next.handle(request).pipe(
      tap({
        next: (event) => {},

        error: (_error) => {
          if (_error instanceof HttpErrorResponse) {
            if (_error.status === 401 || _error.status === 403) {
              this.auth.logout();
              this.router.navigate(['/auth/login']);
            }
          }
        },
      })
    );
  }
}
