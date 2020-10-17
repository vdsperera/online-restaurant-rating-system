import { Component, OnInit, Input, Output, EventEmitter, ViewEncapsulation } from '@angular/core';
import { Rating } from '../models/rating';

@Component({
  selector: 'app-restaurant-details',
  templateUrl: './restaurant-details.component.html',
  styleUrls: ['./restaurant-details.component.css']
})
export class RestaurantDetailsComponent implements OnInit {

  public snack_bar_duration: number = 2000;
  public rating_array = [];
  public rating_model = new Rating;


  constructor() { }

  ngOnInit(): void {

  }

  rating_event_hander($event: any)
  {
    this.rating_model = $event;
    console.log('even emitter');
    console.log(this.rating_model);
  }

}
