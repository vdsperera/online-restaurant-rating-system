import { Component, OnInit, ViewChild, TemplateRef } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { Observable } from 'rxjs'
import { Router } from '@angular/router'

import { ApiService } from '../api.service' 
import { Restaurant } from '../restaurant';
import { map } from 'rxjs/operators'; 
import { FilterPipe } from '../pipes/filter.pipe'

@Component({
  selector: 'app-restaurant-list',
  templateUrl: './restaurant-list.component.html',
  styleUrls: ['./restaurant-list.component.css']
})
export class RestaurantListComponent implements OnInit {
  @ViewChild('secondDialog') secondDialog: TemplateRef<any>;
  // restaurants$: Observable<Restaurant[]>;
  restaurants: Restaurant;
  rests: any;
  private system_dishes;
  searchText = '';

  constructor(private apiService: ApiService, private router: Router, private dialog: MatDialog) { }

  ngOnInit(): void {
    this.get_restaurants();
    this.get_system_dish_list()
  }

  openDialogWithRef(ref: TemplateRef<any>) {
    this.dialog.open(ref);
  }

  openOtherDialog() {
    this.dialog.open(this.secondDialog);
  }

  public get_restaurants() {
    let value = (<HTMLSelectElement>document.getElementById('dishesdrop')).value;
    // if(value != 'null')
    //   this.get_restaurants_dish(value)
    if(value == 'null')
    {
      // this.restaurants$ = this.apiService.get_restaurants();
      this.apiService.get_restaurants()
      .subscribe((data) => {
         console.log('start component console restaurants')
         // this.restaurants$ = data['data']['restaurant_list']
         this.restaurants = data['data']['restaurant_list']
         // this.rests = data['data']['restaurant_list']
         // // console.log(this.rests)
         
         // // this.rests.sort(function(a, b){return a.restaurant_id - b.restaurant_id});
         // this.restaurants.sort(function(a, b){return b.overall_rating - a.overall_rating});

         console.log(this.restaurants)
         console.log('end component console restaurants')
      });
      // console.log('start component console')
      // console.log(this.rests)
      // console.log(this.restaurants)
      // console.log('end component console')
    }
    else{
      this.get_restaurants_dish(value)
    }


  }

  public get_restaurants_dish(value)
  {
    // let value = (<HTMLSelectElement>document.getElementById('dishesdrop')).value;
    console.log('selected one is ' + value)
    this.apiService.get_restaurants_dish(value)
    .subscribe((data) => {
       console.log('start component console restaurant dish')
       // this.restaurants$ = data['data']['restaurant_list']
       this.restaurants = data['data']['restaurant_list']
       // this.rests = data['data']['restaurant_list']
       // // console.log(this.rests)
       
       // // this.rests.sort(function(a, b){return a.restaurant_id - b.restaurant_id});
       // this.restaurants.sort(function(a, b){return b.overall_rating - a.overall_rating});

       console.log(this.restaurants)
       console.log('end component console restaurant dish')
    });    
  }

  public order_list_by_overall_rating_des()
  {
    this.restaurants.sort(function(a, b){return b.overall_rating - a.overall_rating});
  }

  public order_list_by_overall_rating_ase()
  {
    this.restaurants.sort(function(a, b){return a.overall_rating - b.overall_rating});
  }

  public order_list_by_no_of_ratings_des()
  {
    this.restaurants.sort(function(a, b){return b.total_no_of_ratings - a.total_no_of_ratings});
  }

  public order_list_by_no_of_ratings_ase()
  {
    this.restaurants.sort(function(a, b){return a.total_no_of_ratings - b.total_no_of_ratings});
  }

  public view_details(restaurant_id) {
    console.log(restaurant_id)
    this.router.navigate(['/restaurants', restaurant_id]);
  }
  public ar
  public rn

  public questioner(x) {
    this.ar =  Array(Math.round(x));
    this.rn = Math.floor(x)
    // console.log(this.rn)
    // return `<span class="fa fa-star checked"></span>`; 
  }

  public arrayOne(n: number): any[] {
    // console()
    // return this.ar;
    return Array(this.rn)
  }

  public arrayTwo(n: number): any[] {
    // console()
    // return this.ar;
    return Array(5-this.rn)
  }

  public get_system_dish_list()
  {
    this.apiService.get_system_dish_list()
    .subscribe((data) => {
      this.system_dishes = data['data']['dishes']
      console.log(this.system_dishes)
    });
  }

  public find_now()
  {
    console.log('finding')
    let address = 'Lenny'
    let item1 = this.restaurants.filter(i => i.address == address);
    var result = this.restaurants.filter(item => 
             Object.keys(item).some(k => item[k] != null && 
             item[k].toString().toLowerCase()
             .includes(address.toLowerCase()))
             );

    console.log(result)
  }

}
