import { Component, Input, OnDestroy } from '@angular/core';
import { ApiService } from '../../services/api.service';
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap';
import { UploadType } from './types';

@Component({
  selector: 'app-file-upload',

  templateUrl: './file-upload.component.html',
  styleUrl: './file-upload.component.scss',
})
export class FileUploadComponent implements OnDestroy {
  file: File | null = null;
  @Input() uploadType: UploadType | null = UploadType.FILE;
  @Input() id: number | null = null;

  constructor(
    public activeModal: NgbActiveModal,
    private apiService: ApiService
  ) {}
  ngOnDestroy(): void {
    this.uploadType = null;
  }

  onFilechange(event: any) {
    this.file = event.target.files[0];
  }

  upload() {
    if (this.file) {
      if (this.uploadType === UploadType.FILE) {
        this.apiService.addFile(this.file).subscribe({
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
}
