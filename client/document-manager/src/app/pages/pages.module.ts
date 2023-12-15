import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { PagesRoutingModule } from './pages-routing.module';
import { DashboardComponent } from './dashboard/dashboard.component';
import { BaseComponent } from './base/base.component';
import { ManagerComponent } from './manager/manager.component';
import { VersionsComponent } from './versions/versions.component';
import { PartialsModule } from '../partials/partials.module';

@NgModule({
  declarations: [
    DashboardComponent,
    BaseComponent,
    ManagerComponent,
    VersionsComponent,
  ],
  imports: [CommonModule, PagesRoutingModule, PartialsModule],
})
export class PagesModule {}
