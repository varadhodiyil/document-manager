import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { ApiService } from '../../services/api.service';
import { AuthService } from '../../services/auth.service';
import { Login } from '../../services/types';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss'],
})
export class RegisterComponent implements OnInit {
  signUpForm = new FormGroup({
    email: new FormControl('', [Validators.required, Validators.email]),
    password: new FormControl('', [Validators.required]),
    confirmpassword: new FormControl('', [Validators.required]),
  });
  errors = new Array();
  constructor(
    private apiService: ApiService,

    private router: Router
  ) {}

  ngOnInit() {
    this.signUpForm.controls.confirmpassword.addValidators(
      Validators.pattern(this.signUpForm.controls.password.value || '')
    );
  }

  doSignUp() {
    if (this.signUpForm.invalid) {
      return;
    }
    this.apiService.register(this.signUpForm.value as Login).subscribe({
      next: (d: any) => {
        this.errors = ['Sign Up Successful. Please Login'];

        this.router.navigate(['/auth']);
      },
      error: (e) => {
        this.errors = Object.keys(e.error).map((d) => `${d} --  ${e.error[d]}`);

        setTimeout(() => {
          this.errors = [];
        }, 5000);
      },
    });
  }
}
