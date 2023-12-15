import { Injectable } from '@angular/core';
import { Router } from '@angular/router';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  constructor(private router: Router) {}
  AUTH_KEY = 'TOKEN_PROP';

  public getToken(): string | null {
    return localStorage.getItem(this.AUTH_KEY);
  }
  public isLoggedIn() {
    return this.getToken() !== null;
  }

  public logout() {
    localStorage.clear();
    this.router.navigate(['/auth']);
  }
  public login(token: string) {
    localStorage.setItem(this.AUTH_KEY, token);
  }
}
