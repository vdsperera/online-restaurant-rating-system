import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { RegisterRestaurantComponent } from './register-restaurant/register-restaurant.component';
import { RestaurantListComponent } from './restaurant-list/restaurant-list.component';
import { RestaurantDetailsComponent } from './restaurant-details/restaurant-details.component';

const routes: Routes = [
  {path: '', component: RestaurantListComponent},
  {path: 'registerrestaurant', component: RegisterRestaurantComponent},
  {path: 'restaurants/:id', component: RestaurantDetailsComponent},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
