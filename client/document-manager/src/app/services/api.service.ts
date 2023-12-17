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
  register(registerParam: Login) {
    return this.httpClient.post(`${this.API_BASE}/register/`, registerParam);
  }
  me() {
    return this.httpClient.get(`${this.API_BASE}/users/me/`);
  }

  getFiles() {
    return this.httpClient.get(`${this.API_BASE}/files/`);
  }
  versions(id: number) {
    return this.httpClient.get(`${this.API_BASE}/files/${id}`);
  }

  deleteFile(id: number) {
    return this.httpClient.delete(`${this.API_BASE}/files/${id}`);
  }
  deleteFileVersion(id: number) {
    return this.httpClient.delete(`${this.API_BASE}/file_versions/${id}`);
  }

  addFile(file: File, file_url: string) {
    let formParams = new FormData();
    formParams.append('uploaded_file', file);
    formParams.append('file_url', file_url);
    return this.httpClient.post(`${this.API_BASE}/files/`, formParams);
  }

  addFileVersion(file: File, fileId: number) {
    let formParams = new FormData();
    formParams.append('uploaded_file', file);
    formParams.append('file', fileId.toString());
    return this.httpClient.post(`${this.API_BASE}/file_versions/`, formParams);
  }

  viewDocument(document_url: string, version: number) {
    return this.httpClient.get(
      `${this.BASE}${document_url}?revision=${version}`,
      { responseType: 'blob', observe: 'response' }
    );
  }
}
