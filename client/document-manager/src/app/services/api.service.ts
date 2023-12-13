import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from '../../environments/environment';
import { Login } from './types';
@Injectable({
  providedIn: 'root',
})
export class ApiService {
  constructor(private httpClient: HttpClient) {}

  login(loginParam: Login) {
    return this.httpClient.post(`${environment.host}/auth-token/`, loginParam);
  }
}
