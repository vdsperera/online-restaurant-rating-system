import { Component, OnInit, Input, Output, EventEmitter, ViewEncapsulation } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Rating } from '../models/rating';

@Component({
  selector: 'app-star-rating',
  templateUrl: './star-rating.component.html',
  styleUrls: ['./star-rating.component.css']
})
export class StarRatingComponent implements OnInit {

  @Input('rating') public rating: number;
  @Input('price_rating') public price_rating: number;
  @Input('service_rating') public service_rating: number;

  @Input('star_count') public star_count: number=5;
  @Input('price_star_count') public price_star_count: number=5;
  @Input('service_star_count') public service_star_count: number=5;

  @Input('color') public color: string = 'accent';


  @Output('rating_updated') public rating_updated = new EventEmitter();
  @Output('price_rating_updated') public price_rating_updated = new EventEmitter();
  @Output('service_rating_updated') public service_rating_updated = new EventEmitter();

  public snack_bar_duration: number = 2000;
  public rating_array = [];
  public price_rating_array = [];
  public service_rating_array = [];
  public rating_model = new Rating;
  @Output('rating_model_event') rating_model_event = new EventEmitter<Rating>(); 


  constructor(private snack_bar: MatSnackBar) { }

  ngOnInit(): void {
    for(let index=0; index<this.star_count; index++)
    {
      this.rating_array.push(index);
    }

    for(let index=0; index<this.price_star_count; index++)
    {
      this.price_rating_array.push(index);
    }


    for(let index=0; index<this.service_star_count; index++)
    {
      this.service_rating_array.push(index);
    }
  }

  show_icon(index: number)
  {
    if(this.rating >= index+1)
    {
      return 'star';
    }
    else
    {
      return 'star_border';
    }

  }

  show_price_icon(index: number)
  {
    if(this.price_rating >= index+1)
    {
      return 'star';
    }
    else
    {
      return 'star_border';
    }

  }

  show_service_icon(index: number)
  {
    if(this.service_rating >= index+1)
    {
      return 'star';
    }
    else
    {
      return 'star_border';
    }

  }

  onClick(rating:number) {
    console.log(rating);
    this.snack_bar.open('You rated ' + rating + ' / ' + this.star_count, '', {
      duration: this.snack_bar_duration
    });
    //this.rating_updated.emit(rating);
    console.log(this.rating);
    this.rating = rating;
    this.rating_model.set_dish_rating(rating);
    return false;
  }  

  on_price_click(price_rating:number) {
    console.log(price_rating);
    this.snack_bar.open('You rated price' + price_rating + ' / ' + this.price_star_count, '', {
      duration: this.snack_bar_duration
    });
    //this.rating_updated.emit(rating);
    console.log(this.price_rating);
    this.price_rating = price_rating;
    this.rating_model.set_price_rating(price_rating);
    return false;
  }

  on_service_click(service_rating:number) {
    console.log(service_rating);
    this.snack_bar.open('You rated service' + service_rating + ' / ' + this.service_star_count, '', {
      duration: this.snack_bar_duration
    });
    //this.rating_updated.emit(rating);
    console.log(this.service_rating);
    this.service_rating = service_rating;
    this.rating_model.set_service_rating(service_rating);
    console.log(this.rating_model);
    this.rating_model_event.emit(this.rating_model);
    return false;

  }

}

export enum star_rating_color
{
  primary = 'primary',
  accent = 'accent',
  warn = 'warn'

}