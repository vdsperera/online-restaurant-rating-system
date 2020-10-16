import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { RestaurantListComponent } from './restaurant-list/restaurant-list.component';
import { ToolbarComponent } from './toolbar/toolbar.component';
import { RegisterRestaurantComponent } from './register-restaurant/register-restaurant.component';
import { RestaurantDetailsComponent } from './restaurant-details/restaurant-details.component';
import { StarRatingComponent } from './star-rating/star-rating.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatSidenavModule } from '@angular/material/sidenav';

@NgModule({
  declarations: [
    AppComponent,
    RestaurantListComponent,
    ToolbarComponent,
    RegisterRestaurantComponent,
    RestaurantDetailsComponent,
    StarRatingComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    MatSidenavModule,    
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
