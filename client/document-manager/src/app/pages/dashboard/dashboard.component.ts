import { Component, OnInit } from '@angular/core';

import { ApiService } from '../../services/api.service';
import { FileResponse } from './files';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { VersionsComponent } from '../versions/versions.component';
import { FileUploadComponent } from '../../partials/file-upload/file-upload.component';
import { UploadType } from '../../partials/file-upload/types';

@Component({
  selector: 'app-dashboard',

  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.scss',
})
export class DashboardComponent implements OnInit {
  fileResponse: FileResponse = new Array();
  constructor(private apiService: ApiService, private modalService: NgbModal) {}

  fetchFiles() {
    this.apiService.getFiles().subscribe({
      next: (d) => (this.fileResponse = d as FileResponse),
    });
  }
  ngOnInit(): void {
    this.fetchFiles();
  }
  viewVersion(id: number) {
    const modalRef = this.modalService.open(VersionsComponent, { size: 'lg' });
    modalRef.componentInstance.id = id;
    modalRef.closed.subscribe({
      next: (_e) => this.fetchFiles(),
    });
  }
  deleteFile(id: number) {
    this.apiService.deleteFile(id).subscribe({
      next: (e) => this.fetchFiles(),
    });
  }

  openUploadModel() {
    const modalRef = this.modalService.open(FileUploadComponent);
    modalRef.componentInstance.uploadType = UploadType.FILE;
    modalRef.closed.subscribe({
      next: (_e) => this.fetchFiles(),
    });
  }
}
