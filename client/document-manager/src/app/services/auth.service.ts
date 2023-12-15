import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  constructor() {}
  AUTH_KEY = 'TOKEN_PROP';

  public getToken(): string | null {
    return localStorage.getItem(this.AUTH_KEY);
  }
  public isLoggedIn() {
    return this.getToken() !== null;
  }

  public logout() {
    localStorage.clear();
  }
  public login(token: string) {
    localStorage.setItem(this.AUTH_KEY, token);
  }
}
