import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FileUploadComponent } from './file-upload/file-upload.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';

@NgModule({
  declarations: [FileUploadComponent],
  imports: [CommonModule, FormsModule, ReactiveFormsModule],
  exports: [FileUploadComponent],
})
export class PartialsModule {}
