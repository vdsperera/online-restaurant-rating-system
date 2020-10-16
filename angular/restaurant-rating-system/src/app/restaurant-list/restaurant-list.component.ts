import { Component, OnInit } from '@angular/core';
import { Observable } from 'rxjs'
import { Router } from '@angular/router'
import { ApiService } from '../api.service' 
import { Restaurant } from '../restaurant';

@Component({
  selector: 'app-restaurant-list',
  templateUrl: './restaurant-list.component.html',
  styleUrls: ['./restaurant-list.component.css']
})
export class RestaurantListComponent implements OnInit {

  restaurants$: Observable<Restaurant[]>;

  constructor(private apiService: ApiService, private router: Router) { }

  ngOnInit(): void {
    this.get_restaurants();
    console.log(this.restaurants$);
  }

  public get_restaurants() {
    this.restaurants$ = this.apiService.get_restaurants();

  }

  public view_details(restaurant_id) {
    console.log(restaurant_id)
    this.router.navigate(['/restaurants', restaurant_id]);
  }

}
