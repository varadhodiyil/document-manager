import { Component, OnInit, OnDestroy } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { ApiService } from '../../services/api.service';
import { Login } from '../../services/types';

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
  errors: [] = [];
  constructor(private apiService: ApiService) {}

  ngOnInit() {}
  ngOnDestroy() {}

  doLogin() {
    if (this.loginForm.invalid) {
      return;
    }
    this.apiService.login(this.loginForm.value as Login).subscribe(
      (d) => {
        console.log(d);
      },
      (e) => {
        this.errors = e.error.non_field_errors;

        setTimeout(() => {
          this.errors = [];
        }, 5000);
      }
    );
  }
}
