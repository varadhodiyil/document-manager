import { Component, OnInit, OnDestroy } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { ApiService } from '../../services/api.service';
import { Login } from '../../services/types';
import { AuthService } from '../../services/auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss'],
})
export class LoginComponent implements OnInit, OnDestroy {
  loginForm = new FormGroup({
    username: new FormControl('', [Validators.required, Validators.email]),
    password: new FormControl('', [Validators.required]),
  });
  errors = new Array();
  constructor(
    private apiService: ApiService,
    private authService: AuthService,
    private router: Router
  ) {}

  ngOnInit() {}
  ngOnDestroy() {}

  doLogin() {
    if (this.loginForm.invalid) {
      return;
    }
    this.apiService.login(this.loginForm.value as Login).subscribe({
      next: (d: any) => {
        this.errors = ['Login Successful'];
        this.authService.login(d['token']);
        this.router.navigate(['/']);
      },
      error: (e) => {
        this.errors = e.error.non_field_errors;

        setTimeout(() => {
          this.errors = [];
        }, 5000);
      },
    });
  }
}
