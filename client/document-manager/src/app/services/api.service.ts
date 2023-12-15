import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from '../../environments/environment';
import { Login } from './types';
@Injectable({
  providedIn: 'root',
})
export class ApiService {
  protected BASE = environment.host;
  protected API_BASE = `${this.BASE}/api`;
  constructor(private httpClient: HttpClient) {}

  login(loginParam: Login) {
    return this.httpClient.post(`${this.BASE}/auth-token/`, loginParam);
  }
  me() {
    return this.httpClient.get(`${this.API_BASE}/users/me`);
  }
}
