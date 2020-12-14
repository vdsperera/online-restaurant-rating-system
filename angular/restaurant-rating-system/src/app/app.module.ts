import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { RestaurantListComponent } from './restaurant-list/restaurant-list.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatSliderModule } from '@angular/material/slider';
import { MatCardModule } from '@angular/material/card';
import { FlexLayoutModule } from '@angular/flex-layout';
import { MatButtonModule } from '@angular/material/button';
import { MatSidenavModule } from '@angular/material/sidenav';
import { LayoutModule } from '@angular/cdk/layout';
import { MatToolbarModule } from '@angular/material/toolbar';
// import { NavbarModule, WavesModule, ButtonsModule } from 'angular-bootstrap-md';
import { ToolbarComponent } from './toolbar/toolbar.component';
import { MatIconModule } from '@angular/material/icon';
import { MatMenuModule } from '@angular/material/menu';
import { RegisterRestaurantComponent } from './register-restaurant/register-restaurant.component';
// import { MDBBootstrapModule } from 'angular-bootstrap-md';
import { MatFormFieldModule } from '@angular/material/form-field'
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { RestaurantDetailsComponent } from './restaurant-details/restaurant-details.component';
import { MatSnackBarModule } from '@angular/material/snack-bar';
import { MatDialogModule } from '@angular/material/dialog';
import { StarRatingComponent } from './star-rating/star-rating.component';
import { FilterPipe } from './pipes/filter.pipe';
import { IntercepterService } from './services/intercepter.service';
import { ModalModule } from './_modal'

@NgModule({
  declarations: [
    AppComponent,
    RestaurantListComponent,
    ToolbarComponent,
    RegisterRestaurantComponent,
    RestaurantDetailsComponent,
    StarRatingComponent,
    FilterPipe,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    LayoutModule,
    BrowserAnimationsModule,
    MatSliderModule,
    MatCardModule,
    FlexLayoutModule,
    MatButtonModule,
    MatSidenavModule,
    MatToolbarModule,
    // NavbarModule,
    // WavesModule,
    // ButtonsModule,
    MatIconModule,
    MatMenuModule,
    // MDBBootstrapModule.forRoot(),
    // MDBBootstrapModule,
    MatFormFieldModule,
    MatInputModule,
    MatSelectModule,
    FormsModule,
    ReactiveFormsModule,
    MatSnackBarModule,
    MatDialogModule,
    ModalModule,

  ],
  providers: [
  {
      provide: HTTP_INTERCEPTORS,
      useClass: IntercepterService,
      multi: true}
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
