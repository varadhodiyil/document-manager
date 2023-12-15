import { Component, Input, OnInit } from '@angular/core';
import { ApiService } from '../../services/api.service';
import { ActivatedRoute } from '@angular/router';
import { Files } from './versions';
import { NgbActiveModal, NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { FileUploadComponent } from '../../partials/file-upload/file-upload.component';
import { UploadType } from '../../partials/file-upload/types';

@Component({
  selector: 'app-versions',
  templateUrl: './versions.component.html',
  styleUrl: './versions.component.scss',
})
export class VersionsComponent implements OnInit {
  @Input() id: number | string | null = null;
  fileVersions: Files | null = null;
  constructor(
    private apiService: ApiService,
    private modalService: NgbModal,
    public activeModal: NgbActiveModal
  ) {}
  ngOnInit(): void {
    this.fetchVersions();
  }
  fetchVersions() {
    console.log(this.id);
    if (!this.id) {
      return;
    }
    this.id = Number(this.id);
    this.apiService.versions(this.id).subscribe({
      next: (e) => (this.fileVersions = e as Files),
      error: (e) => this.activeModal.close(),
    });
  }
  download(versionId: number) {
    console.log(versionId);
  }

  deleteVersion(versionId: number) {
    this.apiService.deleteFileVersion(versionId).subscribe({
      next: (e) => this.fetchVersions(),
    });
  }

  openUploadModel() {
    const modalRef = this.modalService.open(FileUploadComponent);
    modalRef.componentInstance.uploadType = UploadType.Version;
    modalRef.componentInstance.id = this.fileVersions?.id;
    modalRef.closed.subscribe({
      next: (_e) => this.fetchVersions(),
    });
  }
}
