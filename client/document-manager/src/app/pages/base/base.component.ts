import { Component, OnInit } from '@angular/core';
import { ApiService } from '../../services/api.service';
import { User } from './user';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-base',
  templateUrl: './base.component.html',
  styleUrl: './base.component.scss',
})
export class BaseComponent implements OnInit {
  user: User | null = null;
  constructor(
    private apiService: ApiService,
    private authService: AuthService
  ) {}
  ngOnInit(): void {
    this.apiService.me().subscribe({
      next: (e) => {
        this.user = e as User;
      },
    });
  }
  logout() {
    this.authService.logout();
  }
}
