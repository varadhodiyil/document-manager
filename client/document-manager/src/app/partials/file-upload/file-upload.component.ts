import { Component, Input, OnDestroy, OnInit } from '@angular/core';
import { ApiService } from '../../services/api.service';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
import { UploadType } from './types';
import { FormControl, Validators } from '@angular/forms';

@Component({
  selector: 'app-file-upload',

  templateUrl: './file-upload.component.html',
  styleUrl: './file-upload.component.scss',
})
export class FileUploadComponent implements OnDestroy, OnInit {
  file: File | null = null;
  @Input() uploadType: UploadType | null = UploadType.FILE;
  @Input() id: number | null = null;
  urlControl = new FormControl('', Validators.required);
  showURL = this.uploadType === UploadType.FILE;
  errors: [string] = [''];

  constructor(
    public activeModal: NgbActiveModal,
    private apiService: ApiService
  ) {}
  ngOnDestroy(): void {
    this.uploadType = null;
  }
  ngOnInit(): void {
    this.showURL = this.uploadType === UploadType.FILE;
  }

  onFilechange(event: any) {
    this.file = event.target.files[0];
  }

  upload() {
    if (this.file) {
      if (this.uploadType === UploadType.FILE) {
        if (!this.urlControl.value) {
          return;
        }
        this.apiService.addFile(this.file, this.urlControl.value).subscribe({
          next: (_d) => this.activeModal.close(),
        });
      } else if (this.uploadType === UploadType.Version) {
        if (!this.id) {
          return;
        }
        this.apiService.addFileVersion(this.file, this.id).subscribe({
          next: (e) => this.activeModal.close(),
        });
      }
    } else {
      alert('Please select a file first');
    }
  }
  shouldEnable() {
    if (this.uploadType === UploadType.FILE) {
      return this.file && this.urlControl.valid;
    }
    if (this.uploadType === UploadType.Version) {
      return this.file;
    }
    return false;
  }
}
